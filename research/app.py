import os
from dotenv import load_dotenv
import certifi
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import create_agent










os.environ["SSL_CERT_FILE"] = certifi.where()
load_dotenv()

OPEN_API_KEY = os.getenv("OPEN_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
os.environ["LANGCHAIN_VERBOSE"] = "true"
os.environ["LANGCHAIN_DEBUG"] = "true"


search_tool = TavilySearchResults(max_results=2)
result = search_tool.invoke("Give me the latest news on AI and machine learning.")
result


                                                                                                                # import google.generativeai as genai
                                                                                                                # import os

                                                                                                                # genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

                                                                                                                # for m in genai.list_models():
                                                                                                                #     if 'generateContent' in m.supported_generation_methods:
                                                                                                                #         print(m.name)
                                                                                                                # print("Google key exists:", bool(os.getenv("GOOGLE_API_KEY")))

                                                                                                                # gemini_llm = ChatGoogleGenerativeAI(
                                                                                                                #     model="gemini-pro",
                                                                                                                #     temperature=0, google_api_key= GOOGLE_API_KEY
                                                                                                                # )

                                                                                                                # print("LLM type:", type(gemini_llm))

                                                                                                                # response = gemini_llm.invoke("What is an AI agent?")
                                                                                                                # print(response.content)

                                                                                                                # response = llm.invoke("Give me the latest news on AI and machine learning.")
                                                                                                                # response
# Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

system_prompt = """
You are a helpful AI assistant.

Use the search tool when you need current information.
Use the weather tool when you need weather information.
"""

response = llm.invoke("Tell me a joke about AI")
response

agents = create_agent (
    model=llm,
    tools=[search_tool],
    system_prompt=system_prompt,
    debug=True
)
# Pass the input as a structured state dictionary
results = agents.invoke({"messages": [("user", "Tell me a joke about AI")]})

# Print the clean text from the final message
print(results["messages"][-1].content)
