# GitHub Copilot demo

## Autocomplete
Open ```main.py``` in ```api-processing``` and type ```# Configure Prometheus``` and wait for suggestions.

## Next edit suggestion
Open ```main.py``` in ```api-processing``` and around line 52 change ```credential``` to ```azure_credential``` and wait for suggestions.

## Prompt files
Ask this in chat: ```Generate CRUD in Python for product API```

We will get functions using standard Python convention which is snake_case.

Clear chat and attach prompt file camelbase and ask again. We will get different response.

## KQL
Attach [query_data.cvs](./kql/query_data.csv) and ask ```Give me microsoft Kusto Query (KQL) to display percentage of procesor time grouped by instance and process id which is part of properties. Name of table is AppPerformanceCounters. Attached are example data.``.

## SQL
Attach [users_denormalized.json](./sql/users_denormalized.json) and ask ```Generate CREATE commands for normalized users and orders using Microsoft SQL..```

Than use output to ask ```Given the following Microsoft SQL schema. generate SQL query to get sum of order prices grouped by user.```

## Vision
Attach [classes.png](./vision/classes.png) and ask ```Generate code for classes in Python according to attached schema.```
