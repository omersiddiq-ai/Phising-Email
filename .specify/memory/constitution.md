<!--
Version change: placeholder → 1.0.0
Modified principles: placeholder → purpose-driven, incremental delivery, testable quality, maintainable simplicity, reviewable delivery
Added sections: Core Principles, Additional Constraints, Development Workflow, Governance
Removed sections: none
Templates requiring updates:
- .specify/templates/plan-template.md ✅ aligned
- .specify/templates/spec-template.md ✅ aligned
- .specify/templates/tasks-template.md ✅ aligned
Follow-up TODOs: none
-->

# CLASSES Constitution

## Core Principles

### I. Purpose-Driven Scope
Every feature must map to a clear, user- or stakeholder-facing outcome. Scope is defined by value delivered, not by internal convenience, and every work item must justify why it exists.

### II. Incremental Delivery
Work is delivered in small, reviewable increments that can be validated independently. Each change must be testable, releasable, and designed to minimize risk while preserving forward momentum.

### III. Testable Quality
Requirements are expressed as explicit acceptance criteria and measurable tests. Every meaningful behavior must have automated or documented verification before it is considered complete.

### IV. Maintainable Simplicity
Designs favor clarity and maintainability over premature optimization. Complexity must be justified, constrained, and removed when it no longer serves the project.

### V. Reviewable Delivery
All changes require review, rationale, and alignment with repository conventions. Version-awareness, documentation, and risk analysis are mandatory for non-trivial work.

## Additional Constraints
Decisions must be traceable and documented in the repository. Work must use existing repo conventions, avoid undocumented patterns, and be explicit about any deviations from standard practices.

## Development Workflow
Use feature branches, peer review, and iterative validation for every change. Plans, specs, and tasks must cite this constitution; exceptions are documented with rationale and approval from at least one reviewer.

## Governance
This constitution is the baseline for planning, spec writing, task generation, and review. Amendments require a written rationale, review approval, and an update to any dependent templates, guidance, or process artifacts.

- Versioning policy: start at `1.0.0`; increment MAJOR for principle removals or incompatible governance changes; MINOR for new principles or material section additions; PATCH for wording, clarification, or formatting improvements.
- Compliance review: every plan, spec, and task set must reference the constitution and note any permitted exceptions.
- Review expectations: use PR review to validate alignment, verify testing and risk mitigation, and confirm that scope is appropriate.

**Version**: 1.0.0 | **Ratified**: 2026-06-07 | **Last Amended**: 2026-06-07

