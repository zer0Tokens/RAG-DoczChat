import re


UNWANTED = [
    r"\\n",
    "  —",
    "——————————",
    "—————————",
    "—————",
    r"\\u[\dA-Fa-f]{4}",
    r"\uf075",
    r"\uf0b7",
]


def clean(text: str) -> str:
    # fix hyphenated line breaks
    text = re.sub(r"(\w+)-\n(\w+)", r"\1\2", text)

    for pat in UNWANTED:
        text = re.sub(pat, "", text)

    # tidy spaces / hyphens
    text = re.sub(r"(\w)\s*-\s*(\w)", r"\1-\2", text)
    return re.sub(r"\s+", " ", text).strip()
