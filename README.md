# GitHub Copilot demo
This repo contains example code to demonstrate GitHub Copilot features. It is not intended to be used in production.

# In-line code suggestions
## Autocomplete
Open ```main.py``` in ```api-processing``` and type ```# Configure Prometheus``` and wait for suggestions. Use TAB to accept, ESC to reject or CTRL+arrow to accept partially.

## Next edit suggestion
Open ```main.py``` in ```api-processing``` and around line 52 change ```credential``` to ```azure_credential``` and wait for suggestions.

# Examples using Ask and Edits
## Codebase search
```Where in my code I am processing messages from Service Bus queues and what is the code doing? #codebase```

## KQL
Attach [query_data.cvs](./kql/query_data.csv) and ask ```Give me microsoft Kusto Query (KQL) to display percentage of procesor time grouped by instance and process id which is part of properties. Name of table is AppPerformanceCounters. Attached are example data.``.

## SQL
Attach [users_denormalized.json](./sql/users_denormalized.json) and ask:
- ```Generate CREATE commands for normalized users, addresses and orders using Microsoft SQL.```
- ```Based on data structure, create 10 lines of sample data and make sure it make sense and foreign keys are respected.```
- ```Give me SQL statement to list userId, name, number of orders and number of addresses for each user.```

## Vision
Attach [classes.png](./vision/classes.png), create classes.py and ask ```Generate code for classes in Python according to attached schema.```  in Ask mode.

Create README.md file and in Edit mode follow with ```Create markdown documentation for classes.py and include mermaid diagram.```

## Multi-file editing
Add ```api-processing/main.py```, ```worker/main.py``` and terraform files such as ```terraform/service_bus.tf``` and ```terraform.rbac.tf```.

Ask ```In this code I am using Service Bus Queues, but I need to move to Service Bus Topics. Make sure to update my Terraform and Python code accordingly and add topic subscriptions and RBAC.```

# Copilot customization
## Extensions
```@azure /costs What can you tell me about storage costs im my subscription 673af34d-6b28-41dc-bc7b-f507418045e6```

## Repository instructions and prompt files
Ask this in chat: ```Generate CRUD in Python for product API```

We will get functions using standard Python convention which is snake_case.

Clear chat and attach prompt file camelcase and ask again. We will get different response.

Discuss repo-wide instructions at [./.github/copilot-instructions.md](./.github/copilot-instructions.md).

## Search and Fetch
Ask ```Did Pinecone introduced MCP support already? When and in what release?``` and Copilot will not know.
You can use Web Search for Copilot extension using your Bing or Tavily key. This question should be answered now:

```Did Pinecone introduced MCP support already? When and in what release? Use #websearch```

You can also Fetch specific file from URL directly. There is new standard **llms.txt** designed to give AI-friendly version of web site. Try this:

```Did Pinecone introduced MCP support already? When and in what release? #fetch https://docs.pinecone.io/llms-full.txt```

## Connect tools via MCP
Run MCP server in folder ```random_string_mcp```. This runs locally and is configured in ```mcp.json``` file on workspace. 

Use this prompt in Agent mode to demonstrate:

```Generate names for 10 containers in format app1-xxxxxx where xxxxxx is random suffix consisting of lowercase letters and numbers```


## Bring your own model
Install ```Ollama``` and download Deepseek Coder models (small and mid size).

```
ollama pull deepseek-coder:1.3b
ollama pull deepseek-coder:6.7b
ollama pull qwen2.5-coder
```

In Copilot click on Manage Models and add Ollama models. Than try some of the above examples with different models.

# Agent mode
Take files from ```frontend``` and using agent mode ask ```Enable dark mode for my frontend. User will have button to switch between light and dark mode. Implement necessary changes in the code and css.```

Than try ```Now add other modes and make UI to switch them easier. Colorful, contrast, green and MS DOS```

# Code Review
After few changes create branch, showcase commit message, PR creation and do Code Review.

# Code Security
In GitHub show vulnerabilities and demonstrate autofix.

# Brainstorming with Copilot Workspace
[Copilot Workspace](https://copilot-workspace.githubnext.com/)

# No-code with GitHub Spark
[GitHub Spark](https://spark.githubnext.com/)