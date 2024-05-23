import chainlit as cl
from langchain.schema.runnable.config import RunnableConfig
from sql_agent import SQLAgent

# ChainLit Integration
@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("agent", SQLAgent)

@cl.on_message
async def on_message(message: cl.Message):
    agent = cl.user_session.get("agent")  # Get the agent from the session
    cb = cl.AsyncLangchainCallbackHandler(stream_final_answer=True)
    config = RunnableConfig(callbacks=[cb])

    async with cl.Step(name="SmartQuery Agent", root=True) as step:
        step.input = message.content
        result = await agent.ainvoke(message.content, config=config)

        # Assuming the result is a dictionary with a key 'output' containing the final answer
        final_answer = result.get('output', 'No answer returned')

        # Stream the final answer as a token to the step
        await step.stream_token(final_answer)
