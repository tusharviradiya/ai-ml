# Detailed topics to learn for MLA-C02

Use this as a learning checklist. A checked item means you can explain it, apply it to a small example, and recognize when it is the wrong choice. Reading a definition alone is insufficient.

**Depth:** learn service selection, configuration concepts, failure diagnosis, and tradeoffs. Algorithm derivations and research-level model development are supporting knowledge rather than the main study priority. The exam's role boundaries are described in the [official guide](https://docs.aws.amazon.com/aws-certification/latest/machine-learning-engineer-associate-02/machine-learning-engineer-associate-02.html).

## How this covers the official outline

The following ranges account for **107 numbered skills across 12 tasks** in the guide checked on 4 November 2026. They map into the modules below; a module can support more than one task. The guide remains the authority for exact wording and later changes.

| Official task | Skills covered, inclusive | Learning modules |
|---|---|---|
| 1.1 Data collection/storage | 1.1.1–1.1.9 | 02, 03, 04, 06 |
| 1.2 Transformation/features/preparation | 1.2.1–1.2.9 | 04, 06, 08 |
| 1.3 Quality and bias | 1.3.1–1.3.7 | 05, 06 |
| 2.1 Modeling choices | 2.1.1–2.1.8 | 07, 08 |
| 2.2 Training/customization | 2.2.1–2.2.9 | 08, 09, 10 |
| 2.3 Evaluation | 2.3.1–2.3.10 | 11, 12, 15, 19 |
| 3.1 Deployment choices | 3.1.1–3.1.8 | 13, 14, 15, 16 |
| 3.2 Resources/configuration | 3.2.1–3.2.11 | 13, 14, 16, 17, 21 |
| 3.3 Automation/CI/CD | 3.3.1–3.3.11 | 15, 17, 18 |
| 4.1 Inference/performance monitoring | 4.1.1–4.1.6 | 19, 20 |
| 4.2 Cost and resource efficiency | 4.2.1–4.2.10 | 14, 20, 22 |
| 4.3 Workload security | 4.3.1–4.3.9 | 16, 18, 21, 23 |

Sources: official [Domain 1](https://docs.aws.amazon.com/aws-certification/latest/machine-learning-engineer-associate-02/machine-learning-engineer-associate-02-domain1.html), [Domain 2](https://docs.aws.amazon.com/aws-certification/latest/machine-learning-engineer-associate-02/machine-learning-engineer-associate-02-domain2.html), [Domain 3](https://docs.aws.amazon.com/aws-certification/latest/machine-learning-engineer-associate-02/machine-learning-engineer-associate-02-domain3.html), and [Domain 4](https://docs.aws.amazon.com/aws-certification/latest/machine-learning-engineer-associate-02/machine-learning-engineer-associate-02-domain4.html).

## Foundations

### Module 00 — Python, SQL, mathematics, and ML revision

These prerequisites support the exam topics; they are not an additional official domain.

- [ ] Python: functions, modules, environments, exceptions, logging, file handling, JSON, and dependency management.
- [ ] NumPy/pandas: array shapes, filtering, joins, aggregation, missing values, and reading/writing datasets.
- [ ] SQL: joins, grouping, window functions, deduplication, and time-based filtering.
- [ ] Git and Linux: commits, branches, environment variables, processes, permissions, and reading logs.
- [ ] Mathematics: vectors/matrices, dot products, distance and cosine similarity, mean/variance, probability, conditional probability, and gradient descent intuition.
- [ ] ML lifecycle: problem framing, labels/features, training versus inference, parameters versus hyperparameters, baselines, and reproducibility.
- [ ] Supervised versus unsupervised learning; classification, regression, clustering, forecasting, anomaly detection, NLP, and computer vision use cases.
- [ ] Generalization: bias/variance, overfitting/underfitting, regularization, and validation without test-set tuning.

**Outcome:** create a local baseline model and explain its split, metric, and limitations. Reuse relevant notebooks in `../11_Practice/` where useful.

### Module 01 — AWS and software engineering foundations

- [ ] Regions, Availability Zones, regional service availability, account boundaries, and shared responsibility.
- [ ] IAM identities, roles, temporary credentials, trust policies, permission policies, and least privilege.
- [ ] S3 objects/buckets/prefixes; EC2 instances; block, file, and object storage differences.
- [ ] VPCs, CIDR/subnets, routing, security groups, network ACL basics, endpoints, and NAT concepts.
- [ ] AWS CLI, Boto3, ARNs, SDK errors, pagination, retries/backoff, and service quotas.
- [ ] Docker images/containers, registries, HTTP APIs, request/response payloads, health checks, and logs.
- [ ] Infrastructure as code, automated builds, reproducible environments, and basic unit/integration testing.
- [ ] Console versus SDK/API operation; separate permissions for provisioning a resource and using it.

**Outcome:** explain which identity runs a training job, how it reaches private data, and which logs help diagnose failure. Read [IAM best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html).

## Domain 1 — Data preparation, 28%

### Module 02 — Storage and data formats

- [ ] Choose S3, EBS, or EFS for an object dataset, attached disk, or shared filesystem; recognize FSx use cases.
- [ ] Understand relational, key-value, document, search, and vector data sources; connect RDS, DynamoDB, and OpenSearch to a data pipeline.
- [ ] Compare CSV/JSON with Parquet/ORC: schema, nested data, column pruning, compression, and analytical scans.
- [ ] Organize raw, validated, and processed datasets; partition by useful access patterns and avoid excessive tiny files.
- [ ] Consider lifecycle, retention, versioning, encryption, access patterns, and data movement when selecting storage.
- [ ] Diagnose missing objects, wrong paths, incompatible schemas, capacity limits, and access failures.

**Outcome:** justify a storage/format choice for a large tabular training dataset and a multimodal dataset.

### Module 03 — Batch and streaming ingestion

- [ ] Extract and combine source data using SQL, Python, Glue, or Spark; identify faulty joins and duplicate records.
- [ ] Glue Data Catalog, crawlers, ETL jobs, job bookmarks, schema evolution, and Athena querying.
- [ ] EMR/Spark versus Glue: operational control, existing Spark code, scale, and maintenance tradeoffs.
- [ ] Distinguish Kinesis Data Streams, Data Firehose delivery, Kafka/MSK concepts, and Flink stream processing.
- [ ] Streaming partitions/shards, producer/consumer throughput, retention, lag, event time, windows, and late records.
- [ ] Idempotency, replay, checkpoints, retries, dead-letter handling, and transformations with Lambda or Spark.
- [ ] Debug throttling, hot partitions, malformed events, failed writes, and incomplete ingestion.

**Outcome:** draw both a scheduled ingestion flow and a live feature ingestion flow. Read [AWS Glue](https://docs.aws.amazon.com/glue/latest/dg/what-is-glue.html).

### Module 04 — Transformation, feature engineering, and feature management

- [ ] Imputation, categorical encoding, scaling/standardization, normalization, binning, log transforms, and feature splitting.
- [ ] Feature interactions, timestamps, text features, and feature selection; determine which transformations suit an algorithm.
- [ ] Fit preprocessing on training data only; apply the same fitted transformation during inference.
- [ ] Use pandas/scikit-learn locally and understand managed preparation with Glue, DataBrew, Data Wrangler, and processing jobs.
- [ ] Feature Store feature groups, record identifiers, event timestamps, ingestion, and online versus offline access.
- [ ] Reuse feature definitions; prevent training-serving skew and future-data leakage in historical training joins.

**Outcome:** build one reusable transformation pipeline and explain online serving versus offline training features. Read [Feature Store](https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store.html) and [preprocessing pitfalls](https://scikit-learn.org/stable/common_pitfalls.html).

### Module 05 — Data quality, labels, imbalance, and fairness

- [ ] Check completeness, type/range validity, uniqueness, referential consistency, freshness, and distribution changes.
- [ ] Define Glue Data Quality rules and decide whether violations warn, quarantine records, or block training.
- [ ] Detect outliers, duplicates, missingness patterns, label errors, and train/test contamination.
- [ ] Use random, stratified, grouped, or chronological splits according to the prediction setting.
- [ ] Labeling/annotation guidelines, reviewer disagreement, human review, and image/text annotation quality.
- [ ] Address imbalance with class weighting, sampling, augmentation, and suitable metrics; apply resampling within training only.
- [ ] Identify representation, selection, historical, and label bias; compare outcomes across relevant groups.
- [ ] Evaluate numeric, text, and image subsets rather than relying on one aggregate score.

**Outcome:** produce a quality report and explain why a high overall accuracy could hide poor minority-class performance. Read [Glue Data Quality](https://docs.aws.amazon.com/glue/latest/dg/glue-data-quality.html).

### Module 06 — Text, embeddings, multimodal data, and FM datasets

- [ ] Parse documents while preserving headings, tables, source identifiers, and useful metadata.
- [ ] Tokenization, context windows, text normalization, image/audio handling, and domain-specific augmentation.
- [ ] Embedding vectors: dimensionality, similarity, model selection, and compatibility between indexing and querying.
- [ ] Chunk size/overlap, semantic boundaries, metadata filters, and how chunking changes recall, context quality, and cost.
- [ ] Configure vector storage concepts using OpenSearch, PostgreSQL/pgvector, or S3 vector capabilities; distinguish object storage from a vector index.
- [ ] Prepare prompt/response datasets for fine-tuning, unlabeled corpora for continued pretraining, and teacher outputs for distillation.
- [ ] Validate formats, deduplicate sources, screen unsafe examples, redact sensitive data, and prevent evaluation-set leakage.

**Outcome:** transform a document collection into traceable chunks and a small retrieval evaluation set. Read [Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html).

## Domain 2 — Model and foundation model development, 24%

### Module 07 — Traditional model and managed AI service selection

- [ ] Linear/logistic regression, decision trees, random forests, gradient boosting/XGBoost, and k-nearest neighbors: suitable data and limitations.
- [ ] Clustering, PCA/dimensionality reduction, anomaly detection, and forecasting: business use cases and evaluation challenges.
- [ ] Neural network, CNN, recurrent network, and transformer intuition; recognize when transfer learning is practical.
- [ ] Familiarize yourself with SageMaker algorithm families: Linear Learner, XGBoost, K-Means, PCA, Random Cut Forest, and DeepAR as useful examples.
- [ ] Compare interpretable baselines with more complex models using quality, training time, inference latency, and maintenance costs.
- [ ] Select Textract for document extraction, Rekognition for visual analysis, Comprehend for text analysis, and Transcribe for speech-to-text.
- [ ] Recognize Translate, Polly, Lex, and Personalize use cases; decide when a managed capability avoids unnecessary custom training.

**Outcome:** choose a reasonable first approach for tabular risk prediction, document extraction, and image classification. Read [SageMaker algorithms](https://docs.aws.amazon.com/sagemaker/latest/dg/algos.html).

### Module 08 — Foundation model choice and customization strategy

- [ ] Compare models by modality, task quality, context length, supported customization, latency, deployment options, and total cost.
- [ ] Understand Bedrock managed model access versus SageMaker model training/hosting responsibilities.
- [ ] Prompt techniques: instructions, few-shot examples, structured output requirements, and versioned prompt templates.
- [ ] Choose prompting for task guidance, RAG for retrieved knowledge, and fine-tuning for learned task behavior; combine techniques when justified.
- [ ] Supervised fine-tuning, parameter-efficient tuning/LoRA intuition, continued pretraining, and distillation; recognize catastrophic forgetting.
- [ ] Retrieval patterns: vector, lexical/hybrid, metadata filtering, and reranking; balance recall against irrelevant context.
- [ ] Evaluate custom code versus managed solutions, pretrained models, and solution templates against the actual requirements.

**Outcome:** justify how to add frequently changing company knowledge and how to teach a consistent output style. Read [Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html) and [model customization](https://docs.aws.amazon.com/bedrock/latest/userguide/custom-models.html).

### Module 09 — SageMaker training execution

- [ ] Studio/workspace concepts; separate development compute, processing jobs, training jobs, and inference resources.
- [ ] Configure data inputs, training script, framework container, dependencies, execution role, hyperparameters, instance type/count, and output location.
- [ ] Understand built-in algorithms versus supported framework script mode and framework/library compatibility.
- [ ] Follow the lifecycle from dataset through job logs to saved artifacts; make inference preprocessing match training.
- [ ] Reproduce a run with a code commit, dependency versions, dataset version, random seed, and configuration.
- [ ] Diagnose shape/type errors, missing dependencies, incompatible data, inaccessible artifacts, memory exhaustion, and job timeouts.

**Outcome:** explain a training job configuration and find the artifact and logs after a run. Read [SageMaker training](https://docs.aws.amazon.com/sagemaker/latest/dg/how-it-works-training.html).

### Module 10 — Hyperparameter tuning and efficient training

- [ ] Epochs, steps, learning rate, batch size, optimizer, tree depth, regularization, and early stopping.
- [ ] Search spaces and objective metrics; compare random, Bayesian, grid, and Hyperband concepts where supported.
- [ ] Configure tuning job budgets, concurrency, metric direction, and stopping criteria.
- [ ] Diagnose loss curves: high learning rate, insufficient capacity, excessive capacity, noisy data, or unsuitable features.
- [ ] Distributed data versus model parallelism; know when communication overhead can erase scaling benefits.
- [ ] Spot training, checkpoints, resume behavior, and interruption tolerance; compare CPU/GPU requirements.
- [ ] Ensembles and cascades: improve quality or reserve expensive models for difficult cases; assess added latency and cost.

**Outcome:** propose a bounded tuning experiment rather than changing many parameters without tracking results. Read [automatic model tuning](https://docs.aws.amazon.com/sagemaker/latest/dg/automatic-model-tuning.html).

### Module 11 — Traditional ML evaluation, explainability, and experiments

- [ ] Confusion matrix, precision, recall, F1, specificity, ROC-AUC, PR-AUC, log loss, and threshold selection.
- [ ] MAE, MSE/RMSE, R², and percentage-error limitations; match a metric to the business penalty.
- [ ] Cross-validation, temporal validation, subgroup evaluation, and baseline comparison; avoid using test data for model selection.
- [ ] Precision = TP/(TP+FP); recall = TP/(TP+FN); F1 = 2PR/(P+R). Work through a small example by hand.
- [ ] Reproducible experiment tracking with MLflow on SageMaker AI: parameters, metrics, artifacts, and run comparison.
- [ ] Global versus local explanations, feature importance, SHAP intuition, and why explanations do not establish causality.
- [ ] Establish a reference performance/data baseline and diagnose poor convergence or validation degradation.

**Outcome:** select a fraud-screening threshold and explain false-positive versus false-negative costs. Read [evaluation metrics](https://scikit-learn.org/stable/modules/model_evaluation.html) and [explainability](https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-model-explainability.html).

### Module 12 — Generative AI and retrieval evaluation

- [ ] Maintain representative questions, expected facts, relevant documents, and difficult/unanswerable cases.
- [ ] Separate retrieval failures from generation failures using retrieval recall/precision and answer relevance/faithfulness.
- [ ] Interpret BLEU/ROUGE overlap, BERTScore/semantic similarity, and their limits as proxies for usefulness or factuality.
- [ ] Evaluate hallucinations, groundedness, safety, bias, citation correctness, and instruction-following.
- [ ] Compare automated metrics, human rubrics, and LLM-as-a-judge; calibrate judge outputs and watch for positional/model biases.
- [ ] Use Bedrock evaluation capabilities, prompt versions, and controlled datasets for repeatable comparisons.
- [ ] Measure end-to-end latency and usage alongside quality so improvements do not hide unacceptable operational cost.

**Outcome:** explain why a fluent answer with a high similarity score can still be unsupported. Read [Bedrock evaluations](https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation.html).

## Domain 3 — Deployment and workflow orchestration, 24%

### Module 13 — Choose an inference and hosting strategy

- [ ] Real-time endpoints for interactive prediction; batch transform for scheduled offline datasets.
- [ ] Asynchronous inference for queued requests whose clients can wait; understand input/output storage and completion handling.
- [ ] Serverless inference for supported intermittent workloads; account for cold starts and feature restrictions.
- [ ] Single-model, multi-model, multi-container, and inference pipeline concepts; distinguish many models from sequential processing stages.
- [ ] Bedrock managed inference versus self-hosted FMs; on-demand versus provisioned capacity and custom model import where supported.
- [ ] Assess payload size, runtime, GPU need, concurrency, latency objective, traffic shape, and model compatibility together.
- [ ] Understand how an externally trained model is packaged and made compatible with its AWS hosting target.

**Outcome:** choose among four SageMaker inference modes for four workload descriptions. Read [deployment options](https://docs.aws.amazon.com/sagemaker/latest/dg/deploy-model.html), [serverless](https://docs.aws.amazon.com/sagemaker/latest/dg/serverless-endpoints.html), and [asynchronous inference](https://docs.aws.amazon.com/sagemaker/latest/dg/async-inference.html).

### Module 14 — Compute, containers, and scaling

- [ ] Select CPU/GPU/accelerator families by memory, compute, compatibility, throughput, and benchmark results.
- [ ] Dockerfile, image dependencies, entry points, inference handlers, health checks, image tags/digests, and ECR.
- [ ] Recognize SageMaker, EC2, ECS, EKS, Lambda, and Batch responsibilities without trying to master every platform.
- [ ] Deploy programmatically using the SageMaker SDK, CLI, or Boto3; distinguish model, endpoint configuration, and endpoint resources.
- [ ] Autoscaling minimum/maximum capacity, target tracking, cooldowns, warmup, and supported scaling metrics.
- [ ] Evaluate invocation load, queue depth, utilization, concurrency, GPU memory, and scaling delay for the chosen serving mode.
- [ ] Diagnose OOM errors, image pull/startup failures, overloaded endpoints, throttling, and unavailable capacity.

**Outcome:** explain why scaling on CPU alone might miss a GPU memory bottleneck. Read [model deployment](https://docs.aws.amazon.com/sagemaker/latest/dg/deploy-model.html) and [training infrastructure](https://docs.aws.amazon.com/sagemaker/latest/dg/train-model.html).

### Module 15 — Release strategies and model lifecycle

- [ ] Model Registry versions, metadata, lineage, approval status, and links to evaluation artifacts.
- [ ] Blue/green, canary, linear traffic shifting, rollback conditions, and deployment alarms.
- [ ] A/B tests send responses from different variants to assigned users; shadow tests evaluate a candidate without returning its responses to users.
- [ ] Compare production and shadow variants on latency/errors and assess model quality with appropriate labels or offline analysis.
- [ ] Keep a deployable previous version and validate that model, preprocessing, and feature schemas remain compatible.
- [ ] Track code, model, dataset, image, configuration, and prompt versions together where applicable.

**Outcome:** describe a deployment that automatically rolls back when latency exceeds its threshold. Read [Model Registry](https://docs.aws.amazon.com/sagemaker/latest/dg/model-registry.html).

### Module 16 — Deploy and operate AI agents

- [ ] Agent loop: model decision, tool request, tool execution, returned observation, and completion.
- [ ] Tool schemas, validation, permissions, timeouts, retries, and safe handling of repeated tool calls.
- [ ] Session state versus persistent memory; isolation between users and correct state recovery.
- [ ] AgentCore runtime, identity, gateway/tool access, memory, and observability concepts; distinguish these from the model itself.
- [ ] Agent/tool communication concepts such as MCP and agent-to-agent interactions; learn protocol purpose rather than obscure wire details.
- [ ] Trace failed tools, coordination errors, runaway loops, truncated streams, and missing context.
- [ ] Bound resource use; version agent code/configuration and verify behavior before promotion.

**Outcome:** draw a document assistant that calls one read-only tool and explain its identity, state, and failure handling. Read [AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html).

### Module 17 — Workflow orchestration and infrastructure as code

- [ ] SageMaker Pipelines: processing, training, evaluation, conditional checks, registration, dependencies, parameters, and caching concepts.
- [ ] Step Functions: states, branching, parallel work, waits, retries, catches, and service integration.
- [ ] EventBridge triggers/schedules; SQS work queues, SNS notifications, and when MWAA/Airflow fits an existing workflow.
- [ ] CloudFormation/CDK: parameterized stacks, outputs, resource dependencies, repeatability, and environment separation.
- [ ] Connect provisioning, workflow execution, and deployment without hard-coded resource identifiers.
- [ ] Retrain on a justified schedule or validated signal; make ingestion and workflow retries idempotent.

**Outcome:** draw a pipeline that only registers a model after passing quality checks. Read [SageMaker Pipelines](https://docs.aws.amazon.com/sagemaker/latest/dg/pipelines.html).

### Module 18 — CI/CD and LLMOps automation

- [ ] Source integration/CodeConnections, CodeBuild, CodePipeline, CodeDeploy, and CodeCommit concepts; diagnose source/build/deployment permission failures.
- [ ] Test transformation code, data contracts, model quality, inference compatibility, and deployment health.
- [ ] Scan code/dependencies/container images; understand Inspector and CodeGuru roles at the selection level.
- [ ] Use approvals and environment-specific settings; protect artifacts, credentials, and deployment roles.
- [ ] Automate prompt regression tests, agent tool tests, FM version promotion, and fine-tuned model rollout.
- [ ] Refresh knowledge bases on source changes and coordinate document, embedding, index, and prompt versions.
- [ ] Keep evaluation gates and rollback procedures for RAG/agent updates as well as traditional model updates.

**Outcome:** explain why a successful build is insufficient evidence to deploy a new model or prompt. Read [Pipelines](https://docs.aws.amazon.com/sagemaker/latest/dg/pipelines.html) and the [official deployment domain](https://docs.aws.amazon.com/aws-certification/latest/machine-learning-engineer-associate-02/machine-learning-engineer-associate-02-domain3.html).

## Domain 4 — Operations, performance, and security, 24%

### Module 19 — Model, data, and workflow monitoring

- [ ] Separate data quality, prediction quality, concept drift, bias changes, and feature-attribution changes.
- [ ] Capture suitable inference inputs/outputs and join predictions with delayed ground-truth labels securely.
- [ ] Establish baselines and scheduled checks; select thresholds and alert actions that avoid excessive false alarms.
- [ ] Understand that a distribution shift does not itself prove predictive quality has degraded.
- [ ] Monitor ingestion freshness, processing failures, inference errors, and retraining workflows.
- [ ] Use evaluation and investigation before retraining; distinguish schema bugs from a real need to update a model.
- [ ] Understand Model Monitor concepts for older material, but use custom drift/evaluation jobs where unavailable.

**Outcome:** propose separate responses to a missing feature, changed input distribution, and declining labeled recall. Read [Model Monitor concepts and availability](https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor.html).

### Module 20 — Observability for ML, RAG, and agents

- [ ] CloudWatch metrics/logs/alarms/dashboards; distinguish observability from CloudTrail audit history.
- [ ] p50/p95/p99 latency, throughput, errors, throttling, queue age, saturation, and resource utilization.
- [ ] Trace an application through retrieval, generation, and tools using supported tracing, including X-Ray/AgentCore observability concepts.
- [ ] Track retrieval misses, stale documents, time to first token, completion failures, tokens, and end-to-end task success.
- [ ] Detect tool errors, session failures, broken agent coordination, repeated calls, and partial streaming results.
- [ ] Build actionable dashboards and runbooks: symptom, probable causes, evidence to collect, and corrective action.

**Outcome:** locate whether a slow answer came from retrieval, inference, or a downstream tool. Read [CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html) and [AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html).

### Module 21 — IAM, network isolation, encryption, and audit

- [ ] Execution roles versus user roles; trust, resource policies, explicit deny, `iam:PassRole`, and cross-account basics.
- [ ] Use appropriate temporary IAM credentials for workloads; understand Bedrock API key alternatives and their management requirements.
- [ ] Separate training, inference, data, and deployment permissions; scope access to required actions and resources.
- [ ] Protect data/artifacts using TLS, encryption at rest, KMS key policies, secret storage, and controlled sharing.
- [ ] Configure VPC subnets/security groups and private access paths; distinguish network reachability from authorization.
- [ ] CloudTrail for API activity, Config for resource configuration/compliance, and CloudWatch for operational telemetry.
- [ ] Debug AccessDenied, role trust failures, S3/KMS policy issues, missing routes, endpoint policy restrictions, and blocked connections.

**Outcome:** explain why S3 permission alone might not allow a role to read a KMS-encrypted object. Read [IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html) and [SageMaker VPC access](https://docs.aws.amazon.com/sagemaker/latest/dg/infrastructure-give-access.html).

### Module 22 — Cost and performance optimization

- [ ] Right-size development, training, and serving resources; benchmark before choosing a larger instance.
- [ ] Compare on-demand, Spot, and applicable commitment-based purchasing options by interruption tolerance and usage stability.
- [ ] Reduce idle capacity, tune autoscaling, batch suitable requests, reuse results, and avoid unnecessary data transfers.
- [ ] Understand Cost Explorer analysis, Budgets alerts/actions, cost allocation tags, and usage/service quotas as different tools.
- [ ] Estimate FM input/output token costs plus retrieval, embeddings, reranking, vector storage, and agent tool/runtime costs.
- [ ] Evaluate smaller models, prompt length, output limits, caching, and repeated agent calls while retaining required quality.
- [ ] Track cost per successful task rather than cost per request alone.

**Outcome:** explain why a cheaper model could increase total cost if it needs more retries or tool calls. Read [AWS Budgets](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html) and [Bedrock inference](https://docs.aws.amazon.com/bedrock/latest/userguide/inference.html).

### Module 23 — Responsible AI and application safeguards

- [ ] Distinguish IAM/network controls from safeguards on model inputs and outputs.
- [ ] Bedrock Guardrails concepts: harmful-content filtering, denied topics, word filters, sensitive information handling, and grounding-related checks.
- [ ] Prompt injection, untrusted retrieved content, accidental disclosure, and excessive tool permissions.
- [ ] Enforce authorization during retrieval and tool execution; do not rely on a prompt to enforce access boundaries.
- [ ] Redact data from logs where appropriate; consider retention, consent, data provenance, and auditable review.
- [ ] Evaluate subgroup fairness, human escalation, refusal behavior, and safeguards against application-specific misuse.
- [ ] Validate code/image vulnerabilities and configuration controls throughout the release process.

**Outcome:** propose layered controls for a document assistant handling sensitive records. Read [Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html).

## When a module is complete

For each module, retain: a short explanation in your own words, one worked example or configuration sketch, one failure and diagnosis, one service comparison, and corrected practice questions. Use [the labs](02_STUDY_PLAN_AND_LABS.md) and [readiness checks](04_EXAM_READINESS.md) to verify understanding.
