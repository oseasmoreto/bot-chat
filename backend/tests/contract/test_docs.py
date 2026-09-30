"""A documentação acompanha o código: links válidos e trechos de código idênticos aos arquivos."""

import re
from pathlib import Path

ROOT = Path(__file__).parents[2]
DOC_FILES = sorted(
    [
        ROOT / "README.md",
        ROOT / "CONTRIBUTING.md",
        *(ROOT / "docs").rglob("*.md"),
        *(ROOT / ".github").rglob("*.md"),
    ]
)
LINK = re.compile(r"\]\(([^)\s]*?)(?:#([^)\s]*))?\)")
HEADING = re.compile(r"^#{1,6} (.+)$", re.MULTILINE)
FENCE = re.compile(r"```[\w-]*\n(.*?)```", re.DOTALL)
# Título que é só um caminho de arquivo, ex.: "## `core/scope.py`" ou "## `container.py` — …"
PATH_HEADING = re.compile(r"^#{2,3} `([\w./-]+)`(?: .*)?$", re.MULTILINE)
# Bloco cuja primeira linha diz de qual arquivo é, ex.: "# routes/public.py"
PATH_COMMENT = re.compile(r"^# ([\w/]+\.py)\n")


def slug(heading: str) -> str:
    """Âncora gerada por GitLab/GitHub/VS Code para um título."""
    return re.sub(r"[^\w\- ]", "", heading.strip().lower()).replace(" ", "-")


def anchors(markdown: Path) -> set[str]:
    return {slug(h) for h in HEADING.findall(markdown.read_text(encoding="utf-8"))}


def source(relative: str) -> Path | None:
    for base in (ROOT / "api", ROOT):
        candidate = base / relative
        if candidate.is_file():
            return candidate
    return None


def test_internal_links_point_to_existing_files_and_anchors() -> None:
    broken = []
    for doc in DOC_FILES:
        for target, anchor in LINK.findall(doc.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            path = (doc.parent / target).resolve() if target else doc
            if not path.exists():
                broken.append(f"{doc.relative_to(ROOT)} → {target}")
            elif anchor and path.suffix == ".md" and anchor not in anchors(path):
                broken.append(f"{doc.relative_to(ROOT)} → {target}#{anchor}")

    assert not broken, "Links quebrados:\n" + "\n".join(broken)


def embedded_sources(doc: Path) -> list[tuple[str, str]]:
    """(caminho, conteúdo) de cada bloco de código que representa um arquivo real."""
    text = doc.read_text(encoding="utf-8")
    found = []
    for heading in PATH_HEADING.finditer(text):
        block = FENCE.search(text, heading.end())
        next_heading = HEADING.search(text, heading.end())
        if block is None or (next_heading is not None and next_heading.start() < block.start()):
            continue
        if not PATH_COMMENT.match(block.group(1)):
            found.append((heading.group(1), block.group(1)))
    for block in FENCE.finditer(text):
        comment = PATH_COMMENT.match(block.group(1))
        if comment:
            found.append((comment.group(1), block.group(1)[comment.end() :]))
    return found


def test_code_in_docs_matches_source_files() -> None:
    outdated = []
    for doc in DOC_FILES:
        for relative, content in embedded_sources(doc):
            file = source(relative)
            if file is not None and file.read_text(encoding="utf-8") != content:
                outdated.append(f"{doc.relative_to(ROOT)} → {relative}")

    assert not outdated, "Trechos de código desatualizados nos docs:\n" + "\n".join(outdated)
