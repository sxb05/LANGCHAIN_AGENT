# LangChain AI Assistant

A Streamlit-based AI assistant that can answer general questions, search the web for current information, and report the current weather for a city. The assistant uses a LangChain agent powered by Google Gemini and keeps the conversation in the current Streamlit session.

## Live Demo

[Open the deployed web app](https://langchain-agent-p2z5.onrender.com/)

## Features

- Conversational chat interface with session-based message history
- Google Gemini model for response generation
- Tavily web search for up-to-date information
- Weatherstack integration for current weather updates
- Sidebar control to clear the current conversation
- Friendly error messages when a service or API key is unavailable

## Tech Stack

- Python 3.11
- Streamlit
- LangChain
- Google Generative AI / Gemini
- Tavily Search
- Weatherstack

## Local Setup

Create and activate a Conda environment, then install the dependencies:

```bash
conda create -n lagent python=3.11 -y
conda activate lagent
pip install -r requirements.txt
```

Create a `.env` file in the project root with the API keys used by the app:

```env
GEMINI_3.8_KEY=your_gemini_api_key
WEATHER_API_KEY=your_weatherstack_api_key
TAVILY_API_KEY=your_tavily_api_key
```

The Gemini key is required to initialize the agent. The weather and search integrations require their respective keys when those tools are used.

## Run Locally

```bash
streamlit run app.py
```

Then open the local URL shown by Streamlit in your browser.

## Project Structure

```text
.
├── app.py                 # Streamlit application and LangChain agent
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
└── research/
	└── agent_demo.ipynb   # Related experiments and demonstrations
```

## How It Works

1. Streamlit loads the chat interface and restores messages from session state.
2. A LangChain agent connects the Gemini model to the Tavily search and weather tools.
3. The agent selects a tool when a question needs current web or weather data.
4. The final response is displayed and added to the conversation history.