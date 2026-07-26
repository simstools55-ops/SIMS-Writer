# SERP Analysis Input Contract v2.0

A valid SERP evidence package contains:
- query;
- locale/device when known;
- observed_at date;
- up to 10 organic result records;
- for each record: URL, title and inspected content observations;
- source status: `live_inspected`, `user_supplied`, or `unavailable`.

Search snippets without page inspection may support result discovery but cannot establish that an article covers a topic.
