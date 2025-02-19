# Enterprise demo flow
>> SLIDE: GitHub Enterprise overview
>> SLIDE: GitHub Copilot Enterprise overview

## GitHub Copilot
- Next-suggestion TAB experience in code editor (Terraform example), mention new gpt-4o-copilot finetuned model
- Discuss future of SLMs for autocomplete and fine-tuning preview

## Copilot Chat Enterprise
- Chat - model selection, o3-mini Elo on Codeforces (2032) vs. future with GPT-5 (Elo 2727), Google and Anthropic models
- Chat - Attach screenshot (insiders)
- Chat - Knowledgebase on web copilot (Enteprise)
I am creating new project to implement SDK for our public APIs and publish it for general public. What license should I pick, Apache, GPL or MIT?

- Chat - Azure extension
@azure /resources Do I have any Azure Container Apps deployed?
@azure /help I have created NSG to filter traffic, but it is still passing.
@azure /costs What can you tell me about storage costs im my subscription 673af34d-6b28-41dc-bc7b-f507418045e6

- Chat - custom extensions
@tomaskubica-gh-extension test

>> SLIDE: GitHub openness with selection of different AI models, support for Azure, AWS, GCP and onprem workloads

## Edits and Codespaces
- Edits option 1 - codespaces -> main, test.http, script.js, README.md
I need to change path for my processing api to be on /api/v1/process in my code, docs and tests.

- Edits option 2 - insiders Agent mode, frontend/src, frontend/public, package.json - start app first with npm start to see current version
Add dark mode to this app.

Nice, now also add contrast and colorful mode

>> SLIDE: Benefits and pricing for Codespaces

## Development cycle and DevSecOps
- Commit, PR with generate message and summary
- Ask Copilot Agent to become reviewer + use Code Review in VS Code

- DevSecOps - see dependabot
- DevSecOps - see issues from CodeQL, OSS, Sonar and apply Copilot AutoFix
- Approve and deploy to ACA -> CI stage (build container, VNET integrated managed agents), CD stage (ACA deploy)
- Check failed actions and click "Explain error" via Copilot

>> SLIDE: Benefits of full GitHub Enterprise suite with all addons
>> SLIDE: Migration to GitHub Enterprise
>> SLIDE: Trust - source code in cloud, security and compliance, case studies
>> SLIDE: Customer studies and measured benefits of GitHub Advanced Security

## Future of application development with GitHub Copilot Enterprise and AI Agents
- Workspaces - go to Issues and open in workspace to get analysis of current situation, suggestions and plan for changes
- Workspaces - run Brainstorming
- Workspaces - run Code in Codespaces
- Workspaces - implement proposed changes to codebase
- GitHub Spark - text-to-code platform

>> SLIDE: Agentic future of software development with project Padawan