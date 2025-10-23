# Knowledge Sources & Access Tiers

| Source | Description | Access Tier | Refresh Cadence | Notes |
| ------ | ----------- | ----------- | --------------- | ----- |
| FinOps Foundation Public Site | Articles, working group outputs, public PDFs | Public | Weekly crawl | Originates from finops.org; respect robots.txt and canonical URLs |
| FinOps Member Portal | Member-only playbooks, benchmark studies | Member | Weekly incremental | Requires authenticated API/key vault; content tagged with embargo dates |
| Slack FinOps Workspace | Discussions, AMA transcripts | Internal | Daily | Use approved export API; anonymize participant names on ingest |
| FinOps Webinars & YouTube | Recorded sessions, presentations | Public | Monthly | Use AWS Transcribe for captions; attach slide decks where possible |
| FinOps Certified Training Material | Curriculum PDFs and labs | Confidential | Quarterly | Requires explicit legal approval; store in restricted bucket |
| Partner Contributions | Co-authored case studies under NDA | Confidential | Ad-hoc | Managed via secure file drop; enforce document owners |
| Public Cloud Docs (AWS, Azure, GCP) | Pricing, billing guides | Public | Monthly | Only ingest sections relevant to FinOps practice |
| Analyst Reports (Gartner, IDC) | Licensed market analysis | Confidential | As licensed | Store access metadata and license terms |

## Access Tier Definitions

- **Public**: Safe for anonymous users; may appear in unrestricted answers.
- **Member**: Restricted to authenticated FinOps Foundation members. Requires Cognito group `finops_member`.
- **Internal**: Restricted to internal staff and WG leads. Cognito group `finops_internal`.
- **Confidential**: Highly sensitive; available only to authorized SMEs via explicit approval (`finops_confidential`). Never surfaced unless the user session has `can_view_confidential = true` and the question scope requires it.

## Metadata Schema (DynamoDB `documents` Table)

```json
{
  "document_id": "uuid",
  "source": "finops_member_portal",
  "title": "FinOps Playbook 2025",
  "ingest_timestamp": "2025-10-01T12:00:00Z",
  "access_tier": "member",
  "content_tags": ["capabilities", "maturity-model"],
  "pii_detected": false,
  "expires_at": null,
  "owner_contact": "mailto:content@finops.org",
  "license": "FinOps member license",
  "checksum": "sha256",
  "retention_policy_days": 365
}
```
