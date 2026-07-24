# SIMS Writer v1.3.5 Final Output Integration

## Added
- Canonical `publication_view` generated from the final QA-reviewed draft.
- User-facing publication verdict, public message, advisories, and QA change list.
- Backward-compatible `publication_qa` extension for SIMS_FEEDBACK payloads.
- Publication package suppression: unpublishable drafts are never exposed as release content.

## Compatibility
- Existing Runtime publish decision remains unchanged.
- Existing SIMS_FEEDBACK fields are preserved; QA metadata is appended.
