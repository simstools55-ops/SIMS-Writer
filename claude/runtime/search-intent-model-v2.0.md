# Search Intent Model v2.0

Build the intent model from three evidence groups in this order:
1. the main query and Search Console query clusters;
2. the current top 10 result pages;
3. the target article and its existing strengths.

Output internally:
- primary task the searcher wants completed;
- secondary questions required to complete that task;
- expected answer format (definition, steps, comparison, troubleshooting, list, calculator, etc.);
- entities and exact terminology that identify the problem;
- intent boundaries: relevant but separate questions that should not be forced into the article.

The model must distinguish search-intent alignment from mere keyword inclusion.
