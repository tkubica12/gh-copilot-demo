---
applyTo: '**/*.tf,**/*.tfvars'
---
- We will use mix of azurerm provider for standard common resources and azapi provider for scenarios where we need to use latest Azure features not yet available in azurerm provider.
- Separate resources into files based on their type such as `networking.tf`, `service_bus.tf`,  `rbac.tf`,etc. If there are a lot of resources of the same type, consider adding another level of separation such as `container_app.frontend.tf`, `container_app.backend.tf`, etc.
- When defining variables, provide smart defaults where possible.
- With variables always provide rich multiline descriptions that explain the purpose of the variable, its type, and any constraints and give examples.
- Do not add comments explaining changes or adding notes. Comments are reserved only for description of resource when needed or to comment on critical non-obvious attributes beyond standard.
- As this is demo environment, I do not insist of adding tags to resources unless necessary or unless user asks for it.