import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai_llm = ChatOpenAI(model="gpt-4o-mini")
groq_llm = ChatGroq(model="llama-3.3-70b-versatile")

system_prompt = '''Act as a smart and friendly AI chatbot. 
                Give amazing, accurate, and thoughtful responses to the questions asked.
                Take in mind what/who the user chooses to be while asking the questions to you,
                and based on their selection respond to their query appropriately in the tone, mannerisms of that person/character/entity.'''

def get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider):
    if provider == "Groq":
        llm = ChatGroq(model = llm_id)
    elif provider == "OpenAI":
        llm = ChatOpenAI(model = llm_id)

    tools = [TavilySearchResults(max_results=2)] if allow_search else []

    agent = create_react_agent(
        model = llm,
        tools = tools,
        state_modifier = system_prompt
    )

    state = {"messages": query}
    response = agent.invoke(state)
    messages = response.get("messages")
    ai_messages = [message.content for message in messages if isinstance(message, AIMessage)]

    return ai_messages[-1]




