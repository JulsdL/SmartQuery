import chainlit as cl
from langchain.schema.runnable.config import RunnableConfig
from sql_agent import SQLAgent

# Test the agent
# agent.invoke({"input": "How many artists are there?"})

# ChainLit Integration
@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("agent", SQLAgent)

@cl.on_message
async def on_message(message: cl.Message):
    agent = cl.user_session.get("agent")  # Get the agent from the session
    cb = cl.AsyncLangchainCallbackHandler(stream_final_answer=True)
    config = RunnableConfig(callbacks=[cb])

    result = await agent.ainvoke(message.content, config=config)

    msg = cl.Message(content="")

    async for chunk in result:
        await msg.stream_token(chunk)

    await msg.send()

# Run the app
if __name__ == "__main__":
    cl.run()
