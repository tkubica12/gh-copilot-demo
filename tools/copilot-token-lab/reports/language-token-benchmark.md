# Language tokenizer benchmark

Encoding: `o200k_base`. This is a tokenizer-only micro-benchmark, not Copilot OpenTelemetry. It demonstrates that fewer characters do not necessarily mean fewer tokens.

| Group | Language | Text | Chars | UTF-8 bytes | Tokens | vs English | Note |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| simple sentence | English | `I met a huge dog` | 16 | 16 | 5 | 1.00x | baseline |
| simple sentence | Czech | `Potkal jsem obrovského psa` | 26 | 27 | 7 | 1.40x | Czech |
| terse code task | English | `Fix auth bug. Add test. Return diff only.` | 41 | 41 | 11 | 1.00x | baseline |
| terse code task | Czech | `Oprav auth chybu. Přidej test. Vrať jen diff.` | 45 | 47 | 17 | 1.55x | Czech |
| structured API task | English | `POST /api/users<br>Validate: name req, email req+valid<br>400 errors<br>201 user` | 71 | 71 | 20 | 1.00x | baseline |
| structured API task | Czech | `POST /api/users<br>Validuj: name pov, email pov+platny<br>400 chyby<br>201 user` | 70 | 70 | 23 | 1.15x | Czech structured prompt |
| verbose API task | English | `Create a POST /api/users endpoint that validates required name and email, returns 400 with errors on failure, and returns 201 with the created user.` | 148 | 148 | 31 | 1.00x | baseline |
| verbose API task | Czech | `Vytvoř endpoint POST /api/users, který validuje povinné name a email, při chybě vrátí 400 s detaily a při úspěchu vrátí 201 s vytvořeným uživatelem.` | 148 | 163 | 50 | 1.61x | Czech prose |
| handoff style | Normal | `After implementation, summarize what changed, why the approach was chosen, which files were edited, how validation was performed, and what risks remain.` | 152 | 152 | 28 | 1.00x | baseline |
| handoff style | Caveman | `Impl done. Say: changed files, why, validation, risks. No intro. No recap. Five bullets max.` | 92 | 92 | 24 | 0.86x | human-readable terse output |
| handoff style | Wenyan | `done -> files | why | checks | risks. no intro. <=5 bullets.` | 60 | 60 | 17 | 0.61x | machine-oriented handoff |

## Takeaways

1. Prefer terse English for prompts and instructions unless the task specifically requires Czech.
2. Czech is understandable to the model, but the benchmark should measure token cost instead of assuming character count predicts cost.
3. Structured prompts often matter more than language choice.
4. Caveman-style output can be useful when a human still reads the response; more extreme handoff styles are better reserved for agent-to-agent or durable context.
