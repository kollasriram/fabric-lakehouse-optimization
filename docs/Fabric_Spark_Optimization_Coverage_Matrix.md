# Microsoft Fabric Spark Optimization Coverage Matrix

Scope: current Microsoft Learn Fabric Spark/Data Engineering guidance reviewed on 2026-11-23 and reconciled with:

- `Fabric_Lakehouse_Optimization_and_Maintenance_Customer.ipynb`
- `Fabric_Lakehouse_Optimization_Validation.ipynb`

Evidence class meanings:

- **SCANNED** — the assessment inspects a table/property/history signal and generates a candidate action.
- **BENCHMARKED** — the validation notebook runs a correctness-preserving control/variant test.
- **CONFIG-PROBED** — the runtime setting is set/read back, but benefit is not inferred.
- **EXTERNAL REQUIRED** — requires a real consumer, owner, capacity, network, package, or platform surface.
- **UNSUPPORTED HERE** — the active runtime/API cannot execute the feature or the current docs restrict it.

This matrix is a coverage register, not a claim that every technique benefits every workload.

## Delta layout and maintenance

| Technique | Official guidance | Notebook coverage | Evidence class |
|---|---|---|---|
| Adaptive target file size | `tune-file-size#adaptive-target-file-size` | Scans evaluated property; customer A/B procedure; benchmark adaptive vs explicit target | SCANNED + BENCHMARKED |
| Explicit `delta.targetFileSize` override | `tune-file-size#set-target-file-size-consistently` | Detects legacy explicit override and requires justification | SCANNED + BENCHMARKED |
| Optimize Write | `tune-file-size#optimize-write` | Existing control matrix and small-file action plan | SCANNED + BENCHMARKED |
| Auto compaction | `table-compaction#auto-compaction` | Write matrix; property/config support; checkpoint-only probe | BENCHMARKED + CONFIG-PROBED |
| Auto compaction thresholds | `table-compaction#tune-auto-compaction-thresholds` | min/max file and min-file-count support probes | CONFIG-PROBED |
| Manual `OPTIMIZE` bin compaction | `table-compaction#optimize-command` | Detects candidate history/file evidence and benchmarks before/after | SCANNED + BENCHMARKED |
| Fast Optimize | `table-compaction#fast-optimize` | Enabled in validation; tunable min-files/parquet-coefficient probes; idempotence observation | CONFIG-PROBED + BENCHMARKED |
| File-level compaction targets | `table-compaction#file-level-compaction-targets` | Enabled/probed and covered by adaptive target lifecycle | CONFIG-PROBED |
| `OPTIMIZE` operation metrics | `table-compaction#optimize-output-metrics` | File count/size and operation-duration evidence | BENCHMARKED |
| Z-Order | `table-compaction#optimize-with-z-order` | Represented as a controlled legacy/clone test; Liquid Clustering preferred | CONDITIONAL |
| Liquid Clustering | `liquid-clustering` | Large-unclustered and quality-review findings; control/clustered benchmark | SCANNED + BENCHMARKED |
| `OPTIMIZE FULL` | `table-compaction#optimize-full` | Tested and intentionally rejected on non-clustered tables | BENCHMARKED |
| Incremental clustering | `liquid-clustering#incremental-liquid-clustering` | Runtime 2.0-only guidance; incremental `OPTIMIZE`, not full rewrite, is prescribed | CONDITIONAL |
| `clusteringQuality()` | `liquid-clustering#evaluate-clustering-quality` | New customer action; validation records real metrics where Scala/runtime access allows | SCANNED + EXTERNAL RUNTIME FEATURE |
| Hive partitioning | `delta-lake-partitioning` | Detects over-partitioning and benchmarks partitioned/unpartitioned layouts | SCANNED + BENCHMARKED |
| Deletion Vectors | `delta-lake-deletion-vectors` | Mutation/off-on benchmark and candidate detection | SCANNED + BENCHMARKED |
| DV purge / `REORG APPLY (PURGE)` | `delta-lake-deletion-vectors` | Lifecycle/maintenance validation; routine use remains conditional | BENCHMARKED |
| `VACUUM RETAIN 168 HOURS` | `delta-lake-vacuum` | Safe floor, DRY RUN, correctness, and storage checks | SCANNED + BENCHMARKED |
| `VACUUM LITE` | `delta-lake-vacuum#vacuum-in-lite-mode` | Safe Runtime 2.0 support probe on disposable data | CONFIG/OPERATION PROBED |
| `VACUUM USING INVENTORY` | `delta-lake-vacuum#vacuum-with-an-inventory-table` | Included as scale-path guidance; requires a real inventory process | EXTERNAL REQUIRED |
| Delta log cleanup limitations | `delta-lake-vacuum#understand-what-vacuum-doesnt-remove` | Documented: VACUUM does not clean `_delta_log`; no blanket cleanup recommendation | GUIDANCE |

## Write path and file statistics

| Technique | Official guidance | Notebook coverage | Evidence class |
|---|---|---|---|
| Frequent-small-write buffering | Streaming / compaction guidance | Detects per-event/small append abuse and requires producer redesign test | SCANNED |
| Resource profile `writeHeavy` | `configure-resource-profile-configurations` | Resolve/profile test plus session-level review | CONFIG-PROBED |
| Resource profile `readHeavyForSpark` | same | Resolve/profile test plus session-level review | CONFIG-PROBED |
| Resource profile `readHeavyForPBI` | same | Resolve/profile test and Direct Lake consumer requirement | CONFIG-PROBED + EXTERNAL REQUIRED |
| V-Order | `delta-optimization-and-v-order` | Consumer-specific table finding and write/read/size benchmark | SCANNED + BENCHMARKED |
| Direct Lake V-Order/row groups | Cross-workload maintenance / Direct Lake performance | New row-group/update-pattern finding and Delta Analyzer action | SCANNED + EXTERNAL REQUIRED |
| Data-skipping statistics | `delta-lake-file-skipping` | Candidate-column and wide-string reviews; explicit stats test | SCANNED + BENCHMARKED |
| Predicate/type compatibility | `delta-lake-file-skipping` | Typed-filter plan probe | BENCHMARKED |
| 32-column statistics scope | `delta-lake-file-skipping` / `automated-table-statistics` | Column-order and candidate outside-stats detection | SCANNED |
| Automated extended statistics | `automated-table-statistics` | Write overhead and config probes | CONFIG-PROBED + BENCHMARKED |
| Statistics injection with frequent mutations/DV | `automated-table-statistics` | New CBO/DV risk finding and injection on/off plan/runtime test | SCANNED + BENCHMARKED |
| Statistics recomputation | `automated-table-statistics#recompute-statistics` | Action guidance; real schema-change workload remains environment-specific | CONDITIONAL |
| CBO / `ANALYZE TABLE` | `automated-table-statistics` | Catalog registration, all-columns statistics, and join A/B | SCANNED + BENCHMARKED |
| Delta column mapping | `delta-lake-column-mapping` | Detected and retained in table profile; schema-evolution test remains workload-specific | SCANNED |

## Spark query and code optimization

| Technique | Official guidance | Notebook coverage | Evidence class |
|---|---|---|---|
| AQE and coalesced shuffle partitions | Spark best-practices basics | On/off benchmark and resolved config probes | CONFIG-PROBED + BENCHMARKED |
| AQE skew join | Spark best-practices basics | Synthetic hot-key on/off benchmark | BENCHMARKED |
| Broadcast join threshold/hint | Spark best-practices basics | Small-dimension plan/runtime A/B | BENCHMARKED |
| Predicate and projection pruning | Spark best-practices basics | Early/late logical-shape and typed filter probes | BENCHMARKED / INCONCLUSIVE |
| Coalesce versus repartition | Spark best-practices basics | Narrow write control/variant | BENCHMARKED |
| Avoid repeated actions / `Observation` | Notebook best practices | Count-then-write vs one-write Observation | BENCHMARKED |
| Bounded `collect()` | Spark performance guidance | Driver guardrail test | BENCHMARKED |
| Native Spark functions over Python UDFs | Spark best-practices basics | Python UDF vs built-in expression | BENCHMARKED |
| Shared Window specs | Spark/DataFrame guidance | Window spec reuse test | BENCHMARKED |
| Bounded MERGE predicate | Delta/Lakehouse guidance | Full-target vs equivalent bounded merge | BENCHMARKED |
| Spark DataFrame caching | Spark performance guidance | Uncached vs reused cached benchmark | BENCHMARKED |
| Intelligent cache | `intelligent-cache` | Repeat-read useCache A/B and size/config probes | CONFIG-PROBED + BENCHMARKED |
| Salting/hot-key repartitioning | Spark best-practices basics | Skew fixture validates AQE; explicit salting remains customer-query specific | BENCHMARKED + CONDITIONAL |
| Memory/OOM controls and spill | Spark best practices / monitoring | Existing validation and run-monitoring guidance; no unsafe blanket memory increase | GUIDANCE |

## Runtime, engine, pools, and capacity

| Technique | Official guidance | Notebook coverage | Evidence class |
|---|---|---|---|
| Runtime 2.0 | `runtime-2-0` | Explicit compatibility/preflight guidance; used for validation environment | CONFIG/PLATFORM |
| Runtime compatibility migration | `runtime-2-0-migration-guide` | Library/JAR/Python/Scala/Delta interoperability external checklist | EXTERNAL REQUIRED |
| NEE | `native-execution-engine-overview` | Off by default; on/off test; plan/fallback and consumer validation guidance | CONFIG-PROBED + BENCHMARKED |
| NEE structured-streaming exclusion | NEE overview | Streaming tests intentionally run without NEE assumptions | GUIDANCE |
| NEE JSON/XML fallback | NEE overview | Explicit limitation in notebook guidance | GUIDANCE |
| NEE private Blob/DFS endpoints | NEE overview | Explicit networking prerequisite | EXTERNAL REQUIRED |
| Efficient scaledown / RSM | `efficient-scaledown-remote-shuffle-manager` | Session-level platform review and external pool/NEE validation | EXTERNAL REQUIRED |
| Autotune | `autotune` | Marked runtime-compatibility check; do not enable on unsupported Runtime 2.0 | UNSUPPORTED HERE / CHECK ON RELEASE |
| High concurrency | `configure-high-concurrency-session-notebooks` | Session-level review and orchestration external check | EXTERNAL REQUIRED |
| Starter/custom/live pools | Spark compute and live pool docs | Pool-startup, overflow, node-size and cost checks in coverage ledger | EXTERNAL REQUIRED |
| Autoscale/dynamic allocation | Spark compute | Capacity/pool sizing review; fix skew before scaling | EXTERNAL REQUIRED |
| Resource profiles | Resource profile docs | Runtime config resolution and end-user workload test | CONFIG-PROBED |
| Queueing, bursting, 430 throttling | Job concurrency/queueing | Monitoring and capacity-load validation requirement | EXTERNAL REQUIRED |
| Autoscale Billing for Spark | Spark billing docs | CU/cost-only validation under an authorized capacity | EXTERNAL REQUIRED |
| Spark UI/History, Advisor, Resources | Monitoring docs | Required evidence for every benchmark and action | REQUIRED EVIDENCE |
| Diagnostic Emitter | Spark diagnostics docs | External Log Analytics/Storage/Event Hubs validation | EXTERNAL REQUIRED |

## Streaming and external consumers

| Technique | Official guidance | Notebook coverage | Evidence class |
|---|---|---|---|
| Structured Streaming `availableNow` | Lakehouse streaming docs | Tested with Delta output and restart/checkpoint | BENCHMARKED |
| Streaming trigger/file-size pattern | Lakehouse streaming docs | Coverage guidance; customer benchmark uses controlled event volume | CONDITIONAL |
| Streaming RocksDB state store | Runtime/provider guidance | Runtime compatibility probe | UNSUPPORTED HERE IF FAILED |
| Checkpoint cleanup/orphan detection | Operational retention guidance | Scanner/coverage tracks checkpoints; aged cleanup remains long-lived test | EXTERNAL REQUIRED |
| Direct Lake framing/transcoding | Direct Lake performance docs | Delta Analyzer and consumer-specific action | EXTERNAL REQUIRED |
| Power BI row-group sizing | Cross-workload / Direct Lake docs | `DIRECT_LAKE_ROWGROUP_REVIEW` action; only actual model proves benefit | SCANNED + EXTERNAL REQUIRED |
| Pipeline/Dataflow writer maintenance | Cross-workload maintenance docs | Owner/writer source must be reviewed; Dataflow incremental restrictions documented | CONDITIONAL |
| Mirrored data | Cross-workload maintenance docs | Source-managed/system-managed ownership; no consumer-side DDL | GUIDANCE |

## Notebook and framework guardrails

- NEE is not enabled mid-session by `spark.conf.set`; it must be set in the first `%%configure` or Environment Acceleration setting.
- NEE is not a requirement for all 79+ benchmark rows. Use a separate NEE on/off study and an explicit JVM fallback control.
- Audit mode must remain non-mutating.
- Every production maintenance command requires exact-table approval and a rollback/recovery path.
- `PASS` means correctness preserved; it does not mean performance benefit.
- For every beneficial claim, retain equal-data/equal-compute control, warm/cold protocol, at least five measured repetitions, correctness checksum, file/byte metrics, and CU where available.

## Official documentation URLs

- https://learn.microsoft.com/fabric/data-engineering/table-compaction
- https://learn.microsoft.com/fabric/data-engineering/tune-file-size
- https://learn.microsoft.com/fabric/data-engineering/liquid-clustering
- https://learn.microsoft.com/fabric/data-engineering/delta-lake-vacuum
- https://learn.microsoft.com/fabric/data-engineering/delta-lake-deletion-vectors
- https://learn.microsoft.com/fabric/data-engineering/delta-lake-file-skipping
- https://learn.microsoft.com/fabric/data-engineering/automated-table-statistics
- https://learn.microsoft.com/fabric/data-engineering/delta-optimization-and-v-order
- https://learn.microsoft.com/fabric/data-engineering/native-execution-engine-overview
- https://learn.microsoft.com/fabric/data-engineering/intelligent-cache
- https://learn.microsoft.com/fabric/data-engineering/efficient-scaledown-remote-shuffle-manager
- https://learn.microsoft.com/fabric/data-engineering/configure-resource-profile-configurations
- https://learn.microsoft.com/fabric/data-engineering/spark-best-practices-development-monitoring
- https://learn.microsoft.com/fabric/data-engineering/spark-best-practices-basics
- https://learn.microsoft.com/fabric/data-engineering/runtime-2-0
- https://learn.microsoft.com/fabric/fundamentals/table-maintenance-optimization
