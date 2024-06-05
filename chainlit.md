# Welcome to SmartQuery! 🔍📊

Hello and welcome to SmartQuery, your intelligent assistant designed to help you interact with your database effortlessly. Whether you're a business analyst, data scientist, or a curious user, our tool will help you get answers from your database without writing a single line of SQL.

## Getting Started

### Sample Questions to Try:

- "What is the most expensive track?"
- "List the total sales per country. Which country's customers spent the most?"
- "Who are the 3 most listened artists and what is their average revenue?"

## About the Database 🎶💽

The database powering SmartQuery is the Chinook Database, a sample database representing a digital media store. It contains tables for:

- **Artists**: Information about music artists.
- **Albums**: Details of albums released by artists.
- **Tracks**: Data on individual tracks, including their length and price.
- **Genres**: Different genres of music.
- **Customers**: Information about the customers of the store.
- **Invoices**: Purchase records containing information on sales transactions.
- **InvoiceLines**: Details about each item in an invoice.
- **Employees**: Data on employees managing the store.
- **Playlists**: User-generated playlists.
- **PlaylistTracks**: Mapping of tracks to playlists.
- **MediaTypes**: Types of media the tracks are available in.

This structure allows you to ask a wide range of questions about sales, customer preferences, artist performance, and more. Feel free to explore the richness of the data and uncover valuable insights.

## How It Works 🧠

SmartQuery is an agentic application that leverages GPT-4o to understand your queries in plain English and convert them into SQL queries to retrieve the desired information from the database. You can interact with SmartQuery via text or voice, making it incredibly versatile and user-friendly.

Key Features:

- Natural Language to SQL: Users can ask questions in plain English, and the application generates the corresponding SQL queries to fetch the required data from the database.
- Advanced Prompt Engineering: The application employs sophisticated prompt engineering techniques to accurately interpret user inputs and generate precise SQL queries.
- Few-shot Learning: Dynamically selected examples improve the accuracy and relevance of generated queries.
- Complex Queries: The application can handle intricate SQL operations, including JOINs and filters, to address complex user queries effectively.
- Proper Noun Correction Tool: Handles high-cardinality columns containing proper nouns (such as addresses, song names, or artists) by querying a vector store of known entities, ensuring accurate and relevant results (e.g., if you ask for Methalika titles, it will "understand" Metallica).

## The Tech Behind It 💡🤖

SmartQuery is built using state-of-the-art technologies, including:

- **LangChain**: For LLM and agent orchestration.
- **OpenAI GPT-4o**: For understanding and processing natural language queries.
- **FAISS**: For efficient similarity search and retrieval.
- **Chainlit**: For building interactive AI applications front-end.
- **Eleven Labs**: For speech-to-text functionalities, enabling voice interactions.

## Links and Resources 🌐

- Github Repository: https://github.com/JulsdL/SmartQuery
- LangChain documentation: https://python.langchain.com/v0.2/docs/tutorials/sql_qa/#execute-sql-query
- ChainLit documentation: https://docs.chainlit.io/get-started/overview

## Ready to Query?

With SmartQuery, transform your database interactions into a seamless experience. Dive into your data, uncover insights, and make data-driven decisions more effectively than ever before. Happy querying!
