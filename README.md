## Overview
The **Claim–Source Verification Library** is a research resource for examining the relationship between claims and the sources cited to support them. It is designed to preserve not only the claim and its citation, but also the evidence found in the source, the location of that evidence, the assessment reached, and the reasoning behind that assessment.

The project is intended to support transparent, reproducible research into claim verification and the evaluation of AI-assisted fact-checking. Its structured data makes it possible for researchers and developers to inspect individual assessments, build on the dataset, and develop consistent methods for comparing human and automated evaluations.

The initial dataset contains a pilot collection of human-assessed claims. It is a starting point for a resource that can be expanded with additional articles, claims, sources, evidence and assessments.

## Why this project matters
A source being cited does not automatically mean that it supports the statement attached to it. A cited source may:
- Directly support the full claim.
- Support only part of the claim.
- Discuss the same subject without establishing the specific statement.
- Present evidence that conflicts with the claim.
- Provide insufficient information to reach a clear conclusion.
A useful verification resource therefore needs to record more than a binary true/false label. It should make the assessment traceable: a reader should be able to see what was checked, which source was examined, what evidence was found, where it appeared, and why a particular verdict was assigned.

This library is organised around that principle.

## Project objectives

1. Preserve claim–source relationships. Keep each claim connected to its article, cited source and corresponding assessment.
2. Record traceable evidence. Store exact evidence quotations and their locations in the source wherever evidence is available.
3. Represent nuanced assessments. Distinguish full support, partial support, lack of support, contradiction and uncertainty.
4. Make the data machine-readable. Use a consistent JSON structure and a JSON Schema for validation.
5. Support reproducible workflows. Provide documentation and Python tooling that help others inspect, validate and prepare compatible data.
6. Enable future evaluation. Establish a structured foundation for future human–AI comparison and benchmarking.

## Repository contents
The repository is organised around the dataset, its schema, the supporting documentation and the Python processing tools.

claimSourceVerificationLibrary/
│
├── data/
│   ├── extracted_articles/
│   │   ├── air_pollution_claims.json
│   │   ├── air_pollution_extracted.json
│   │   └── air_pollution_wikitext.txt
│   │
│   ├── claims.json
|   |── claimVerificationResearch.xlsx
│   ├── schema.json
│   
├── docs/
│   |── annotation_guidelines.md
|   └── data-model.md
│
├── scripts/
│   |── excel_to_json.py
|   |── extract_candidate_claims.py
|   |── validate_schema.py
|   |── wikipedia_extractor.py
│
├── requirements.txt
└── README.md

## Main components


| Component | Purpose |
|---|---|
| `data/claims.json` | Contains the structured, machine-readable claim-verification dataset, including claims, cited sources, evidence, verdicts and reasoning. |
| `data/schema.json` | Defines the expected JSON structure, required fields, data types and permitted values. It is used to validate the dataset. |
| `data/claimVerificationResearch.xlsx` | The working Excel workbook containing the original claim-verification research records used by the conversion script. |
| `data/extracted_articles/` | Stores extracted article materials used in the claim-verification research. These files preserve article content and related claim information in different formats for reference and further processing. |
| `data/extracted_articles/air_pollution_claims.json` | Contains candidate claims identified from the air pollution article in a structured JSON format. |
| `data/extracted_articles/air_pollution_extracted.json` | Contains extracted article sections, paragraphs and associated references in JSON format. |
| `data/extracted_articles/air_pollution_wikitext.txt` | Contains the raw wikitext of the Wikipedia air pollution article, preserving its source markup and content. |
| `docs/annotation_guidelines.md` | Documents the annotation process, evidence-assessment criteria and guidelines for assigning verification verdicts. |
| `docs/data_model.md` | Describes the dataset's structure, fields, data types and relationships between the claim-verification records. |
| `scripts/excel_to_json.py` | Converts the Excel research workbook into structured JSON and validates the generated dataset against the schema. |
| `scripts/extract_candidate_claims.py` | Identifies candidate claims from extracted Wikipedia article content for further examination and verification. |
| `scripts/validate_schema.py` | Checks whether the JSON dataset conforms to the defined JSON Schema. |
| `scripts/wikipedia_extractor.py` | Extracts Wikipedia article content and prepares it for further processing and claim identification. |
| `requirements.txt` | Lists the Python dependencies required to run the project's processing scripts. |

## Dataset
The main dataset is stored in data/claims.json. It contains a top-level claims collection, with each item representing an assessed claim.

A claim record can include:
- Claim identifier and text — the record ID and the statement being examined.
- Category — the claim's classification in the research dataset.
- Article information — the Wikipedia article title and URL associated with the claim.
- Source evaluations — information about the cited source or sources being assessed.
- Evidence — exact quotations extracted from the source, together with their locations.
- Subclaims — smaller components of a claim where separate assessment is necessary.
- Overall verdict — the final assessment of the claim.
- Evidence gaps — aspects of the claim for which adequate supporting evidence was not identified.
- Reasoning — an explanation of how the evidence supports the assessment.
The structure is intended to retain the relationship between a claim, its cited source, the evidence located in that source and the resulting assessment. Evidence quotations should not be paraphrased when entered as direct quotations. Locations should be as precise as the source allows, such as a PDF page and paragraph or a webpage section.

## Assessment labels
The dataset uses the following assessment outcomes:

| Verdict | Meaning |
|---|---|
| `Supported` | The available source evidence supports the claim as stated. |
| `Partially supported` | The evidence supports some, but not all, of the claim. |
| `Unsupported` | The examined source does not provide adequate support for the claim. |
| `Contradicted` | The evidence conflicts with the claim. |
| `Unclear` | The available evidence is insufficient or ambiguous for a confident assessment. |

These labels concern the relationship between the claim and the cited source. They should not automatically be interpreted as a definitive judgement about whether the claim is true in every possible context.

## Data structure and validation
The dataset is stored as JSON so that it can be read by people and processed by software. The accompanying schema.json describes the expected structure, required fields, data types and permitted assessment values.

The schema uses JSON Schema Draft 2020-12.

Validation helps identify structural problems such as:
- Missing required properties.
- Incorrect data types.
- Invalid verdict values.
- Evidence records that do not follow the expected structure.
- Other deviations from the defined dataset format.

A successful schema validation confirms that the JSON conforms to the defined structure. It does not, by itself, establish that a quotation is accurate, that a source supports a claim, or that an annotation is factually correct. Those questions require source-level and research review.

## Python tools
The current Python utility, scripts/excel_to_json.py, prepares structured JSON from the working Excel workbook.

At present, the script:
1. Reads the configured workbook and the Claims worksheet.
2. Extracts the claim, article, source, evidence and assessment information.
3. Normalises selected values, including verdict labels.
4. Preserves individual evidence quotations and their associated locations.
5. Builds the JSON dataset.
6. Validates the generated data against data/schema.json.
7. Writes the resulting JSON to data/claims.json.

The converter is a practical processing tool for the current research workflow. The longer-term reusable-library direction is to make the underlying functionality easier to import and call from other Python projects, rather than requiring users to edit and run a script with fixed file paths.

## Getting started

### 1. Requirements
- Python 3.9 or later.
- The files in this repository.
- The dependencies listed in requirements.txt.

### 2. Get the project
Clone the repository:

git clone <repository-url>
cd claim-source-verification-library

Replace <repository-url> with the repository's actual Git URL.

### 3. Create and activate a virtual environment

python -m venv .venv

**On Windows:**

.venv\Scripts\activate

**On macOS or Linux:**

source .venv/bin/activate

### 4. Install dependencies

python -m pip install -r requirements.txt

## 5. Check the project files
Make sure the workbook, schema and script are in the locations expected by the converter:

data/claimVerificationResearch.xlsx
data/schema.json
scripts/excel_to_json.py

## 6. Run the converter

From the repository root:
python scripts/excel_to_json.py

If the conversion completes successfully, the script reports the number of claims converted and the location of the generated JSON file.

Important: The current script uses configured paths rather than command-line arguments. It writes to data/claims.json, so keep a copy of any JSON file you want to preserve before running the converter again.
Using the JSON dataset
You do not need to run the converter to read the existing dataset. Any tool or programming language that can parse JSON can inspect it.

For example, in Python:

````python
import json
from pathlib import Path

dataset_path = Path("data/claims.json")

with dataset_path.open("r", encoding="utf-8") as file:
    dataset = json.load(file)

claims = dataset["claims"]

print(f"Number of claims: {len(claims)}")

for claim in claims:
    print(claim["claimID"], claim["overallVerdict"])
````

This example reads the existing JSON file; it does not modify the dataset.

**Validating an existing JSON file**
The converter validates the JSON it generates. To validate an existing JSON file independently, you can use the jsonschema package:

```python
import json
from jsonschema import Draft202012Validator

with open("data/schema.json", encoding="utf-8") as schema_file:
    schema = json.load(schema_file)

with open("data/claims.json", encoding="utf-8") as data_file:
    dataset = json.load(data_file)

validator = Draft202012Validator(schema)
errors = sorted(validator.iter_errors(dataset), key=lambda error: list(error.path))

if errors:
    for error in errors:
        print(f"Validation error at {list(error.path)}: {error.message}")
else:
    print("The dataset is valid against the schema.")
```

### Annotation and quality assurance
The annotation guidelines describe how claims are examined and how evidence and verdicts should be recorded. They should be used alongside the schema:

- The annotation guidelines explain the research decisions and annotation procedure.
- The JSON schema defines the machine-readable structure in which those decisions are recorded.
- The dataset contains the resulting annotated records.

Quality assurance should consider both technical validity and research quality. In particular:

- Check that evidence quotations match the cited source.
- Record precise evidence locations and do not invent missing locations.
- Distinguish evidence that supports a complete claim from evidence that supports only one component.
- Explain unsupported, contradictory or unclear assessments.
- Review ambiguous cases consistently.
- Keep the dataset and schema aligned when the structure changes.

Schema validation is one part of quality assurance, not a replacement for human review.

### Reuse and future development
The project is intended to grow beyond a one-off conversion workflow. Potential next steps include:

- Reusable Python interface: refactor the current script into functions that can be imported and called by other Python projects.
- Configurable inputs and outputs: allow users to supply workbook, schema and output paths instead of editing hard-coded paths.
- Command-line interface: support commands such as converting a source file and validating an existing JSON dataset.
- Automated tests: test conversion behaviour, evidence extraction, location handling, verdict normalisation and schema validation.
- Dataset expansion: add further assessed claims while retaining the same data conventions.
- Benchmarking examples: provide reproducible examples for analysing and comparing human and AI assessments.
- Contribution documentation: explain how new records, sources and assessments should be added without breaking consistency.
These are development directions, not claims that all of these features are already implemented.

### Contributing
Contributions that improve the dataset, documentation, schema or Python tooling are welcome, subject to the project's review process.

Before contributing:

1. Read the annotation guidelines.
2. Follow the existing JSON structure.
3. Preserve exact evidence quotations and source locations.
4. Use the established verdict labels.
5. Validate changes against the schema.
6. Explain substantive annotation decisions clearly.

For code changes, include or update tests where appropriate and describe how the change was checked.

### Scope and limitations
The current dataset is a pilot research resource, not an exhaustive collection of all Wikipedia claims or cited sources. Its assessments reflect the evidence examined and the annotation decisions recorded for each case.

A valid JSON record is not automatically a correct research judgement. The quality and usefulness of the benchmark depend on transparent evidence, consistent annotation, careful review and clear documentation of limitations.

### Licence and citation
**Licence:** Add the project's chosen data and software licences here before public release. Do not assume that the dataset, source material and code all share the same licence.

**Citation:** Add the preferred citation for the project or dataset when the project citation details have been established.

### Acknowledgements

This project is being developed in the context of the Outreach Round 33 microtask - claim verification
 #7037 work. The aim is to contribute a transparent and reusable resource for studying how well cited sources support claims and for supporting future evaluation of claim-verification approaches.