from typing import Dict, List, Final
from discord import app_commands


EMBED_LINK: Final[str] = "fxtwitter.com"

languages: List[Dict[str, str]] = [
    {"name": "Arabic", "code": "ar"},
    {"name": "Czech", "code": "cs"},
    {"name": "Danish", "code": "da"},
    {"name": "German", "code": "de"},
    {"name": "Greek", "code": "el"},
    {"name": "English", "code": "en"},
    {"name": "Spanish", "code": "es"},
    {"name": "French", "code": "fr"},
    {"name": "Hindi", "code": "hi"},
    {"name": "Hungarian", "code": "hu"},
    {"name": "Indonesian", "code": "id"},
    {"name": "Italian", "code": "it"},
    {"name": "Japanese", "code": "ja"},
    {"name": "Korean", "code": "ko"},
    {"name": "Norwegian", "code": "no"},
    {"name": "Dutch", "code": "nl"},
    {"name": "Polish", "code": "pl"},
    {"name": "Portuguese", "code": "pt"},
    {"name": "Romanian", "code": "ro"},
    {"name": "Russian", "code": "ru"},
    {"name": "Swedish", "code": "sv"},
    {"name": "Turkish", "code": "tr"},
    {"name": "Chinese", "code": "h"}
]


def list_to_choice_list() -> List[app_commands.Choice[str]]:
    languageList: List[app_commands.Choice[str]] = []
    for lang in languages:
        languageList.append(app_commands.Choice(name=lang["name"], value=lang["code"]))

    return languageList
