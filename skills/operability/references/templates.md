# Templates

## Runbook (five lines)

File `runbooks/<alert-name>.md`; the alert name is the file name.

```
Means:    <what is broken for which users, in one sentence>
Triage:   <PostHog query or insight link; filter by request id for one failing request>
Mitigate: <the fastest action that stops user impact: flag off, shed load, scale, fix config>
Rollback: <redeploy the last good deployment via use-railway; name the service and environment>
Verify:   <the query that shows the SLI back above target for one short window>
```

## Experiment card (one per external dependency, staging)

```
Dependency:    <name>
Hypothesis:    <when X is slow or failing, the service does Y, and the SLI stays above Z>
Steady state:  <metric, number, query; read and recorded before injection, abort if it is not met>
Variable:      <the one thing changed: added latency of N s, or an error rate of N%>
Abort:         <script that removes the fault and restores the system within 30 s; tested first>
Result:        <measured numbers during and after injection>
Learning:      <what differed from the hypothesis>
Fix:           <Linear ticket, owner, due date>
```

## Postmortem (one page, blameless)

```
Impact:       <who, what, how long, how much of the error budget>
Timeline:     <UTC; detection, page, mitigation, recovery; time from start to detection>
Causes:       <contributing causes as system conditions, with no individual named as the cause>
Went well:    <detection, tooling, and decisions to keep>
Went wrong:   <what delayed detection or recovery>
Got lucky:    <what limited the damage by chance>
Actions:      <action | type: prevent, detect, or mitigate | owner | due date | Linear ticket>
```
