<!-- omit from toc -->
# GitHub Copilot Demo
This repository contains example code to demonstrate GitHub Copilot features across the development lifecycle - from basic coding assistance to advanced agentic workflows. It is designed for demonstrations and learning, not for production use.

## Table of Contents
- [1. Copilot as Coding Assistant](#1-copilot-as-coding-assistant)
  - [1.1 Inline Code Suggestions](#11-inline-code-suggestions)
  - [1.2 Chat: Ask and Edit Modes](#12-chat-ask-and-edit-modes)
  - [1.3 Query Languages (KQL and SQL)](#13-query-languages-kql-and-sql)
  - [1.4 Vision (Image to Code)](#14-vision-image-to-code)
  - [1.5 Web Search and Fetch](#15-web-search-and-fetch)
  - [1.6 Simple Multi-File Editing](#16-simple-multi-file-editing)
  - [1.7 Context from Git](#17-context-from-git)
- [2. Agent Mode](#2-agent-mode)
  - [2.1 Development Workflow Best Practices](#21-development-workflow-best-practices)
  - [2.2 Simple Multi-File Task](#22-simple-multi-file-task)
  - [2.3 Complex Task with Testing](#23-complex-task-with-testing)
- [3. Customize and Provide Rich Context](#3-customize-and-provide-rich-context)
  - [3.1 Custom instructions](#31-custom-instructions)
  - [3.2 Prompt Files](#32-prompt-files)
  - [3.3 Custom Chat Modes](#33-custom-chat-modes)
  - [3.4 Bring Your Own Model (BYOM)](#34-bring-your-own-model-byom)
  - [3.5 Multi-Repository Planning with Copilot Spaces](#35-multi-repository-planning-with-copilot-spaces)
- [4. Model Context Protocol (MCP) Tools](#4-model-context-protocol-mcp-tools)
  - [4.1 Simple MCP: Random String Generator](#41-simple-mcp-random-string-generator)
  - [4.2 Kubernetes MCP](#42-kubernetes-mcp)
  - [4.3 GitHub MCP](#43-github-mcp)
  - [4.4 Azure MCP](#44-azure-mcp)
  - [4.5 Database MCP](#45-database-mcp)
  - [4.6 Playwright MCP for Testing](#46-playwright-mcp-for-testing)
- [5. Copilot Coding Agent](#5-copilot-coding-agent)
  - [5.1 Example Delegated Tasks](#51-example-delegated-tasks)
  - [5.2 From GitHub Issues](#52-from-github-issues)
  - [5.3 When to Use Coding Agent vs Agent Mode](#53-when-to-use-coding-agent-vs-agent-mode)
- [6. Code Review, Security, and Autofix](#6-code-review-security-and-autofix)
  - [6.1 Code Review with Copilot](#61-code-review-with-copilot)
  - [6.2 Security Vulnerability Detection](#62-security-vulnerability-detection)
  - [6.3 Automated Security Fixes](#63-automated-security-fixes)
- [7. GitHub Spark](#7-github-spark)
- [8. Azure SRE Agent](#8-azure-sre-agent)
  - [8.1 What is Azure SRE Agent?](#81-what-is-azure-sre-agent)
  - [8.2 Key Capabilities](#82-key-capabilities)
- [TODO](#todo)

---

# 1. Copilot as Coding Assistant

Learn the fundamentals of GitHub Copilot - inline suggestions, chat interactions, and quick code generation tasks.

## 1.1 Inline Code Suggestions

### Autocomplete
Open `main.py` in `src/api-processing` and type `# Configure Prometheus` and wait for suggestions. Use TAB to accept, ESC to reject or CTRL+arrow to accept partially.

### Next Edit Suggestion
Open `main.py` in `src/api-processing` and around line 52 change `credential` to `azure_credential` and wait for suggestions. Copilot will predict your next likely edit.

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

**Note**: GitHub Copilot automatically indexes repositories for semantic search to improve context accuracy. For more information, see [Repository indexing](https://docs.github.com/en/copilot/concepts/context/repository-indexing). You can also configure content exclusion to prevent Copilot from accessing sensitive files - see [Excluding content from GitHub Copilot](https://docs.github.com/en/copilot/how-tos/configure-content-exclusion/exclude-content-from-copilot).

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
Attach [query_data.csv](./demo/kql/query_data.csv) and ask:
```
Give me microsoft Kusto Query (KQL) to display percentage of processor time grouped by instance and process id which is part of properties. Name of table is AppPerformanceCounters. Attached are example data.
```

### SQL
Attach [users_denormalized.json](./demo/sql/users_denormalized.json) and ask:
- `Generate CREATE commands for normalized users, addresses and orders using Microsoft SQL.`
- `Based on data structure, create 10 lines of sample data and make sure it makes sense and foreign keys are respected.`
- `Give me SQL statement to list userId, name, number of orders and number of addresses for each user.`

## 1.4 Vision (Image to Code)

Attach [classes.png](./demo/vision/classes.png), create `classes.py` and ask:
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
Let's do change that requires modification of various files. When you want to help Copilot to pin specific files, you can add them to explicit context. Add `src/api-processing/main.py`, `src/worker/main.py` and terraform files such as `deploy/terraform/service_bus.tf` and `deploy/terraform/rbac.tf` to context.

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

Take files from `src/frontend` and using agent mode ask:
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
- Integration tests against real database - testing Create, then update, then read, then delete
- User profile contain following fields: userId, userFullName, department

# Implementation steps
- Create base folder in src/api-user-profile and uv init
- Create mocked CRUD APIs and write and run unit tests for it
- Use Azure CLI to create resource group and Azure Database for PostgreSQL Flexible Server
- Get access details and credentials for database and store it in .env
- Add code to connect to database and write and run integration tests to make sure DB is accessible
- Write code that will check whether schema exists and if not create it with simple table for user profiles
- Change CRUD implementation from mocks to real database
- Write and run integration test script against real database
- Write comprehensive README.md with architecture and how to use
```

---

# 3. Customize and Provide Rich Context

Tailor Copilot's behavior to your team's standards, coding conventions, and operational practices.

## 3.1 Custom instructions
Today VS Code with GitHub Copilot fully support [AGENTS.md](https://agents.md/) standard. See exaple in repository and selected subfolders (good for monorepo situations).

**Note**: Apart from repository custom instructions (`.github/copilot-instructions.md`), you can also configure [personal custom instructions](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions) for your own preferences and [organization custom instructions](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-organization-instructions) for team-wide standards.

Tips what to include:
- Coding style (Terraform structure, code structure, use Pydantic, ...)
- Frameworks and tools (eg. use FastAPI, uv as package manager, use azurerm provider in Terraform, use Helm charts rather than Kustomize, ...)
- Procedures and recommendations (always check solution design, keep implementation log, common errors)
- Tests and ad-hoc stuff (prefer regular testing, when using something adhoc prefix it and delete afterwards, ...)
- Common envs and configuration styles (use ini file, use .env, check envs directly vs. use config class, ...)
- Documentation strategy (use docstrings, do not comment inline what is obvious, ...)
- Tools (prefer tool use over CLI and scripts, write adhoc test scripts when something becomes too complex, ...)

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

## 3.4 Bring Your Own Model (BYOM)

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

## 3.5 Multi-Repository Planning with Copilot Spaces

[Copilot Spaces](https://www.github.com/copilot/spaces) enables strategic planning across multiple repositories:

- Architecture discussions spanning microservices
- Cross-repo refactoring planning
- Enterprise-wide technical decisions
- Design reviews involving multiple teams

You can also use that knowledge base in your GitHub Copilot agent query via MCP:

```
What are common errors when automating email processing? #list_copilot_spaces #get_copilot_space 
```

---

# 4. Model Context Protocol (MCP) Tools

MCP enables Copilot to interact with external tools and services, dramatically extending its capabilities beyond code generation. For more advanced scenarios, you can also develop [custom VS Code extensions](https://docs.github.com/en/copilot/concepts/extensions) with specialized UI.

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

🎥 See [recording](./docs/video/MCP-Kubernetes.mp4) of this demo.

## 4.3 GitHub MCP
See all available calls under GitHub MCP.

Few things to try:
- `What plans we have for implementing PDF in our app? Check GitHub Issues.` which uses list_issues and get_issue
- `In what repository am I using Event Sourcing pattern with CosmosDB?` which uses search_code
- `Our api-processing do have performance issues. Gather information about this service and create GitHub issue and assign tkubica12 to look into it` which uses create_isse


## 4.4 Azure MCP

- Query Azure resources (storage accounts, VMs, App Services)
- Analyze costs and resource utilization
- Diagnose issues with Azure Monitor
- Manage Azure resources directly from Copilot

Example prompts to start with:

- `What versions my AKS clusters run?`
- `See my storage accounts, can I improve resiliency and data protection?`


## 4.5 Database MCP
In our example we will use PostgreSQL extension and MCP server. Deploy Azure Database for PostgreSQL and connect to it. Thank you can try this prompt:

```
Connect to PSQL psql-mcp and create table users with following fields:
- user id
- user full name
- address
- phone

Generate about 100 rows of some test date and insert it.
```

Then you can use UI of extension to see data in that table.

## 4.6 Playwright MCP for Testing

- Generate E2E tests
- Run Playwright tests from Copilot
- Debug test failures with screenshots

Here is example prompt:

`Run my src/frontend in separate terminal and try to submit file /demo/image/example.jpg using Playwright MCP.`


---

# 5. Copilot Coding Agent

Delegate long-running tasks to Copilot Coding Agent that works asynchronously in the background, committing changes to a branch and opening PRs.

## 5.1 Example Delegated Tasks
Use "delegate to copilot agent" button with these prompts:

- `I have k6 perftest, but no README for it. Create README.md file explaining how to run the perftest, what scenarios it covers, and how to interpret results.`
- `Some of Python services are using pip and requirements.txt. I want to migrate everything to uv as package manager. Make sure to migrate to toml files, remove requirements.txt and change Dockerfile and READMEs accordingly. Test your able to sync uv and that Dockerfile builds without errors.`

## 5.2 From GitHub Issues

1. Go to **Issues** in your repository
2. Create or select an issue
3. Assign it to **Copilot Coding Agent**
4. Agent will create a branch, implement changes, and open a PR

See [Copilot Agents page](https://github.com/copilot/agents) to manage multiple agent tasks across repositories.

## 5.3 When to Use Coding Agent vs Agent Mode

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

---

# 7. GitHub Spark

No-code/low-code prototyping with natural language. Build functional applications without writing code manually.

[GitHub Spark](https://github.com/spark)

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

---

# TODO

- [ ] More GitHub Spark examples
- [ ] Azure SRE Agent full demo
- [ ] Copilot CLI
- [ ] Copilot App Modernization
