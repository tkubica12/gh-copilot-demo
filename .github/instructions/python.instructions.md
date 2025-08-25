---
applyTo: '**/*.py'
---
- When writing APIs in Python in this project we focus on `FastAPI`.
- To ease local development prefer using different default local port for each service.
- Always use `docstrings` for all public methods and classes explaining its purpose, parameters, return values, and exceptions.
- Never add and continuously remove any comments that document the obvious or progress of the code, only use comments to explain non-obvious lines worth extra documentation.
- Use `Pydantic` models for data validation and serialization. Store models in `models/` folder.
- Use Python's built-in logging module for logging, with appropriate log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL). 
- Use `pytest` for tests.