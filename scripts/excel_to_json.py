import json
import re
import warnings
from pathlib import Path
from datetime import datetime, date
from urllib.parse import urlparse

from openpyxl import load_workbook
from jsonschema import validate, ValidationError


# --------------------------------------------------
# 1. FILE LOCATIONS
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent

EXCEL_FILE = PROJECT_DIR / "data" / "claimVerificationResearch.xlsx"
SCHEMA_FILE = PROJECT_DIR / "data" / "schema.json"
OUTPUT_FILE = PROJECT_DIR / "data" / "claims.json"

SHEET_NAME = "Claims"

NO_EVIDENCE_MARKERS = {
    "nil",
    "n/a",
    "not applicable"
}


# --------------------------------------------------
# 2. GENERAL HELPER FUNCTIONS
# --------------------------------------------------

def normalise_header(value):
    """Standardise an Excel column heading."""

    if value is None:
        return ""

    return re.sub(r"\s+", " ", str(value).strip().lower())


def get_column(headers, possible_names):
    """Return the column number for the first matching heading."""

    for name in possible_names:
        if name in headers:
            return headers[name]

    return None


def get_cell(row, column):
    """Read a cell safely and return a cleaned string."""

    if column is None:
        return ""

    value = row[column - 1].value

    if value is None:
        return ""

    return str(value).replace("\xa0", " ").strip()


def is_no_evidence(value):
    """Check whether a value is an agreed no-evidence marker."""

    return str(value).strip().casefold() in NO_EVIDENCE_MARKERS


def normalise_verdict(value):
    """
    Standardise verdict spelling, capitalisation and spacing.

    'Partially' is converted to 'Partially supported'.
    """

    text = re.sub(r"\s+", " ", str(value or "").strip())
    text = text.rstrip(".").casefold()

    if not text:
        return ""

    verdicts = {
        "supported": "Supported",
        "partially": "Partially supported",
        "partially supported": "Partially supported",
        "unsupported": "Unsupported",
        "contradicted": "Contradicted",
        "unclear": "Unclear",
        "o": "O"
    }

    if text not in verdicts:
        raise ValueError(
            f"Unrecognised verdict: {value!r}. "
            "Expected Supported, Partially supported, "
            "Unsupported, Contradicted or Unclear."
        )

    return verdicts[text]


def split_entries(value):
    """
    Split ordinary text entries separated by blank lines.

    Wrapped lines within an entry are joined with spaces. This function
    is for fields such as source titles and verdicts, not evidence quotes.
    """

    if value is None:
        return []

    text = (
        str(value)
        .replace("\r\n", "\n")
        .replace("\r", "\n")
        .strip()
    )

    if not text:
        return []

    entries = re.split(r"\n\s*\n+", text)
    cleaned = []

    for entry in entries:
        entry = " ".join(
            line.strip()
            for line in entry.splitlines()
            if line.strip()
        ).strip()

        if entry and not is_no_evidence(entry):
            cleaned.append(entry)

    return cleaned


def split_lines_or_entries(value):
    """Split URLs separated by blank lines or individual lines."""

    entries = split_entries(value)

    if len(entries) > 1:
        return entries

    if not entries:
        return []

    lines = [
        line.strip()
        for line in str(value).splitlines()
        if line.strip()
    ]

    if len(lines) > 1 and all(
        line.startswith(("http://", "https://"))
        for line in lines
    ):
        return lines

    return entries


def normalise_date(value):
    """Return a date in YYYY-MM-DD format where possible."""

    if value in (None, ""):
        return None

    if isinstance(value, (datetime, date)):
        return value.strftime("%Y-%m-%d")

    text = str(value).strip()

    if not text:
        return None

    entries = [
        entry.strip()
        for entry in re.split(r"\n\s*\n+", text)
        if entry.strip()
    ]
    text = entries[0] if entries else text

    try:
        return datetime.strptime(text, "%d/%m/%Y").strftime("%Y-%m-%d")
    except ValueError:
        # Keep an unrecognised date as entered rather than guessing.
        return text


def get_category(section):
    """Identify the category heading in the first Excel column."""

    section = (section or "").upper().replace("_", " ")

    if "NOT AI FLAGGED" in section:
        return "Not AI flagged"

    if "NOT-AI-FLAGGED" in section:
        return "Not AI flagged"

    if "NOT-FLAGGED" in section or "NOT FLAGGED" in section:
        return "Not AI flagged"

    if "AI FLAGGED" in section:
        return "AI flagged"

    return ""


# --------------------------------------------------
# 3. SUBCLAIM PROCESSING
# --------------------------------------------------

def parse_subclaims(text, verdict_text, claim_id=None):
    """
    Extract subclaims and retain their existing subclaim-level verdicts.

    Numbered subclaims keep their supplied IDs. Unnumbered subclaims are
    separated by blank lines and receive IDs based on the parent claim ID.
    """

    if not text or is_no_evidence(text):
        return []

    cleaned = (
        str(text)
        .replace("\r\n", "\n")
        .replace("\r", "\n")
        .replace("\xa0", " ")
        .replace("&#x20;", " ")
        .replace("&nbsp;", " ")
    )
    cleaned = re.sub(r"<br\s*/?>", "\n", cleaned, flags=re.IGNORECASE).strip()

    # First, identify explicitly numbered subclaims.
    numbered_lines = [
        line.strip()
        for line in cleaned.splitlines()
        if line.strip()
    ]

    subclaims = []
    has_numbered_ids = any(
        re.match(r"^\d+\.\d+\.?\s*", line)
        for line in numbered_lines
    )

    if has_numbered_ids:
        for line in numbered_lines:
            match = re.match(r"^(\d+\.\d+)\.?\s*(.*)$", line)

            if match:
                subclaims.append({
                    "subclaimID": match.group(1),
                    "text": match.group(2).strip(),
                    "verdict": "",
                    "evidence": []
                })
            elif subclaims:
                subclaims[-1]["text"] += " " + line

    else:
        blocks = [
            block.strip()
            for block in re.split(r"\n\s*\n+", cleaned)
            if block.strip()
        ]

        for index, block in enumerate(blocks, start=1):
            block_text = " ".join(
                line.strip()
                for line in block.splitlines()
                if line.strip()
            )
            identifier = f"{claim_id}.{index}" if claim_id is not None else str(index)

            subclaims.append({
                "subclaimID": identifier,
                "text": block_text,
                "verdict": "",
                "evidence": []
            })

    # Retain verdicts at subclaim level where the Excel entries map to
    # subclaims. Evidence-level verdicts are assigned separately below.
    numbered_verdicts = {}
    ordered_verdicts = []

    for line in [
        item.strip()
        for item in re.split(r"\n\s*\n+", str(verdict_text or ""))
        if item.strip() and not is_no_evidence(item)
    ]:
        match = re.match(r"^(\d+\.\d+)\.?\s+(.+)$", line)

        if match:
            numbered_verdicts[match.group(1)] = match.group(2).strip()
        else:
            ordered_verdicts.append(line)

    for index, subclaim in enumerate(subclaims):
        subclaim_id = subclaim["subclaimID"]

        if subclaim_id in numbered_verdicts:
            subclaim["verdict"] = normalise_verdict(
                numbered_verdicts[subclaim_id]
            )
        elif index < len(ordered_verdicts):
            subclaim["verdict"] = normalise_verdict(
                ordered_verdicts[index]
            )

    return subclaims


# --------------------------------------------------
# 4. EVIDENCE PROCESSING
# --------------------------------------------------

def split_evidence_quotes(value, claim_id=None, row_number=None):
    """
    Extract individual evidence quotations, accepting straight and curly
    double quotation marks as opening/closing delimiters.

    Paragraph breaks inside a quotation are preserved. A single location
    can later be reused for several quotations.
    """

    if value is None:
        return []

    text = (
        str(value)
        .replace("\r\n", "\n")
        .replace("\r", "\n")
        .strip()
    )

    if not text or is_no_evidence(text):
        return []

    opening_marks = {'"', '“'}
    closing_marks = {'"', '”'}

    if not any(mark in text for mark in opening_marks | closing_marks):
        return split_entries(text)

    entries = []
    current_entry = []
    inside_quote = False
    found_delimiter = False
    index = 0

    while index < len(text):
        character = text[index]

        if not inside_quote and character in opening_marks:
            found_delimiter = True
            inside_quote = True
            current_entry = []
            index += 1
            continue

        if inside_quote and character in closing_marks:
            found_delimiter = True

            # Preserve doubled straight quotation marks as literal quotes.
            if (
                character == '"'
                and index + 1 < len(text)
                and text[index + 1] == '"'
            ):
                current_entry.append('"')
                index += 2
                continue

            entry = "".join(current_entry).strip()
            if entry and not is_no_evidence(entry):
                entries.append(entry)

            current_entry = []
            inside_quote = False
            index += 1
            continue

        if inside_quote:
            current_entry.append(character)
        elif character.isalnum():
            marker_match = re.match(
                r"(?i)(?:nil|n/a|not applicable)\b",
                text[index:]
            )

            if marker_match:
                index += len(marker_match.group(0))
                continue

            context = f"Claim {claim_id}" if claim_id is not None else ""
            if row_number is not None:
                context += f", Excel row {row_number}" if context else f"Excel row {row_number}"
            warnings.warn(
                f"{context}: text outside a quoted evidence entry was ignored. "
                "Please review that Excel cell."
            )

        index += 1

    if inside_quote:
        entry = "".join(current_entry).strip()
        if entry and not is_no_evidence(entry):
            entries.append(entry)

        context = f"Claim {claim_id}" if claim_id is not None else ""
        if row_number is not None:
            context += f", Excel row {row_number}" if context else f"Excel row {row_number}"
        warnings.warn(
            f"{context}: an evidence quotation has no closing quotation mark. "
            "The remaining text was retained."
        )

    if not found_delimiter:
        return split_entries(text)

    return entries


def split_evidence_slots(value):
    """
    Return evidence entries in order, retaining NIL as an empty slot.

    Accept matching or mixed quotation delimiters, including:
    - “quotation”
    - "quotation"
    - “quotation"
    - "quotation”
    """
    if value is None:
        return []

    text = (
        str(value)
        .replace("\\r\\n", "\\n")
        .replace("\\r", "\\n")
        .strip()
    )

    if not text:
        return []

    pattern = re.compile(
        r'“(.*?)(?:”|")|"(.*?)(?:"|”)|\\bNIL\\b|\\bN/A\\b|\\bnot applicable\\b',
        re.IGNORECASE | re.DOTALL
    )

    slots = []

    for match in pattern.finditer(text):
        token = match.group(0).strip()

        if token.casefold() in {"nil", "n/a", "not applicable"}:
            slots.append(None)
            continue

        quote = match.group(1) if match.group(1) is not None else match.group(2)
        quote = quote.strip()

        if quote and not is_no_evidence(quote):
            slots.append(quote)
        else:
            slots.append(None)

    if slots:
        return slots

    return split_entries(text)


def split_location_slots(value):
    """Split distinct location entries while retaining NIL placeholders.

    A single returned location may describe a group of evidence quotations;
    build_evidence broadcasts it across that group.
    """
    if value is None:
        return []
    text = str(value).replace("\r\n", "\n").replace("\r", "\n").strip()
    if not text:
        return []
    return [
        None if is_no_evidence(part.strip()) else " ".join(
            line.strip() for line in part.splitlines() if line.strip()
        )
        for part in re.split(r"\n\s*\n+", text)
        if part.strip()
    ]


def build_evidence(
    quote_cell,
    location_cell,
    claim_id=None,
    row_number=None
):
    """Pair quotations and locations, preserving NIL slots.

    When one location is supplied for multiple quotations, that location
    is shared by every quotation and is repeated in each JSON evidence item.
    """
    quote_slots = split_evidence_slots(quote_cell)
    location_slots = split_location_slots(location_cell)

    if not quote_slots and not location_slots:
        return [], []

    # A single location entered for a group of quotations applies to every
    # quotation in that group. Copy it to each evidence object in the JSON.
    if len(quote_slots) > 1 and len(location_slots) == 1:
        location_slots = location_slots * len(quote_slots)

    slot_count = max(len(quote_slots), len(location_slots))
    evidence_slots = []
    for index in range(slot_count):
        quote = quote_slots[index] if index < len(quote_slots) else None
        location = location_slots[index] if index < len(location_slots) else None
        if quote is None and location is None:
            evidence_slots.append(None)
        else:
            evidence_slots.append({
                "quote": quote or "",
                "location": location or "",
                "verdict": ""
            })

    return [item for item in evidence_slots if item is not None], evidence_slots


def parse_evidence_verdicts(value):
    """Return evidence verdicts in the order entered in Excel."""
    verdicts = []

    for entry in split_entries(value):
        # Accept optional subclaim identifiers such as "10.1 Supported".
        match = re.match(r"^\d+\.\d+\.?\s+(.+)$", entry)
        if match:
            entry = match.group(1).strip()

        verdicts.append(normalise_verdict(entry))

    return verdicts


def apply_evidence_verdicts(evidence, subclaims, verdict_text, claim_id, row_number):
    """Assign evidence verdicts only when the evidence belongs to a subclaim.

    For claims with subclaims, the evidence inherits the verdict of the
    subclaim to which it has been attached. A subclaim with no evidence keeps
    its own verdict and an empty evidence array. For claims without subclaims,
    evidence-level verdicts remain empty because only the overall claim verdict
    is recorded in the workbook.
    """

    if not subclaims:
        return

    for subclaim in subclaims:
        for item in subclaim["evidence"]:
            item["verdict"] = subclaim["verdict"]


def values_for_sources(value, source_count, split_urls=False):
    """Return one value per source, using empty strings where missing."""

    if split_urls:
        values = split_lines_or_entries(value)
    else:
        values = split_entries(value)

        if not values and value not in (None, ""):
            values = [str(value).strip()]

    return [
        values[index] if index < len(values) else ""
        for index in range(source_count)
    ]


def attach_evidence_to_subclaims(subclaims, evidence_slots):
    """Attach evidence by aligned slots; NIL creates an empty evidence array."""
    if not subclaims:
        return
    if len(evidence_slots) == len(subclaims):
        for subclaim, slot in zip(subclaims, evidence_slots):
            if slot is not None:
                subclaim["evidence"].append(slot)
        return
    if not evidence_slots:
        return
    warnings.warn(
        f"Found {len(evidence_slots)} evidence/NIL slots for "
        f"{len(subclaims)} subclaims. The workbook entries do not align "
        "one-to-one; evidence was retained in order under the final "
        "subclaim for manual review."
    )
    for index, slot in enumerate(evidence_slots):
        if slot is not None:
            target = min(index, len(subclaims) - 1)
            subclaims[target]["evidence"].append(slot)


def normalise_identifier(value):
    """Remove spaces and punctuation for source-name matching."""

    return re.sub(r"[^a-z0-9]", "", str(value).lower())


def assign_evidence_to_sources(
    evidence,
    source_urls,
    source_titles,
    claim_id,
    row_number
):
    """
    Assign evidence to sources using the source title or publication
    name mentioned in the evidence location.

    If a location does not identify a source, retain the evidence under
    the first source and issue a warning for manual review.
    """

    source_evidence = [[] for _ in source_urls]

    if not evidence:
        return source_evidence

    if len(source_urls) == 1:
        source_evidence[0] = evidence
        return source_evidence

    for item in evidence:
        location = item.get("location", "").strip()

        if not location:
            source_evidence[0].append(item)

            warnings.warn(
                f"Claim {claim_id}, Excel row {row_number}: "
                "an evidence entry has no location. It has been retained "
                "under the first listed source. Please review its assignment."
            )
            continue

        normalised_location = normalise_identifier(location)
        matches = []

        for index, (url, title) in enumerate(zip(source_urls, source_titles)):
            identifiers = []

            if title:
                identifiers.append(title)

            host = urlparse(url).hostname or ""
            domain_label = (
                host.lower()
                .removeprefix("www.")
                .split(".")[0]
            )

            if domain_label:
                identifiers.append(domain_label)

                if domain_label.startswith("the") and len(domain_label) > 3:
                    identifiers.append(domain_label[3:])

            for identifier in identifiers:
                normalised = normalise_identifier(identifier)

                if normalised and normalised in normalised_location:
                    matches.append(index)
                    break

        matches = list(dict.fromkeys(matches))

        if len(matches) == 1:
            source_evidence[matches[0]].append(item)

        elif not matches:
            source_evidence[0].append(item)

            warnings.warn(
                f"Claim {claim_id}, Excel row {row_number}: "
                f"could not match this evidence location to a source: "
                f"{location!r}. The evidence was retained under the "
                "first listed source. Please review its assignment."
            )

        else:
            raise ValueError(
                f"Claim {claim_id}, Excel row {row_number}: "
                f"the evidence location matches multiple sources: "
                f"{location!r}. Please make the source name more specific."
            )

    return source_evidence


# --------------------------------------------------
# 5. CHECK AND LOAD FILES
# --------------------------------------------------

if not EXCEL_FILE.exists():
    raise FileNotFoundError(f"Excel file not found: {EXCEL_FILE}")

if not SCHEMA_FILE.exists():
    raise FileNotFoundError(f"Schema file not found: {SCHEMA_FILE}")

workbook = load_workbook(EXCEL_FILE, data_only=True)

if SHEET_NAME not in workbook.sheetnames:
    raise ValueError(f"Worksheet '{SHEET_NAME}' was not found.")

worksheet = workbook[SHEET_NAME]

with open(SCHEMA_FILE, "r", encoding="utf-8") as file:
    schema = json.load(file)


# --------------------------------------------------
# 6. IDENTIFY EXCEL COLUMNS
# --------------------------------------------------

headers = {}

for cell in worksheet[1]:
    header = normalise_header(cell.value)

    if header:
        headers[header] = cell.column


columns = {
    "claim_id": get_column(headers, ["claim id"]),
    "claim": get_column(headers, ["claim"]),
    "article_title": get_column(headers, ["article title"]),
    "article_url": get_column(headers, ["article url"]),
    "source_title": get_column(headers, ["source title"]),
    "source_url": get_column(headers, ["source url"]),
    "source_citation": get_column(headers, ["source citation"]),
    "access_status": get_column(headers, ["access status"]),
    "access_notes": get_column(headers, ["access notes"]),
    "accessed_date": get_column(
        headers,
        ["accessed date", "aceess date"]
    ),
    "subclaim_text": get_column(headers, ["subclaim text"]),
    "evidence_quote": get_column(headers, ["evidence quote"]),
    "evidence_location": get_column(headers, ["evidence location"]),
    "subclaim_verdict": get_column(headers, ["subclaim verdict"]),
    "overall_verdict": get_column(headers, ["overall verdict"]),
    "evidence_gap": get_column(headers, ["evidence gap"]),
    "reason": get_column(headers, ["reason"])
}


required_columns = [
    "claim_id",
    "claim",
    "article_url",
    "source_url",
    "access_status"
]

for name in required_columns:
    if columns[name] is None:
        raise ValueError(f"Required Excel column is missing: {name}")


# --------------------------------------------------
# 7. READ AND CONVERT CLAIMS
# --------------------------------------------------

claims = []
current_category = ""

for row_number in range(2, worksheet.max_row + 1):
    row = worksheet[row_number]

    first_cell = get_cell(row, 1)
    detected_category = get_category(first_cell)

    if detected_category:
        current_category = detected_category
        continue

    row_is_blank = all(
        cell.value in (None, "")
        for cell in row
    )

    if row_is_blank:
        # Preserve the workbook's existing category-transition behaviour.
        if current_category == "AI flagged":
            if any(
                merged.min_row == row_number
                and merged.max_row == row_number
                and merged.min_col == 1
                for merged in worksheet.merged_cells.ranges
            ):
                current_category = "Not AI flagged"

        continue

    claim_id = get_cell(row, columns["claim_id"])
    claim_text = get_cell(row, columns["claim"])

    if not claim_id or not claim_text:
        continue

    # --------------------------------------------------
    # 7A. READ SOURCE INFORMATION
    # --------------------------------------------------

    source_urls = split_lines_or_entries(
        get_cell(row, columns["source_url"])
    )

    source_titles = split_entries(
        get_cell(row, columns["source_title"])
    )

    source_citations = split_entries(
        get_cell(row, columns["source_citation"])
    )

    access_statuses = split_entries(
        get_cell(row, columns["access_status"])
    )

    access_notes = split_entries(
        get_cell(row, columns["access_notes"])
    )

    source_count = max(
        1,
        len(source_urls),
        len(source_titles),
        len(source_citations),
        len(access_statuses),
        len(access_notes)
    )

    source_titles = values_for_sources(
        get_cell(row, columns["source_title"]),
        source_count
    )

    source_urls = values_for_sources(
        get_cell(row, columns["source_url"]),
        source_count,
        split_urls=True
    )

    source_citations = values_for_sources(
        get_cell(row, columns["source_citation"]),
        source_count
    )

    access_statuses = values_for_sources(
        get_cell(row, columns["access_status"]),
        source_count
    )

    access_notes = values_for_sources(
        get_cell(row, columns["access_notes"]),
        source_count
    )

    accessed_date_value = (
        row[columns["accessed_date"] - 1].value
        if columns["accessed_date"]
        else None
    )

    accessed_date = normalise_date(accessed_date_value)

    # --------------------------------------------------
    # 7B. READ EVIDENCE
    # --------------------------------------------------

    quote_value = (
        row[columns["evidence_quote"] - 1].value
        if columns["evidence_quote"]
        else None
    )

    location_value = (
        row[columns["evidence_location"] - 1].value
        if columns["evidence_location"]
        else None
    )

    evidence, evidence_slots = build_evidence(
        quote_value,
        location_value,
        claim_id,
        row_number
    )

    # --------------------------------------------------
    # 7C. READ SUBCLAIMS
    # --------------------------------------------------

    subclaims = parse_subclaims(
        get_cell(row, columns["subclaim_text"]),
        get_cell(row, columns["subclaim_verdict"]),
        claim_id
    )

    # --------------------------------------------------
    # 7D. PLACE EVIDENCE
    # --------------------------------------------------

    if subclaims:
        # Compound claims store evidence under their subclaims.
        attach_evidence_to_subclaims(subclaims, evidence_slots)
        source_evidence = None

    else:
        # Claims without subclaims store evidence under sourceEvaluation.
        source_evidence = assign_evidence_to_sources(
            evidence,
            source_urls,
            source_titles,
            claim_id,
            row_number
        )

    # --------------------------------------------------
    # 7D-1. ASSIGN VERDICTS TO INDIVIDUAL EVIDENCE
    # --------------------------------------------------

    apply_evidence_verdicts(
        evidence,
        subclaims,
        get_cell(row, columns["subclaim_verdict"]),
        claim_id,
        row_number
    )

    # --------------------------------------------------
    # 7E. BUILD SOURCE EVALUATION
    # --------------------------------------------------

    source_evaluation = []

    for index in range(source_count):
        source = {
            "sourceTitle": source_titles[index],
            "sourceURL": source_urls[index],
            "sourceCitation": source_citations[index],
            "accessStatus": access_statuses[index],
            "accessNotes": access_notes[index],
            "accessedDate": accessed_date
        }

        if not subclaims:
            source["evidence"] = source_evidence[index]

        source_evaluation.append(source)

    # --------------------------------------------------
    # 7F. BUILD THE MAIN CLAIM RECORD
    # --------------------------------------------------

    claim_record = {
        "claimID": str(claim_id),
        "claim": claim_text,
        "category": current_category,
        "article": {
            "title": get_cell(row, columns["article_title"]),
            "url": get_cell(row, columns["article_url"])
        },
        "sourceEvaluation": source_evaluation,
        "subclaims": subclaims,
        "overallVerdict": normalise_verdict(
            get_cell(row, columns["overall_verdict"])
        ),
        "evidenceGap": split_entries(
            get_cell(row, columns["evidence_gap"])
        ),
        "reasoning": get_cell(row, columns["reason"])
    }

    claims.append(claim_record)


# --------------------------------------------------
# 8. PREPARE AND VALIDATE THE JSON
# --------------------------------------------------

output_data = {
    "claims": claims
}

try:
    validate(
        instance=output_data,
        schema=schema
    )

except ValidationError as error:
    raise ValueError(
        "The generated JSON does not match schema.json.\n"
        f"Problem: {error.message}\n"
        f"Location: {list(error.absolute_path)}"
    ) from error


# --------------------------------------------------
# 9. SAVE THE JSON FILE
# --------------------------------------------------

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        output_data,
        file,
        indent=4,
        ensure_ascii=False
    )


# --------------------------------------------------
# 10. DISPLAY THE CONVERSION SUMMARY
# --------------------------------------------------

print("Conversion completed successfully.")
print(f"Total claims converted: {len(claims)}")
print(f"Output saved to: {OUTPUT_FILE}")
