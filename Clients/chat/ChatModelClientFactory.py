import os
import dotenv
from utils.load_config_obj import load_config_obj
from langchain.chat_models import init_chat_model

dotenv.load_dotenv()

available_models = [
    "o3-mini"
]

CONFIG = load_config_obj("config.json")
CHAT_CLIENT_CONFIG = CONFIG.get("chatClient", {})
CHAT_COMPLETIONS_CONFIG = CONFIG.get("chatCompletions", {})

def validate_chat_client_env(env: dict) -> None:
    """
    Validates the chat client environment variables.

    :param env: Dictionary containing chat client environment variables.
    :raises ValueError: If required keys are missing or invalid.
    """
    required_keys = ["api_key", "endpoint", "api_version"]
    for key in required_keys:
        if key not in env:
            raise ValueError(f"Missing required chat client environment variable: {key}")


def create_chat_model_client():
    """
    Creates and returns a ChatModelClient instance.

    :return: An instance of ChatModelClient.
    """
    env = {
        "api_key": os.getenv("AZURE_INFERENCE_CREDENTIAL"),
        "endpoint": os.getenv("AZURE_INFERENCE_ENDPOINT"),
        "api_version": os.getenv("AZURE_OPENAI_API_VERSION")
    }

    validate_chat_client_env(env)

    client = init_chat_model(
            "o3-mini",
            model_provider="azure_openai"
    )        

    return client