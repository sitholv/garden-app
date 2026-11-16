"""Generate simple gardening advice without performing input on import.

The pure advice function can be reused by a console or another interface.
Run this file to choose a season and plant type interactively.
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


def read_choice(label, choices):
    """Prompt until a supported choice is entered.

    :param str label: Human-readable name of the choice being requested.
    :param dict choices: Supported labels and their advice.
    :return: A validated, normalised key.
    :rtype: str
    :raises EOFError: If input closes before a choice is made.
    :raises KeyboardInterrupt: If the user cancels with Ctrl+C.
    """
    prompt = label + " (" + ", ".join(choices) + "): "
    while True:
        try:
            return normalise_choice(input(prompt), choices)
        except ValueError as error:
            # Keep the retry at the input boundary; get_advice stays reusable.
            print(error)


def main():
    """Read two choices and print advice, returning exit status zero.

    EOF and Ctrl+C cancel without a traceback or a partially built response.
    Seasons are selected by the user rather than inferred from their country.

    :return: Zero after either a successful request or user cancellation.
    :rtype: int
    """
    print("Gardening advice: choose the season relevant to your location.")
    try:
        season = read_choice("Season", SEASON_ADVICE)
        plant_type = read_choice("Plant type", PLANT_ADVICE)
    except (EOFError, KeyboardInterrupt):
        print("\nAdvice request cancelled.")
        return 0
    print(get_advice(season, plant_type))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
