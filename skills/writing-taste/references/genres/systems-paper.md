# Systems research paper

What this genre teaches, and where it parts from an internal design doc. Two exemplars:

- Giuseppe DeCandia et al., "Dynamo: Amazon's Highly Available Key-Value Store", SOSP 2007. The paper is on the page: https://www.allthingsdistributed.com/2007/10/amazons_dynamo.html
- James Bornholt et al., "Using Lightweight Formal Methods to Validate a Key-Value Storage Node in Amazon S3", SOSP 2021. Author's copy: https://jamesbornholt.com/papers/shardstore-sosp21.pdf. Publication record: https://www.amazon.science/publications/using-lightweight-formal-methods-to-validate-a-key-value-storage-node-in-amazon-s3

Use this when the piece is a systems paper, or when a design narrative has to teach a technique. For an internal design doc, use [design doc](design-doc.md) and borrow only the moves below.

## What it teaches

Requirements and assumptions come first, as constraints on the design. Dynamo §2.1 states the query model (primary-key access, objects usually under 1 MB, no operation spans items), rejects ACID in exchange for availability, requires commodity hardware at the 99.9th percentile, and assumes a non-hostile environment, one instance per service, and a scale of hundreds of hosts. ShardStore §3.1 states the correctness properties the work will actually check (durability and consistency) and says availability and performance are out of scope because other methods already cover them.

A technique-per-problem table makes the design scannable. Dynamo's Table 1 pairs each problem with one technique and the advantage that justified it: consistent hashing for partitioning, vector clocks with reconciliation during reads for write availability, sloppy quorum and hinted handoff for temporary failure, Merkle-tree anti-entropy for permanent failure, gossip for membership.

Lessons come from production, with the numbers the authors can share. Dynamo §6 covers durability against latency, uneven load, how often versions diverge, client-driven against server-driven coordination, and background work stealing foreground capacity. ShardStore §8 reports that checking each property with the tool that fits it, against executable reference models, kept 16 issues out of production, including crash consistency and concurrency, and that engineers who are not formal-methods specialists extended the checks as the code changed. §8.4's lesson is to start while the design is still moving, one component at a time, so the models stay relevant.

## How it differs from a design doc

The audience is the research community, not the team that will build and operate the system. The paper argues a result: Dynamo, that a synthesis of known techniques yields a production store with a tunable consistency window; ShardStore, that lightweight formal methods can validate a storage node under ongoing feature work. An internal design doc argues a decision against the organization's goals and names the owner, the rollout, the fallback, and the open questions. A paper spends that space on related work and on evidence. It does not carry operational ownership, flag order, or a note that routes reviewers.

Borrow the opening constraints, the technique table, and the production lessons. Do not borrow the paper's shape as the shape of a design doc.
