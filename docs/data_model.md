# Data Model

## 1. Purpose
This document describes how the Claim-Source Verification Library organises its claim assessment data. It explains the information recorded for each claim, the structure of the dataset and how claims, articles, cited sources, evidence and verdicts relate to one another.

The dataset is structured in JSON format to support consistent storage, retrieval, analysis and reuse of human assessments of Wikipedia claims against their cited sources.

## 2. Dataset Overview
The dataset is stored in JSON format and contains 20 assessed Wikipedia claims.

The claims are divided into two categories:
•	**AI flagged**: Claims identified as AI-flagged.
•	**Not AI flagged:** Additional claims selected for assessment.

Each claim has a unique identifier, represented by the claimID field.
The current dataset uses string identifiers numbered from 1-20.

-   Each claim record has information about:
-   The original Wikipedia claim.
-   Its category and associated Wikipedia article.
-   The cited source or sources used to assess it.
-   Evidence extracted from the cited sources.
-   Individual subclaim assessments, where applicable.
-   The overall verdict and reasoning for the assessment.

## 3. Data Fields and Descriptions

The JSON dataset uses the following fields to organise claim verification records

| Property | Description |
|---|---|
| `claimID` | Unique identifier assigned to each claim. |
| `claim` | Exact wording of the claim being assessed. |
| `category` | Identifies whether the claim is AI flagged or Not AI flagged. |
| `article` | Object containing information about the Wikipedia article. |
| `article.title` | Title of the Wikipedia article containing the claim. |
| `article.url` | URL of the Wikipedia article. |
| `subclaims.subclaimID` | Unique identifier for each subclaim, linked to its parent Claim ID |
| `subclaims` | Array containing individual factual statement extracted from a compund claim, where applicable. |
| `subclaims.text` | Wording of the individual subclaim. |
| `subclaims.evidence` | Array containing evidence entries relevant to that subclaim. |
| `subclaims.evidence.quote` | Exact quaotation taken from the source. |
| `subclaims.evidence.location` | Location of the quotation in the cited source. |
| `subclaims.verdict` | Assessment assigned to the individual subclaim. |
| `sourceEvaluation` | Array containing the evaluation of each cited source. |
| `sourceEvaluation.sourceTitle` | Title of the cited source. |
| `sourceEvaluation.sourceURL` | URL of the cited source. |
| `sourceEvaluation.sourceCitation` | Citation details associated with the cited source, where available. |
| `sourceEvaluation.accessStatus` | Records the accessibility status of the cited source. |
| `sourceEvaluation.accessNotes` | Provides additional information about accessing the source, where applicable. |
| `sourceEvaluation.accessDate` | Date which the source was accessed. |
| `sourceEvaluation.evidence` | Array containing evidence entries extracted from the cited source. |
| `sourceEvaluation.evidence.quote` | Exact quotation taken from the source. |
| `sourceEvaluation.evidence.location` | Indicates where the quotation can be found in the source, such as a page number or webpage section. |
| `overallVerdict` | Records the assessment outcome: Supported, Partially Supported, Unsupported, Contradicted or Unclear. |
| `evidenceGap` | Array recording specific gaps between the claim and the evidence found in the cited source. |
| `reasoning` | Explains why the verdict was assigned. |


## 4. Relationships Between Data Components

The dataset is organised around individual claim records. Each record connects the riginal Wikipedia claim to its  article, the cited source, the evidence examined, and the assessment outcome.

The relationships work as follows:

-   **Claim and article:** Each claim is associated with a Wikipedia article through the article object, which records the article title and URL.
-   **Claim and source evaluations:** Each claim has one or more source evaluations. The sourceEvaluation array stores the details and accessibility information of the cited source or sources.
-   **Claim and subclaims:** Where a claim contains multiple factual assertions, it can be divided into individual subclaims. Each subclaim has its own identifier, text, evidence and verdict.
-   **Source and evidence:** Evidence is recorded as quotations with precise locations in the cited sources. For claims with subclaims, evidence is stored under the relevant subclaim. For claims without subclaims, evidence is stored directly under the source evaluation.
-   **Assessment and overall verdict:** Individual subclaims receive separate verdicts where applicable. The overallVerdict field records the final assessment of the complete claim, while reasoning explains the assessment.
-   **Evidence gaps:** The evidenceGap field records aspects of the claim that could not be established or adequately supported by the available evidence.

This structure allows the dataset to retain both the individual assessments of compound claims and the final assessment of the original Wikipedia statement.


## 5. Example JSON Record
The following example shows how a compound claim is represented in the dataset. It uses claim 12, which contains three independently assessed factual assertions.

```json
{
    "claimID": "12",
    "claim": "Some hazardous air pollutants are produced in plastic and rubber production, whereas chloroform can be produced during water chlorination, and arsenic is found in the mining industry.",
    "category": "Not AI flagged",
    "article": {
        "title": "Air Pollution",
        "url": "https://en.wikipedia.org/wiki/Air_pollution"
    },
    "sourceEvaluation": [
        {
            "sourceTitle": "Understanding Environmental Pollution",
            "sourceURL": "https://en.wikipedia.org/wiki/Air_pollution#CITEREFHill2020",
            "sourceCitation": "Hill MK (2020). Understanding environmental pollution (Fourth ed.). Cambridge, United Kingdom ; New York, NY: Cambridge University Press. ISBN 978-1-108-42308-3.",
            "accessStatus": "Accessible via search",
            "accessNotes": "The book was not directly accessible through the Wikipedia citation or initial ISBN search. It was eventually located through a manual search using the book title, author, and publication year. The relevant page (103) was accessed and reviewed through Google Books preview.",
            "accessedDate": "2026-11-06"
        }
    ],
    "subclaims": [
        {
            "subclaimID": "12.1",
            "text": "Some hazardous air pollutants are produced in plastic and rubber production..",
            "verdict": "Supported",
            "evidence": [
                {
                    "quote": "Manufacturing plastic, rubber, adhesives, cushions",
                    "location": "Page 103, Table 5.5, row 9",
                    "verdict": "Supported"
                }
            ]
        },
        {
            "subclaimID": "12.2",
            "text": "… whereas chloroform can be produced during water chlorination…",
            "verdict": "Supported",
            "evidence": [
                {
                    "quote": "Formed during water chlorination.",
                    "location": "Page 103, Table 5.5, row 5 (Chloroform)",
                    "verdict": "Supported"
                }
            ]
        },
        {
            "subclaimID": "12.3",
            "text": "..and arsenic is found in the mining industry…",
            "verdict": "Supported",
            "evidence": [
                {
                    "quote": "2. Arsenic     2. Mining and smelting operations, glass making, petroluem refining, metal alloys",
                    "location": "Page 103, Table 5.5, inorganic pollutants, row 2 (Arsenic)",
                    "verdict": "Supported"
                }
            ]
        }
    ],
    "overallVerdict": "Supported",
    "evidenceGap": [],
    "reasoning": "The table directly identifies plastic and rubber manufacturing as sources of a hazardous air pollutant.\n\n\nThe source explicitly identifies water chlorination as a source of chloroform.\n\n\nThe source directly identifies mining operations as a source of arsenic."
}
```

The example demonstrates how the main claim is divided into subclaims, with each subclaim receiving its own evidence and verdict. The overall verdict summarises the assessment of the complete claim.

For a claim without subclaims, the subclaims array can be empty, and the evidence quotations are instead recorded within the relevant sourceEvaluation entry.

## 6. Verdict Categories

The dataset uses five verdict categories to describe how well the cited source supports the claim or individual subclaim.

-   **Supported:** The cited source provides sufficient evidence for the claim.
-   **Partially Supported**: The source supports some aspects of the claim but does not fully establish all its details.
-    **Unsupported**: The cited source does not provide sufficient evidence for the claim.
-    **Contradicted**: The source provides evidence that conflicts with the claim.
-   **Unclear:** The available information is insufficient to reach a clear conclusion.

For compound claims, verdicts are assigned to individual subclaims before an overall verdict is determined for the complete claim.
