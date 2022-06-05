"""
Various utility methods used through out the app.
"""
from textwrap import dedent
import markdown
import bleach


def md_to_html(text: str):
    """
    Parses and sanitizes Markdown to HTML.

    Args:
        md (str): The Markdown text.

    Returns:
        str: The parsed and sanitized HTML.
    """
    text = dedent(text.strip())
    html = markdown.markdown(text)

    return bleach.clean(
        html,
        tags=[
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
        attributes={"img": ["src"], "a": ["href"]},
    )
