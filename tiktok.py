from typing import Final, Dict, List
import discord
from discord import app_commands

TIKTOK_VOICE_CODES: Final[List[Dict[str, str]]] = [
    # DISNEY VOICES
    {"name": "Ghost Face", "code": "en_us_ghostface"},
    {"name": "Chewbacca", "code": "en_us_chewbacca"},
    {"name": "C3PO", "code": "en_us_c3po"},
    {"name": "Stitch", "code": "en_us_stitch"},
    {"name": "Stormtrooper", "code": "en_us_stormtrooper"},
    {"name": "Rocket", "code": "en_us_rocket"},

    # UK
    {"name": "English UK - Male 1", "code": "en_uk_001"},
    {"name": "English UK - Male 2", "code": "en_uk_003"},
    # AU
    {"name": "English AU - Female", "code": "en_au_001"},
    {"name": "English AU - Male", "code": "en_au_002"},
    # US
    {"name": "The most overused female voice", "code": "en_us_001"},
    {"name": "English US - Male 1", "code": "en_us_006"},

    # EMOTIONAL ENGLISH ONES
    {"name": "Narrator", "code": "en_male_narration"},
    {"name": "Wacky", "code": "en_male_funny"},
    {"name": "Peaceful", "code": "en_female_emotional"},
    {"name": "Serious", "code": "en_male_cody"},
    # VOCALS
    {"name": "Alto", "code": "en_female_f08_salut_damour"},
    {"name": "Tenor", "code": "en_male_m03_lobby"},
    {"name": "Sunshine Soon", "code": "en_male_m03_sunshine_soon"},
    {"name": "Warmy Breeze", "code": "en_female_f08_warmy_breeze"},
    {"name": "Glorious", "code": "en_female_ht_f08_glorious"},
    {"name": "It Goes Up", "code": "en_male_sing_funny_it_goes_up"},
    {"name": "Chipmunk", "code": "en_male_m2_xhxs_m03_silly"},
    {"name": "Dramatic", "code": "en_female_ht_f08_wonderful_world"}
]

