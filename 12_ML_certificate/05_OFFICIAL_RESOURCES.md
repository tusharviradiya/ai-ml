# Official resources and reading order

Exam/technical references reviewed on **4 November 2026**. Skill Builder integration added **5 November 2026**: see [the Premium resource audit](06_SKILL_BUILDER_PREMIUM_PLAN.md) for course/lab links, access evidence, classroom distinctions, and module mapping; see [the tracker](07_SKILL_BUILDER_TRACKER.md) for personal access and completion evidence. The audit supplements these technical references; it does not establish personal entitlement. You do not need to read every linked developer guide from beginning to end.

## Exam authority

| Resource | Use it for |
|---|---|
| [MLA-C02 exam guide](https://docs.aws.amazon.com/aws-certification/latest/machine-learning-engineer-associate-02/machine-learning-engineer-associate-02.html) | Candidate profile, scoring description, domain weights, and scope |
| [Domain 1](https://docs.aws.amazon.com/aws-certification/latest/machine-learning-engineer-associate-02/machine-learning-engineer-associate-02-domain1.html) | Exact data preparation tasks and numbered skills |
| [Domain 2](https://docs.aws.amazon.com/aws-certification/latest/machine-learning-engineer-associate-02/machine-learning-engineer-associate-02-domain2.html) | Exact modeling, training, and evaluation tasks |
| [Domain 3](https://docs.aws.amazon.com/aws-certification/latest/machine-learning-engineer-associate-02/machine-learning-engineer-associate-02-domain3.html) | Exact deployment and automation tasks |
| [Domain 4](https://docs.aws.amazon.com/aws-certification/latest/machine-learning-engineer-associate-02/machine-learning-engineer-associate-02-domain4.html) | Exact operations, cost, and security tasks |
| [In-scope services](https://docs.aws.amazon.com/aws-certification/latest/machine-learning-engineer-associate-02/mla-02-in-scope-services.html) | Service inventory; review for scope changes |
| [Out-of-scope services](https://docs.aws.amazon.com/aws-certification/latest/machine-learning-engineer-associate-02/mla-02-out-of-scope-services.html) | Avoid spending study time on unrelated AWS products |
| [C01 versus C02 comparison](https://docs.aws.amazon.com/aws-certification/latest/machine-learning-engineer-associate-02/mla-02-comparison.html) | Check older courses for missing or outdated coverage |
| [Certification overview and registration](https://aws.amazon.com/certification/certified-machine-learning-engineer-associate/) | Current beta/availability, format, price, and scheduling links |
| [MLA-C02 Skill Builder preparation](https://skillbuilder.aws/category/exam-prep/machine-learning-engineer-associate-MLA-C02) | Version-specific preparation and practice resources |
| [Certification general information](https://aws.amazon.com/certification/policies/general-information/) | AWS service abbreviations and exam information |

AWS describes some specialist architecture/strategy tasks as outside the target candidate role. The practice capstones in this folder are learning exercises integrating the individual engineering skills; they do not mean broad expert-level architecture is an additional exam requirement.

## Data and traditional ML

| Resource | Study questions |
|---|---|
| [AWS Glue overview](https://docs.aws.amazon.com/glue/latest/dg/what-is-glue.html) | How are data discovery, cataloging, transformation, and movement handled? |
| [Glue Data Quality](https://docs.aws.amazon.com/glue/latest/dg/glue-data-quality.html) | How do rules quantify and gate dataset quality? |
| [SageMaker AI overview](https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html) | Which parts of the ML lifecycle does the service manage? |
| [Feature Store](https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store.html) | How do feature groups and online/offline access support consistent features? |
| [Algorithms and pretrained models](https://docs.aws.amazon.com/sagemaker/latest/dg/algos.html) | Which algorithm families suit which business/data problems? |
| [Managed training](https://docs.aws.amazon.com/sagemaker/latest/dg/how-it-works-training.html) | What must a training job specify, and what does AWS manage? |
| [Training workflow and features](https://docs.aws.amazon.com/sagemaker/latest/dg/train-model.html) | How do data, containers, jobs, and model artifacts connect? |
| [Automatic model tuning](https://docs.aws.amazon.com/sagemaker/latest/dg/automatic-model-tuning.html) | How are search spaces, metrics, trials, and stopping configured? |
| [scikit-learn metrics](https://scikit-learn.org/stable/modules/model_evaluation.html) | Which metric answers the actual prediction problem? |
| [scikit-learn common pitfalls](https://scikit-learn.org/stable/common_pitfalls.html) | How do inconsistent preprocessing and leakage invalidate evaluation? |

The scikit-learn links are primary library documentation for supporting ML concepts, not AWS exam scope documents.

## Foundation models, RAG, and agents

| Resource | Study questions |
|---|---|
| [Bedrock overview](https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html) | What does managed FM access provide? |
| [Bedrock inference](https://docs.aws.amazon.com/bedrock/latest/userguide/inference.html) | How are invocation, permissions, and request interfaces configured? |
| [Model customization](https://docs.aws.amazon.com/bedrock/latest/userguide/custom-models.html) | What changes when customizing model parameters, and which methods fit the task? |
| [Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html) | How do ingestion, indexing, retrieval, and grounding fit together? |
| [Bedrock evaluations](https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation.html) | How are models and retrieval/generation quality evaluated? |
| [AgentCore overview](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html) | How are agent runtime, tools, identity, state, and observability supported? |
| [Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) | Which safeguards address harmful content, sensitive information, and application policies? |

Learn capability and tradeoff concepts rather than memorizing a changing list of FM provider names or model identifiers. Check support and access before implementing a lab.

## Deployment, operations, and security

| Resource | Study questions |
|---|---|
| [Model deployment](https://docs.aws.amazon.com/sagemaker/latest/dg/deploy-model.html) | Which inference mode fits latency, traffic, and operational requirements? |
| [Serverless inference](https://docs.aws.amazon.com/sagemaker/latest/dg/serverless-endpoints.html) | When are automatic capacity and cold-start tradeoffs acceptable? |
| [Asynchronous inference](https://docs.aws.amazon.com/sagemaker/latest/dg/async-inference.html) | How do queued requests, S3 payloads, and later results work? |
| [SageMaker Pipelines](https://docs.aws.amazon.com/sagemaker/latest/dg/pipelines.html) | How are repeatable ML workflows orchestrated? |
| [Model Registry](https://docs.aws.amazon.com/sagemaker/latest/dg/model-registry.html) | How are model versions, metrics, approvals, and deployment tracked? |
| [CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html) | How do metrics, logs, alarms, and dashboards support diagnosis? |
| [IAM best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html) | How are roles, temporary credentials, and least privilege applied? |
| [SageMaker VPC resource access](https://docs.aws.amazon.com/sagemaker/latest/dg/infrastructure-give-access.html) | How do job/container network paths reach private data? |
| [AWS Budgets](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html) | How do cost tracking, alerts, and configured actions work? |

## Availability notes for older tutorials

The documentation currently states that [Model Monitor](https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor.html), [Clarify](https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-model-explainability.html), and [Bedrock Agents Classic](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html) are not open to new customers. This affects whether you can reproduce an older hands-on tutorial. It does not remove the need to understand monitoring, explainability, fairness, or agents.

Follow current service documentation for implementation and the current exam outline for scope. The study plan supplies alternative exercise paths where access is restricted.

## Keep this roadmap current

Before booking, revisit the certification overview and domain pages. Update the study checklist if numbered skills or scope change. Reconfirm beta/general availability details and question timing. When choosing a course or practice set, verify that it explicitly covers MLA-C02 and the GenAI/agent additions.
