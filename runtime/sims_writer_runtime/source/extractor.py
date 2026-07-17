from __future__ import annotations

import hashlib
import html
import re
from dataclasses import asdict, dataclass, field
from html.parser import HTMLParser
from typing import Any


@dataclass(frozen=True)
class SourceSnapshot:
    status: str
    source_type: str
    content_format: str
    target_url: str | None
    title: str
    headings: list[dict[str, Any]] = field(default_factory=list)
    plain_text: str = ""
    original_content: str = ""
    character_count: int = 0
    line_count: int = 0
    content_hash: str | None = None
    warnings: list[str] = field(default_factory=list)
    requested_url: str | None = None
    final_url: str | None = None
    http_status: int | None = None
    media_type: str | None = None
    byte_count: int | None = None

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["normalized_text"] = self.plain_text
        return data


class _HTMLContentParser(HTMLParser):
    SKIP_TAGS = {"script", "style", "noscript", "svg"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.skip_depth = 0
        self.current_heading: str | None = None
        self.heading_parts: list[str] = []
        self.title_parts: list[str] = []
        self.in_title = False
        self.text_parts: list[str] = []
        self.headings: list[dict[str, Any]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag in self.SKIP_TAGS:
            self.skip_depth += 1
            return
        if self.skip_depth:
            return
        if tag == "title":
            self.in_title = True
        if re.fullmatch(r"h[1-6]", tag):
            self.current_heading = tag
            self.heading_parts = []
        if tag in {"p", "br", "li", "div", "section", "article", "tr"}:
            self.text_parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in self.SKIP_TAGS and self.skip_depth:
            self.skip_depth -= 1
            return
        if self.skip_depth:
            return
        if tag == "title":
            self.in_title = False
        if self.current_heading == tag:
            text = _clean_text(" ".join(self.heading_parts))
            if text:
                self.headings.append({"level": int(tag[1]), "text": text})
                self.text_parts.append(f"\n{text}\n")
            self.current_heading = None
            self.heading_parts = []

    def handle_data(self, data: str) -> None:
        if self.skip_depth:
            return
        value = data.strip()
        if not value:
            return
        if self.in_title:
            self.title_parts.append(value)
        if self.current_heading:
            self.heading_parts.append(value)
        self.text_parts.append(value)


class ArticleSourceExtractor:
    """Convert supplied article content into a deterministic source snapshot.

    It accepts supplied content and converts it into a deterministic snapshot.
    Network access, when enabled, is handled by ArticleSourceAcquisition.
    """

    SUPPORTED_FORMATS = {"auto", "html", "markdown", "plain_text"}

    def extract(
        self,
        content: str | None,
        *,
        content_format: str = "auto",
        target_url: str | None = None,
        fallback_title: str = "",
    ) -> SourceSnapshot:
        raw = (content or "").strip()
        requested_format = (content_format or "auto").strip().lower()
        if requested_format not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported content format: {requested_format}")

        if not raw:
            status = "missing" if target_url else "not_applicable"
            warning = "Article content was not supplied" if target_url else "No source content is required"
            return SourceSnapshot(
                status=status,
                source_type="request_payload",
                content_format=requested_format,
                target_url=target_url,
                title=fallback_title.strip(),
                warnings=[warning],
            )

        detected = self._detect_format(raw) if requested_format == "auto" else requested_format
        if detected == "html":
            title, headings, plain = self._extract_html(raw)
        elif detected == "markdown":
            title, headings, plain = self._extract_markdown(raw)
        else:
            title, headings, plain = "", [], _clean_text(raw, preserve_lines=True)

        title = title or fallback_title.strip()
        digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        warnings: list[str] = []
        if len(plain) < 200:
            warnings.append("Source content is very short and may be incomplete")
        if not headings:
            warnings.append("No headings were detected in source content")

        return SourceSnapshot(
            status="available",
            source_type="request_payload",
            content_format=detected,
            target_url=target_url,
            title=title,
            headings=headings,
            plain_text=plain,
            original_content=raw,
            character_count=len(plain),
            line_count=len([line for line in plain.splitlines() if line.strip()]),
            content_hash=f"sha256:{digest}",
            warnings=warnings,
        )

    @staticmethod
    def _detect_format(content: str) -> str:
        if re.search(r"<(?:html|body|article|main|h[1-6]|p|div|section)\b", content, re.I):
            return "html"
        if re.search(r"(?m)^#{1,6}\s+\S", content) or re.search(r"(?m)^[-*+]\s+\S", content):
            return "markdown"
        return "plain_text"

    @staticmethod
    def _extract_html(content: str) -> tuple[str, list[dict[str, Any]], str]:
        parser = _HTMLContentParser()
        parser.feed(content)
        parser.close()
        title = _clean_text(" ".join(parser.title_parts))
        plain = _clean_text(" ".join(parser.text_parts), preserve_lines=True)
        return title, parser.headings, plain

    @staticmethod
    def _extract_markdown(content: str) -> tuple[str, list[dict[str, Any]], str]:
        headings: list[dict[str, Any]] = []
        title = ""
        lines: list[str] = []
        in_fence = False
        for raw_line in content.splitlines():
            line = raw_line.rstrip()
            if line.strip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            match = re.match(r"^\s*(#{1,6})\s+(.+?)\s*#*\s*$", line)
            if match:
                text = _clean_text(match.group(2))
                level = len(match.group(1))
                headings.append({"level": level, "text": text})
                if not title and level == 1:
                    title = text
                lines.append(text)
                continue
            line = re.sub(r"!\[([^]]*)\]\([^)]*\)", r"\1", line)
            line = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", line)
            line = re.sub(r"^\s*[-*+]\s+", "", line)
            line = re.sub(r"^\s*>\s?", "", line)
            line = re.sub(r"[*_~`]", "", line)
            lines.append(html.unescape(line))
        return title, headings, _clean_text("\n".join(lines), preserve_lines=True)


def _clean_text(value: str, preserve_lines: bool = False) -> str:
    value = html.unescape(value).replace("\u3000", " ")
    if preserve_lines:
        cleaned_lines: list[str] = []
        for line in value.splitlines():
            line = re.sub(r"[ \t]+", " ", line).strip()
            if line:
                cleaned_lines.append(line)
        return "\n".join(cleaned_lines)
    return re.sub(r"\s+", " ", value).strip()
