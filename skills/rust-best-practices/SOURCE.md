# Source and local corrections

Imported from [Pedro Nauck's Rust best-practices skill](https://github.com/pedronauck/skills/tree/0422940cea5d9960b3697016d1cb28c8ed02b030/skills/mine/rust-best-practices).
Upstream revision: `0422940cea5d9960b3697016d1cb28c8ed02b030`.
The upstream skill declares MIT in its frontmatter.

Local corrections on 2026-09-26:

- Replaced the invalid manual `Future` example with [Tokio's pinning guidance](https://docs.rs/tokio/latest/tokio/time/struct.Sleep.html).
- Corrected the recursive `OctreeNode` type name.
- Corrected array allocation guidance and [SmallVec's inline-storage behavior](https://docs.rs/smallvec/latest/smallvec/struct.SmallVec.html).
- Made native `async fn` in traits the default async-trait example, with the `Send` form for public traits; `async-trait` stays for `dyn` dispatch (2026-09-26).

Preserve these corrections when updating. `.skill-lock.json` records upstream identity, not a claim that local files are unmodified.
