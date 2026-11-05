# Skill Builder Premium integration and plan review

Revised **5 November 2026**. Goal: practical AWS development plus MLA-C02 preparation, using the learner's reported active student Premium subscription. This supersedes the earlier chat-only/resource-optional learning arrangement. We still assign one task at a time and review evidence before advancing.

**Preparation deadline: 30 November 2026; exam date: 29 December 2026.** The learner confirmed **2–3 hours daily** and December M.Tech exams. Follow the [active November plan](08_NOVEMBER_COMPLETION_PLAN.md), which supersedes the 16-week calendar. Prioritize selected core course units, focused labs and integrated projects within 52–78 available hours. Full optional depth courses remain a separate backlog; no required AWS study is allocated in December. Readiness is assessed from evidence, not the deadline.

## Review of the previous plan

| Finding | Revision |
|---|---|
| The syllabus covers the four exam domains, but subscription resources were only loosely referenced. | Map named training resources to modules and lab deliverables below. |
| Labs were exercise specifications, not a sequence of available hosted labs. | Start with a suitable Skill Builder environment, then independently reproduce or extend the work. |
| The first assignment exposed gaps in feature timing, leakage, and training versus inference. | Keep a short foundations checkpoint. Do not infer broad coding/cloud proficiency from repository contents. |
| A fixed 16-week estimate was made without knowing completed courses or available time. | Use milestone gates; the schedule is a provisional sequence, not a deadline. |
| Practical application development was mostly supporting knowledge. | Add an early serverless ingestion project with SDKs, infrastructure as code, errors/retries, tests, and operational evidence. |
| Integrated projects and incident exercises arrived late. | Build a small vertical slice early; add quality gates, permissions, observability, and rollback incrementally. |
| Course completion and demonstrated skill were not tracked separately. | Track access, completion, independent evidence, and tutor review separately in the resource tracker. |
| Live classes, Digital Classroom, hosted lab costs, and student entitlements were not distinguished. | Apply the access policy below before selecting any resource. |

The basic opening lesson is appropriate for the demonstrated gaps. Staying at that level for weeks would not meet the practical goal. Progression will depend on explanations, working artifacts, and troubleshooting—not video hours.

## What is verified, and what remains unknown

**Publicly verified is not account-verified.** I can inspect public AWS documentation and indexed catalog listings, but cannot see your signed-in entitlements, completed courses, subscription expiry, or launch a lab in your account. Some Skill Builder pages returned JavaScript-only screens; where used, indexed catalog metadata is identified below. No enrollment or launch was performed.

Use these evidence labels:

- **F — Public free listing:** the item explicitly lists free access. Sign-in can still be required.
- **S — Public subscription evidence:** AWS identifies the resource/category as subscriber training. Student-account access remains unverified.
- **A — Annual/team condition:** Digital Classroom is publicly described as an annual/team benefit. Student Premium equivalence is not assumed.
- **C — Check current listing/access:** title/topic is documented, but current availability, exact tier, or individual assessment is not established.

No paid resource is marked personally accessible until you confirm that its signed-in page permits launch without a purchase. All personal-access entries start as unknown.

| Resource type | Public evidence and how we will use it |
|---|---|
| Guided AWS Builder Labs | Subscription offerings include hosted guided labs. Prefer these for first exposure to real AWS resources. Some foundational content is free. |
| Cloud Quest / SimuLearn | Use selected relevant assignments for requirements, service choices, and implementations. They are alternatives for overlapping content, not two mandatory full tracks. |
| Digital Classroom | Self-paced instructor-delivered material; use selected developer/MLOps modules after prerequisites and access confirmation. |
| Live Classroom Training | A separate instructor-led product. Not established as included in the student's Premium entitlement; exclude from required work unless a separate entitlement is confirmed. |
| Certification preparation | The current MLA-C02 plan is public; some components require a subscription. Verify each assessment's version and availability. |
| Lab Tutorials in your own account | Training access does not cover AWS resource usage in your account. They differ from temporary hosted Builder Lab environments. |

Sources: [subscription comparison](https://skillbuilder.aws/subscriptions), [AWS digital training formats](https://aws.amazon.com/training/digital/), [digital training FAQ](https://skillbuilder.aws/support/faq/digital-training), and an [AWS employee's student Premium overview](https://builder.aws.com/content/3INXkQMOPfAJSUkkIr3eHXsLai4). The student overview supports using guided labs and role-based experiences; it is not an exhaustive student entitlement contract.

## Prioritized resources

Links marked **catalog search** are discovery links, not direct course pages. Legacy direct links may redirect to catalog search. No course IDs have been guessed. Durations are indicative public catalog values, not our study-time estimates.

| ID / priority | Exact resource name and link | Evidence | Placement and practical purpose |
|---|---|---|---|
| R01 / Now, targeted | [Fundamentals of Machine Learning and Artificial Intelligence](https://skillbuilder.aws/learn/16ASDUHF86/fundamentals-of-machine-learning-and-artificial-intelligence/M7JZCTA94N) | **F**, indexed item says Free; about 1 hour | Module 00. Review supervised learning and lifecycle terms; use our correction exercise to demonstrate understanding. Skip already-mastered sections. |
| R02 / Early | [AWS Technical Essentials — catalog search](https://skillbuilder.aws/search?searchText=AWS%20Technical%20Essentials) | **C**, digital course exists; verify chosen variant's access | Module 01 and Lab 01. Select the digital course, not the identically named live class. Assess existing progress before repeating basics. |
| R03 / Core | [AWS ML Engineer Associate Learning Plan (includes labs)](https://explore.skillbuilder.aws/learn/public/learning_plan/view/2224/aws-ml-engineer-associate-learning-plan-includes-labs) | **S**, paid plan announced by AWS; current indexed catalog describes updated ML/GenAI coverage | Modules 02–23. Main role-training backbone. Use relevant components in our module order, not the entire advanced plan immediately. Current catalog: about 25h25m; verify its outline after sign-in. |
| R04 / Data lab candidate | [Lab – Analyze and Prepare Data with Amazon SageMaker Data Wrangler and Amazon EMR](https://explore.skillbuilder.aws/learn/course/external/view/elearning/19744/lab-analyze-and-prepare-data-with-amazon-sagemaker-data-wrangler-and-amazon-emr) | **C**, linked by AWS's ML training page; legacy link redirects | Modules 03–04, Labs 02/04. Inspect transformations and document one reusable feature pipeline. Use current R03 data labs if this legacy lab is unavailable. |
| R05 / Streaming | [Lab – Transform Data with Amazon Data Firehose](https://skillbuilder.aws/learn/42V835HNCZ/lab-transform-data-with-amazon-data-firehose/JB9EA6J98V) | **S**, AWS subscriber-lab announcement; direct redirect resolved, launch unverified | Module 03, Lab 03. Transform events and inspect bad-record handling. This does not replace learning stream replay/stateful processing. |
| R06 / Developer lab | [Lab – Create Queues and Handle Messages using Amazon Simple Queue Service (Amazon SQS)](https://skillbuilder.aws/learn/JNYEQ1XUDD/lab-create-queues-and-handle-messages-using-amazon-simple-queue-service-amazon-sqs/JNYEQ1XUDD) | **S**, AWS subscriber-lab announcement; launch unverified | Modules 01/17. Practice message handling before building the serverless project. |
| R07 / Core GenAI lab course | [Building Generative AI Applications Using Amazon Bedrock (Includes Labs)](https://skillbuilder.aws/learn/K5FK8EE82U/building-generative-ai-applications-using-amazon-bedrock-includes-labs/UX8DFX691K) | **S**, indexed item says Subscription Needed; about 9 hours | Modules 06/08/12/16/23, Labs 08–10. Start after Python, AWS access, Lambda, Bedrock, and prompt fundamentals. Favor this hosted-lab variant over the similarly named own-account walkthrough. |
| R08 / Selected applied practice | [AWS Cloud Quest: Machine Learning — catalog search](https://skillbuilder.aws/search?searchText=AWS%20Cloud%20Quest%3A%20Machine%20Learning) | **S**, current indexed catalog and Cloud Quest documentation identify subscription access | Choose data ingestion, model hosting, and anomaly-detection assignments to complement gaps. Do not require every broad AI assignment just to collect a badge. |
| R09 / Alternative applied practice | [AWS SimuLearn: Bring Your Own Model — catalog search](https://skillbuilder.aws/search?searchText=AWS%20SimuLearn%3A%20Bring%20Your%20Own%20Model) | **S**, indexed catalog labels Subscription | Modules 13–14, Lab 06. Explain a customer's hosting requirement, implement it, then compare with our own inference design. Use instead of overlapping R08 work. |
| R10 / Developer depth | [Digital Classroom - Developing on AWS — catalog search](https://skillbuilder.aws/search?searchText=Digital%20Classroom%20Developing%20on%20AWS) | **A**, catalog confirms subscription course; annual/team category rule | Modules 01/14/17/18. Select SDK/CLI, application deployment, debugging, and relevant lab units. Requires programming readiness. |
| R11 / MLOps depth | [Digital Classroom - MLOps Engineering on AWS — catalog search](https://skillbuilder.aws/search?searchText=Digital%20Classroom%20MLOps%20Engineering%20on%20AWS) | **A**, catalog and AWS launch announcement | Modules 15/17–20, Lab 07 and Capstone A. Reinforce automation and operational maturity after an initial working training/serving flow. |
| R12 / Optional GenAI alternative | [Digital Classroom - Developing Generative AI Applications on AWS — catalog search](https://skillbuilder.aws/search?searchText=Digital%20Classroom%20Developing%20Generative%20AI%20Applications%20on%20AWS) | **A**, catalog and AWS announcements | Select for deeper instructor explanation if accessible; overlaps R07. Do not require both full courses. |
| R13 / Optional development extension | [Digital Classroom - Developing Serverless Solutions on AWS — catalog search](https://skillbuilder.aws/search?searchText=Digital%20Classroom%20Developing%20Serverless%20Solutions%20on%20AWS) | **A**, catalog lists subscription course | Extend the serverless project with deployment practices and failure handling. Selected units only; broader than exam scope. |
| R14 / Certification backbone | [Exam Prep Plan: AWS Certified Machine Learning Engineer - Associate (MLA-C02 - English)](https://skillbuilder.aws/learning-plan/XGYSGHMJD2/exam-prep-plan-aws-certified-machine-learning-engineer--associate-mlac02--english/5FD2DC27G1) | **S**, indexed current plan explicitly says some components require subscription | Review overview early, domain reviews after implementation, and readiness assessments near the end. Do not use the retired C01 prep plan. |
| R15 / Question format and later review | [Official Practice Question Set: AWS Certified Machine Learning - Associate (MLA-C02 - English)](https://skillbuilder.aws/learn/FCCHUGZKPJ/variant/6HKC8HDE5C) | **F**, indexed item says Free; 20 questions | Learn question format after fundamentals; retain first-attempt results. Repeated identical items do not measure fresh readiness. |
| R16 / Conditional assessments | Official Pretest / Official Practice Exam for MLA-C02 — locate inside **R14** | **C**, subscription supports assessments generally; exact current MLA-C02 items not independently verified | Use a pretest after initial domain exposure if available; save a practice exam for later. Check exact title, C02 version, format, and account launch before scheduling. Do not substitute a C01 test silently. |

Public catalog details for R03: [current role-plan listing](https://skillbuilder.aws/search?category=learning_plan&examCertificationName=AWS+Certified+Machine+Learning+Engineer+-+Associate&page=1). R03/R04 are linked from [AWS ML training recommendations](https://aws.amazon.com/ai/learn/machine-learning-specialist/). R05/R06/R11 are supported by the [AWS April 2025 training announcement](https://aws.amazon.com/blogs/training-and-certification/april-2025-new-offerings//). R08 also has [current Cloud Quest documentation](https://docs.cloudquest.skillbuilder.aws/coming-soon/index.html). Classroom catalogs can change; use the matching English course title and product type, then record the resolved item URL.

Course content may use older service interfaces. For example, the Bedrock course description includes Agents, while current documentation describes restrictions on Agents Classic for new customers. Use the supplied training environment when supported; for an independent project, use currently available AgentCore functionality rather than assuming tutorial access. The same caution applies to older Clarify/Model Monitor labs.

## Revised learning sequence and completion gates

| Stage | Resources and modules | Required evidence before advancing |
|---|---|---|
| 0. Establish access and starting level | R01/R02 as needed; Modules 00–01 | Resource tracker updated with launch/access observations; Assignment 001 correction reviewed; short coding/AWS diagnostic before advanced labs |
| 1. Build a small AWS application | R06 and selected R10 units if accessible | Project P0 below: functional SDK calls, deployed or hosted-lab slice, basic tests, logs, permission explanation, cleanup |
| 2. Prepare reliable data | R03 data components, R04/R05 where available; Modules 02–06 | Existing Labs 02–04 plus independent transformation, schema/quality checks, and failure diagnosis |
| 3. Train, evaluate, and serve | R03 model/hosting components; selected R08 or R09 | Existing Labs 05/06/09: reproducible baseline, metrics, tuning comparison, chosen serving mode, valid inference |
| 4. Automate and operate | R03 operations, R11 units if accessible; Modules 15/17–23 | Lab 07 and Capstone A: quality gate, registry/versioning, rollback, delayed-label monitoring, IAM/network diagnosis |
| 5. Build grounded AI and agents | R07; R12 only as an alternative/targeted supplement | Labs 08–12 and Capstone B: retrieval evaluation, tool failure recovery, access controls, traces, refresh/versioning, cost analysis |
| 6. Demonstrate exam readiness | R14/R15 and R16 if available | Domain error log, fresh timed assessments, independent tradeoff explanations, review against current exam outline |

Earlier guided/cloud labs contribute to later projects, so we will not repeat them merely to complete multiple plans. Optional developer extensions can continue after exam readiness.

## Practical projects and stronger acceptance criteria

**P0 — Serverless document intake, built incrementally.** Upload synthetic documents to S3; process metadata with Lambda; store job status in DynamoDB; introduce SQS for decoupling/retries; expose a status API when ready. Start with one upload and a successful log entry. Add SDK/CLI use, structured logs, malformed-event handling, duplicate-message handling, least-privilege roles, and a small CDK/CloudFormation definition. Retain code, diagram, test results, failure notes, and cost/cleanup evidence. These are authored project requirements, not claims that a named course includes this exact project.

**Capstone A — ML service.** Retain the existing classification capstone. Add an application interface, versioned data/configuration, automated quality gate, a tested release failure/rollback, and a runbook distinguishing bad inputs, poor model quality, and unavailable infrastructure. Complete one meaningful extension without step-by-step instructions.

**Capstone B — Grounded assistant.** Retain the document assistant. Add a fixed retrieval/answer evaluation set, authorized retrieval/tool use, prompt injection tests, source refresh, per-stage latency/cost measurements, and an agent/tool failure trace. Explain what changed and why the evidence supports the result.

Temporary hosted labs may not allow all services, persistent resources, exports, or independent modifications. Respect lab limits. Save permitted code/configuration and sanitized results before the session ends. If independent reproduction needs an own-account deployment, plan that separately with explicit cost estimates and resource cleanup; subscription access does not establish cloud credits.

## How we will use Premium each week

Target roughly **20% explanation/course material, 60% building/debugging, and 20% recall/review**. Adjust while foundations are being repaired. A learning cycle is: my explanation → selected course segment or lab → your implementation → a small variation/failure investigation → my review and progress update. Course completion alone never marks a module mastered.

Prefer subscriber labs and selected depth courses over spending the subscription period on free videos alone. Before choosing a new course, inspect overlap with R03/R07 and existing progress. Rebuild a meaningful part independently instead of doing two nearly identical guided labs.

For Jam/challenge/microcredential offerings, treat them as optional demonstrations after the relevant projects. The exact event, prerequisites, attempts, and student entitlement must be checked; none is assumed included or assigned now. Live classroom seats and actual certification exam fees are also outside the confirmed benefits in this review.

## Current next step

Learning progression remains on hold at the learner's request while this plan is reviewed. Assignment 001 is preserved and incomplete. The only immediate planning check is the short account/course inventory in [07_SKILL_BUILDER_TRACKER.md](07_SKILL_BUILDER_TRACKER.md). We will use the learner's current courses rather than requiring a restart. When learning resumes, review the pending correction and assign one suitable course segment or lab—not this entire catalog.
