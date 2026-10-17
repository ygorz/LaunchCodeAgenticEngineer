"""
Formatting and reporting utilities for the parallel agent-session example.

This module is intentionally correct but lightly documented. It is designed for
the "Session B" agent task: improve docstrings in this file and update README.md,
without modifying any test files.
"""

from __future__ import annotations


def format_currency(amount: float) -> str:
    """Format a number as a US-dollar string with thousands separators.

    Negative amounts get a leading minus sign before the dollar sign.

    Args:
        amount: The value to format.

    Returns:
        The amount rounded to two decimal places, e.g. ``"$1,234.50"`` or
        ``"-$5.00"``.
    """
    if amount < 0:
        return f"-${abs(amount):,.2f}"
    return f"${amount:,.2f}"


def build_report_title(project_name: str, version: str) -> str:
    """Build a report title from a project name and version.

    Extra whitespace is collapsed in the project name and trimmed from the
    version. A blank project name becomes ``"Untitled Project"`` and a blank
    version becomes ``"draft"``.

    Args:
        project_name: The project name to show in the title.
        version: The version label, e.g. ``"v1.2"``.

    Returns:
        A title in the form ``"<project> — <version>"``.
    """
    clean_project = " ".join(project_name.strip().split())
    clean_version = version.strip()

    if not clean_project:
        clean_project = "Untitled Project"
    if not clean_version:
        clean_version = "draft"

    return f"{clean_project} — {clean_version}"


def mask_email(email: str) -> str:
    """Mask the local part of an email address.

    The first and last characters of the local part are kept and the rest are
    replaced with ``*``. Local parts of one or two characters keep only the
    first character, or none if there is just one. The domain is lowercased.

    Args:
        email: The email address to mask. Surrounding whitespace is ignored.

    Returns:
        The masked address, e.g. ``"j**n@example.com"`` for ``"john@Example.com"``.

    Raises:
        ValueError: If the address has no ``@``, or the local part or domain
            is empty.
    """
    email = email.strip()
    if "@" not in email:
        raise ValueError("email must contain @")

    local_part, domain = email.split("@", 1)
    if not local_part or not domain:
        raise ValueError("email must include a local part and domain")

    if len(local_part) == 1:
        masked_local = "*"
    elif len(local_part) == 2:
        masked_local = local_part[0] + "*"
    else:
        masked_local = local_part[0] + "*" * (len(local_part) - 2) + local_part[-1]

    return f"{masked_local}@{domain.lower()}"


def generate_summary_line(name: str, status: str, score: int) -> str:
    """Build a one-line status summary for a person or item.

    The name has its whitespace collapsed and is title-cased, falling back to
    ``"Unknown"`` when blank. The status is lowercased with underscores
    replaced by spaces.

    Args:
        name: The display name.
        status: The status label, e.g. ``"IN_PROGRESS"``.
        score: A numeric score shown in parentheses.

    Returns:
        A line in the form ``"<Name>: <status> (<score>)"``.
    """
    display_name = " ".join(name.strip().split()).title()
    display_status = status.strip().lower().replace("_", " ")

    if not display_name:
        display_name = "Unknown"

    return f"{display_name}: {display_status} ({score})"


def create_markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    """Render a list of row dictionaries as a Markdown table.

    Columns appear in the order given. A row missing a column gets an empty
    cell, and keys not listed in ``columns`` are ignored. Values are converted
    with ``str()`` and are not escaped.

    Args:
        rows: The table rows, each mapping column names to values.
        columns: The column names to include, in display order.

    Returns:
        The table as a newline-separated string with a header row and a
        separator row. An empty ``rows`` list yields just those two lines.

    Raises:
        ValueError: If ``columns`` is empty.
    """
    if not columns:
        raise ValueError("columns cannot be empty")

    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"

    body_lines = []
    for row in rows:
        values = [str(row.get(column, "")) for column in columns]
        body_lines.append("| " + " | ".join(values) + " |")

    return "\n".join([header, separator, *body_lines])


def truncate_text(text: str, max_length: int = 80) -> str:
    """Collapse whitespace in text and shorten it to a maximum length.

    Text longer than ``max_length`` is cut, trailing whitespace is removed,
    and ``"..."`` is appended so the result is at most ``max_length``
    characters.

    Args:
        text: The text to clean and truncate.
        max_length: The maximum length of the result, including the ellipsis.

    Returns:
        The cleaned text, unchanged if it already fits.

    Raises:
        ValueError: If ``max_length`` is less than 4.
    """
    if max_length < 4:
        raise ValueError("max_length must be at least 4")

    clean_text = " ".join(text.strip().split())
    if len(clean_text) <= max_length:
        return clean_text

    return clean_text[: max_length - 3].rstrip() + "..."
