# Agent HQ and orchestration

This chapter is about moving from a single useful agent to coordinated multi-agent delivery across local, background, and cloud execution modes.

## Why it matters

- The different operating surfaces become easier to understand when they are connected through one workflow.
- Work can move between local interactive sessions, background tasks, cloud execution, and Agent HQ.
- Agent HQ acts as mission control for multi-agent work.

## Operating ladder

1. Local work in VS Code agent mode for interactive tasks.
2. Copilot CLI when the shell is part of the task.
3. Background agents when work should continue asynchronously.
4. Cloud agents when the outcome should land in a governed GitHub flow such as a branch or pull request.
5. Agent HQ for launching, tracking, and steering several agent tasks together.

## Key concepts to cover

### Multi-agent orchestration

The repository examples illustrate:

- one orchestrator splitting a task into bounded workstreams
- handoff packets between agents
- parallel specialists when tasks are independent
- merged summaries and reviewable outputs

### Background and long-running work

Background agents are useful when:

- the task will outlast one prompt
- the operator does not want to babysit every step
- the team wants resumable work with checkpoints and review points

### Cloud agents

Cloud agents are the natural step when the work should end in GitHub-native review surfaces such as branches, pull requests, checks, and audit trails.

### Agent HQ

Agent HQ is the mission-control story:

- coordinate several tasks
- steer work across surfaces
- monitor progress and outputs
- keep the human in charge of prioritization and review

### Memory and Spaces in orchestration

The broader GitHub context story also fits here:

- Copilot Memory helps recurring work avoid starting from zero
- Copilot Spaces package reusable shared context across repositories and teams
- both strengthen handoff, planning, and review when work spans more than one session or one surface

## Repository examples

- `examples\agents\01-cli-orchestration-and-handoff.md`
- `examples\agents\03-long-running-agent-pattern.md`
- [`.github/agents/workshop-orchestrator.agent.md`](../.github/agents/workshop-orchestrator.agent.md)
- [`enterprise_demo_flow.md`](enterprise_demo_flow.md)

## What to emphasize

- orchestration is about scope, delegation, and review, not just launching more chats
- background and cloud agents are useful because they support handoff and governance
- Agent HQ matters when the user becomes a manager of agent work, not only a direct operator

## Supporting material

- `examples\agents\README.md`
- [`README.md`](../README.md)
