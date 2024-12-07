import re

regex_snake_1 = re.compile(r"(.)([A-Z][a-z]+)")
regex_snake_2 = re.compile(r"([a-z0-9])([A-Z])")


def to_snakecase(name: str) -> str:
    s1 = regex_snake_1.sub(r"\1_\2", name)
    return regex_snake_2.sub(r"\1_\2", s1).lower()
