# UthyAgent Wireframes and User Flows

## Home

```text
┌──────────────────────────────────────────────────────────────────────────┐
│ UthyAgent                                      Provider: OpenRouter  ●   │
├──────────────────────┬───────────────────────────────────────────────────┤
│ Home                 │ Desktop agent                                    │
│ Agent Chat           │ Describe a task. UthyAgent observes, acts, verifies│
│ Live Computer Use    │                                                   │
│ Tasks                │ ┌───────────────────────────────────────────────┐ │
│ Workflows            │ │ Type a natural-language task...               │ │
│ Agents               │ │                                               │ │
│ Integrations         │ │ [Start task] [Voice input] [Emergency stop]   │ │
│ Activity Logs        │ └───────────────────────────────────────────────┘ │
│ Settings             │                                                   │
│                      │ Execution activity                                │
│                      │ ┌───────────────────────────────────────────────┐ │
│                      │ │ Idle / Observe / Plan / Act / Verify          │ │
│                      │ │ Current app, action tooltip, last result      │ │
│                      │ └───────────────────────────────────────────────┘ │
└──────────────────────┴───────────────────────────────────────────────────┘
```

## Live Computer Use

```text
┌──────────────────────────────────────────────────────────────────────────┐
│ Task: Find the latest project log                              [Pause]  │
├──────────────────────────────┬───────────────────────────────────────────┤
│ TASK TIMELINE                │ LIVE DESKTOP                              │
│  ✓ Opened file manager       │ ┌───────────────────────────────────────┐ │
│  ● Searching for logs        │ │ Screenshot / accessible target overlay│ │
│  ○ Verify result             │ │                                       │ │
│                              │ │         [target highlight]             │ │
│ Current action               │ └───────────────────────────────────────┘ │
│ "Clicking search field"      │ Active app: Files                         │
│ Target: Search entry         │ Target bounds: x, y, width, height        │
│                              │                                           │
│ [Pause] [Cancel] [Details]   │ [Refresh screenshot] [Copy diagnostics]   │
└──────────────────────────────┴───────────────────────────────────────────┘
```

## Provider setup

```text
┌──────────────────────────────────────────────────────────────┐
│ Settings / AI Provider                                       │
│                                                              │
│ Provider     [OpenRouter                  v]                 │
│ Base URL     [https://openrouter.ai/api/v1]                  │
│ API key      [••••••••••••••••             Show]              │
│ Model        [openrouter/free             v]                 │
│                                                              │
│ [Fetch models] [Test connection]                              │
│                                                              │
│ Local-first: [ ] Prefer local endpoint when available        │
│ [Save provider]                                               │
└──────────────────────────────────────────────────────────────┘
```

## First-run flow

```mermaid
flowchart TD
  A[Launch UthyAgent] --> B[Explain local-first data handling]
  B --> C[Detect GNOME and display session]
  C --> D[Check GTK, AT-SPI, screenshot permissions]
  D --> E[Choose local or remote AI provider]
  E --> F[Test provider connection]
  F --> G[Run read-only desktop inspection]
  G --> H[Show a sample action and tooltip]
  H --> I[Enable optional Telegram with user allowlist]
  I --> J[Complete first task]
```

## Task execution flow

```mermaid
sequenceDiagram
  participant U as User / Telegram
  participant T as Task Manager
  participant P as Perception
  participant M as AI Model
  participant S as Safety Policy
  participant A as Automation Backend
  U->>T: Natural-language task
  T->>P: Observe desktop
  P-->>T: Accessibility tree + screenshot metadata
  T->>M: Task + bounded observation
  M-->>T: Proposed structured action
  T->>S: Validate action and risk
  S-->>T: Permit, reject, or require approval
  T->>A: Execute permitted action
  A-->>T: Action result
  T->>P: Observe updated state
  P-->>T: Updated state
  T->>M: Verify progress or request next action
  T-->>U: Progress and final result
```
