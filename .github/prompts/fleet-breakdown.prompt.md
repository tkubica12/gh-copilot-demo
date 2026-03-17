---
mode: agent
description: Break a larger request into safe parallel tracks for /fleet-capable clients or for subagent execution.
---
Break the current task into independent tracks that can run in parallel.

For each track provide:

- owner or suggested custom agent,
- scope,
- dependencies,
- concrete deliverable,
- validation step,
- merge or handoff criteria.

End with a short recommendation on whether `/fleet` is worth it when available or whether a single agent is simpler.
