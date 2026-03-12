# Vibe Coding Frameworks Router

> **Skill**: Vibe Coding Frameworks Selector & Executor
> **Description**: A skill designed to help AI agents select and utilize the most appropriate Vibe Coding framework (BMad, Spec-kit, or OpenSpec) based on project complexity, team structure, and development goals.

## Supported Frameworks

### 1. BMad (Breakthrough Method for Agile Ai Driven Development)
- **Origin**: `bmad-code-org/bmad-method`
- **Core Philosophy**: True scale-adaptive intelligence. Acts as expert collaborators guiding structured processes across analysis, planning, architecture, and implementation.
- **Key Features**: 
  - Specialized Agents (PM, Architect, Developer, UX, Scrum Master)
  - Scale-Domain-Adaptive planning depth
  - Extensive module ecosystem (Test Architect, Game Dev Studio, Creative Intelligence Suite)
  - `bmad-help` skill for contextual guidance
- **Installation**: `npx bmad-method install`
- **When to Use**: 
  - Enterprise systems or highly complex projects
  - Projects requiring comprehensive agile workflows
  - When you need multiple agent personas collaborating ("Party Mode")
  - Complete lifecycle development from brainstorming to deployment

### 2. Spec-kit
- **Origin**: `github/spec-kit`
- **Core Philosophy**: Spec-Driven Development. Specifications become executable, directly generating working implementations rather than just guiding them. Focuses on predictable outcomes.
- **Key Features**: 
  - 6-step structured process: Constitution -> Spec -> Review -> Implement -> Test -> Commit
  - Feature isolation using Git branch context awareness
  - Library-first approach driven by slash commands (e.g., `/speckit.constitution`)
- **Installation**: `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git` then `specify init . --ai claude`
- **When to Use**:
  - Open source projects and standardized new feature development
  - Projects demanding strict code specifications and predictable outcomes
  - TDD-focused environments ("Spec first, code later")

### 3. OpenSpec
- **Origin**: `Fission-AI/OpenSpec`
- **Core Philosophy**: Fluid, iterative workflow. Artifact-guided development that is scalable from personal projects to enterprise levels. Built for both greenfield and brownfield projects.
- **Key Features**:
  - Non-linear OPSX workflow using slash commands (`/opsx:propose`, `/opsx:apply`, `/opsx:archive`)
  - Highly customizable instructions via `schema.yaml` and editable templates
  - Instant effect on prompt changes without waiting for framework updates
- **Installation**: `npm install -g @fission-ai/openspec@latest` then `openspec init`
- **When to Use**:
  - Existing projects requiring rapid iteration (brownfield)
  - Teams/individuals needing highly customized AI workflows and prompts
  - Fluid feature development where requirements often change mid-implementation

## Usage Guide (For the AI Agent)

When a user asks to start a new project or feature using a Vibe Coding framework:

1. **Assess the Request**:
   - Ask clarifying questions about project complexity, greenfield vs. brownfield status, and preferred workflow rigidity.
2. **Recommend a Framework**:
   - Suggest the best-fit framework from the three options above, explaining *why* it fits their specific scenario.
3. **Initialize the Environment**:
   - Execute the corresponding installation command in the user's workspace.
4. **Follow the Framework's Workflow**:
   - **BMad**: Ask the user to run their AI IDE in the folder, or utilize `bmad-help` to begin the first agile phase.
   - **Spec-kit**: Guide the user to define the `/speckit.constitution` and create the initial specification document.
   - **OpenSpec**: Prompt the user with `/opsx:propose "your idea"` to generate the initial proposals and specs, then proceed to `/opsx:apply`.

## Tool Access Required
- `exec` (for installing CLI tools and initializing projects)
- `write` (for generating configuration files or specifications when needed)