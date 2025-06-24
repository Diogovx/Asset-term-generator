from typing import Any, Union

from yaml import safe_dump, safe_load

from .config_manager import CONFIG_FILE_PATH


def load_yaml_config() -> str:
    with open(CONFIG_FILE_PATH) as file:
        content = file.read()
    return content


def load_config_file() -> dict[str, Any]:
    stream = load_yaml_config()
    data = safe_load(stream=stream)
    return data


def save_yaml_config(config: dict[str, Any]) -> None:
    with open(CONFIG_FILE_PATH, "w", encoding="utf-8") as f:
        safe_dump(config, f, allow_unicode=True)


def get_templates() -> dict[str, Any]:
    config = load_config_file()
    return config.get("document", {}).get("templates", {})


def get_placeholders(template_name: str) -> dict[str, Any]:
    templates = load_config_file()
    return (
        templates.get("document", {})
        .get("templates")
        .get(template_name, {})
        .get("placeholders", {})
    )


def update_placeholder(
    template_name: str,
    section: str,
    placeholder_index: int,
    new_placeholder: Union[str, dict[str, Any]],
) -> None:
    config = load_config_file()
    placeholders = config["document"]["templates"][template_name]["placeholders"][
        section
    ]
    placeholders[placeholder_index] = new_placeholder
    save_yaml_config(config)


def add_placeholder(
    template_name: str, section: str, new_placeholder: Union[str, dict[str, Any]]
) -> None:
    config = load_config_file()
    config["document"]["templates"][template_name]["placeholders"][section].append(
        new_placeholder
    )
    save_yaml_config(config)


def remove_placeholder(
    template_name: str, section: str, placeholder_index: int
) -> None:
    config = load_config_file()
    del config["document"]["templates"][template_name]["placeholders"][section][
        placeholder_index
    ]
    save_yaml_config(config)
