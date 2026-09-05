
import os

import certifi
import requests
import streamlit as st
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_google_genai import ChatGoogleGenerativeAI

os.environ["SSL_CERT_FILE"] = certifi.where()
load_dotenv()

st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 AI Assistant")
st.caption("Ask questions, search the web, or check the weather.")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")


@tool
def get_current_weather(location: str) -> str:
    """Fetch the current temperature and weather description for a city."""
    if not WEATHER_API_KEY:
        return "Weather API key is not configured."

    try:
        response = requests.get(
            "http://api.weatherstack.com/current",
            params={
                "access_key": WEATHER_API_KEY,
                "query": location,
            },
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()

        if "error" in data:
            return f"Weather error: {data['error'].get('info', 'Unknown error')}"

        current = data["current"]
        description = ", ".join(current.get("weather_descriptions", []))
        temperature = current.get("temperature")

        return (
            f"The current weather in {location} is "
            f"{temperature}°C with {description}."
        )
    except requests.RequestException as error:
        return f"Could not retrieve weather data: {error}"


@st.cache_resource
def get_agent():
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY is not configured.")

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        google_api_key=GOOGLE_API_KEY,
        temperature=0,
    )

    search_tool = TavilySearchResults(max_results=2)

    return create_agent(
        model=llm,
        tools=[search_tool, get_current_weather],
        system_prompt=(
            "You are a helpful AI assistant. "
            "Use the search tool for current information. "
            "Use the weather tool for weather questions. "
            "Answer clearly and concisely."
        ),
    )


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask me anything...")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Thinking..."):
                agent = get_agent()
                result = agent.invoke(
                    {"messages": [("user", prompt)]}
                )
                answer = result["messages"][-1]
                if isinstance(answer.content, list) and len(answer.content) > 0:
                    clean_text = answer.content[0].get("text", "")
                else:
                    clean_text = answer.content 

            st.markdown(clean_text)
            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )
        except Exception as error:
            st.error(f"Unable to process your request: {error}")

with st.sidebar:
    st.header("Settings")

    if st.button("Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.info(
        "The assistant can answer general questions, search for "
        "current information, and provide weather updates."
    )






# import os
# from dotenv import load_dotenv
# import certifi
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_community.tools.tavily_search import TavilySearchResults
# from langchain.agents import create_agent
# from langchain.tools import tool
# import requests










# os.environ["SSL_CERT_FILE"] = certifi.where()
# load_dotenv()

# OPEN_API_KEY = os.getenv("OPEN_API_KEY")
# TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
# os.environ["LANGCHAIN_VERBOSE"] = "true"
# os.environ["LANGCHAIN_DEBUG"] = "true"


# search_tool = TavilySearchResults(max_results=2)
# result = search_tool.invoke("Give me the latest news on AI and machine learning.")
# result

# @tool
# def get_current_weather(location: str) -> str:  

     
#     """Fetch the current temperature and weather description for a given city location."""  
#     url = (f"http://api.weatherstack.com/current?access_key={WEATHER_API_KEY}&query={location}")
#     response = requests.get(url)
#     if response.status_code == 200:
#         data = response.json()
#         temperature = data["current"]["temperature"]
#         description = data["current"]["weather_descriptions"]
#         return f"The current weather in {location} is {temperature}°C with {description}."
#     else:       
#         return f"Could not retrieve weather data for {location}. Please check the location name and try again."


#                                                                                                                 # import google.generativeai as genai
#                                                                                                                 # import os

#                                                                                                                 # genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#                                                                                                                 # for m in genai.list_models():
#                                                                                                                 #     if 'generateContent' in m.supported_generation_methods:
#                                                                                                                 #         print(m.name)
#                                                                                                                 # print("Google key exists:", bool(os.getenv("GOOGLE_API_KEY")))

#                                                                                                                 # gemini_llm = ChatGoogleGenerativeAI(
#                                                                                                                 #     model="gemini-pro",
#                                                                                                                 #     temperature=0, google_api_key= GOOGLE_API_KEY
#                                                                                                                 # )

#                                                                                                                 # print("LLM type:", type(gemini_llm))

#                                                                                                                 # response = gemini_llm.invoke("What is an AI agent?")
#                                                                                                                 # print(response.content)

#                                                                                                                 # response = llm.invoke("Give me the latest news on AI and machine learning.")
#                                                                                                                 # response
# # Gemini
# llm = ChatGoogleGenerativeAI(
#     model="gemini-3.6-flash",
#     google_api_key=os.getenv("GOOGLE_API_KEY")
# )

# system_prompt = """
# You are a helpful AI assistant.

# Use the search tool when you need current information.
# Use the weather tool when you need weather information.
# """

# response = llm.invoke("Tell me a joke about AI")
# response

# agents = create_agent (
#     model=llm,
#     tools=[search_tool, get_current_weather],
#     system_prompt=system_prompt,
#     debug=True
# )
# # Pass the input as a structured state dictionary
# results = agents.invoke({"messages": [("user", "Tell me the current capital city of karnataka and its weather status")]})

# # Print the clean text from the final message
# print(results["messages"][-1].content)