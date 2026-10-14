# Requirements-driven decision — Oxide RFD 110

- Link: https://rfd.shared.oxide.computer/rfd/0110
- Author: David Pacheco, Oxide. State: published
- Title: CockroachDB for the control plane database
- Genre: a decision doc that answers requirements which already exist
- Use when: the requirements are settled and the job is to choose, with enough evidence to move forward.

## What it teaches

It answers requirements that live elsewhere and links them: RFD 48 (control-plane architecture) and RFD 53 (control-plane data storage). The opening states the requirement and what this document decides. It does not restate those RFDs.

The goals draw the boundary of the decision in one sentence: not seeking to completely de-risk the choice of database, just enough confidence to move forward. Absolute performance is out of scope because RFD 53 already says it is not the hard part, and the doc links there instead of repeating the numbers.

A note to readers routes the review. Conclusions are the goals plus the executive summary. Weighing in on the recommendation means the whole document. The detailed test results sit in two companion documents, and most readers are told they can skip them.

The executive summary states the conclusion (solid enough to continue; not worth a comparable evaluation of the other options right now) and asks reviewers two questions: which results should worry us more than this writeup does, and which tests should run before proceeding.

Each choice carries its reason:

- Hands-off operation. One component to deploy, pointed at the cluster. TiDB is several components to monitor and scale, deployed with Kubernetes, Ansible, or TiUP.
- Jepsen. The CockroachDB report was strong. The Yugabyte and TiDB reports, from 2019, found serious issues, including operational ones. The doc says those issues have likely been fixed since, and still treats the reports as evidence of where to look.
- Range sharding. Keys stay sorted, so a large collection can be paginated. Yugabyte was primarily hash-sharded; its range sharding, at the time of the notes, lacked active rebalancing. TiDB is separated on operations and on MySQL compatibility, not on sharding.

The choice is grounded in an outage the authors lived. Joyent Manta kept availability with a sharded fleet of PostgreSQL, and the surrounding failover was the distributed system. Maintenance debt (vacuum, replication apply lag, checkpoint lag) accrued for months and then took a database offline for days. That is why a store designed for distributed failure is preferred over one operated as a single system. The outage is evidence.

A short basics section explains how CockroachDB actually works (gateway node, ranges, replicas, leaseholders), enough to judge the tests that follow.

Risks are one table: area, likelihood, impact, and what they would do about it. Untested conditions are listed beside it (overload, backup under load, a controlled scale test, multi-node partitions, clock rollback, and others). Open questions stay open. Questions that got answers are kept under "Previously open questions," with the answer under the question.

## Take the structure, not the length

The document is long because it is partly a test report, and it says so by parking the raw results in companion docs. Copy the routing, the bounded goal, the reason beside each choice, the risk table, and the untested list.

## Where this shape stops

Answered questions stay in the RFD under their own heading. The [design doc](design-doc.md) folds an answer into the body and deletes the question. Mitigation in the RFD sits inside the details cell; the design-doc risk table gives it a column.
