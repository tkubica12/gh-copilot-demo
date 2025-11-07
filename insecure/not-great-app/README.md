# Not Great App

This is a demo application with intentionally vulnerable and outdated dependencies for security testing purposes.

## Note on Dependencies

This app uses extremely old versions of packages (circa 2018-2019) that contain known vulnerabilities. These versions may not build or install correctly with modern Python versions (3.10+) due to breaking changes in Python internals.

The pyproject.toml has been created for documentation purposes, but you may need to use an older Python version (3.6-3.8) to actually run this application.

### Migration Notes

During the migration from requirements.txt to pyproject.toml:
- Removed explicit `urllib3==1.24.1` as it conflicts with `requests==2.18.4` requirements
- uv resolves `urllib3==1.22` as a transitive dependency from requests (compatible version)
- The original requirements.txt had conflicting constraints that prevented installation

## Dependencies

- Flask==0.12.3 (vulnerable)
- requests==2.18.4 (outdated) → pulls urllib3==1.22
- Django==1.11.20 (vulnerable)
- Jinja2==2.10 (vulnerable)
- PyYAML==3.13 (vulnerable)
- pillow==6.2.1 (vulnerable)
- lxml==4.3.4 (vulnerable)
- sqlalchemy==1.2.17 (outdated)

## Purpose

This application is used to demonstrate:
- Security scanning tools
- Vulnerable dependency detection
- Various web application vulnerabilities (SQL injection, XSS, command injection, etc.)

**DO NOT use this application in production or expose it to the internet.**
