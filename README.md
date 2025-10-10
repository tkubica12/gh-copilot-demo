# GitHub Copilot Demo
This repository contains example code to demonstrate GitHub Copilot features across the development lifecycle - from basic coding assistance to advanced agentic workflows. It is designed for demonstrations and learning, not for production use.

## Table of Contents
1. [Copilot as Coding Assistant](#1-copilot-as-coding-assistant)
2. [Agent Mode](#2-agent-mode)
3. [Customize and Provide Rich Context](#3-customize-and-provide-rich-context)
4. [Model Context Protocol (MCP) Tools](#4-model-context-protocol-mcp-tools)
5. [Copilot Coding Agent](#5-copilot-coding-agent)
6. [Code Review, Security, and Autofix](#6-code-review-security-and-autofix)
7. [GitHub Spark](#7-github-spark)
8. [Azure SRE Agent](#8-azure-sre-agent)
9. [Model Selection Strategies](#9-model-selection-strategies)

---

# 1. Copilot as Coding Assistant

Learn the fundamentals of GitHub Copilot - inline suggestions, chat interactions, and quick code generation tasks.

## 1.1 Inline Code Suggestions

### Autocomplete
Open `main.py` in `api-processing` and type `# Configure Prometheus` and wait for suggestions. Use TAB to accept, ESC to reject or CTRL+arrow to accept partially.

### Next Edit Suggestion
Open `main.py` in `api-processing` and around line 52 change `credential` to `azure_credential` and wait for suggestions. Copilot will predict your next likely edit.

## 1.2 Chat: Ask and Edit Modes

### Model selection
- Auto - let Copilot decide what model to use, if it selects premium model than 1x gets discounted to 0.9x
- Base models do not consume premium requests (0x)
  - Use it for simple text tasks and searches. 
  - As of October 2025 I prefer gpt-5-mini
- Premium models consume premium requests, most often one per request (1x)
  - 10x models in my opinion are usual not worth the increased cost
  - Switch model when Copilot is not able to move beyond some issue or after previous one finished so you get second opinion
  - As of October 2025 I combine gpt-5-codex and sonnet 4.5 for coding and gpt-5 or Gemini 2.5 Pro for document writing and brainstorming

### Codebase Search
Ask Copilot to search and understand your code:
```
Where in my code am I processing messages from Service Bus queues and what is the code doing?
```

Experiment with different models selection.

### Documentation Generation
Create README.md and add all Terraform files to context. Then ask:

- `Create basic Markdown documentation into README.md for my Terraform project. Start by describing this project as demo Terraform infrastructure, explain how to deploy it using Terraform CLI and list tree structure of tf files in the project with short description of each file into my README.md.`
- `Create list of cloud resources used in this project.`
- `Research what container apps are and add short description of this service into existing section with list of cloud resources used in this project. #websearch`
- `Research what Service Bus is and add short description of this service into existing section with list of cloud resources used in this project. #websearch`
- `Create chapter listing environment variables used with each container app and put it into nice table.`
- `Add chapter TODO to end of document and describe next steps for this Terraform project. Make sure to include CI/CD using GitHub Actions, Infrastructure as Code security using DevSecOps tools, adding FinOps and other topics that are important for enterprise usage of this project as you see fit.`

## 1.3 Query Languages (KQL and SQL)

### KQL (Kusto Query Language)
Attach [query_data.csv](./kql/query_data.csv) and ask:
```
Give me microsoft Kusto Query (KQL) to display percentage of processor time grouped by instance and process id which is part of properties. Name of table is AppPerformanceCounters. Attached are example data.
```

### SQL
Attach [users_denormalized.json](./sql/users_denormalized.json) and ask:
- `Generate CREATE commands for normalized users, addresses and orders using Microsoft SQL.`
- `Based on data structure, create 10 lines of sample data and make sure it makes sense and foreign keys are respected.`
- `Give me SQL statement to list userId, name, number of orders and number of addresses for each user.`

## 1.4 Vision (Image to Code)

Attach [classes.png](./vision/classes.png), create `classes.py` and ask:
```
Generate code for classes in Python according to attached schema.
```

Create README.md file and in Edit mode follow with:
```
Create markdown documentation for classes.py and include mermaid diagram.
```

## 1.5 Web Search and Fetch

Ask questions about current information:

Try without tools using just model knowledge.
```
When did Microsoft released Microsoft Agent Framework SDK for Python and what is current version? Do NOT use any tools.
```

I have Tavily MCP Server (see in later section) so try with tools.
```
When did Microsoft released Microsoft Agent Framework SDK for Python and what is current version?
```

But if you have specific documentation in mind, you can just reference it here (eg. llms.txt)
```
When did Microsoft released Microsoft Agent Framework SDK for Python and what is current version?
#fetch 
https://github.com/microsoft/agent-framework/releases
https://learn.microsoft.com/en-us/agent-framework/overview/agent-framework-overview
https://github.com/microsoft/agent-framework
```

## 1.6 Simple Multi-File Editing
Let's do change that requires modification of various files. When you want to help Copilot to pin specific files, you can add them to explicit context. Add `api-processing/main.py`, `worker/main.py` and terraform files such as `terraform/service_bus.tf` and `terraform/rbac.tf` to context.

Ask:
```
In this code I am using Service Bus Queues, but I need to move to Service Bus Topics. Make sure to update my Terraform and Python code accordingly and add topic subscriptions and RBAC.
```

## 1.7 Context from Git
You can see your Git history and add previous versions of files into Copilot chat for reference. Useful when asking for what changed or helping Copilot undo something.

---

# 2. Agent Mode

Agent Mode enables Copilot to work autonomously across multiple files, run tests, deploy infrastructure, and iteratively solve complex problems. This section demonstrates progressive complexity and best practices for agentic workflows.

## 2.1 Development Workflow Best Practices

Before starting complex tasks with Agent Mode, establish a solid foundation:

### Solution Design and Planning
Start with high-level design documents:
- Create `SolutionDesign.md` outlining architecture, components, and integration points
- Define Product Requirements Document (PRD) for features
- Break down work into discrete, testable tasks

### Documentation-Driven Development
Maintain living documentation in `docs/`:
- **`ImplementationLog.md`**: Track progress, technical decisions, and architectural choices as you implement
- **`ImplementationPlan.md`**: Create step-by-step plan before major changes
- **`CommonErrors.md`**: Document issues encountered and their solutions for future reference

💡 **Pro tip**: Ask the agent to update these documents as it works, creating a traceable development history.

## 2.2 Simple Multi-File Task

Take files from `frontend` and using agent mode ask:
```
Enable dark mode for my frontend. User will have button to switch between light and dark mode. Implement necessary changes in the code and CSS.
```

Then iterate:
```
Now add other modes and make UI to switch them easier. Colorful, contrast, green and MS DOS.
```

## 2.3 Complex Task with Testing

```markdown
Create new service called api-user-profile that provides API for CRUD over user profiles.

# Solution Architecture
- Python with uv as package manager
- PostgreSQL database deployed in Azure Database for PostgreSQL Flexible Server in cheap burstable tier
- Implemented in FastAPI
- No authentication required at this point
- Unit tests for APIs
- Integration tests against real endpoints and databases - testing Create, then update, then read, then delete
- User profile contain following fields: userId, userFullName, department

# Implementation steps
- Create base folder and uv init
- Create mocked CRUD APIs and write and run unit tests for it
- Use Azure CLI to create resource group and Azure Database for PostgreSQL Flexible Server
- Get access details and credentials for database and store it in .env
- Add code to connect to database and write and run integration tests to make sure DB is accessible
- Write code that will check whether schema exists and if not create it with simple table for user profiles
- Change CRUD implementation from mocks to real database
- Write and run integration test against real endpoints
- Write comprehensive README.md with architecture and how to use
```

## 2.4 Infrastructure with Intentional Challenges

Simulate real-world scenarios where things don't work on first try:

```
Deploy a PostgreSQL database in Azure and configure our api-processing to connect to it. Store connection strings securely in Key Vault and configure proper RBAC. The database should be accessible only from our Container Apps.

Note: Intentionally misconfigure the firewall rules or connection string format to simulate a real troubleshooting scenario.
```

The agent should:
1. Create Terraform resources
2. Attempt connection
3. Diagnose connectivity issues
4. Fix firewall rules/network configuration
5. Verify connectivity
6. Document the solution

## 2.5 Complex Security Integration

```
To enhance security frontend should integrate with Entra ID using OpenID Connect to get user identity and make sure it is part of MyDemo security group. Our APIs api-processing and api-status, that interact directly with frontend, should be registered as APIs in Entra and user should consent to access to those.

Implement those changes in code, write comprehensive README explaining how authentication and authorization works in our application and prepare scripts to configure Entra ID according to our requirements. Where keys need to be used make sure to use environmental variables and .env capability. Do not forget to modify our Terraform deployment manifests to include newly introduced envs.
```

## 2.6 Agent Mode Strategies

**When to use Agent Mode:**
- Multi-file refactoring
- Feature implementation across frontend/backend/infrastructure
- Test-driven development workflows
- Debugging complex issues

**Tips for success:**
- Provide clear context and constraints
- Reference existing patterns in codebase
- Ask agent to update documentation as it works
- Use `#codebase` to help agent understand project structure
- Review changes before accepting

---

# 3. Customize and Provide Rich Context

Tailor Copilot's behavior to your team's standards, coding conventions, and operational practices.

## 3.1 Repository-Wide Instructions

Instructions in `.github/instructions/` apply automatically based on file patterns:

- **`general.instructions.md`** (applies to `**`): Project-wide standards
- **`python.instructions.md`** (applies to `**/*.py`): Python-specific conventions
- **`terraform.instructions.md`** (applies to `**/*.tf`, `**/*.tfvars`): IaC standards

### Example: Coding Convention
Ask in chat:
```
Generate CRUD in Python for product API
```

You'll get functions using standard Python convention (snake_case).

## 3.2 Prompt Files

Clear chat and attach prompt file `camelcase.prompt` and ask again. You'll get different response following camelCase convention.

Prompt files override default behavior for specific contexts.

## 3.3 Custom Chat Modes

Switch to **MyTeacher** chat mode and ask:
```
Should I migrate to https://gateway-api.sigs.k8s.io/ ?
```

Or put some file into context and ask:
```
What is this file about?
```

Custom chat modes provide specialized personas for teaching, reviewing, or domain-specific guidance.

## 3.4 Azure Extensions

Copilot can integrate with Azure services:
```
@azure /costs What can you tell me about storage costs in my subscription 673af34d-6b28-41dc-bc7b-f507418045e6
```

## 3.5 Bring Your Own Model (BYOM)

Install `Ollama` and download models:

```powershell
ollama pull deepseek-coder:1.3b
ollama pull deepseek-coder:6.7b
ollama pull qwen2.5-coder
```

In Copilot click on **Manage Models** and add Ollama models. Try examples from Section 1 with different models.

**Use cases:**
- Privacy-sensitive code on local models
- Cost optimization with smaller models
- Experimentation with specialized models

## 3.6 Multi-Repository Planning with Copilot Spaces

[Copilot Spaces](https://www.github.com/copilot/spaces) enables strategic planning across multiple repositories:

- Architecture discussions spanning microservices
- Cross-repo refactoring planning
- Enterprise-wide technical decisions
- Design reviews involving multiple teams

**📝 TODO:** Create example Copilot Space configuration for this demo project

---

# 4. Model Context Protocol (MCP) Tools

MCP enables Copilot to interact with external tools and services, dramatically extending its capabilities beyond code generation.

## 4.1 Simple MCP: Random String Generator

Run MCP server in folder `mcp/random_string_mcp/src/`. This runs locally and is configured in `mcp.json` file on workspace.

Use this prompt in Agent mode:
```
Generate names for 10 containers in format app1-xxxxxx where xxxxxx is random suffix consisting of lowercase letters and numbers
```

## 4.2 Kubernetes MCP

Install AKS and Kubernetes apps using [this guide](./mcp/README.md). Then try this conversation flow:

```
What namespaces I have in my Kubernetes cluster? [enter][end]
Show me pods in blue namespace [enter][end]
I have some error with app1, can you kill one of the pods? [enter][end]
Check logs from new pod that was created afterwards, does it start normally? [enter][end]
Hmm, do we have enough resources in app1 allocated? [enter][end]
How would I do that, show me [enter][end]
If I would like to do the steps you did in this chat using Kubernetes CLI next time, how it would look like? [enter][end]
```

🎥 See [recording](./video/MCP-Kubernetes.mp4) of this demo.

## 4.3 Azure MCP

**📝 TODO:** Add Azure MCP demos:
- Query Azure resources (storage accounts, VMs, App Services)
- Analyze costs and resource utilization
- Diagnose issues with Azure Monitor
- Manage Azure resources directly from Copilot

Example prompts to prepare:
```
What resources do I have in resource group rg-demo?
Show me the cost breakdown for the last 30 days
Are there any alerts firing in my subscription?
```

## 4.4 Tavily Search and Azure Docs MCP

**📝 TODO:** Add search capabilities:
- Tavily for web search
- Azure documentation search
- Code sample search from Microsoft Learn

Example prompts:
```
Search for best practices on Azure Container Apps scaling
Find code examples for Azure Service Bus with managed identity
```

## 4.5 Database MCP

**📝 TODO:** Add database interaction demos:
- Query Cosmos DB
- Execute SQL queries against Azure SQL
- Schema inspection and optimization suggestions

## 4.6 Playwright MCP for Testing

**📝 TODO:** Add browser automation:
- Generate E2E tests
- Run Playwright tests from Copilot
- Debug test failures with screenshots

## 4.7 GitHub MCP

**📝 TODO:** Add GitHub operations:
- Query issues and PRs
- Analyze repository insights
- Automate workflow operations

---

# 5. Copilot Coding Agent

Delegate long-running tasks to Copilot Coding Agent that works asynchronously in the background, committing changes to a branch and opening PRs.

## 5.1 From GitHub Issues

1. Go to **Issues** in your repository
2. Create or select an issue
3. Assign it to **Copilot Coding Agent**
4. Agent will create a branch, implement changes, and open a PR

## 5.2 From Copilot Agents Page

Work from [Copilot Agents page](https://github.com/copilot/agents) to manage multiple agent tasks across repositories.

## 5.3 Example Delegated Tasks

Use "delegate to copilot agent" button with these prompts:

### Add Unit Tests and CI Integration
```
My worker, unlike other microservices, does not have any unit tests. Write unit tests using pytest and create README explaining those tests and how to run them. There is GitHub Actions workflow to build worker when code changes. Add tests to the workflow so we do not build container if tests are failing.
```

### Documentation Task
```
I have k6 perftest, but no README for it. Create README.md file explaining how to run the perftest, what scenarios it covers, and how to interpret results.
```

### Feature Implementation
```
Add health check endpoints to all microservices (api-processing, api-status, worker). Implement /health and /ready endpoints following Kubernetes probe best practices. Update Kubernetes manifests with proper liveness and readiness probes.
```

## 5.4 When to Use Coding Agent vs Agent Mode

| Use Coding Agent When | Use Agent Mode When |
|----------------------|---------------------|
| Task can be completed independently | You need interactive feedback |
| You want PR-based review workflow | Making rapid iterations |
| Working on multiple tasks in parallel | Learning or exploring code |
| Task is well-defined with clear acceptance criteria | Requirements need clarification |

---

# 6. Code Review, Security, and Autofix

## 6.1 Code Review with Copilot

After making changes:
1. Create a new branch
2. Copilot can suggest **commit messages** based on your changes
3. Open a **Pull Request**
4. Use Copilot to review the PR:
   - Suggest improvements
   - Identify potential bugs
   - Check for best practices
   - Assess security implications

## 6.2 Security Vulnerability Detection

In GitHub:
1. Navigate to **Security** tab
2. View **Dependabot alerts** and **Code scanning alerts**
3. Review detected vulnerabilities

## 6.3 Automated Security Fixes

Demonstrate **Autofix** capability:
1. Copilot analyzes the vulnerability
2. Suggests a fix with explanation
3. Creates a PR with the remediation
4. Includes testing recommendations

**📝 TODO:** Create example scenarios:
- SQL injection vulnerability
- Dependency with known CVE
- Secrets in code
- Insecure cryptography

---

# 7. GitHub Spark

No-code/low-code prototyping with natural language. Build functional applications without writing code manually.

[GitHub Spark](https://github.com/spark)

## 7.1 Example: Kubernetes YAML Editor

```
Create text editor that specializes on creating Kubernetes YAML manifests. Here is how I want it:
- Keyboard shortcuts similar to Visual Studio Code
- Syntax highlighting for YAML and for Kubernetes objects, for example known values should have distinctive colors. kind: Pod should look differently from kind: SomethingElse because SomethingElse is not known Kubernetes kind.
- Editor should suggest completions for Kubernetes objects and fields directly as you type inside text editor together with little bubbles explaining each field - its purpose, possible values
- Navigation that lets user quickly build skeleton of most common Kubernetes objects and some drag and drop features for values inside those objects (for example health check, resource limits etc.)
- AI chatbot that allows to talk about currently open file
- Suggestions based on common practice, for example recommend to set resource requests and limits for Pods and Deployments. This should be icon showing number of new suggestions and when user clicks on it they can acknowledge those. Generate suggestions using AI in background as user is adding objects to the solution.
- IMPORTANT: Retro style and graphical design must simulate ASCII-based user interfaces for DOS similar to how FoxPro applications looked like.
```

## 7.2 Additional Spark Examples

**📝 TODO:** Add more Spark examples:
- Cloud cost calculator
- Infrastructure diagram generator
- API testing tool
- Log analyzer

---

# 8. Azure SRE Agent

[Azure SRE Agent](https://learn.microsoft.com/en-us/azure/sre-agent/overview) is an AI-powered reliability assistant that demonstrates how AI agents extend into production operations and incident management.

## 8.1 What is Azure SRE Agent?

Azure SRE Agent helps teams:
- **Diagnose and resolve** production issues autonomously or with human approval
- **Reduce MTTR** (Mean Time To Resolution) through intelligent automation
- **Proactive monitoring** with daily health summaries and anomaly detection
- **Explainable RCA** (Root Cause Analysis) correlating metrics, logs, traces, and deployments

## 8.2 Key Capabilities

- **Incident Automation**: Diagnose and orchestrate workflows across Azure Monitor, PagerDuty, ServiceNow
- **Natural Language Insights**: Ask questions like "What changed in production in the last 24 hours?"
- **Customizable Workflows**: Follow your team's SRE best practices and runbooks
- **Dev Integration**: Automatically create work items in GitHub/Azure DevOps with repro steps

## 8.3 Example Interactions

```
What's the CPU and memory utilization of my app?
Which resources are unhealthy?
What changed in my web app last week?
What alerts are active now?
```

## 8.4 Demo Setup

**📝 TODO:** Create demo scenario:
1. Deploy Azure SRE Agent in your subscription
2. Configure it to monitor demo resource groups
3. Simulate an incident (high CPU, failed requests)
4. Show agent detecting, diagnosing, and suggesting remediation
5. Demonstrate creating GitHub issue with RCA

## 8.5 Integration with This Demo

SRE Agent can monitor:
- Container Apps (`api-processing`, `api-status`, `frontend`, `worker`)
- Service Bus queues and dead-letter queues
- Cosmos DB performance
- Application Insights telemetry

**Learn more**: [Azure SRE Agent Documentation](https://learn.microsoft.com/en-us/azure/sre-agent/overview)

---

# 9. Model Selection Strategies

Choosing the right AI model for different tasks optimizes quality, speed, and cost.

## 9.1 Available Models in Copilot

- **GPT-4o**: Most capable, best for complex reasoning and multi-step tasks
- **GPT-4o-mini**: Faster, cost-effective for simpler tasks
- **Claude 3.5 Sonnet**: Excellent for code generation and refactoring
- **o1-preview/o1-mini**: Advanced reasoning for complex problem-solving
- **Local models** (via Ollama): Privacy-focused, offline capability

## 9.2 When to Use Which Model

| Task Type | Recommended Model | Why |
|-----------|------------------|-----|
| Simple code completion | GPT-4o-mini, local models | Fast responses, adequate for autocomplete |
| Complex refactoring | GPT-4o, Claude 3.5 Sonnet | Better understanding of context |
| Architecture decisions | o1-preview, GPT-4o | Advanced reasoning required |
| Documentation | GPT-4o-mini, Claude 3.5 Sonnet | Good quality, cost-effective |
| Security-sensitive code | Local models (Ollama) | Data stays on your machine |
| Debugging complex issues | GPT-4o, o1-preview | Deep analysis needed |

## 9.3 Dynamic Model Switching Strategies

### During Development
Start with **faster models** for iteration:
1. Use **GPT-4o-mini** for rapid prototyping
2. Switch to **GPT-4o** when hitting complexity limits
3. Use **local models** for sensitive code sections

### During Code Review
Use **more powerful models** for thorough analysis:
1. Switch to **GPT-4o** or **Claude 3.5 Sonnet** for PR reviews
2. Use **o1-preview** for security and architecture reviews
3. Leverage advanced reasoning for critical changes

### Cost Optimization Strategy
```
Simple tasks → mini/local models
↓ (if results inadequate)
Standard tasks → GPT-4o-mini, Claude 3.5 Sonnet
↓ (if complex reasoning needed)
Complex tasks → GPT-4o, o1-preview
```

## 9.4 Experimentation Guide

Try the same prompt with different models:

**Prompt**: `Refactor the Service Bus message processing to use topics instead of queues, update Terraform accordingly`

Compare results from:
- GPT-4o-mini (speed)
- GPT-4o (comprehensiveness)
- Claude 3.5 Sonnet (code quality)
- Local Deepseek (privacy)

Document which models work best for your team's common scenarios.

## 9.5 Model Selection Best Practices

1. **Start broad, narrow down**: Begin with capable models, optimize later
2. **Context matters**: Larger context windows (GPT-4o, Claude) for large codebases
3. **Iterate with feedback**: Note which models give best results for your patterns
4. **Privacy first**: Use local models for proprietary algorithms or sensitive data
5. **Cost vs Quality**: Balance project constraints with quality requirements

---

## TODO / Upcoming Features

- [ ] Add file from commit examples
- [ ] MCP marketplace integration guide
- [ ] AGENTS.md configuration examples
- [ ] Complete Playwright MCP demo
- [ ] Complete Database MCP demo
- [ ] Complete Azure MCP comprehensive examples
- [ ] Complete GitHub MCP demo
- [ ] Complete Tavily and Azure docs MCP demo
- [ ] Create Copilot Space example for multi-repo scenario
- [ ] Security vulnerability autofix scenarios
- [ ] More GitHub Spark examples
- [ ] Azure SRE Agent full demo setup
- [ ] Model performance comparison matrix
