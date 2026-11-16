"""Generate simple gardening advice without performing input on import.

The pure advice function can be reused by a console or another interface.
The summer/flower example preserves the supplied starter output.
"""

SEASON_ADVICE = {
    "summer": "Water your plants regularly and provide some shade.",
    "winter": "Protect your plants from frost with covers.",
}

PLANT_ADVICE = {
    "flower": "Use fertiliser to encourage blooms.",
    "vegetable": "Keep an eye out for pests!",
}


def normalise_choice(value, choices):
    """Return a supported, case-insensitive choice without outer spaces.

    :param str value: The user's season or plant choice.
    :param dict choices: Supported labels mapped to their advice.
    :return: The normalised dictionary key.
    :rtype: str
    :raises TypeError: If the value is not a string.
    :raises ValueError: If the label is empty or unsupported.
    """
    if not isinstance(value, str):
        raise TypeError("A choice must be text.")
    choice = value.strip().casefold()
    if choice not in choices:
        raise ValueError("Choose one of: " + ", ".join(choices) + ".")
    return choice


def get_advice(season, plant_type):
    """Combine supported season and plant advice in two lines.

    :param str season: Summer or winter, ignoring case and outer spaces.
    :param str plant_type: Flower or vegetable, normalised the same way.
    :return: Season advice, a newline, then plant advice.
    :rtype: str
    :raises TypeError: If either choice is not text.
    :raises ValueError: If either choice is unsupported.
    """
    season = normalise_choice(season, SEASON_ADVICE)
    plant_type = normalise_choice(plant_type, PLANT_ADVICE)
    return SEASON_ADVICE[season] + "\n" + PLANT_ADVICE[plant_type]


def main():
    """Print the starter's example when executed directly."""
    print(get_advice("summer", "flower"))


if __name__ == "__main__":
    main()
