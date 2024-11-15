from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableLambda

from langgraph.prebuilt import ToolNode


def handle_tool_error(state) -> dict:
    error = state.get("error")
    tool_calls = state["messages"][-1].tool_calls
    return {
        "messages": [
            ToolMessage(
                content=f"Error: {repr(error)}\n please fix your mistakes.",
                tool_call_id=tc["id"],
            )
            for tc in tool_calls
        ]
    }


def create_tool_node_with_fallback(tools: list) -> dict:
    return ToolNode(tools).with_fallbacks(
        [RunnableLambda(handle_tool_error)], exception_key="error"
    )

def _print_event(event: dict, _printed: set, max_length=1500):
    """
    Prints the latest message in a chat event if it hasn't been printed before.
    """

    # Check for messages to print
    message = event.get("messages")

    if "Tool Calls:" in str(event) or "Tool Message:" in str(event):
        return  # Skip tool messages

    if message:
        if isinstance(message, list):
            message = message[-1]
        # Check if message is from a tool and skip if it is
        if getattr(message, 'type', None) in ["tool_message", "Tool Message"] or \
           getattr(message, 'role', None) == "tool":
            return  # Skip tool messages
        if message.id not in _printed:
            msg_repr = message.pretty_repr(html=True)
            if len(msg_repr) > max_length:
                msg_repr = msg_repr[:max_length] + " ... (truncated)"
            print(msg_repr)
            _printed.add(message.id)

def interact_with_chatbot(send_message):
    """
    Continuously interact with the chatbot via CLI.
    :param send_message: Function to send a message to the chatbot and receive a response.
    """
    _printed = set()
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in {"exit", "quit"}:
            print("Exiting chat.")
            break
        
        # Send the user input to the chatbot
        event = send_message(user_input)
        
        # Print the chatbot's response if it's new
        _print_event(event, _printed)
