"""Safe Markdown rendering for the read-only learner viewer."""

from __future__ import annotations

from html import escape
from urllib.parse import urlsplit

from markdown_it import MarkdownIt
from markdown_it.token import Token


def _is_external_url(href: str) -> bool:
    parsed = urlsplit(href)
    return bool(parsed.scheme or href.startswith("//"))


def _render_link_open(
    tokens: list[Token], index: int, options: dict[str, object], env: object
) -> str:
    token = tokens[index]
    href = token.attrGet("href") or ""
    if _is_external_url(href):
        token.attrSet("rel", "noopener noreferrer")
    return MARKDOWN.renderer.renderToken(tokens, index, options, env)


def _render_image_as_alt(
    tokens: list[Token], index: int, options: dict[str, object], env: object
) -> str:
    token = tokens[index]
    alt = token.attrGet("alt") or token.content or "Image"
    return f'<span class="markdown-image-alt">[Image: {escape(alt)}]</span>'


MARKDOWN = (
    MarkdownIt("commonmark", {"html": False, "linkify": False, "typographer": False})
    .enable("table")
    .enable("strikethrough")
)
MARKDOWN.renderer.rules["link_open"] = _render_link_open
MARKDOWN.renderer.rules["image"] = _render_image_as_alt


def render_markdown(source: str) -> str:
    """Render Markdown without raw HTML, remote images, or unsafe links."""

    return MARKDOWN.render(source)
