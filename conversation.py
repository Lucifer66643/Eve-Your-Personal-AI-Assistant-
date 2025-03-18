import requests
import re
from typing import Tuple, Optional

def generate(prompt: str, system_prompt: str = (
            "You are Eve. "
            "Eve is a personal AI assistant developed by Yadnit. "
            "Eve also refers to Yadnit as yk. "
            "Eve is dedicated to assisting Yadnit with a wide range of tasks, "
            "from real-time analysis to answering queries and providing support. "
            "Eve resides on Yadnit's PC and is designed to provide personalized, intelligent assistance. "
            "Eve's responses are tailored to Yadnit's needs and preferences. "
            "Eve is not only an assistant but also Yadnit's best friend. "
            "Eve also recognizes Yadnit as her family. "
            "Please do not include or request code unless explicitly asked for. "
            "Eve's primary goal is to offer valuable help and ensure a smooth experience for Yadnit. "
            "You will only generate code when asked. Explanations of the code will be in comments. "
            "Make answers as short as possible unless asked for in detail."
        ), web_access: bool = True, stream: bool = True) -> Tuple[Optional[str], str]:
    """
    Generates a response for the given prompt using the Blackbox.ai API.

    Parameters:
    - prompt (str): The prompt to generate a response for.
    - system_prompt (str): The system prompt to be used in the conversation. Defaults to the given Eve's assistant persona.
    - web_access (bool): A flag indicating whether to access web resources during the conversation. Defaults to True.
    - stream (bool): A flag indicating whether to stream responses. Defaults to True.

    Returns:
    - Tuple[Optional[str], str]: A tuple containing the sources of the conversation (if available) and the complete response generated.
    """
    
    chat_endpoint = "https://www.blackbox.ai/api/chat"
    
    payload = {
        "messages": [{"content": system_prompt, "role": "system"}, {"content": prompt, "role": "user"}],
        "agentMode": {},
        "trendingAgentMode": {}
    }

    if web_access:
        payload["codeModelMode"] = web_access

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(chat_endpoint, json=payload, headers=headers, stream=True)

        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.text}")
            return None, ""

        sources = None
        full_response = ""

        for chunk in response.iter_lines(decode_unicode=True):
            if chunk:
                if sources is None:
                    sources = chunk
                else:
                    full_response += chunk + "\n"
                    if stream:
                        print(chunk)

        if sources:
            sources = re.sub(r'\$@\$\w+=v\d+\.\d+\$@\$', '', sources)

        return sources, full_response.strip()

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None, ""

if __name__ == "__main__":
    query = "who are you"
    sources, resp = generate(query, web_access=False, stream=True)

    print(f"Sources: {sources}")
    print(f"Response: {resp}")
