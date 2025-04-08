# GitHub Copilot demo

## Autocomplete
Open ```main.py``` in ```api-processing``` and type ```# Configure Prometheus``` and wait for suggestions.

## Next edit suggestion
Open ```main.py``` in ```api-processing``` and around line 52 change ```credential``` to ```azure_credential``` and wait for suggestions.

## KQL
Attach [query_data.cvs](./kql/query_data.csv) and ask ```Give me microsoft Kusto Query (KQL) to display percentage of procesor time grouped by instance and process id which is part of properties. Name of table is AppPerformanceCounters. Attached are example data.``.

## SQL
Attach [users_denormalized.json](./sql/users_denormalized.json) and ask ```Generate CREATE commands for normalized users and orders using Microsoft SQL.```

Than use output to ask ```Given the following Microsoft SQL schema. generate SQL query to get sum of order prices grouped by user.```

## Vision
Attach [classes.png](./vision/classes.png) and ask ```Generate code for classes in Python according to attached schema.``` Follow with ```now create PlanUML diagram out of this```

## Prompt files
Ask this in chat: ```Generate CRUD in Python for product API```

We will get functions using standard Python convention which is snake_case.

Clear chat and attach prompt file camelbase and ask again. We will get different response.

## Search and Fetch
Ask ```What is new in version v0.98.0 of CrewAI?``` and Copilot will not know.
You can use Web Search for Copilot extension using your Bing or Tavily key. This question should be answered now:

```What is new in version v0.98.0 of CrewAI? #websearch```

You can also Fetch specific file from URL directly. There is new standard **llms.txt** designed to give AI-friendly version of web site. Try this:

```What is new in version v0.98.0 of CrewAI? #fetch https://docs.crewai.com/llms-full.txt```

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

## Agent
Take files from ```frontend``` and using agent mode ask ```Enable dark mode for my frontend. User will have button to switch between light and dark mode. Implement necessary changes in the code and css.```

## Code Review
After few changes create branch, showcase commit message, PR creation and do Code Review.

## Code Security
In GitHub show vulnerabilities and demonstrate autofix.

## Brainstorming with Copilot Workspace
[Copilot Workspace](https://copilot-workspace.githubnext.com/)

## No-code with GitHub Spark
[GitHub Spark](https://spark.githubnext.com/)