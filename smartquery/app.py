from io import BytesIO
import os
import chainlit as cl
import httpx
from dotenv import load_dotenv
from langchain.schema.runnable.config import RunnableConfig
from smartquery.sql_agent import SQLAgent
from openai import AsyncOpenAI
from chainlit.element import Audio

# Load the .env file
load_dotenv()

# Set up the transcription API (e.g., Eleven Labs)
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.environ.get("ELEVENLABS_VOICE_ID")

if not ELEVENLABS_API_KEY or not ELEVENLABS_VOICE_ID:
    raise ValueError("ELEVENLABS_API_KEY and ELEVENLABS_VOICE_ID must be set")

# Set up the OpenAI API
client = AsyncOpenAI()

@cl.step(type="tool")
async def speech_to_text(audio_file):
    response = await client.audio.transcriptions.create(
        model="whisper-1", file=audio_file
    )
    return response.text


@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("agent", SQLAgent)

    # Configure Chainlit features for audio capture
    cl.user_session.set("audio_settings", {
        "min_decibels": -80,
        "initial_silence_timeout": 500,
        "silence_timeout": 2500,
        "max_duration": 15000,
        "chunk_duration": 1000,
        "sample_rate": 44100
    })
    print("Chat session started and audio settings configured")

@cl.on_message
async def on_message(message: cl.Message):
    await process_message(message.content)

@cl.on_audio_chunk
async def on_audio_chunk(chunk: cl.AudioChunk):
    print("Received audio chunk")
    try:
        if chunk.isStart:
            buffer = BytesIO()
            buffer.name = f"input_audio.{chunk.mimeType.split('/')[1]}"
            # Initialize the session for a new audio stream
            cl.user_session.set("audio_buffer", buffer)
            cl.user_session.set("audio_mime_type", chunk.mimeType)

        cl.user_session.get("audio_buffer").write(chunk.data)

    except Exception as e:
        print(f"Error handling audio chunk: {e}")

@cl.on_audio_end
async def on_audio_end(elements: list[Audio]):
    try:
        print("Audio recording ended")
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

        whisper_input = (audio_buffer.name, audio_file, audio_mime_type)
        transcription = await speech_to_text(whisper_input)
        print("Transcription received:", transcription)

        await process_message(transcription)

    except Exception as e:
        print(f"Error processing audio: {e}")
        await cl.Message(content="Error processing audio. Please try again.").send()

    finally:
        # Reset audio buffer and mime type
        cl.user_session.set("audio_buffer", None)
        cl.user_session.set("audio_mime_type", None)
        print("Audio buffer reset")

async def process_message(content: str, answer_message=None):
    agent = cl.user_session.get("agent")
    cb = cl.AsyncLangchainCallbackHandler(stream_final_answer=True) # Create a callback handler
    config = RunnableConfig(callbacks=[cb]) # Add the callback handler to the config

    async with cl.Step(name="SmartQuery Agent", root=True) as step:
        step.input = content
        result = await agent.ainvoke(content, config=config)

        final_answer = result.get('output', 'No answer returned')

        await step.stream_token(final_answer)

        if answer_message:
            answer_message.content = final_answer
            await answer_message.update()
