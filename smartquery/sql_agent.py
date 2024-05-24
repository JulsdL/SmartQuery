import ast
import re
from dotenv import load_dotenv
from langchain_community.agent_toolkits import create_sql_agent
from langchain.tools.retriever import create_retriever_tool
from langchain_community.vectorstores import FAISS
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.prompts import ChatPromptTemplate, FewShotPromptTemplate, MessagesPlaceholder, PromptTemplate, SystemMessagePromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from smartquery.prompt_templates import few_shot_examples, system_prefix


# Load the .env file
load_dotenv()

# Initialize the SQL database
db = SQLDatabase.from_uri("sqlite:///database/Chinook.db")

# Check the database connection
print(db.dialect)
print(db.get_usable_table_names())
db.run("SELECT * FROM Artist LIMIT 10;")

# Initialize the LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# Function to query database and get list of elements
def query_as_list(db, query):
    res = db.run(query)
    res = [el for sub in ast.literal_eval(res) for el in sub if el]
    res = [re.sub(r"\b\d+\b", "", string).strip() for string in res]
    return list(set(res))

# Create lists of artists and albums
artists = query_as_list(db, "SELECT Name FROM Artist")
albums = query_as_list(db, "SELECT Title FROM Album")

# Create a vector store and use it as a retriever
vector_db = FAISS.from_texts(artists + albums, OpenAIEmbeddings())
retriever = vector_db.as_retriever(search_kwargs={"k": 5})

# Create a search proper nouns tool
description = """Use to look up values to filter on. Input is an approximate spelling of the proper noun, output is \
valid proper nouns. Use the noun most similar to the search."""
retriever_tool = create_retriever_tool(
    retriever,
    name="search_proper_nouns",
    description=description,
)

# Example selector will dynamically select examples based on the input question
example_selector = SemanticSimilarityExampleSelector.from_examples(
    few_shot_examples,
    OpenAIEmbeddings(),
    FAISS,
    k=5,
    input_keys=["input"],
)

# Few-shot prompt template
few_shot_prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=PromptTemplate.from_template(
        "User input: {input}\nSQL query: {query}"
    ),
    input_variables=["input", "dialect", "top_k"],
    prefix=system_prefix,
    suffix="",
)

# Full prompt template
full_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate(prompt=few_shot_prompt),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ]
)

# Create the SQL agent
SQLAgent = create_sql_agent(
    llm=llm,
    db=db,
    extra_tools=[retriever_tool],
    prompt=full_prompt,
    agent_type="openai-tools",
    verbose=True,
)
