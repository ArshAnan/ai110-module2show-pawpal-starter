# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Features

| Feature | Description |
|---|---|
| Multi-pet support | Add multiple pets per owner; tasks are tracked per pet |
| Priority scheduling | Tasks sorted high → medium → low; higher-priority tasks always scheduled first |
| Time budgeting | Owner sets daily available minutes; tasks that don't fit are skipped, not dropped silently |
| Sort by start time | Tasks displayed in chronological order (HH:MM) in the UI |
| Recurring tasks | Daily and weekly tasks auto-generate their next occurrence when marked complete |
| Conflict detection | Overlapping timed tasks surface a warning before the schedule is shown |
| Filter by pet / status | Backend filter to view tasks for a specific pet or only incomplete tasks |
| Plan explanation | Each scheduled and skipped task includes a reason in the output |

## Smarter Scheduling

PawPal+ includes algorithmic features beyond basic priority sorting:

- **Sort by time** — `Scheduler.sort_by_time()` orders tasks by their `start_time` (HH:MM), with untimed tasks sorted last.
- **Filter tasks** — `Scheduler.filter_tasks()` returns tasks matching a pet name, completion status, or both.
- **Recurring tasks** — Tasks can have a `frequency` of `"daily"` or `"weekly"`. Calling `mark_complete()` on a recurring task returns a new `Task` instance due on the next occurrence (`due_date + 1 day` or `+ 7 days`).
- **Conflict detection** — `Scheduler.detect_conflicts()` scans all timed tasks and returns warning messages for any pair whose time windows overlap, without crashing the program.

## Testing PawPal+

Run the full test suite with:

```bash
python -m pytest
```

The suite covers 17 test cases across these areas:

| Area | What's tested |
|---|---|
| Task basics | `mark_complete()` changes status; `add_task()` / `remove_task()` work correctly |
| Scheduler | Tasks sorted by priority; tasks that don't fit are skipped |
| Sorting | `sort_by_time()` returns chronological order; untimed tasks sort last |
| Filtering | Filter by pet name; filter by completion status |
| Recurring tasks | Daily tasks spawn next occurrence (+1 day); weekly tasks spawn next (+7 days); one-time tasks return `None` |
| Conflict detection | Overlapping time windows flagged; back-to-back and untimed tasks are not flagged |
| Edge cases | Owner with no pets; pet with no tasks; zero available minutes; no start times set |

**Confidence level: ★★★★☆**
Core scheduling logic and algorithmic features are well covered. The main gap is UI-level testing (Streamlit interactions are not automated) and integration tests across the full owner → pet → task → plan flow with multiple pets simultaneously.
