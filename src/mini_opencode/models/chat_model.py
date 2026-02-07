from langchain_core.language_models import BaseChatModel
from langchain_deepseek import ChatDeepSeek
from langchain_openai.chat_models import ChatOpenAI

from mini_opencode.config import get_config_section


def init_chat_model() -> BaseChatModel:
    """
    Initialize the chat model client based on the configuration.

    The configuration is read from the `models/chat_model` section in `config.yaml`.
    Supports different model types like 'deepseek', 'kimi', and defaults to OpenAI-compatible.

    Returns:
        BaseChatModel: An instance of a LangChain chat model.

    Raises:
        ValueError: If required configuration settings are missing.
    """
    settings = get_config_section(["models", "chat_model"])
    if not settings:
        raise ValueError(
            "The `models/chat_model` section in `config.yaml` is not found. "
            "Please check your configuration file."
        )

    model_name = settings.get("model")
    if not model_name:
        raise ValueError(
            "The `model` name is not specified in the `models/chat_model` section."
        )

    api_key = settings.get("api_key")
    if not api_key:
        raise ValueError(
            "The `api_key` is not specified in the `models/chat_model` section."
        )

    # Prepare settings for the model constructor
    rest_settings = settings.copy()
    model_type = rest_settings.pop("type", None)
    rest_settings.pop("model", None)
    rest_settings.pop("api_key", None)

    if model_type == "deepseek":
        return ChatDeepSeek(model=model_name, api_key=api_key, **rest_settings)

    # Default to OpenAI for other types or if type is not specified
    return ChatOpenAI(model=model_name, api_key=api_key, **rest_settings)


if __name__ == "__main__":
    chat_model = init_chat_model()
    print(chat_model.invoke("Hello!"))
