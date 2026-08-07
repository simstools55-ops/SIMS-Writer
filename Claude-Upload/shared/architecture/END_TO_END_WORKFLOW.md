# End-to-End Workflow v1.0

1. SBM discovers or receives a problem and creates a Case when diagnosis or multi-step treatment is required.
2. SBM builds an Evidence Package and sends a Doctor request.
3. Doctor returns diagnosis and one or more non-executable referrals.
4. SBM validates routing, Workflow Lock, evidence, dependencies, and user approval requirements.
5. SBM issues Writer, Creator, or Merge treatment requests.
6. The specialist returns a treatment result to SBM.
7. The user applies approved changes and SBM records publication separately.
8. SBM measures at 7/14/21/28 days and longer where required.
9. SBM closes the Case or requests Doctor re-examination.

Daily low-risk Writer improvements may bypass Doctor. Complex, failed, declining, cannibalized, merge, deletion, noindex, and new-article cases should use Doctor routing.
