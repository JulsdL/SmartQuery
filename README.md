title: SmartQuery
emoji: 🔍
colorFrom: blue
colorTo: yellow
sdk: docker
pinned: false

# SmartQuery

SmartQuery is an intelligent assistant designed to provide seamless interaction with your database. Built on top of LangChain and Chainlit, and using the OpenAI API, SmartQuery allows users to query their database using natural language, either through text or voice commands.

## Features

- **Natural Language Querying:** Interact with your database using plain English, no SQL required.
- **Voice Commands:** Ask questions out loud and get verbal responses.
- **Rich Insights:** Get detailed answers and insights from your data.
- **User-Friendly Interface:** Simple chat-based interaction for ease of use.

## Setup

Clone the repository:

```bash
git clone https://github.com/your-repo/SmartQuery.git
cd SmartQuery
```

Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

Create and populate the database:

```bash
sqlite3 database/Chinook.db
.read database/Chinook_Sqlite.sql
.exit
```

Create a .env file and add your environment variables:

```bash
OPENAI_API_KEY=your-openai-key-here
ELEVENLABS_API_KEY=your-elevenlabs-key-here
ELEVENLABS_VOICE_ID=your-elevenlabs-voice-id-here
```

Run the application using the following command:

```bash
chainlit run app.py
```

## Usage

Start a chat session and ask questions related to the content of the Chinook database. The application supports both text and voice input. For voice input, press the microphone button, speak your question, and let SmartQuery process your query. It might take some time to answer complex questions (usually less than 1 minute), so please be patient.

### Sample Questions to Try:

- "What is the most expensive track?"
- "List the total sales per country. Which country's customers spent the most?"
- "Who are the 3 most listened artists and what is their average revenue?"

## About the Database

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

## Acknowledgements

This project uses technologies including LangChain, OpenAI's GPT models, FAISS for vector storage, Eleven Labs for speech-to-text and text-to-speech, and ChainLit for building interactive AI applications. Thanks to all open-source contributors and organizations that make these tools available.
