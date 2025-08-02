"""
VERN Pop Culture Reference Mapping
---------------------------------
Maps well-known characters, stories, and genres to archetype resonance vectors.
Used for onboarding and quick user profiling.

Functions:
- get_archetype_profile_from_character(character_name): returns resonance dict
- get_archetype_profile_from_genre(genre_name): returns resonance dict

Example mappings included; expand as needed.
"""

CHARACTER_ARCHETYPE_MAP = {
    "Harry Potter": {"Sage": 0.8, "Protector": 0.7, "Explorer": 0.6, "Nurturer": 0.5, "Phoenix": 0.8},
    "Katniss Everdeen": {"Challenger": 0.9, "Protector": 0.8, "Advocate": 0.7, "Builder": 0.5, "Phoenix": 0.7},
    "Dumbledore": {"Sage": 0.9, "Nurturer": 0.7, "Visionary": 0.8, "Phoenix": 0.9},
    "Iron Man": {"Creator": 0.8, "Visionary": 0.7, "Builder": 0.7, "Jester": 0.6, "Phoenix": 0.7},
    "Hermione Granger": {"Scholar": 0.9, "Builder": 0.7, "Advocate": 0.6, "Phoenix": 0.8},
    "Frodo Baggins": {"Explorer": 0.8, "Nurturer": 0.7, "Healer": 0.6, "Phoenix": 0.8},
    "Batman": {"Protector": 0.9, "Challenger": 0.7, "Builder": 0.6, "Phoenix": 0.7},
    "Spock": {"Scholar": 0.9, "Builder": 0.7, "Sage": 0.8, "Phoenix": 0.8},
    "Wonder Woman": {"Advocate": 0.9, "Protector": 0.8, "Visionary": 0.7, "Phoenix": 0.8},
    "Deadpool": {"Jester": 0.9, "Challenger": 0.7, "Creator": 0.6, "Phoenix": 0.7},
}

GENRE_ARCHETYPE_MAP = {
    "Fantasy": {"Explorer": 0.8, "Visionary": 0.7, "Nurturer": 0.6, "Phoenix": 0.8},
    "Science Fiction": {"Visionary": 0.8, "Creator": 0.7, "Scholar": 0.6, "Phoenix": 0.8},
    "Romance": {"Nurturer": 0.9, "Healer": 0.8, "Advocate": 0.7, "Phoenix": 0.7},
    "Mystery": {"Scholar": 0.8, "Builder": 0.7, "Explorer": 0.6, "Phoenix": 0.7},
    "Action": {"Protector": 0.8, "Challenger": 0.7, "Builder": 0.6, "Phoenix": 0.7},
    "Comedy": {"Jester": 0.9, "Creator": 0.7, "Nurturer": 0.6, "Phoenix": 0.7},
}

def get_archetype_profile_from_character(character_name: str) -> dict:
    """
    Returns archetype resonance dict for a given character.
    """
    return CHARACTER_ARCHETYPE_MAP.get(character_name, {})

def get_archetype_profile_from_genre(genre_name: str) -> dict:
    """
    Returns archetype resonance dict for a given genre.
    """
    return GENRE_ARCHETYPE_MAP.get(genre_name, {})

# Example usage:
# profile = get_archetype_profile_from_character("Harry Potter")
# genre_profile = get_archetype_profile_from_genre("Fantasy")
