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
    extraction_profile: str | None = None
    removed_noise_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["normalized_text"] = self.plain_text
        return data


class _HTMLContentParser(HTMLParser):
    """Small deterministic article parser with conservative noise removal."""

    ALWAYS_SKIP_TAGS = {"script", "style", "noscript", "svg", "template", "canvas", "iframe"}
    STRUCTURAL_NOISE_TAGS = {"header", "nav", "footer", "aside", "form"}
    VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
    NOISE_TOKEN_RE = re.compile(
        r"(?:^|[-_\s])(?:"
        r"ad|ads|advert|advertisement|banner|breadcrumb|breadcrumbs|comment|comments|"
        r"cookie|footer|global-nav|header-nav|menu|navigation|newsletter|pagination|"
        r"popular|ranking|recommend|recommended|related|share|sharing|sidebar|social|"
        r"sponsor|sponsored|subscription|toc-widget|widget"
        r")(?:$|[-_\s])",
        re.I,
    )
    CONTENT_TOKEN_RE = re.compile(
        r"(?:^|[-_\s])(?:article|content|entry-content|entry-body|main|post-content|post-body)(?:$|[-_\s])",
        re.I,
    )

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._skip_stack: list[bool] = []
        self.skip_depth = 0
        self.current_heading: str | None = None
        self.heading_parts: list[str] = []
        self.title_parts: list[str] = []
        self.in_title = False
        self.text_parts: list[str] = []
        self.headings: list[dict[str, Any]] = []
        self.removed_noise_count = 0
        self.content_hint_count = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attr_map = {key.lower(): (value or "") for key, value in attrs}
        own_skip = self._is_noise(tag, attr_map)
        inherited_skip = self.skip_depth > 0
        effective_skip = own_skip or inherited_skip
        if tag not in self.VOID_TAGS:
            self._skip_stack.append(own_skip)
        if own_skip:
            self.skip_depth += 1
            self.removed_noise_count += 1
        if effective_skip:
            return

        tokens = " ".join([attr_map.get("id", ""), attr_map.get("class", "")])
        if tag in {"article", "main"} or self.CONTENT_TOKEN_RE.search(tokens):
            self.content_hint_count += 1
        if tag == "title":
            self.in_title = True
        if re.fullmatch(r"h[1-6]", tag):
            self.current_heading = tag
            self.heading_parts = []
        if tag in {"p", "br", "li", "div", "section", "article", "main", "tr", "blockquote"}:
            self.text_parts.append("\n")

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in self.VOID_TAGS:
            return
        was_skipped = self._skip_stack.pop() if self._skip_stack else False
        if self.skip_depth > 0:
            if was_skipped:
                self.skip_depth -= 1
            return
        if was_skipped:
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

    def _is_noise(self, tag: str, attrs: dict[str, str]) -> bool:
        if tag in self.ALWAYS_SKIP_TAGS or tag in self.STRUCTURAL_NOISE_TAGS:
            return True
        role = attrs.get("role", "").lower()
        if role in {"banner", "contentinfo", "navigation", "complementary", "dialog"}:
            return True
        if attrs.get("aria-hidden", "").lower() == "true" or "hidden" in attrs:
            return True
        tokens = " ".join([attrs.get("id", ""), attrs.get("class", "")]).strip()
        if tokens and self.NOISE_TOKEN_RE.search(tokens):
            return True
        return False


class ArticleSourceExtractor:
    """Convert supplied article content into a deterministic source snapshot."""

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
        removed_noise_count = 0
        extraction_profile: str | None = None
        if detected == "html":
            title, headings, plain, removed_noise_count, extraction_profile = self._extract_html(raw)
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
        if removed_noise_count:
            warnings.append(f"Removed {removed_noise_count} non-article element(s) during extraction")

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
            extraction_profile=extraction_profile,
            removed_noise_count=removed_noise_count,
        )

    @staticmethod
    def _detect_format(content: str) -> str:
        if re.search(r"<(?:html|body|article|main|h[1-6]|p|div|section)\b", content, re.I):
            return "html"
        if re.search(r"(?m)^#{1,6}\s+\S", content) or re.search(r"(?m)^[-*+]\s+\S", content):
            return "markdown"
        return "plain_text"

    @staticmethod
    def _extract_html(content: str) -> tuple[str, list[dict[str, Any]], str, int, str]:
        parser = _HTMLContentParser()
        parser.feed(content)
        parser.close()
        title = _clean_text(" ".join(parser.title_parts))
        plain = _clean_text(" ".join(parser.text_parts), preserve_lines=True)
        profile = "article-aware-noise-filter-v1"
        return title, parser.headings, plain, parser.removed_noise_count, profile

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
        previous = ""
        for line in value.splitlines():
            line = re.sub(r"[ \t]+", " ", line).strip()
            if line and line != previous:
                cleaned_lines.append(line)
                previous = line
        return "\n".join(cleaned_lines)
    return re.sub(r"\s+", " ", value).strip()
