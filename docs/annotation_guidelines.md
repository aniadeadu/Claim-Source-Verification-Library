# Annotation Guidelines

## 1. Purpose
These guidelines explain how to assess Wikipedia claims against their cited sources and record the findings consistently.

## 2. Scope of Verification
The primary task is to evaluate the relationship between a specific Wikipedia claim and its cited source.
Researchers should determine whether:

- The cited source directly supports the claim.
- The source supports only some parts of the claim.
- The source does not provide evidence for the claim.
- The source provides evidence that conflicts with the claim.
- The available information is insufficient to reach a reliable conclusion.

**Important:** The assessment focuses on whether the cited source supports the Wikipedia claim. A claim should not automatically be marked as Supported simply because it appears factually correct or is supported by other sources. The assessment must be based on the cited source being examined.

## 3. Annotation Principles
All assessments should follow these principles:

-   **Accuracy:** Preserve the original wording of the Wikipedia claim and the exact wording of source quotations.
-   **Traceability:** Ensure that every recorded quotation can be located in the cited source.
-   **Consistency:** Apply the same assessment criteria and verdict definitions to all claims.
-   **Objectivity:** Base assessments on the available evidence rather than personal opinions or assumptions.
-   **Transparency:** Clearly document evidence gaps, access limitations and uncertainties.


## 4. Assessment Steps (recommended)
The following steps provide a recommended procedure for assessing each claim.

- **Identify the Claim:** Identify and record the factual claim from the selected Wikipedia article.
- **Access the Cited Source:** Open the source linked to the claim.
- **Search for Evidence:** Use Ctrl + F to search for the exact wording of the claim. If no match is found, search for important keywords from the claim.
- **Read the material**: Read the matching sections carefully to understand the information and determine whether it supports the claim. If the searches do not produce useful results, read through the entire source.
- **Record the evidence:** Copy relevant quotations exactly as they appear in the source without changing the wording.
- **Record the Evidence Location:** Indicate where the quotation appears, such as the webpage section, paragraph or PDF page number.
- **Assign a Verdict:** Choose the verdict that best describes how the cited evidence relates to the claim.
- **Provide Reasoning**: Briefly explain why the evidence supports, partly supports, contradicts or fails to establish the claim.

## 5. Claim Identification and SubClaims

### 5.1 Claim Identification

-   Each assessment must have a unique Claim ID.
-   Claim IDs should follow the numbering used in the   research document to maintain consistency and make individual records easy to locate.
-   Researchers should preserve the original wording of the Wikipedia claim as much as possible. Claims should not be rewritten in a way that changes their meaning.
-   Each record should identify the relevant Wikipedia article and provide its URL. Where possible, the article URL should point to the specific revision from which the claim was collected.

### 5.2 Identifying SubClaims

Some Wikipedia claims contain multiple factual statements. Where these statements can be assessed independently, the main claim may be divided into subclaims.

For example, a claim stating that poverty can limit access to healthcare, increase the risk of malnutrition, and contribute to the spread of infectious diseases contains three independently assessable statements.

In such cases:

-   Divide the main claim into its relevant factual components.
-   Preserve the original meaning and wording of each component as much as possible.
-   Assign each subclaim a unique identifier linked to its parent Claim ID.
-   Use a consistent numbering format to define hierachical relationship, such as 12.1, 12.2 and 12.3 for the subclaims belonging to Claim 12.
-   Avoid dividing a straightforward claim into unnecessary subclaims.

**Note:** Subclaims should represent meaningful factual statements, not arbitrary fragments of a sentence.

## 5.3 Assessing Subclaims
Each subclaim should be assessed individually against the relevant cited evidence.

Researchers should:

-   Record the evidence relevant to each subclaim.
-   Provide the exact quotation and its location.
-   Assign a verdict to each subclaim.
-   Explain how the evidence relates to that particular statement.

**Note:** A source may support one subclaim while failing to support another. Researchers should not assume that evidence supporting one component automatically supports the entire claim.

## 5.4 Overall Claim Assessment

Where a claim has multiple subclaims, an overall verdict must also be assigned to the complete claim.

The overall verdict should reflect the combined assessment of its subclaims.

As a general guide:

-   **Supported:** All material components of the claim are adequately supported.
-   **Partially supported:** Some components are supported, but other material components are not established or are only partly supported.
-   **Unsupported:** The cited evidence does not establish the material components of the claim.
-   **Contradicted:** The cited evidence directly conflicts with the claim or a material component of it.
-   **Unclear:** The available information is insufficient to make a reliable overall assessment.

The overall verdict should not be assigned automatically without considering the significance of the individual subclaims and the evidence available.

## 6. Verdict Classification
Researchers must assign one of the following five verdicts to each claim.

### 6.1 Supported
- Use Supported when the cited source provides sufficient evidence for the claim.
- The evidence should correspond to the information expressed in the claim, including its relevant details and qualifications.
- A source does not need to repeat the exact wording of the Wikipedia claim, but its content must substantively support the claim.

### 6.2 Partially supported
Use Partially supported when the cited source provides evidence for some, but not all, of the claim.

This verdict is appropriate when:
-   The source supports the general idea but does not establish an important detail.
-   The source supports some components of a claim but not others.
-   The source provides evidence for the claim but omits a significant qualification, comparison or relationship expressed in it.

Researchers must identify which parts are supported and which parts are not established by the source.

**Note:** Do not use this verdict simply because the source uses different wording from the Wikipedia article.

### 6.3 Unsupported
Use Unsupported when the cited source does not provide sufficient evidence for the claim.

This may occur when:
-	The source does not discuss the subject or information expressed in the claim.
-	The source discusses a related topic but does not establish the specific claim.
-	The relevant information cannot be located in the cited source.
Unsupported does not necessarily mean that the claim is false. It means that the cited source does not provide the necessary support.

### 6.4 Contradicted
Use Contradicted when the cited source provides evidence that directly conflicts with the claim.

- The source must contain information that is inconsistent with what the Wikipedia claim states.
- Researchers should identify the conflicting information and explain why it contradicts the claim.
- Do not use Contradicted merely because the source does not mention the claim. Absence of supporting evidence is not, by itself, evidence of contradiction.

### 6.5 Unclear
Use Unclear when the available information is insufficient to make a reliable assessment.

This may occur when:
-   The cited source is inaccessible.
-   The relevant passage cannot be interpreted confidently.
-   The source is ambiguous or incomplete.
-   The available evidence does not allow the researcher to distinguish between the possible verdicts.

Researchers should explain why the assessment remains uncertain.

**Note:** Unclear should not be used simply because the assessment requires additional reading or careful interpretation.

## 7. Source Accessibility

-   Record the accessibility status of each cited source in the accessStatus field.
-   Use accessNotes to describe access restrictions, unavailable content or other relevant access issues, where applicable.
-   Do not invent or infer evidence from a source that could not be examined.
-   Where source accessibility prevents a reliable assessment, consider whether the appropriate verdict is Unclear.

**Note:** Accessibility should be assessed based on whether the researcher could inspect the relevant source content, not simply whether a webpage or document link opens.

## 8. Evidence Collection
Researchers must record the evidence used to justify each verdict.

Evidence should be obtained from the cited source and should be relevant to the specific claim being assessed.

The following rules should be observed:
-   Keep evidence quotations faithful to the original source.
-   Record the exact wording of the relevant passage wherever possible.
-   Do not invent, paraphrase or alter a quotation while presenting it as a direct quotation.
-   When a claim has multiple cited sources, each source should be assessed separately and recorded in its own source evaluation.
-   Where multiple quotations are taken from the same source, record each quotation as a separate evidence entry..
-   Ensure that the evidence is sufficiently specific to demonstrate its relationship to the claim.
-   Do not treat a source's title, abstract or general topic as sufficient evidence unless the relevant information is actually established there.
-   Where multiple quotations are taken from the same source, record each quotation as a separate evidence entry.
-   Consider the surrounding context of a quotation to avoid misrepresenting the source's meaning.

**Note:** If no supporting passage can be identified, researchers should state that no relevant supporting evidence was located rather than inventing a quotation.

Where no evidence quotation is available, use the agreed placeholder convention in the structured dataset and explain the absence of evidence in the reasoning or evidence-gap field. A placeholder must never be presented as an actual quotation.

## 9. Evidence Location
Every evidence quotation should have a location that allows another researcher to find and inspect it.

-   For webpages, provide the relevant section heading or subsection where the quote or passage appears.
-   For PDF documents, provide the page number and, where possible, the relevant section or paragraph.
-   For other source formats, provide the most precise location available.
-   The location should correspond to the quotation recorded in the evidence field.
-   Where several quotations are used, identify the location of each quotation separately.

**Note:** Avoid vague descriptions such as "in the article" or "somewhere on page 10" when a more precise location can be provided.

## 10. Reasoning and Justification
Each verdict must be accompanied by a clear explanation.

The reasoning should:
-   Explain how the evidence relates to the claim.
-   Identify which parts of the claim are supported or not supported.
-   Explain any important omissions or contradictions.
-   Justify why the selected verdict is more appropriate than the alternatives.
-   Reasoning should be specific to the claim being assessed.

**Note:** Avoid explanations that simply repeat the verdict, such as "The source supports the claim." Instead, explain what the source establishes and how that corresponds to the claim.

For claims containing multiple subclaims, the overall reasoning should also explain how the individual assessments contribute to the final verdict.



## 11. Use of Multiple Sources and External Information

Where a Wikipedia claim has multiple cited sources:

-   Record the details of each cited source separately.
-   Assess each source on the evidence it provides.
-   Do not assume that every cited source supports every component of the claim.
-   Do not combine evidence from different sources and present it as though it came from one source.
-   Ensure that the reasoning distinguishes between evidence provided by the sources being examined.

The primary assessment must be based on the cited source being examined.

Researchers should not use information from unrelated sources to make an unsupported cited source appear sufficient.

Where external information is consulted for clarification, it should not be confused with evidence from the original cited source. The distinction between what the cited source establishes and what other sources establish must remain clear.

## 12. Consistency and Quality 
Before finalising an assessment, researchers should check that:

-   The claim matches the wording in the relevant Wikipedia article or revision.
- The correct cited source has been examined.
-   Compound claims have been divided into meaningful subclaims where necessary.
-   Subclaim numbering is consistent with the parent Claim ID.
-   Each evidence quotation corresponds to the appropriate claim or subclaim.
-   The evidence quotation accurately reflects the source.
-   The evidence location is precise and traceable.
-   The verdict follows the definitions in these guidelines.
-   The overall verdict reflects the assessment of the complete claim.
-   The reasoning explains the verdict.
-   The Claim ID is consistent across the research document and structured dataset.

**Note:** Researchers should avoid assigning verdicts based on assumptions, personal opinions or the apparent credibility of a source alone. Where an assessment is uncertain, the researcher should explain the uncertainty rather than force a definitive verdict.

## 13. Expected Annotation Record
Each claim assessment should contain the following information:

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

**Notes: **For claims without subclaims, evidence may be recorded under the relevant source evaluation. For claims with subclaims, evidence should be recorded under the corresponding subclaims, following the established dataset structure.

## 14. Final Considerations

The purpose of these guidelines is to promote a consistent and transparent approach to evaluating claim-source relationships.

Researchers should prioritise the accuracy of the original claim, the reliability of recorded quotations, the traceability of evidence and the clarity of their reasoning.

The objective is not simply to determine whether a Wikipedia statement is true or false. It is to establish whether the cited source provides adequate evidence for the statement and to document that assessment in a way that other researchers can inspect, understand and reuse.