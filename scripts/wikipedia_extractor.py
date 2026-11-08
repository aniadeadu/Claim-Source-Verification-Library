
import requests
import mwparserfromhell
import json
import re
from pathlib import Path


ARTICLE_TITLE = "Air pollution"
API_URL = "https://en.wikipedia.org/w/api.php"


# Retrieve Wikipedia article
params = {
    "action": "parse",
    "page": ARTICLE_TITLE,
    "prop": "wikitext",
    "format": "json"
}

headers = {
    "User-Agent": "ClaimSourceVerificationLibrary/1.0"
}

response = requests.get(
    API_URL,
    params=params,
    headers=headers,
    timeout=30
)
response.raise_for_status()

data = response.json()

if "error" in data:
    raise RuntimeError(data["error"]["info"])

wikitext = data["parse"]["wikitext"]["*"]
article = mwparserfromhell.parse(wikitext)


# Extract citation details from a reference
def extract_reference(tag, reference_id):

    raw_citation = str(tag.contents) if tag.contents else ""
    citation = mwparserfromhell.parse(raw_citation)

    details = {
        "referenceID": reference_id,
        "citation": raw_citation,
        "title": None,
        "url": None,
        "doi": None
    }

    for template in citation.filter_templates():

        for field in ["title", "chapter"]:
            if template.has(field) and not details["title"]:
                details["title"] = str(
                    template.get(field).value
                ).strip()

        for field in ["url", "chapter-url"]:
            if template.has(field) and not details["url"]:
                details["url"] = str(
                    template.get(field).value
                ).strip()

        if template.has("doi") and not details["doi"]:
            details["doi"] = str(
                template.get("doi").value
            ).strip()

    # Use the DOI as a URL when no direct URL is provided
    if not details["url"] and details["doi"]:
        details["url"] = (
            "https://doi.org/" + details["doi"]
        )

    return details


# Get the name of a reference, if it has one
def get_reference_name(tag):

    for attribute in tag.attributes:
        if str(attribute.name).strip() == "name":
            return str(attribute.value).strip().strip('"').strip("'")

    return None


# Build a catalogue of named references
reference_catalogue = {}

for tag in article.filter_tags():

    if str(tag.tag).lower() != "ref":
        continue

    name = get_reference_name(tag)

    if name and tag.contents:
        reference_catalogue[name] = extract_reference(
            tag, name
        )


# Extract sections and paragraphs
sections = []

article_sections = article.get_sections(
    include_headings=True,
    include_lead=True,
    flat=True
)

for section_index, section in enumerate(article_sections, start=1):

    headings = section.filter_headings()

    section_title = (
        str(headings[0].title).strip()
        if headings else "Introduction"
    )

    # Remove heading nodes before processing paragraph text
    body_nodes = [
        node for node in section.nodes
        if not isinstance(node, mwparserfromhell.nodes.Heading)
    ]

    body = mwparserfromhell.wikicode.Wikicode(body_nodes)

    # Split section content into paragraphs
    raw_paragraphs = re.split(r"\n\s*\n", str(body))

    paragraphs = []

    for paragraph_number, raw_paragraph in enumerate(
        raw_paragraphs, start=1
    ):

        parsed_paragraph = mwparserfromhell.parse(raw_paragraph)

        # Remove image and file markup
        for link in list(parsed_paragraph.filter_wikilinks()):

            namespace = str(link.title).split(":", 1)[0].strip().lower()

            if namespace in ["file", "image"] or str(link.title).lower().startswith(
                ("file:", "image:")
            ):
                parsed_paragraph.remove(link)

        references = []
        unnamed_reference_count = 0

        for tag in list(parsed_paragraph.filter_tags()):

            if str(tag.tag).lower() != "ref":
                continue

            name = get_reference_name(tag)

            if tag.contents:
                if name:
                    reference = extract_reference(tag, name)
                else:
                    unnamed_reference_count += 1

                    reference_id = (
                        f"ref_s{section_index}_"
                        f"p{paragraph_number}_"
                        f"{unnamed_reference_count}"
                    )

                    reference = extract_reference(
                        tag, reference_id
                    )

            elif name and name in reference_catalogue:
                reference = reference_catalogue[name]

            else:
                reference = {
                    "referenceID": name,
                    "citation": None,
                    "title": None,
                    "url": None,
                    "doi": None
                }

            references.append(reference)

            # Remove citation markup from paragraph text
            parsed_paragraph.remove(tag)

        # Convert remaining wiki markup into readable text
        paragraph_text = parsed_paragraph.strip_code().strip()

        # Remove leftover image parameters and excess whitespace
        paragraph_text = re.sub(
            r"\bthumb\|.*?\|alt=.*?(?=\s|$)",
            "",
            paragraph_text
        )

        paragraph_text = re.sub(
            r"\s+", " ", paragraph_text
        ).strip()

        if not paragraph_text:
            continue

        paragraphs.append({
            "paragraphNumber": paragraph_number,
            "text": paragraph_text,
            "references": references
        })

    if paragraphs:
        sections.append({
            "section": section_title,
            "paragraphs": paragraphs
        })


# Save extracted data
output_folder = Path("data/extracted_articles")
output_folder.mkdir(parents=True, exist_ok=True)

output_file = output_folder / "air_pollution_extracted.json"

with open(output_file, "w", encoding="utf-8") as file:
    json.dump(
        sections,
        file,
        indent=4,
        ensure_ascii=False
    )


# Display extraction summary
print("Extraction completed!")
print(f"Sections extracted: {len(sections)}")

total_paragraphs = sum(
    len(section["paragraphs"]) for section in sections
)

total_references = sum(
    len(paragraph["references"])
    for section in sections
    for paragraph in section["paragraphs"]
)

print(f"Paragraphs extracted: {total_paragraphs}")
print(f"Reference occurrences: {total_references}")
print(f"Saved to: {output_file}")
