from io import BytesIO
import os
import chainlit as cl
import httpx
from dotenv import load_dotenv
from langchain.schema.runnable.config import RunnableConfig
from sql_agent import SQLAgent
from openai import AsyncOpenAI
from chainlit.element import Audio

# Load the .env file
load_dotenv()

# Set up the transcription API (e.g., Eleven Labs)
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.environ.get("ELEVENLABS_VOICE_ID")

if not ELEVENLABS_API_KEY or not ELEVENLABS_VOICE_ID:
    raise ValueError("ELEVENLABS_API_KEY and ELEVENLABS_VOICE_ID must be set")

client = AsyncOpenAI()

@cl.step(type="tool")
async def speech_to_text(audio_file):
    response = await client.audio.transcriptions.create(
        model="whisper-1", file=audio_file
    )
    return response.text

@cl.step(type="tool")
async def generate_text_answer(transcription, images):
    model = "gpt-4-turbo"
    messages = [{"role": "user", "content": transcription}]
    response = await client.chat.completions.create(
        messages=messages, model=model, temperature=0.3
    )
    return response.choices[0].message.content

@cl.step(type="tool")
async def text_to_speech(text: str, mime_type: str):
    CHUNK_SIZE = 1024
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"

    headers = {
        "Accept": mime_type,
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }

    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    async with httpx.AsyncClient(timeout=25.0) as client:
        response = await client.post(url, json=data, headers=headers)
        response.raise_for_status()  # Ensure we notice bad responses

        buffer = BytesIO()
        buffer.name = f"output_audio.{mime_type.split('/')[1]}"

        async for chunk in response.aiter_bytes(chunk_size=CHUNK_SIZE):
            if chunk:
                buffer.write(chunk)

        buffer.seek(0)
        return buffer.name, buffer.read()

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("agent", SQLAgent)

@cl.on_message
async def on_message(message: cl.Message):
    await process_message(message.content)

@cl.on_audio_chunk
async def on_audio_chunk(chunk: cl.AudioChunk):
    if chunk.isStart:
        buffer = BytesIO()
        # This is required for whisper to recognize the file type
        buffer.name = f"input_audio.{chunk.mimeType.split('/')[1]}"
        # Initialize the session for a new audio stream
        cl.user_session.set("audio_buffer", buffer)
        cl.user_session.set("audio_mime_type", chunk.mimeType)

    cl.user_session.get("audio_buffer").write(chunk.data)

@cl.on_audio_end
async def on_audio_end(elements: list[Audio]):
    audio_buffer: BytesIO = cl.user_session.get("audio_buffer")
    audio_buffer.seek(0)
    audio_file = audio_buffer.read()
    audio_mime_type: str = cl.user_session.get("audio_mime_type")

    input_audio_el = Audio(
        mime=audio_mime_type, content=audio_file, name=audio_buffer.name
    )
    await cl.Message(
        author="You",
        type="user_message",
        content="",
        elements=[input_audio_el, *elements]
    ).send()

    answer_message = await cl.Message(content="").send()

    whisper_input = (audio_buffer.name, audio_file, audio_mime_type)
    transcription = await speech_to_text(whisper_input)

    await process_message(transcription, answer_message, audio_mime_type)

async def process_message(content: str, answer_message=None, mime_type=None):
    agent = cl.user_session.get("agent")
    cb = cl.AsyncLangchainCallbackHandler(stream_final_answer=True)
    config = RunnableConfig(callbacks=[cb])

    async with cl.Step(name="SmartQuery Agent", root=True) as step:
        step.input = content
        result = await agent.ainvoke(content, config=config)

        final_answer = result.get('output', 'No answer returned')

        await step.stream_token(final_answer)

        if mime_type:
            output_name, output_audio = await text_to_speech(final_answer, mime_type)
            output_audio_el = Audio(
                name=output_name,
                auto_play=True,
                mime=mime_type,
                content=output_audio,
            )
            answer_message.elements = [output_audio_el]
            await answer_message.update()
        else:
            await cl.Message(content=final_answer).send()
