# AWS services checklist

Use the [official in-scope list](https://docs.aws.amazon.com/aws-certification/latest/machine-learning-engineer-associate-02/mla-02-in-scope-services.html) for scope. AWS says the list can change and is non-exhaustive. Listing a service does not specify how many questions it receives.

## Suggested study depth

These priorities are study recommendations, not AWS-published service weights.

| Depth | How to study | Main focus |
|---|---|---|
| Deep | Configure a small example, troubleshoot it, and explain alternatives | SageMaker AI lifecycle; Bedrock models/RAG/evaluation/guardrails; AgentCore concepts; S3; IAM; CloudWatch; Glue; VPC |
| Working | Explain configuration, integrations, failure modes, and selection criteria | Feature Store; model registry; Pipelines; MLflow; Athena; streaming services; Step Functions; EventBridge; ECR/Docker; CI/CD; IaC; KMS; CloudTrail; cost tools |
| Recognition | Know purpose, relevant ML/AI use cases, and when it fits better than a custom solution | Remaining managed AI, database, analytics, storage, and governance offerings in the inventory |

Recognition-level topics still need review. Increase depth when practice questions reveal a gap.

## Inventory from the official list

For compactness, common AWS/Amazon prefixes are omitted below. A checked category means you can identify the purpose and relevant use case of every service in it.

| Done | Category | Services/features |
|---|---|---|
| [ ] | Analytics | Athena; Data Firehose; EMR; Glue; Glue DataBrew; Glue Data Quality; Kinesis; Lake Formation; Managed Service for Apache Flink; OpenSearch Service; Quick; Redshift |
| [ ] | Application integration | EventBridge; MWAA; SNS; SQS; Step Functions |
| [ ] | Financial management | Billing and Cost Management; Budgets; Cost Explorer |
| [ ] | Compute | Batch; EC2; Lambda |
| [ ] | Containers | ECR; ECS; EKS |
| [ ] | Databases | DocumentDB; DynamoDB; ElastiCache; Neptune; RDS |
| [ ] | Developer tools | CDK; CodeArtifact; CodeBuild; CodeCommit; CodeConnections; CodeDeploy; CodePipeline; X-Ray |
| [ ] | ML and AI | Bedrock; Bedrock AgentCore; CodeGuru; Comprehend; Comprehend Medical; DevOps Guru; HealthLake; Lex; Personalize; Polly; Rekognition; SageMaker AI; Textract; Transcribe; Translate |
| [ ] | Management/governance | Auto Scaling; CloudFormation; CloudTrail; CloudWatch; Compute Optimizer; Config; Organizations; Service Catalog; Systems Manager; Trusted Advisor |
| [ ] | Media | Kinesis Video Streams |
| [ ] | Migration/transfer | DataSync |
| [ ] | Networking | API Gateway; CloudFront; Direct Connect; VPC |
| [ ] | Security | IAM; Inspector; KMS; Macie; Secrets Manager |
| [ ] | Storage | EBS; EFS; FSx; S3; S3 Glacier; Storage Gateway |

This inventory follows [AWS's published categories](https://docs.aws.amazon.com/aws-certification/latest/machine-learning-engineer-associate-02/mla-02-in-scope-services.html), including the name Amazon Quick shown there at the time of review. Kafka and pgvector also occur in domain skills; do not restrict preparation to product names in this table.

## Feature-level study checklist

### SageMaker AI

- [ ] Data preparation and processing jobs; development versus job versus hosting compute.
- [ ] Feature groups, online/offline stores, ingestion, and feature consistency.
- [ ] Built-in algorithms, framework script mode, inputs/artifacts, logs, tuning, and efficient training.
- [ ] Experiment tracking and reproducible evaluation.
- [ ] Batch, real-time, asynchronous, and serverless inference; model/endpoint configuration.
- [ ] Registry, approvals, lineage, pipeline quality gates, deployment variants, and rollback.
- [ ] Capture/evaluate production data; understand historical Model Monitor/Clarify references and current access restrictions.

References: [SageMaker overview](https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html), [training](https://docs.aws.amazon.com/sagemaker/latest/dg/train-model.html), [deployment](https://docs.aws.amazon.com/sagemaker/latest/dg/deploy-model.html).

### Bedrock and AgentCore

- [ ] Model selection, invocation permissions, inference settings, and capacity choices.
- [ ] Prompt templates/versioning; fine-tuning, continued pretraining, distillation, and custom model import concepts.
- [ ] Knowledge bases, source ingestion, document processing, embeddings, vector retrieval, filters, reranking, and refresh.
- [ ] Model/RAG evaluation, human assessment, and cost/quality/latency comparisons.
- [ ] Guardrails, sensitive data handling, agent/tool identities, session state, tracing, and resource limits.

References: [Bedrock overview](https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html), [Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html), [AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html).

## Comparisons to practice

For each pair or group, write a requirement where one option is preferable and identify the deciding constraint.

| Compare | Deciding questions |
|---|---|
| S3 / EBS / EFS / FSx | Object, attached block, or shared filesystem? Throughput and lifecycle needs? |
| CSV/JSON / Parquet/ORC | Exchange format or analytical scanning? Schema and column access? |
| Glue / EMR / Athena | Transform, run a controlled distributed platform, or query data? |
| Data Streams / Firehose / Flink / Kafka | Consume/replay events, deliver data, or perform stateful stream processing? |
| Feature store / vector store | Reusable predictive features or similarity retrieval over embeddings? |
| SageMaker AI / Bedrock / specialized AI API | Custom training/hosting, managed FM access, or a predefined AI task? |
| Prompting / RAG / fine-tuning | Instructions, changing external knowledge, or learned task behavior? |
| Real-time / batch / async / serverless | Interactive deadline, offline schedule, queued long work, or intermittent compatible traffic? |
| A/B / shadow / canary | Compare user outcomes, observe a candidate, or gradually release? |
| Pipelines / Step Functions / CodePipeline | ML job workflow, general service workflow, or software delivery? |
| CloudWatch / CloudTrail / Config | Operational telemetry, API audit, or configuration history/compliance? |
| IAM / KMS / Guardrails | Authorization, cryptographic access, or model-content safeguards? |
| Budgets / Cost Explorer / service quotas | Spending notification/action, analysis, or resource/API limit? |

Use the topic checklist and [official technical resources](05_OFFICIAL_RESOURCES.md) to verify your answers. Avoid treating a short comparison as a universal rule: supported features, runtime requirements, and account/Region availability can change the choice.
