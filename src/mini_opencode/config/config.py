import os
import threading
from pathlib import Path
from typing import Any

import yaml

# Global configuration cache
__config: dict[str, Any] | None = None
__lock = threading.Lock()


def load_config(config_path: str | Path | None = None) -> dict[str, Any]:
    """
    Load configuration from a YAML file.

    Args:
        config_path: Path to the configuration file. If None, it checks the
                     MINI_OPENCODE_CONFIG environment variable or defaults to 'config.yaml'.

    Returns:
        The loaded configuration as a dictionary.

    Raises:
        FileNotFoundError: If the configuration file cannot be found.
        yaml.YAMLError: If the configuration file is not valid YAML.
    """
    global __config

    if __config is not None:
        return __config

    with __lock:
        # Double-checked locking pattern
        if __config is not None:
            return __config

        if config_path is None:
            config_path = os.getenv("MINI_OPENCODE_CONFIG", "config.yaml")

        path = Path(config_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Configuration file not found at: {path.absolute()}. "
                "Please ensure config.yaml exists or set MINI_OPENCODE_CONFIG environment variable."
            )

        with path.open("r", encoding="utf-8") as f:
            try:
                data = yaml.safe_load(f)
                __config = data if data is not None else {}
            except yaml.YAMLError as e:
                raise yaml.YAMLError(
                    f"Error parsing configuration file {path}: {e}"
                ) from e

    return __config


def get_config_section(key: str | list[str]) -> Any:
    """
    Get a specific section or value from the configuration.

    Args:
        key: A string key or a list of keys for nested access.

    Returns:
        The configuration value or None if not found.
    """
    # Ensure config is loaded
    try:
        config = load_config()
    except FileNotFoundError:
        return None

    keys = [key] if isinstance(key, str) else key

    section = config
    for k in keys:
        if not isinstance(section, dict) or k not in section:
            return None
        section = section[k]

    return section


# Eagerly load configuration when the module is imported.
# This ensures that configuration errors are caught early.
if os.getenv("MINI_OPENCODE_SKIP_CONFIG_LOAD") != "1":
    try:
        load_config()
    except FileNotFoundError:
        # In some contexts (like building docs or simple imports),
        # we might not want to crash if config is missing.
        # But for an agent, it's usually better to fail fast.
        pass


if __name__ == "__main__":
    load_config()
    print(get_config_section("models"))
