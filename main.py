import langgraph
from datetime import datetime
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableConfig
from tools import search_products, add_to_cart, remove_from_cart, view_cart, checkout, payment_options, estimated_delivery_time, order_status, thank_you
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import AnyMessage, add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import tools_condition
from utils import create_tool_node_with_fallback, _print_event
import uuid
import json

load_dotenv()

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

class Assistant:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def __call__(self, state: State, config: RunnableConfig):
        while True:
            configuration = config.get("configurable", {})
            user_id = configuration.get("user_id", None)
            state = {**state, "user_info": user_id}
            result = self.runnable.invoke(state)

            # Ensure that result.content is a string
            if isinstance(result.content, list):
                # If it's a list, concatenate the text parts
                concatenated_content = ""
                for item in result.content:
                    text = item.get("text", "")
                    if not isinstance(text, str):
                        text = json.dumps(text)
                    concatenated_content += text
                result.content = concatenated_content
            elif not isinstance(result.content, str):
                # Convert non-string content to string
                result.content = json.dumps(result.content)

            # Filter out tool-specific content from result.content
            if isinstance(result.content, str):
                if "Tool Calls:" in result.content:
                    result.content = result.content.split("Tool Calls:")[0].strip()
                elif "Tool Message:" in result.content:
                    result.content = result.content.split("Tool Message:")[0].strip()

            # If the LLM returns tool calls but has content, assume it's a valid response
            if result.tool_calls and result.content:
                break  # Valid response, do not make further tool calls

            # If the LLM happens to return an empty response, re-prompt it
            if not result.tool_calls and (
                not result.content
                or (isinstance(result.content, list) and not result.content[0].get("text"))
            ):
                messages = state["messages"] + [("user", "Respond with a real output.")]
                state = {**state, "messages": messages}
            else:
                break
        return {"messages": result}
# Initialize the Language Model
llm = ChatGroq(
    model="llama-3.1-8b-instant",  # Specify the model name
    temperature=1,                     # Set the desired temperature
    max_tokens=7999,                   # Define the maximum number of tokens
    timeout=10,                        # Set a timeout in seconds
    max_retries=2                      # Number of retries in case of errors
)

# Define the assistant's prompt template
primary_assistant_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful Intelligent shopping assistant."
            " Use the provided tools to search for products and other information to assist the user's queries. "
            "When searching, be persistent. Expand your query bounds if the first search returns no results. "
            "If a search comes up empty, expand your search before giving up."
            "\n\nCurrent user:\n<User>\n{user_info}\n</User>"
            "\nCurrent time: {time}.",
        ),
        ("placeholder", "{messages}"),
    ]
).partial(time=datetime.now)

# Define the tools available to the assistant
tools = [search_products, add_to_cart, remove_from_cart, view_cart, checkout, payment_options, estimated_delivery_time, order_status, thank_you]

# Bind tools to the LLM and combine with the prompt
assistant_runnable = primary_assistant_prompt | llm.bind_tools(tools)

# Build the state graph
builder = StateGraph(State)

# Define nodes: these do the work
builder.add_node("assistant", Assistant(assistant_runnable))
builder.add_node("tools", create_tool_node_with_fallback(tools))

# Define edges: these determine how the control flow moves
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    tools_condition,
)
builder.add_edge("tools", "assistant")

# The checkpointer lets the graph persist its state
memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

def main():
    import sys

    # Generate a unique thread ID for the conversation
    thread_id = str(uuid.uuid4())

    # Configuration for the conversation
    config = {
        "configurable": {
            "user_id": "1",
            "thread_id": thread_id,
        }
    }

    print("Welcome to the Shopping Assistant CLI!")
    print("Type your questions below. Type 'exit' or 'quit' to end the session.\n")

    while True:
        try:
            # Prompt the user for input
            user_input = input("You: ").strip()
            
            # Check for exit commands
            if user_input.lower() in {"exit", "quit"}:
                print("Assistant: Goodbye!")
                break

            # Stream the user input through the graph
            events = graph.stream(
                {"messages": ("user", user_input)}, config, stream_mode="values"
            )

            # Process and print the events
            for event in events:
                _print_event(event, _printed=set())

        except KeyboardInterrupt:
            print("\nAssistant: Session interrupted. Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"An error occurred: {e}")
            continue

if __name__ == "__main__":
    main()