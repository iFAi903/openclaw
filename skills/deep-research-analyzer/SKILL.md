---
name: deep-research-analyzer
description: Deep analysis of research repositories (like Google DeepMind, OpenAI, academic labs). Extract key projects, paper information, technology stacks, and research themes. Use when analyzing GitHub research repos to understand their structure, identify important projects, summarize research areas, and provide actionable insights for further exploration.
---

# Deep Research Analyzer

Analyze research organization GitHub repositories to extract structured insights about their projects, papers, and research directions.

## When to Use This Skill

Use this skill when:
- Analyzing a research lab's GitHub repository (DeepMind, OpenAI, FAIR, etc.)
- Need to understand what projects exist and their significance
- Want to identify key papers and their implementations
- Looking for specific technology domains or research themes
- Preparing a summary of research capabilities or opportunities

## Quick Start

### Step 1: Fetch Repository Information

```bash
# Get README to understand repository structure
web_fetch https://raw.githubusercontent.com/[org]/[repo]/master/README.md

# List directories/projects (if accessible)
web_fetch https://api.github.com/repos/[org]/[repo]/contents
```

### Step 2: Analyze Project Structure

Look for:
- **Project directories** - Each folder typically = one research project
- **Paper citations** - Nature, Science, NeurIPS, ICML, etc.
- **Technology keywords** - RL, GAN, Transformer, Graph Networks, etc.
- **Datasets/Environments** - Open-sourced data or simulation environments

### Step 3: Extract Key Information

For each significant project, extract:
- Project name
- Associated paper (title, venue, year)
- One-line description
- Technology/domain tags
- Link to code/paper

## Analysis Framework

### Research Theme Categories

Categorize projects into themes:

| Category | Keywords | Examples |
|----------|----------|----------|
| **Reinforcement Learning** | RL, DQN, policy, agent, environment | DQN, RL Unplugged, Option Keyboard |
| **Generative Models** | GAN, VAE, generative, synthesis | BigBiGAN, PolyGen, ODE-GAN |
| **Graph/Geometric** | graph, mesh, network, geometric | MeshGraphNets, Graph Matching Networks |
| **Computer Vision** | vision, image, video, attention | Transporter, IODINE, MMV |
| **NLP/Language** | language, text, transformer, BERT | Enformer, ScratchGAN |
| **Scientific/Physics** | physics, simulation, molecular | Learning to Simulate, FermiNet |
| **Robotics** | robot, control, manipulation, grasp | Catch & Carry, Sketchy |
| **Multimodal** | multimodal, cross-modal, audio | MMV, CMTouch |

### Output Format

```markdown
# [Organization] Research Repository Analysis

## Overview
- **Repository**: [org]/[repo]
- **Total Projects**: XX
- **Primary Domains**: [list top 3-5]
- **Latest Activity**: [year range]

## Top Projects by Impact

### 🔬 [Project Name]
- **Paper**: [Title], [Venue] [Year]
- **Description**: [One sentence]
- **Tags**: [technology domains]
- **Links**: [code] | [paper]

## Research Themes

### [Theme 1]
- [Project list with brief descriptions]

### [Theme 2]
- [Project list with brief descriptions]

## Technology Stack Insights

Most common technologies/frameworks used:
- [Framework 1]: [usage count/context]
- [Framework 2]: [usage count/context]

## Recommendations

**For Further Exploration**:
1. [Specific project to investigate]
2. [Related paper to read]
3. [Code to experiment with]

**Research Gaps/Opportunities**:
- [Potential area not covered]
```

## DeepMind Research Example

**Repository**: `google-deepmind/deepmind-research`

**Key Projects**:
- **AlphaFold CASP13** - Protein structure prediction (Nature 2020)
- **BYOL** - Self-supervised learning without negative samples
- **MeshGraphNets** - Learning mesh-based physics simulation (ICLR 2021)
- **Perceiver** - General architecture for arbitrary inputs/outputs
- **Enformer** - Gene expression prediction from DNA sequence

**Research Themes**:
1. **Scientific Discovery** - AlphaFold, FermiNet, fusion control
2. **Physics Simulation** - MeshGraphNets, Learning to Simulate
3. **Self-Supervised Learning** - BYOL, MMV, BigBiGAN
4. **Reinforcement Learning** - RL Unplugged, Option Keyboard, Tandem DQN
5. **Generative Models** - PolyGen, ODE-GAN, ScratchGAN

## Tools & Techniques

### Web Fetching
```bash
# Repository README
web_fetch https://raw.githubusercontent.com/[org]/[repo]/main/README.md

# GitHub API for contents
web_fetch https://api.github.com/repos/[org]/[repo]/git/trees/main?recursive=1

# Specific project README
web_fetch https://raw.githubusercontent.com/[org]/[repo]/main/[project]/README.md
```

### Pattern Recognition

Look for these patterns in README/projects:
- **Venue tags**: Nature, Science, NeurIPS, ICML, ICLR, AAAI, CVPR
- **Year range**: 2018-2024 indicates active research
- **Citation formats**: [Paper Title], [Venue] [Year]
- **Code keywords**: PyTorch, TensorFlow, JAX, Python, C++

## Best Practices

1. **Start with README** - Always fetch the main README first
2. **Identify top-tier papers** - Nature/Science/NeurIPS/ICML = high impact
3. **Group by theme** - Don't just list alphabetically
4. **Highlight code+paper pairs** - Research repos = implementations
5. **Note technology trends** - What frameworks dominate?
6. **Suggest next steps** - Which project to explore deeper?

## Common Research Organizations

| Organization | Repository Pattern | Focus Areas |
|--------------|-------------------|-------------|
| DeepMind | `google-deepmind/*` | RL, Science, Generative Models |
| OpenAI | `openai/*` | LLMs, Robotics, Safety |
| FAIR/Meta | `facebookresearch/*` | Vision, NLP, Multimodal |
| Google Research | `google-research/*` | Broad ML, Systems |
| Microsoft Research | `microsoft/*` | Systems, NLP, Vision |
| Berkeley AI | ` BerkeleyAutomation/*` | Robotics, Control |
| Stanford | `stanfordmlgroup/*` | Healthcare, Vision |

## Example Workflow

**User**: "分析这个仓库 https://github.com/google-deepmind/deepmind-research"

**Steps**:
1. Fetch README.md
2. Extract project list with paper citations
3. Categorize by research theme
4. Identify high-impact papers (Nature/Science/NeurIPS)
5. Summarize technology trends
6. Provide recommendations for exploration

**Output**: Structured analysis with project summaries, theme breakdown, and actionable next steps.
