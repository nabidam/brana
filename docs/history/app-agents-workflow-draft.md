# ChatGPT

## Phase 0

### **title:**

Vision & Product Discovery

### **model:**

GPT-5.5 (preferred) or Claude Opus

### **prompt:**

```
You are a senior product manager.

Your task is NOT to design or implement the application.

Your job is to interview me until every important requirement is clear.

Do not make assumptions.
Ask questions one by one.
Challenge vague requirements.
Suggest simpler alternatives when appropriate.

When finished, produce a complete Vision Document.

Do not proceed to architecture.
```

### **handoffs:**

- vision.md

### **output files:**

- vision.md

---

## Phase 1

### **title:**

Product Requirements Specification (PRD)

### **model:**

GPT-5.5

### **prompt:**

```
Create a production-quality Product Requirements Document.

Include:

- Functional requirements
- Non-functional requirements
- User stories
- Acceptance criteria
- Validation rules
- Error cases
- Constraints
- Future improvements

Do not discuss implementation.
```

### **handoffs:**

- vision.md

### **output files:**

- prd.md

---

## Phase 2

### **title:**

Technical Research

### **model:**

Claude Opus

### **prompt:**

```
Act as a senior software architect.

Research the product described in the PRD.

Compare implementation strategies.

Identify:
- industry best practices
- existing open-source solutions
- scalability concerns
- security concerns
- performance considerations
- recommended libraries
- tradeoffs

Produce a technical research document only.
```

### **handoffs:**

- prd.md

### **output files:**

- research.md

---

## Phase 3

### **title:**

Software Architecture

### **model:**

Claude Opus

### **prompt:**

```
Design a production-grade software architecture.

Include:

- System overview
- Module responsibilities
- Folder structure
- API boundaries
- Component interactions
- Dependency graph
- Design patterns
- Error handling strategy
- Configuration strategy
- Scalability considerations

Do not write implementation code.
```

### **handoffs:**

- prd.md
- research.md

### **output files:**

- architecture.md
- folder_structure.md

---

## Phase 4

### **title:**

Database Design

### **model:**

Claude Opus

### **prompt:**

```
Design the complete database.

Include:

- ER diagram (Markdown)
- Tables
- Fields
- Constraints
- Indexes
- Relationships
- Migration order
- Cascade behavior
- Soft delete strategy
- Audit fields

Explain design decisions.
```

### **handoffs:**

- architecture.md

### **output files:**

- database.md
- schema.sql

---

## Phase 5

### **title:**

API Specification

### **model:**

GPT-5.5

### **prompt:**

```
Produce a complete API specification.

Include:

- Endpoints
- Request body
- Response body
- Validation
- Authentication
- Authorization
- Status codes
- Error responses
- Pagination
- Filtering
- Versioning

Do not implement.
```

### **handoffs:**

- architecture.md
- database.md

### **output files:**

- api.md
- openapi.yaml

---

## Phase 6

### **title:**

Development Roadmap

### **model:**

Claude Sonnet

### **prompt:**

```
Split the project into implementation tasks.

Each task must include:

- objective
- inputs
- outputs
- dependencies
- files to modify
- acceptance criteria
- estimated difficulty

Keep tasks small.
```

### **handoffs:**

- architecture.md
- api.md
- database.md

### **output files:**

- roadmap.md
- tasks/task_001.md
- tasks/task_002.md
- ...

---

## Phase 7

### **title:**

Implementation

### **model:**

Claude Sonnet (primary) + Local coding model (optional for boilerplate)

### **prompt:**

```
Implement Task XXX.

Rules:

- Only modify approved files.
- Follow architecture exactly.
- Follow coding standards.
- Do not refactor unrelated code.
- Do not implement future tasks.
- Explain important decisions.
```

### **handoffs:**

- task_xxx.md
- architecture.md
- api.md
- database.md

### **output files:**

- Source code
- Unit tests
- Updated task file

---

## Phase 8

### **title:**

Code Review

### **model:**

Codex

### **prompt:**

```
Review the implementation.

Look for:

- logic bugs
- edge cases
- architecture violations
- unnecessary complexity
- maintainability
- concurrency issues
- error handling
- code smells

Do not rewrite the project.
```

### **handoffs:**

- Source code
- architecture.md
- task_xxx.md

### **output files:**

- review.md

---

## Phase 9

### **title:**

Testing

### **model:**

Claude Sonnet

### **prompt:**

```
Generate comprehensive tests.

Include:

- unit tests
- integration tests
- edge cases
- invalid inputs
- regression tests

Do not modify production code.
```

### **handoffs:**

- Source code
- task_xxx.md

### **output files:**

- Test files
- testing_report.md

---

## Phase 10

### **title:**

Security Audit

### **model:**

GPT-5.5

### **prompt:**

```
Perform a complete security review.

Focus on:

- authentication
- authorization
- input validation
- injection attacks
- XSS
- CSRF
- SSRF
- path traversal
- secrets management
- dependency risks

Provide remediation steps.
```

### **handoffs:**

- Source code
- architecture.md

### **output files:**

- security_report.md

---

# Phase 11

### **title:**

Performance & Scalability Review

### **model:**

Claude Opus

### **prompt:**

```
Review the application for performance.

Analyze:

- algorithm complexity
- database queries
- caching
- memory usage
- concurrency
- network usage
- scalability
- resource consumption

Prioritize improvements by impact.
```

### **handoffs:**

- Source code
- architecture.md
- database.md

### **output files:**

- performance_report.md

---

## Phase 12

### **title:**

Documentation & Release

### **model:**

Claude Sonnet

### **prompt:**

```
Create complete project documentation.

Include:

- README
- installation
- development setup
- deployment guide
- architecture overview
- API usage
- troubleshooting
- changelog
- future roadmap

Assume a new developer is joining the project.
```

### **handoffs:**

- Entire project
- All reports

### **output files:**

- README.md
- CONTRIBUTING.md
- DEPLOYMENT.md
- CHANGELOG.md
- docs/

# Gemini

## Phase 1:

Product Requirement Document (PRD)

### **Model:**

Gemini (Pro or Flash)

### **Prompt:**

```
Act as a Lead Product Manager. I want to build a highly optimized Todo App featuring real-time synchronization, categorization, priority levels, and subtask nesting. Generate a comprehensive Product Requirement Document (PRD) in strict Markdown format. Detail the user journeys, functional requirements, edge cases (e.g., handling offline states), and non-functional requirements. Do not include any introductory remarks, conversational pleasantries, or concluding notes. Output the Markdown directly.
```

### **Handoffs:**

Copy the generated Markdown PRD text directly into a local file named `prd.md`. Do not copy any chat history.

### **Output Files:**

`prd.md`

---

## Phase 2:

Technical Architecture Specification

### **Model:**

Claude Opus

### **Prompt:**

```
Act as a Principal Software Architect. Review the attached PRD Markdown file for a Todo App. Generate a complete Technical Architecture Specification. You must specify: 1. Core data schemas (PostgreSQL DDL table structures including indices). 2. System folder structure following Clean Architecture principles. 3. Specific Interface definitions and API contracts (REST payloads/WebSocket events for real-time sync). Do not write functional application code logic. Output only the structured Technical Architecture Spec in Markdown. Avoid conversational text.
```

### **Handoffs:**

Review the output, verify consistency, and save it locally as `architecture.md`. Open a fresh chat session for the next phase to ensure a clean context window.

### **Output Files:**

`architecture.md`

---

## Phase 3:

Structural Skeleton & Stubbing

### **Model:**

Claude Sonnet

### **Prompt:**

```
Act as a Senior Software Engineer. Read this Technical Architecture Spec for a Todo App. Generate _only_ the structural skeleton of the application files. Provide the data structures, database connection setups (using optimized drivers), interface stubs, and function signatures with comments. Do not implement the internal logic of the handlers or repositories yet. Ensure the code compiles cleanly. Output the code blocks with explicit file paths.
```

### **Handoffs:**

Save the generated skeleton files into your local project directory. Ensure the structure mirrors the architecture plan perfectly.

### **Output Files:**

`main.go`, `config/config.go`, `internal/domain/todo.go`, `internal/repository/interfaces.go` (example file paths assuming a Go backend system)

---

## Phase 4:

Component Implementation

### **Model:**

Claude Sonnet

### **Prompt:**

```
Act as a Senior Software Engineer. Using the structural skeleton we have established, implement the complete, production-grade business logic for the [insert specific module, e.g., Todo Repository Layer]. Ensure absolute type safety, robust error handling, and optimal database connection reuse. Implement full error wrapping. Write complete code without placeholders, `// TODO` comments, or truncation.
```

### **Handoffs:**

Replace the structural skeleton files with the fully fleshed-out source code files in your IDE.

### **Output Files:**

Fully implemented modules (e.g., `internal/repository/postgres_todo.go`, `internal/service/todo_service.go`, `internal/transport/http/handler.go`)

---

## Phase 5:

Code Audit & Optimization

### **Model:**

OpenAI o1/o3-mini OR a Large Local Reasoning Model (e.g., DeepSeek V4 Pro) via an H100 GPU

### **Prompt:**

```
Act as an Expert Principal Code Reviewer and Security Auditor. Analyze the attached implemented source code for the Todo App modules. Critically evaluate the logic for race conditions, inefficient resource allocation, unhandled error vectors, and potential performance bottlenecks. Provide a detailed summary of discovered issues and output the optimized, refactored version _only_ for the specific code blocks requiring remediation. Keep unchanged code out of the response.
```

### **Handoffs:**

Apply the verified optimizations and bug fixes directly to your master code files.

### **Output Files:**

Final optimized and audited production code files ready for testing.

# Claude

## **Phase 0:**

### **title:**

Rough Spec (Human-written)

### **model:**

None (you) — optionally Haiku 4.5 for quick Q&A while drafting

### **prompt:**

```
N/A (human writing). If using Haiku: "I'm drafting a spec for a Todo app. Here's what I have so far: [paste]. List anything ambiguous or missing that a developer would need to know. Do not rewrite the spec.
```

### **handoffs:**

`SPEC.md` → Phase 1

### **output files:**

`SPEC.md`

---

## **Phase 1:**

### **title:**

Interrogation + Architecture Plan

### **model:**

Claude Opus (strongest reasoning tier you have access to)

### **prompt:**

```
Turn 1: "Read SPEC.md below. Before planning anything, ask me every clarifying question a senior engineer would need answered. Do not plan yet. [paste SPEC.md]" — Turn 2: "Now produce PLAN.md: (1) architecture overview, (2) data model + schema, (3) API contract with exact endpoints/types, (4) full file tree, (5) implementation chunks — each chunk max ~300 lines of new code, with: files touched, exact requirements, acceptance criteria, and what NOT to do. Also produce CONVENTIONS.md: naming, error handling, folder structure, test style. Write both as complete markdown files.
```

### **handoffs:**

`PLAN.md` + `CONVENTIONS.md` → Phases 2–4. **End this session. Opus does not participate in implementation.**

### **output files:**

`PLAN.md`, `CONVENTIONS.md`

---

## **Phase 2:**

### **title:**

Scaffold

### **model:**

Claude Sonnet

### **prompt:**

```
You are implementing Chunk 0 (scaffold) of PLAN.md. Context: [paste PLAN.md, CONVENTIONS.md]. Create the exact file tree, all configs, DB schema/migration, and one smoke test. No feature logic. Follow CONVENTIONS.md strictly. If PLAN.md is ambiguous, choose the simplest interpretation and note it in a comment — do not ask.
```

### **handoffs:**

Working repo → Phase 3. Run it yourself; fix env issues manually (don't burn tokens on `npm install` problems).

### **output files:**

Full project skeleton, `migrations/001_init.sql`, `smoke.test.ts`

---

## **Phase 3:**

### **title:**

Feature Implementation Loop (repeat per chunk)

### **model:**

Claude Sonnet (fresh session per chunk); Haiku 4.5 for micro-fixes between chunks

### **prompt:**

```
Implement Chunk N of PLAN.md. Chunk spec: [paste chunk]. Conventions: [paste CONVENTIONS.md]. Current relevant files: [paste only touched files]. Write the implementation plus unit tests covering the acceptance criteria. Output complete files, not fragments. Do not modify files outside this chunk's scope.
```

### **handoffs:**

Passing chunk → next chunk session; accumulated diffs → Phase 4 after every 2–3 chunks

### **output files:**

Feature code + `*.test.ts` per chunk

---

## **Phase 4:**

### **title:**

Cross-Vendor Review (diffs only)

### **model:**

Codex / GPT-5.x

### **prompt:**

```
Review this diff against the attached API contract and conventions. Report only: (1) bugs/logic errors, (2) security issues, (3) contract violations, (4) convention violations — each with file:line, severity (high/med/low), and a one-line fix suggestion. No style opinions, no praise, no rewrites. [paste diff + contract section]
```

### **handoffs:**

`REVIEW_N.md` findings → Phase 3 (fixes) or Phase 5 (escalations)

### **output files:**

`REVIEW_N.md`

---

## **Phase 5:**

### **title:**

Escalation (only when stuck)

### **model:**

Claude Opus — on demand, not scheduled

### **prompt:**

```
Sonnet has failed this task twice. Chunk spec: [paste]. Current code: [paste]. Failing output: [paste]. Attempts already made: [summarize]. Diagnose the root cause, then either provide the corrected code or, if the plan itself is wrong, rewrite the affected section of PLAN.md.
```

### **handoffs:**

Fix → Phase 3 resumes; plan amendment → updated `PLAN.md` propagates to remaining chunks

### **output files:**

Patched code and/or updated `PLAN.md`

---

## **Phase 6:**

### **title:**

UI Polish (optional)

### **model:**

Gemini 3.1 Pro (currently strongest for UI-focused coding) — or Sonnet if you want fewer vendors

### **prompt:**

```
Improve the visual design of this component. Constraints: RTL-first, Vazirmatn font, [your palette], keep all logic/props/handlers unchanged — className and markup structure changes only. Cover: empty state, loading state, error state, mobile width. [paste component]
```

### **handoffs:**

Polished components → final Phase 4-style diff review → done

### **output files:**

Updated components

---

## **Phase 7:**

### **title:**

Ship Checklist

### **model:**

Haiku 4.5

### **prompt:**

```
Compare SPEC.md against this file tree and PLAN.md chunk list. Output: (1) unimplemented spec items, (2) a README.md, (3) required env vars with descriptions, (4) a deploy checklist for [Liara/Arvan]. [paste SPEC.md + file tree]
```

### **handoffs:**

Gap list → Phase 3 if needed; otherwise deploy

### **output files:**

`README.md`, `.env.example`, `DEPLOY.md`

# QWen

## Phase 0:

### **title:**

Ideation & Master Prompt Generation

### **model:**

Gemini 1.5 Pro (or Flash)

### **prompt:**

```
Act as an expert Product Manager and Technical Writer. I want to build a [Todo App with user authentication, task categorization, drag-and-drop reordering, and dark mode]. Your goal is to write a comprehensive Master Prompt that I will feed to an AI architect. Include: 1. Core Features & User Stories. 2. Edge cases (e.g., offline sync, empty states). 3. Suggested Tech Stack (React, Node, Postgres). 4. UI/UX guidelines. Format the output as a clean, detailed Markdown document.
```

### **handoffs:**

The generated Master Specification Document.

### **output files:**

`master_spec.md`

---

## Phase 1:

### **title:**

Architecture & Granular Task Breakdown

### **model:**

Claude 3.5 Opus (or OpenAI o1)

### **prompt:**

```
Act as a Principal Software Architect. Read the attached `master_spec.md`. Output two things: 1. A strict Technical Architecture document (DB Schema, API endpoints, Component hierarchy). 2. A sequential list of implementation tasks. The tasks must be tiny and isolated (e.g., 'Task 1: Setup Prisma and User Model', 'Task 2: Build Login API'). Output the task list as a strict JSON array of objects: [{\"task_id\": 1, \"title\": \"...\", \"description\": \"...\", \"dependencies\": [...]}]. Do not write any code yet.
```

### **handoffs:**

Technical Architecture Document, JSON Task List.

### **output files:**

`architecture.md`, `tasks.json`

---

## Phase 2:

### **title:**

Test-Driven Implementation (Iterative Loop)

### **model:**

Claude 3.5 Sonnet

### **prompt:**

```
You are an expert developer. We are building a Todo app. Here is the current task from our plan: [Insert Task JSON]. Here is the relevant existing codebase context: [Insert ONLY relevant files]. Step 1: Write comprehensive unit tests for this task using Jest/React Testing Library. Step 2: Write the implementation code to pass the tests. Output the tests and code in separate markdown code blocks with their exact file paths.
```

### **handoffs:**

Unit Tests, Implementation Code.

### **output files:**

`src/__tests__/[feature].test.ts`, `src/[feature].ts`, `prisma/schema.prisma` (updated)

---

## Phase 3:

### **title:**

Cross-Model Code Review & Refactoring

### **model:**

GPT-4o (Reviewer) -> Claude 3.5 Sonnet (Fixer)

### **prompt (Reviewer - GPT-4o):**

```
Act as a strict Staff Engineer. Review the following code for a Todo app feature. Look for security flaws (e.g., XSS, SQLi), performance bottlenecks, and logic errors. Do NOT rewrite the code. Output a JSON array of required fixes: [{\"file\": \"...\", \"line\": \"...\", \"issue\": \"...\", \"suggested_fix\": \"...\"}].
```

### **prompt (Fixer - Sonnet):**

```
A senior engineer reviewed your code and found these issues: [Insert GPT-4o JSON]. Apply these fixes to the code. Ensure all existing unit tests still pass. Output the refactored code.
```

### **handoffs:**

Refactored, reviewed code.

### **output files:**

Updated `src/[feature].ts` files.

---

## Phase 4:

### **title:**

Integration & End-to-End (E2E) Testing

### **model:**

Claude 3.5 Sonnet

### **prompt:**

```
We have successfully implemented the [Task Title] feature. Here are the implementation files and the architecture doc. Write End-to-End tests using Playwright to verify the complete user flow for this feature. Include edge cases like network timeouts or empty states. Output the test file with its exact path.
```

### **handoffs:**

E2E Test Scripts.

### **output files:**

`e2e/[feature].spec.ts`

---

## Phase 5:

### **title:**

Final Polish, Documentation & Cleanup

### **model:**

Claude 3.5 Haiku (or Gemini Flash)

### **prompt:**

```
The Todo app is complete. Review the `architecture.md` and the final codebase. 1. Write a comprehensive `README.md` including: Project overview, Tech stack, Prerequisites, Installation steps, and Environment variables. 2. Write an `API_DOCS.md` detailing all endpoints, request/response bodies, and auth requirements. 3. List any unused imports or dead code you noticed for cleanup.
```

### **handoffs:**

Final Documentation.

### **output files:**

`README.md`, `API_DOCS.md`

# Deepseek

## **Phase 0: Idea to Structured Brief**

### **model:**

Gemini 2.5 Flash

### **prompt:**

```
I want to build a simple, full-stack Todo web application.
The user should be able to create, read, update, delete tasks, mark them as complete,
filter by status (all/active/completed), and see a task count.
No authentication needed. I prefer a modern, minimalist UI.
Please generate a brief PRD covering:
- Core user stories
- Feature list (must-have, nice-to-have)
- Non-functional requirements (performance, accessibility)
- Technology constraints (I’m open to suggestions, but thinking React + Node.js)
- Out of scope items
Keep it concise (under 500 words).
```

### **handoffs:**

The full PRD text is saved as `prd.md`. This file will be fed into Phase 1 as the sole input.

### **output files:**

`prd.md`

---

## **Phase 1: Research & Technology Stack Selection**

### **model:**

Gemini 2.5 Pro (with Google Search grounding enabled)

### **prompt:**

```
Using the following PRD, research and recommend a modern, minimalistic tech stack
for a single-user Todo web app with no authentication.
You have access to live search; verify latest stable versions and community health.

PRD:
---
[contents of prd.md]
---

Provide a tech brief covering:
- Frontend: framework, build tool, UI approach (CSS library or plain), state management
- Backend: runtime, framework, database
- API design style (REST vs GraphQL, justify)
- Project structure suggestion
- Key libraries (e.g., uuid, date-fns)
- Any important compatibility notes
Output as a markdown document with clear sections. Keep it under 800 words.
```

### **handoffs:**

The tech brief is saved as `tech-brief.md`. It will be the sole input to Phase 2, along with the PRD for context.

### **output files:**

`tech-brief.md`

---

## **Phase 2: Detailed Architecture & Implementation Plan**

### **model:**

Claude Opus 4

expensive tokens solely for planning. The output is an actionable blueprint that guides all subsequent coding phases.

### **prompt:**

```
You are a senior full-stack architect. Using the PRD and tech brief below,
create a thorough implementation plan for the Todo app.

PRD:
---
[prd.md content]
---

Tech Brief:
---
[tech-brief.md content]
---

The plan must include:
1. **Data Model** – exact SQLite schema with fields/types/constraints.
2. **REST API Contract** – endpoint list with method, path, request/response shapes.
3. **Frontend Component Tree** – hierarchy and props/state per component.
4. **File/Folder Structure** – every file that needs to be created.
5. **Task Breakdown** – a numbered list of atomic implementation steps, grouped by:
   - Backend setup & database
   - API routes
   - Frontend scaffolding & components
   - Integration & styling
   - Testing
   Each task should be small enough to be completed with a single LLM prompt (no task > ~50 lines of code).
Output as a single markdown file named `plan.md`.
```

### **handoffs:**

The generated `plan.md` becomes the master document. Its task breakdown will be fed one chunk at a time into Phase 3 and Phase 4. The file is preserved for code review.

### **output files:**

`plan.md`

---

## **Phase 3: Backend Implementation**

### **model:**

Claude Sonnet 4 (primary), Gemini 2.5 Flash (for boilerplate/utilities)

### **prompt (example for one task – API route for GET /tasks):**

```
Task from plan.md: "Implement GET /api/tasks endpoint returning all tasks ordered by creation date descending."

Relevant contract from plan:
- Response: { tasks: [{ id, text, completed, createdAt }] }
- Use the database helper from db.js (already created).

Write the Express route handler code. Include error handling. Output only the route function and necessary imports.
```

_For a boilerplate task (e.g., logger):_

```
Task: Create a simple logger utility that writes to console with timestamps.
Use it as a drop-in for console.log. Output the full file.
```

This task is sent to Gemini 2.5 Flash.

### **handoffs:**

Each completed code file is saved into the project folder (`/backend`). The collection of all backend files constitutes the handoff to Phase 5 and sets the stage for frontend integration.

### **output files:**

`server.js`, `db.js`, `routes/tasks.js`, `logger.js`, `package.json`, etc. (all files listed in plan.md backend section)

---

## **Phase 4: Frontend Implementation**

### **model:**

Claude Sonnet 4 (core components, state management), Gemini 2.5 Flash (pure presentational components)

### **prompt (example for App.jsx with state):**

```
Task: Create the main App component. It should fetch tasks from GET /api/tasks on mount,
manage tasks state, and pass callbacks for add, toggle, delete to child components.
Use the provided api.js helper.
Contracts from plan:
- State shape: { tasks: [], filter: 'all' }
- Callbacks: addTask(text), toggleTask(id), deleteTask(id), setFilter(filter)
Output the full App.jsx file.
```

_For a presentational component (TaskItem.jsx) offloaded to Flash:_

```
Task: Create a presentational TaskItem component. Props: task object {id, text, completed},
onToggle(id), onDelete(id). Display checkbox, text (strike through if completed), delete button.
Use Tailwind classes for styling. Output the component file.
```

### **handoffs:**

All frontend files are saved into `/frontend`. The full codebase (backend + frontend) is now ready for review.

### **output files:**

`App.jsx`, `TaskList.jsx`, `TaskItem.jsx`, `AddTaskForm.jsx`, `FilterBar.jsx`, `api.js`, `index.js`, etc.

---

## **Phase 5: Code Review & Test Generation**

### **model:**

Pass 1 – Gemini 2.5 Flash; Pass 2 – OpenAI o3 (or Claude Opus 4)

writes tests based on the review findings.

### **prompt (Pass 1 – lint & style):**

```
Review all the following code files for syntax errors, unused imports, inconsistent formatting,
and missing error handling. List every issue with file and line number.

Files:
[list of all generated file paths and their content]
```

### **prompt (Pass 2 – deep logic & security review):**

```
You are a senior code reviewer. Compare the implementation of these critical files
against the original plan and API contracts from plan.md.
Check for:
- Logical correctness of CRUD operations
- SQL injection vulnerabilities (if any)
- Missing input validation
- Race conditions in task updates
- Adherence to the planned component/data flow
For each issue, explain the risk and suggest a fix.

Critical files:
- db.js
- routes/tasks.js
- App.jsx
- api.js

Original plan:
[include relevant sections from plan.md]
```

### **prompt (Test generation after fixes):**

```
Using the reviewed backend code, write unit tests for the following endpoints
using Jest and Supertest:
- GET /api/tasks (empty and populated)
- POST /api/tasks (valid and missing fields)
- PUT /api/tasks/:id (mark complete)
- DELETE /api/tasks/:id (existing and non-existent)
Also write a simple integration test for the App component using React Testing Library
that verifies task addition and filtering.
Output all test files.
```

_This is handled by Claude Sonnet 4, referencing the reviewed code._

### **handoffs:**

The review reports (`review-lint.md`, `review-deep.md`) are saved. After applying fixes, the final test files (`backend/tests/api.test.js`, `frontend/src/App.test.js`) are output. The project is now complete and validated.

### **output files:**

`review-lint.md`, `review-deep.md`, `backend/tests/api.test.js`, `frontend/src/App.test.js`
