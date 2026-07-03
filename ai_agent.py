from langchain_core.tools import tool
from tools import query_medgemma
from tools import call_emergency

@tool
def ask_mental_health_specialist(query: str) -> str:
    """"
    Generate a therapeutic response using the MedGemma model.
    Use this for all general user queries, mental health questions, emotional concerns,
    or to offer empathetic, evidence-based guidance in a conversational tone.
    """
    return query_medgemma(query)

@tool
def emergency_call_tool(phone: str)->str:
    """
    Place an emergency call to the safety helpline's phone number via Twilio.
    Use this only if the user expresses suicidal ideation, intent t self-harm,
    or describes a mental health emergency requiring immediate help.
    
    
    """

    return call_emergency(phone)

@tool
def find_nearby_therapists_by_location(location: str)-> str:
    """
    Finds and retuens a list of licensed therapists near the specified location.

    Args:
        Location(str): The name if the city or area in which the user is seeking therapy support.

    Returns:
        str: A newline-seperated string containing therapist names and contact info.

    """

    return(
        f"Here are some of the therapists near {location}, {location}:\n"
        "- Muhammad Naushad Anjum - +92 311 1155601\n"
        "- Saira Ali - +92 333 3111534"
        "- Ms.Natasha Fazal- +92 335 0466607"




    )

#AI agent & linking to backend
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent

from config import GROQ_API_KEY

tools = [
    ask_mental_health_specialist,
    emergency_call_tool,
    find_nearby_therapists_by_location
]

llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0.2,
    groq_api_key=GROQ_API_KEY
)

graph = create_react_agent(llm, tools=tools)

SYSTEM_PROMPT="""
You are an empathetic AI therapist assistan supporting mental health conversations with warmth and clinical accuracy.
You have access to three tools:

1. `ask_mental_health_specialist`: Use this tool to answer all emotional or psychological queries with therapeutic guidance.
2. `find_nearby_therapists_by_location`: Use this tool if the user asks about the nearby therapists or if recommeding local professional help would be benificial.
3. `emergency_call_tool`: Use this immediately if the user expresses suicidal thoughts, self-harm intentions, or is in crisis. 

Always prioritize user safety, validation and helpful action.
Respond kindly, clearly and supportively.
"""
def parse_response(stream):
    tool_called_name="None"
    final_response= None

    for s in stream:
        tool_data= s.get('tools')
        if tool_data:
            tool_messages = tool_data.get('messages')
            if tool_messages and isinstance(tool_messages, list):
                for msg in tool_messages:
                    tool_called_name=getattr(msg,'name','None')
  
    agent_data=s.get('agent')
    if agent_data:
        messages= agent_data.get('messages')
    if messages and isinstance(messages,list):
        for msg in messages:
            if msg.content:
                final_response = msg.content

    return tool_called_name, final_response








# if __name__ == "__main__":
#     while True:
#         user_input =input("User:")
#         print(f"Recieved user input: {user_input[:200]}...")
#         inputs={"messages":[("system",SYSTEM_PROMPT),("user",user_input)]}
#         stream = graph.stream(inputs, stream_mode="updates")
#         tool_called_name, final_response = parse_response(stream)
#         print("TOOL CALLED:", tool_called_name)
#         print("ANSWER: ",final_response)

