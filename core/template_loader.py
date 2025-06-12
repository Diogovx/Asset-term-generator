from yaml import CLoader as Loader
from yaml import load, safe_dump

from .config_manager import CONFIG_FILE_PATH


def load_yaml_config():
    with open(CONFIG_FILE_PATH) as file:
        content = file.read()
    return content

def load_config_file():
    stream = load_yaml_config()
    data = load(stream=stream, Loader=Loader)
    return data

def save_yaml_config(config):
    with open(CONFIG_FILE_PATH, "w", encoding="utf-8") as f:
        safe_dump(config, f, allow_unicode=True)

def get_templates():
    config = load_config_file()
    return config.get("document", {}).get("templates", {})

def get_placeholders(template_name):
    templates = load_config_file()
    return templates.get(
        'document', {}
        ).get('templates').get(template_name, {}
                            ).get("placeholders", {})

def update_placeholder(template_name, section, placeholder_index, new_placeholder):
    config = load_config_file()
    placeholders = config["document"]["templates"][template_name]["placeholders"][section]
    placeholders[placeholder_index] = new_placeholder
    save_yaml_config(config)

def add_placeholder(template_name, section, new_placeholder):
    config = load_config_file()
    config["document"]["templates"][template_name]["placeholders"][section].append(new_placeholder)
    save_yaml_config(config)

def remove_placeholder(template_name, section, placeholder_index):
    config = load_config_file()
    del config["document"]["templates"][template_name]["placeholders"][section][placeholder_index]
    save_yaml_config(config)