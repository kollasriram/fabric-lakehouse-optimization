# Security

Do not commit a notebook after executing it unless all outputs and runtime metadata have been cleared.

Runtime-generated assessment output may contain:

- workspace, Lakehouse, and table names
- shortcut targets and external storage locations
- file sizes, maintenance history, and implementation plans
- internal operational or ownership details

The published notebook obtains Fabric credentials only at runtime through `notebookutils`. Never replace that pattern with embedded tokens, connection strings, account keys, SAS tokens, client secrets, or passwords.

Before committing:

1. Confirm every notebook cell has empty `outputs`.
2. Confirm every `execution_count` is `null`.
3. Review markdown and parameter cells for environment-specific identifiers.
4. Run the repository secret scan.

Report sensitive-data exposure privately to the repository owner rather than opening a public issue.
