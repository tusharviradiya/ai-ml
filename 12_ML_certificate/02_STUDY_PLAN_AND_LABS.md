# Study plan and practical work

This is a suggested **16-week plan at 12–15 hours per week**, approximately 192–240 hours. This is a planning estimate, not an AWS training requirement or a prediction of when you will pass. Extend it if cloud or ML fundamentals are new; compress topics only when you can demonstrate the outcomes.

Module numbers refer to [the topic checklist](01_TOPICS_TO_LEARN.md). No AWS resources have been provisioned by creating these files.

## Start with a diagnostic

Attempt these without notes and record `independent`, `needed help`, or `not yet`:

1. Load two tables, join them, identify duplicate keys, and explain missing values.
2. Split a dataset correctly and fit preprocessing without leaking validation data.
3. Train a baseline; calculate precision/recall from a confusion matrix.
4. Explain what an IAM role does and how it differs from a human login.
5. Choose S3 versus EBS versus EFS for three storage requirements.
6. Draw a private training job's network and data access paths.
7. Explain a Docker image, a build pipeline, and a model serving endpoint.
8. Explain embeddings, RAG, and fine-tuning using separate examples.

Use the results to adjust Weeks 1–2. Existing exercises elsewhere in this repository are useful revision material, but file presence does not mean a topic is mastered.

## Suggested schedule

| Week | Main study | Practical evidence |
|---|---|---|
| 1 | Modules 00–01: diagnose gaps; AWS, IAM, CLI, core compute/networking | Diagnostic notes; Lab 01 |
| 2 | Modules 02–03: storage, formats, ingestion, Glue/Athena | Lab 02; storage and ingestion comparison notes |
| 3 | Modules 03–04: streaming, transformations, Feature Store | Lab 03; reusable preprocessing code |
| 4 | Modules 05–06: quality, imbalance, labels, document/FM data | Lab 04; Domain 1 practice and error review |
| 5 | Modules 07–08: algorithm, AI service, FM, and RAG choices | Model/service decision table; initial retrieval dataset |
| 6 | Modules 09–10: managed training, hyperparameters, efficiency | Lab 05 |
| 7 | Modules 11–12: ML and GenAI evaluation | Lab 09; Domain 2 practice and error review |
| 8 | Modules 13–14: inference modes, containers, resource sizing | Lab 06 |
| 9 | Modules 15 and 17: registry, rollout, orchestration, IaC | First part of Lab 07 |
| 10 | Modules 16 and 18: agents, CI/CD, prompt/RAG versioning | Finish Lab 07; Lab 10; Domain 3 review |
| 11 | Modules 19–20: drift, observability, failure diagnosis | Lab 11 |
| 12 | Modules 21–23: permissions, private access, cost, safeguards | Lab 12; Domain 4 practice and error review |
| 13 | Revisit Modules 06, 08, 12–13, 18: integrated RAG | Lab 08; improve retrieval and evaluation |
| 14 | Traditional ML capstone | Capstone A evidence and incident exercise |
| 15 | RAG/agent capstone and weak topics | Capstone B evidence; first full timed practice |
| 16 | Mixed scenarios, targeted revision, exam logistics | Fresh timed practice; readiness checklist |

Revisit earlier domains every week. The weeks are organized for learning dependencies rather than strictly distributing hours according to exam percentages.

## Practical exercise catalogue

These are exercise specifications to complete during learning, not prebuilt lab implementations. Start locally when possible. Use small, non-sensitive datasets and a sandbox account or supplied training lab for cloud work.

### Lab 01 — AWS access and basic resources

**Modules:** 01, 21, 22.

Verify your CLI identity, selected Region, and permissions. Set a budget notification, create a private study bucket, upload a small dataset, and read it using an appropriate role. Identify the role's policy and the resource's ARN.

**Save:** resource inventory, sanitized commands, a simple access diagram, and cleanup steps. Never save credential values.

**Diagnose:** explain whether an intentionally restricted read fails because of identity permissions, a resource policy, or encryption access.

### Lab 02 — Build a small analytical dataset

**Modules:** 02–03.

Create raw CSV/JSON records and a partitioned Parquet version. Catalog/query them with Glue/Athena or first demonstrate equivalent transformations locally. Join a second table and validate counts before and after the join.

**Save:** schema, transformation script, queries, row-count assertions, and a comparison of scanned data where available.

**Diagnose:** introduce an incompatible schema or incorrect partition and explain the symptoms and fix.

### Lab 03 — Streaming events and feature freshness

**Modules:** 03–04, 20.

Send synthetic events through a small streaming exercise. Identify producer, stream, consumer, and destination. Transform records and handle duplicates, malformed records, and late events. A local simulator is a useful first step; a managed lab can demonstrate Kinesis/Flink behavior.

**Save:** event schema, processing diagram, lag/freshness measurements, and replay strategy.

**Diagnose:** slow a consumer and explain where backlog appears and how recovery avoids duplicate effects.

### Lab 04 — Data validation and reusable features

**Modules:** 04–06.

Use a small classification dataset with missing values, imbalance, and duplicates. Write quality checks, split correctly, fit preprocessing on training only, and compare sampling/weighting options. Design a Feature Store feature group with identifiers and event timestamps; ingest records if your environment supports it.

**Save:** quality report, preprocessing pipeline, feature schema, and subgroup/class metrics.

**Diagnose:** identify a deliberately leaked feature or inconsistent inference transformation.

### Lab 05 — Managed training and bounded tuning

**Modules:** 07, 09–11, 22.

Train a local baseline, then configure one small SageMaker training job using a built-in algorithm or supported script mode. Compare a few controlled hyperparameter settings. Track code/configuration, inputs, metrics, job logs, artifacts, and duration.

**Save:** run comparison and explanation of the selected model. Set explicit job/runtime limits appropriate to your lab.

**Diagnose:** troubleshoot a bad input path, incompatible data shape, or missing execution-role permission.

### Lab 06 — Serve a model and compare inference modes

**Modules:** 13–15.

Run batch inference and one suitable endpoint mode on a small model. Invoke it programmatically and measure latency and errors. Write configuration sketches for the remaining modes; you do not need to leave four paid deployments running.

**Save:** serving diagram, request/response examples, mode decision table, measured results, and deletion procedure.

**Diagnose:** send an invalid payload and distinguish client validation, model failure, and infrastructure overload.

### Lab 07 — Evaluation-gated release pipeline

**Modules:** 15, 17–18.

Automate preprocessing, training, evaluation, and conditional registration. Associate a model version with its metrics and data/code versions. Add approval and deployment steps or a reviewable deployment configuration. Demonstrate a failed quality gate and a previous-version rollback.

**Save:** pipeline definition, execution evidence, registry metadata, tests, and release/rollback notes.

**Diagnose:** distinguish a source connection error, build error, training failure, and failed deployment health check.

### Lab 08 — Document retrieval and RAG

**Modules:** 06, 08, 12–13, 18, 23.

Create a small document set plus about 20 questions, including unanswerable questions. Parse/chunk documents, attach metadata, embed/index, retrieve, and generate grounded answers. Compare two chunking or retrieval settings while holding the evaluation questions constant. Use Bedrock Knowledge Bases in a suitable lab or account.

**Save:** ingestion/retrieval diagrams, chunk examples, evaluation table, citations, index-refresh procedure, and failure analysis.

**Diagnose:** identify whether a wrong answer comes from missing source data, poor retrieval, or unsupported generation.

### Lab 09 — FM customization preparation and evaluation

**Modules:** 06, 08, 12.

Prepare a small prompt/response dataset; validate schema, duplicates, safety, and train/evaluation separation. Compare prompt variants and two suitable available models with a fixed rubric. Outline fine-tuning versus continued pretraining versus distillation for separate requirements.

**Save:** validated sample dataset, prompt versions, model-selection rationale, human ratings, and quality/latency/usage results.

**Completion:** a paid fine-tuning job is optional. Learn its configuration, artifacts, evaluation, and deployment implications even if you use a walkthrough instead.

### Lab 10 — Agent with controlled tool access

**Modules:** 16, 18, 20–21, 23.

Build a small agent that retrieves information and calls one read-only lookup tool. Define tool input/output schema, identity, session state, retry limits, and error handling. Inspect a successful and a failed execution trace. Use AgentCore or a supported training environment for managed deployment.

**Save:** agent flow, permissions, version identifiers, test cases, traces, and resource limits.

**Diagnose:** simulate a tool timeout, invalid arguments, and duplicate calls; show how the application responds.

### Lab 11 — Drift and operational monitoring

**Modules:** 11–12, 19–20.

Create a reference dataset and a changed dataset. Check schema/missingness/distributions and compare labeled performance where labels exist. Implement a scheduled evaluation or monitoring script and publish relevant results to a dashboard/alert mechanism. Add RAG or agent failure metrics.

**Save:** baseline, drift report, evaluation results, alarm definition, and an incident runbook.

**Diagnose:** explain a case with drift but stable accuracy and a case with declining quality that requires delayed labels to detect.

### Lab 12 — Security and cost review

**Modules:** 18, 21–23.

Review least-privilege roles, S3/KMS access, private connectivity, secret handling, image scanning, and audit logs for a previous lab. Estimate training/hosting costs and RAG/agent usage costs. Test input/output safeguards with non-sensitive examples.

**Save:** access matrix, network sketch, cost worksheet, safeguard results, audit evidence, and final resource inventory.

**Diagnose:** distinguish an IAM denial from a network timeout; explain an unexpected cost increase from token usage or repeated tool execution.

## Two capstones

### Capstone A — Traditional ML prediction service

Combine Labs 02, 04–07, 11–12 into a small classification project such as churn or fraud screening. Include data validation, reusable features, managed training, a model quality gate, registry/versioning, suitable inference, monitoring, least-privilege access, and a rollback plan.

**Acceptance evidence:** reproducible configuration; baseline comparison; explanation of the chosen metric; one successful prediction; one rejected candidate release; one investigated production-like failure; cost estimate; cleanup record.

### Capstone B — Grounded document assistant with a tool

Combine Labs 08–12. Include traceable ingestion, retrieval, a versioned prompt/model choice, answer evaluation, a read-only agent tool, safeguards, appropriate access control, observability, and an index-refresh procedure.

**Acceptance evidence:** fixed evaluation set; retrieval versus generation error breakdown; handling of unanswerable requests; denied unauthorized tool/data access; tool-failure trace; cost-per-task estimate; tested rollback or restoration of the preceding configuration.

## Weekly study method

Use roughly 4 hours for reading/notes, 5–7 hours for practical work, and 3–4 hours for recall, practice questions, and correcting mistakes. Adapt the split to your gaps.

For each topic, answer: What problem does it solve? When would I choose it? What do I configure? What commonly fails? What would I monitor? What costs money? How is access controlled?

Keep one error log with: topic, your incorrect reasoning, corrected rule, relevant source, and a new example. Revisit mistakes after a few days and again the following week.

## Cloud lab costs and current availability

Before a cloud exercise, check its Region, account access, and estimated charges. Budget alerts do not by themselves impose a hard spending cap. Afterward, remove unneeded endpoints, development compute, vector stores, provisioned capacity, and other billable resources; account for retained storage and logs. See [AWS Budgets](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html).

Current documentation says **Model Monitor**, **Clarify**, and **Bedrock Agents Classic** are closed to new customers. Learn their relevant concepts when encountering older material, but do not make access to them a prerequisite for completing this plan. Use custom evaluation/drift checks, local explainability exercises, and AgentCore-based agent work as appropriate. Sources: [Model Monitor](https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor.html), [Clarify](https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-model-explainability.html), [Agents Classic](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html).
