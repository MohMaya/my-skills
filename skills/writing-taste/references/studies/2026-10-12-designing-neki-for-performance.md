# Designing Neki for performance — Dirkjan Bussink

- Link: https://planetscale.com/blog/designing-neki-for-performance
- Author: Dirkjan Bussink (@dbussink), PlanetScale, October 1, 2026
- Genre: technical writing (systems engineering post)
- Found via: shared on X by Ben Dicken (@BenjDicken, PlanetScale) on Oct 1, 2026 ("Doing nothing is wayyyyy faster than doing something."), about 380 likes and 330 bookmarks
- Studied: 2026-10-12

## Core claim

A query router is fast not because it decodes quickly but because it decodes only what each query forces it to, so Neki keeps PostgreSQL results as wire bytes and opens one more layer (rows, column frames, typed values) only when a query needs it.

## Thinking moves

- **Reduce the design to one principle and test every case against it.** The whole post is "do the least possible work." Each section asks what this query forces the router to know, and stops there.
- **Steelman the default before departing from it.** Decoding everything at the boundary is called "a sensible default" and shown in real code from Vitess, the team's own earlier system. The reader sees the cost (a slice and a value for every column of every row) before seeing the alternative, so the alternative feels earned rather than clever.
- **Order cases by how much work they force.** Point lookup (decode nothing), scatter query (still nothing), LIMIT (row boundaries), ORDER BY (one sort key), ORDER BY on an unselected column (decode one column, copy the rest as bytes), GROUP BY (full values). Each rung adds exactly one requirement, so the reader learns the layer model by climbing it.
- **Find where the principle stops.** The aggregate section says plainly that there is no byte-level trick for grouping and summing. Naming the limit makes the rest of the claim trustworthy.
- **Account for the cost of the cleverness.** A section lists the invariants the design must hold (buffers kept alive, three-index slices, per-consumer caches, memory accounting for rows that grow) and the types it must survive. The author shows he knows what the optimization can break.
- **Notice the surprising consequence.** Ordering by an unselected column means the router decodes the one column the client never sees and leaves the ones it asked for as bytes. He points out the oddity instead of hiding it, because it proves the principle.

## Writing moves

- **Opening:** the thesis as a near-truism, then the admission that it is easy to forget. Paragraph two states the problem (an extra hop the router cannot remove), paragraph three turns it into two questions the post will answer.
- **Structure:** one running example (an `orders` table sharded by `account_id`) and a query that changes one clause per section. Headings name the new requirement ("Adding LIMIT", "Sorting means decoding the sort key", "When we really need values").
- **Transitions:** each section ends on what the current case does not yet need and asks the next question ("Counting rows doesn't require that... but what if it did?"), or reaches back ("Recall from the last section").
- **Rhythm:** plain, first-person-plural engineering prose; short punch lines after dense paragraphs ("Sorting rows doesn't require copying the rows."; "No DataRow structs and no columns!").
- **Concrete examples:** real SQL, real protobuf, real Go from both systems, and small state tables (which columns are located versus decoded) instead of diagrams. The code is short and directly serves the point being made.
- **What he cut:** no benchmark charts, no marketing claims, no history of sharding. About 3,000 words of prose, almost all of it about one idea.
- **Ending:** the closing section replays the ladder in one sentence per rung and returns to the opening line. The last case named is the one where the trick stops, so the claim ends at its true size.

## Excerpts

1. Opening on a near-truism: "Nothing is as fast as not doing anything. That sounds obvious, but it is also surprisingly easy to forget when building software."
2. Giving the default its due: "It's a sensible default because it gives the rest of the system one consistent thing to work with."
3. A transition that is a question: "Counting rows doesn't require that... but what if it did?"
4. Owning the surprising consequence: "That's exactly the work this query required."
5. Naming the risk with a joke: "If moving the bytes around changes the result, we've built a very fast bug"

## Exercise

Pick one design decision you made recently and write its principle in one sentence. List four or five cases in order of how much they demand of that principle, from "costs nothing" to "this is where it stops working." Write one short section per case that changes only one thing from the previous case and ends with the question the next case answers. Before you show the alternative, describe the usual approach fairly and show its cost in real code or numbers.
