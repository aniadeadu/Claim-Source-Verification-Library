
import json
import re
from pathlib import Path
import mwparserfromhell


INPUT_FILE = Path(
    "data/extracted_articles/air_pollution_wikitext.txt"
)

OUTPUT_FILE = Path(
    "data/extracted_articles/air_pollution_claims.json"
)


def get_attribute(tag, name):
    for attribute in tag.attributes:
        if str(attribute.name).strip() == name:
            return str(attribute.value).strip('"').strip("'")
    return None


def get_reference_details(tag, reference_id):
    reference = {"referenceID": reference_id}

    contents = mwparserfromhell.parse(str(tag.contents))

    for template in contents.filter_templates(recursive=True):
        for field in ["title", "url", "doi", "website", "work"]:
            if template.has(field) and field not in reference:
                value = str(
                    template.get(field).value.strip_code()
                ).strip()

                if value:
                    reference[field] = value

    if "doi" in reference and "url" not in reference:
        reference["url"] = (
            "https://doi.org/" + reference["doi"]
        )

    return reference


def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        wikitext = file.read()

    article = mwparserfromhell.parse(wikitext)

    named_references = {}

    for tag in article.filter_tags():
        if str(tag.tag).lower() != "ref":
            continue

        name = get_attribute(tag, "name")

        if name and not tag.self_closing:
            named_references[name] = get_reference_details(
                tag, name
            )

    claims = []
    claim_id = 1
    reference_counter = 1

    sections = article.get_sections(
        include_headings=True,
        include_lead=True,
        flat=True
    )

    # Keep track of the article's heading hierarchy.
    heading_stack = []

    for section_index, section in enumerate(sections, start=1):
        section_code = mwparserfromhell.parse(str(section))

        headings = section_code.filter_headings()
        section_path = []

        if headings:
            heading = headings[0]
            heading_level = heading.level
            heading_title = heading.title.strip_code().strip()

            while (
                heading_stack
                and heading_stack[-1][0] >= heading_level
            ):
                heading_stack.pop()

            heading_stack.append(
                (heading_level, heading_title)
            )

            section_path = [
                item[1] for item in heading_stack
            ]

        for heading in headings:
            section_code.remove(heading)

        paragraphs = re.split(
            r"\n\s*\n",
            str(section_code)
        )

        paragraph_number = 0

        for raw_paragraph in paragraphs:
            paragraph_code = mwparserfromhell.parse(
                raw_paragraph
            )

            citation_map = {}

            for tag in list(paragraph_code.filter_tags()):
                if str(tag.tag).lower() != "ref":
                    continue

                name = get_attribute(tag, "name")

                if name and name in named_references:
                    reference = named_references[name]
                else:
                    reference_id = f"ref_{reference_counter}"
                    reference_counter += 1

                    reference = get_reference_details(
                        tag, reference_id
                    )

                    if name:
                        named_references[name] = reference

                marker = (
                    f"CITATIONMARKER{len(citation_map) + 1}END"
                )

                citation_map[marker] = reference
                paragraph_code.replace(tag, marker)

            paragraph_text = paragraph_code.strip_code(
                normalize=True,
                collapse=True
            ).strip()

            if not paragraph_text or not citation_map:
                continue

            paragraph_number += 1

            sentences = re.split(
                r"(?<=END)\s+(?=[A-Z0-9])|"
                r"(?<=[.!?])\s+(?=[A-Z0-9])",
                paragraph_text
            )

            for sentence in sentences:
                markers = re.findall(
                    r"CITATIONMARKER\d+END",
                    sentence
                )

                if not markers:
                    continue

                references = [
                    citation_map[marker]
                    for marker in markers
                    if marker in citation_map
                ]

                clean_claim = re.sub(
                    r"CITATIONMARKER\d+END",
                    "",
                    sentence
                ).strip()

                if not clean_claim or not references:
                    continue

                claims.append({
                    "claimID": claim_id,
                    "sectionPath": section_path,
                    "paragraphNumber": paragraph_number,
                    "claim": clean_claim,
                    "references": references
                })

                claim_id += 1

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(
            claims,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("Claim extraction completed!")
    print(f"Claims extracted: {len(claims)}")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
