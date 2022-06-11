"""
Various utility methods used through out the app.
"""
from textwrap import dedent
import markdown
import bleach

from pymdownx import emoji

extensions = [
    "markdown.extensions.tables",
    "pymdownx.magiclink",
    "pymdownx.betterem",
    "pymdownx.tilde",
    "pymdownx.emoji",
    "pymdownx.tasklist",
    "pymdownx.superfences",
    "pymdownx.saneheaders",
]

extension_configs = {
    "pymdownx.magiclink": {
        "repo_url_shortener": True,
        "repo_url_shorthand": True,
        "provider": "github",
        "user": "facelessuser",
        "repo": "pymdown-extensions",
    },
    "pymdownx.tilde": {"subscript": False},
    "pymdownx.emoji": {
        "emoji_index": emoji.gemoji,
        "emoji_generator": emoji.to_png,
        "alt": "short",
        "options": {
            "attributes": {"align": "absmiddle", "height": "20px", "width": "20px"},
            # "image_path": "https://assets-cdn.github.com/images/icons/emoji/unicode/",
            # "non_standard_image_path": "https://assets-cdn.github.com/images/icons/emoji/",
        },
    },
}

md = markdown.Markdown(extensions=extensions, extension_configs=extension_configs)


def md_to_html(text: str):
    """
    Parses and sanitizes Markdown to HTML.

    Args:
        md (str): The Markdown text.

    Returns:
        str: The parsed and sanitized HTML.
    """
    text = dedent(text.strip())
    html = md.convert(text)

    return bleach.clean(
        html,
        tags=[
            "span",
            "div",
            "a",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "p",
            "em",
            "strong",
            "ul",
            "ol",
            "li",
            "code",
            "img",
            "pre",
        ],
        attributes={
            "img": ["src"],
            "a": ["href"],
            "span": ["class"],
            "div": ["class"],
            "code": ["class"],
        },
    )
