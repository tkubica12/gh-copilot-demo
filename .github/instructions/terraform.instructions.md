---
applyTo: '**/*.tf,**/*.tfvars'
---
- Variables define external interfaces of modules and should be stable. Therefore, avoid using variables directly in resources and rather create locals for them.
- Separate resources into files based on their type such as `networking.tf`, `service_bus.tf`,  `rbac.tf`,etc. If there are a lot of resources of the same type, consider adding another level of separation such as `container_app.frontend.tf`, `container_app.backend.tf`, etc.