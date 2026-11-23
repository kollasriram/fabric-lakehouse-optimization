# Microsoft Fabric Lakehouse Optimization Assessment

A safe, reusable Microsoft Fabric notebook for assessing Lakehouses and producing clear, prioritized optimization recommendations.

## What it does

- Discovers Lakehouses, Delta tables, and OneLake shortcuts in the active workspace
- Profiles file counts, file sizes, partitioning, Delta history, table properties, and maintenance patterns
- Identifies candidates such as small files, excessive partitioning, missing maintenance, stale data, shortcuts, and configuration opportunities
- Produces plain-language recommendations with:
  - intended action and expected benefit
  - prerequisites and ownership
  - approval requirements
  - validation procedure and runnable starter code
  - success criteria and rollback guidance
- Supports controlled maintenance modes with exact-table approvals
- Runs in `audit_only` mode by default and makes no table changes

## Notebook

- [`Fabric_Lakehouse_Optimization_and_Maintenance_Customer.ipynb`](./Fabric_Lakehouse_Optimization_and_Maintenance_Customer.ipynb)
- [Fabric Spark optimization coverage matrix](./docs/Fabric_Spark_Optimization_Coverage_Matrix.md)

## Safe usage

1. Import the notebook into a Microsoft Fabric workspace.
2. Review the prerequisites and Step 1 parameters.
3. Leave `run_mode = "audit_only"` for the initial assessment.
4. Run all cells in order.
5. Treat findings as candidates and validate them against the real workload.
6. Before any mutating run, add exact `lakehouse.schema.table` values to the approval list and review the generated rollback plan.

A default Lakehouse is not required for `audit_only` discovery. It is needed for persistent catalog operations or implementation modes that depend on catalog tables.

## Run modes

| Mode | Behavior |
|---|---|
| `audit_only` | Read-only assessment and recommendations |
| `optimize_only` | Approved `OPTIMIZE` actions only |
| `vacuum_only` | Approved, retention-safe `VACUUM` actions |
| `full_maintenance` | Approved maintenance sequence |

## Evidence and limitations

The framework distinguishes measured benefit, safety validation, conditional recommendations, unsupported capabilities, and checks that require an external production consumer or owner.

Recommendations are not automatic proof for every workload. Validate production queries, writes, concurrency, capacity, data volume, shortcuts, retention requirements, and rollback procedures before changing a table.

The notebook source is published without execution outputs. Runtime-generated table names, shortcut targets, diagnostics, and assessment data can be environment-sensitive and should not be committed to this repository.

## License

See [`LICENSE`](./LICENSE).
