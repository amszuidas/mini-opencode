from langchain.agents.middleware import SummarizationMiddleware
from langchain_core.language_models import BaseChatModel

from mini_opencode.config import get_config_section


def get_summarization_middleware(
    model: BaseChatModel | str,
) -> SummarizationMiddleware | None:
    """
    Get the summarization middleware based on configuration.

    Returns:
        The SummarizationMiddleware instance if enabled, otherwise None.
    """
    config = get_config_section(["middlewares", "configs", "summarization"])
    enabled_middlewares = get_config_section(["middlewares", "enabled"])

    if not enabled_middlewares or "summarization" not in enabled_middlewares:
        return None

    if not config:
        config = {}

    trigger_tokens = config.get("trigger_tokens", 8192)
    keep_messages = config.get("keep_messages", 10)

    return SummarizationMiddleware(
        model=model,
        trigger=("tokens", trigger_tokens),
        keep=("messages", keep_messages),
    )
