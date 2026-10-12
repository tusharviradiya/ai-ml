# ML System Design Interview Prep Sheet

For Applied ML Engineer and Product ML Engineer roles at product-based companies.

This sheet is a sequenced set of 16 problems, from beginner to advanced. Each problem lists its difficulty, the concepts it tests, the components a strong answer should include, and what to study. Work through it in order. Early problems build the framework you reuse in every later one.

Priority markers:
- **P0** = very likely in your target loops. Master these.
- **P1** = common. Know them well.
- **P2** = good depth for senior or stronger candidates.

---

## Contents

- [How to use this sheet](#how-to-use-this-sheet)
- [The core framework](#the-core-framework)
- [Level 1: Beginner](#level-1-beginner)
- [Level 2: Intermediate](#level-2-intermediate)
- [Level 3: Advanced](#level-3-advanced)
- [Cross-cutting concepts checklist](#cross-cutting-concepts-checklist)
- [Practice routine](#practice-routine)

---

## How to use this sheet

1. **Learn the framework first** (below). Every problem in this sheet follows it.
2. **Practice out loud, not on paper.** Set a 35 to 45 minute timer and talk through the design as if to an interviewer. Record yourself once a week.
3. **Draw the diagram in every session.** Boxes, arrows, data stores, and the offline/online split. Diagrams are how interviewers follow your thinking.
4. **Write a one-page summary after each problem:** the key tradeoffs you chose and why, and what you would change at 10x scale.
5. **Revisit P0 problems after two weeks** without notes. Recall beats re-reading.

---

## The core framework

Use this structure for every problem. Spend about 5 minutes on steps 1 to 2, 25 minutes on steps 3 to 7, and the rest on follow-ups.

| Step | What to cover | Typical questions to answer |
|---|---|---|
| 1. Clarify requirements | Functional goals, scope, users, and constraints | Who uses it? What counts as success? What is out of scope? |
| 2. Define metrics | Business metric, online metrics, offline metrics, guardrails | What do we optimize? What could go wrong if we optimize it? |
| 3. Frame the ML problem | Task type (classification, ranking, retrieval), labels, and the decision being made | Is this a binary label or a ranking? What is the training target? |
| 4. Data and features | Data sources, labeling strategy, feature types, and freshness | Which signals are available at serving time? How do we avoid leakage? |
| 5. Model choice | Baseline first, then the model you would actually ship, and why | Why not a simpler model? What are the latency and cost limits? |
| 6. Serving architecture | Online and offline paths, candidate generation, ranking, caching, latency budget | How fast must it respond? What happens at peak traffic? |
| 7. Evaluation and experimentation | Offline evaluation, A/B test design, rollout plan | How do we know it works? How do we ship it safely? |
| 8. Monitoring and iteration | Data drift, model drift, alerting, retraining cadence, feedback loops | How do we detect that it broke? How often do we retrain? |

**Two habits that separate strong candidates:**
- **Name the tradeoffs explicitly.** For each decision, say what you gain and what you give up.
- **Start simple, then scale.** Propose a baseline first, then say what breaks at 10x or 100x traffic and how you would address it.

---

## Level 1: Beginner

These problems establish the framework. Keep the models simple and focus on structure, metrics, and data.

### 1. Spam or Content Moderation Classifier
**Priority:** P1 | **Difficulty:** Easy

**Key concepts:** Binary classification, class imbalance, precision/recall tradeoff, labeling, threshold selection, human review queues.

**Expected components:**
- Labeling pipeline (user reports, human review, and how labels get noisy)
- Feature set (text, metadata, account history)
- Model (logistic regression baseline, then a gradient-boosted tree or a fine-tuned small transformer)
- Thresholding with a human-in-the-loop path for borderline cases
- Feedback loop: how appeals and reviewer decisions flow back into training

**What to learn:** Precision-recall curves, choosing thresholds by cost of false positives versus false negatives, class-weighting versus resampling, and how to handle label noise.

---

### 2. "People You May Know" or Friend Suggestions (Simplified)
**Priority:** P1 | **Difficulty:** Easy to Medium

**Key concepts:** Graph features, candidate generation, similarity scores, cold start, privacy constraints.

**Expected components:**
- Candidate generation from the social graph (friends of friends, shared attributes)
- Scoring model with graph and profile features
- Filtering rules (blocked users, existing connections)
- Offline batch precomputation with online refresh for active users

**What to learn:** Graph-based features (common neighbors, Adamic-Adar), cold-start strategies, and the tradeoff between precomputed and real-time candidate lists.

---

### 3. Autocomplete or Typeahead Suggestions
**Priority:** P1 | **Difficulty:** Easy to Medium

**Key concepts:** Prefix search, trie or inverted index, ranking by popularity and personalization, latency budgets (typically under 100 ms).

**Expected components:**
- Candidate retrieval via a trie or prefix index built offline from query logs
- Lightweight ranking using popularity and recency, optionally personalized
- Caching of popular prefixes
- Logging of impressions and selections for training data

**What to learn:** Latency budgets, the difference between retrieval and ranking, how query logs turn into training labels, and why position bias matters when you measure clicks.

---

## Level 2: Intermediate

These problems introduce the two-stage pattern (retrieval then ranking), large-scale serving, and the feedback loops that make real products hard.

### 4. Search Ranking (Product or Web Search)
**Priority:** P0 | **Difficulty:** Medium

**Key concepts:** Learning to rank (pointwise, pairwise, listwise), query understanding, relevance labels, position bias, NDCG, two-stage retrieval and ranking.

**Expected components:**
- Query understanding (spelling correction, intent classification)
- Candidate retrieval via inverted index (keyword) plus optional embedding-based retrieval
- Learning-to-rank model using query, document, and query-document features
- Relevance labels from human raters and click signals, with debiasing
- Online evaluation via interleaving or A/B tests, with guardrails such as latency and null-result rate

**What to learn:** NDCG and MRR, pairwise versus listwise losses, debiasing click data (inverse propensity weighting, position-based models), and how to combine lexical and semantic retrieval.

---

### 5. Recommendation System (Video, Music, or E-commerce)
**Priority:** P0 | **Difficulty:** Medium

**Key concepts:** Collaborative filtering, two-tower retrieval, candidate generation versus ranking, cold start, exploration versus exploitation, feedback loops.

**Expected components:**
- Candidate generation: two-tower model with approximate nearest neighbor (ANN) search, plus popularity and recent-interest candidates
- Ranking model: gradient-boosted trees or a deep model predicting engagement (click, watch time, add-to-cart)
- Feature store with user, item, and context features, split into batch and streaming
- Re-ranking for diversity, freshness, and business rules
- Offline training pipeline with a time-based split to avoid leakage
- Evaluation: offline recall@K and NDCG, then online A/B testing on engagement and retention

**What to learn:** Two-tower architecture, ANN indexes (HNSW, IVF), negative sampling, how to avoid training on items the user never saw, and how to measure long-term engagement rather than short-term clicks.

---

### 6. Ad Click-Through Rate (CTR) Prediction
**Priority:** P0 | **Difficulty:** Medium to Hard

**Key concepts:** Extreme class imbalance, log loss and calibration, feature hashing, online learning, real-time bidding constraints, delayed feedback.

**Expected components:**
- Feature pipeline with high-cardinality categorical features (hashed or embedded)
- Model: logistic regression with feature crosses as a baseline, then factorization machines or deep models (DeepFM, Wide and Deep)
- Serving under tight latency (often single-digit milliseconds for the model call)
- Calibration step, since predicted probabilities feed auction pricing
- Training on logs with negative downsampling, corrected at inference time
- Monitoring of calibration, not just AUC

**What to learn:** Log loss and calibration (reliability diagrams), negative downsampling and its correction, feature hashing, and how delayed conversions bias training data.

---

### 7. Feed Ranking (Social Media Home Feed)
**Priority:** P0 | **Difficulty:** Hard

**Key concepts:** Multi-objective ranking, engagement versus integrity, candidate sourcing from many producers, real-time signals, fairness and creator diversity.

**Expected components:**
- Candidate sources: followed accounts, recommended content, trending items, each with its own retrieval logic
- Ranking model predicting multiple actions (like, comment, share, long dwell, hide), combined into a weighted score
- Integrity and quality filters (policy-violating or low-quality content demoted before scoring)
- Re-ranking for diversity, freshness, and session-level variety
- Serving with precomputed candidates and real-time re-scoring on each request
- Experiment framework to measure both short-term engagement and long-term retention

**What to learn:** Multi-task learning, how to set and tune weights across objectives, negative feedback signals (hides and reports), and why optimizing for a single engagement metric causes problems.

---

## Level 3: Advanced

These problems assume you can design the basics. The focus is on scale, rare events, real-time decisions, and organizational constraints.

### 8. Fraud Detection (Payments or Account Takeover)
**Priority:** P0 | **Difficulty:** Hard

**Key concepts:** Extreme class imbalance (fraud is often well under 1%), real-time scoring, adversarial adaptation, label delay (chargebacks arrive weeks later), precision at low false-positive budgets.

**Expected components:**
- Real-time feature computation: velocity features (transactions in the last 1, 10, and 60 minutes), device and location signals, and graph features linking accounts, cards, and devices
- Stream processing layer (for example, Kafka plus Flink or a similar stack) for aggregates
- Model: gradient-boosted trees for tabular features, with graph neural networks as an option for ring detection
- Rules engine running alongside the model, with overrides for known patterns
- Decision thresholds tied to business cost (declined fraud versus declined good customers)
- Human review queue and an appeal path
- Monitoring for drift and for adversarial shifts in fraud patterns

**What to learn:** Handling label delay in training, point-in-time correct features (avoiding leakage from future chargebacks), precision-recall at a fixed review budget, and how rules and models complement each other.

---

### 9. Ride-Hailing or Delivery ETA Prediction
**Priority:** P1 | **Difficulty:** Hard

**Key concepts:** Spatiotemporal features, real-time traffic, regression with heavy-tailed errors, uncertainty estimation, batch versus online inference.

**Expected components:**
- Input features: road segment speeds, time of day, weather, historical trip durations, and live driver locations
- Routing engine as a feature source (base travel time from the map graph)
- Model predicting trip duration, trained on completed trips with a time-aware split
- Quantile or interval predictions, since users care about reliability as well as the mean
- Serving with caching of common routes and fallback to the routing engine's estimate when the model is unavailable
- Monitoring of prediction error by region and time of day

**What to learn:** Evaluating regression with MAE and percentile errors, quantile regression, how to design fallbacks, and how to make features consistent between training and serving.

---

### 10. Dynamic Pricing or Demand Forecasting
**Priority:** P1 | **Difficulty:** Hard

**Key concepts:** Time-series forecasting, causal inference for price effects, exploration constraints, business guardrails, fairness across customers.

**Expected components:**
- Forecasting model with seasonality, holidays, and promotions, using a hierarchical structure (product, store, region)
- Elasticity estimation using historical price experiments or causal methods
- Optimization layer that turns forecasts and elasticities into prices, subject to constraints (margin floors, price caps)
- Controlled exploration (for example, small randomized price tests) with explicit guardrails
- Evaluation via holdout markets and A/B tests with careful interference analysis

**What to learn:** Time-series cross-validation, why naive random splits leak information, causal estimation versus correlation, and how to run pricing experiments without harming customers or the business.

---

### 11. Real-Time Personalization at Scale (Homepage or Notification Ranking)
**Priority:** P1 | **Difficulty:** Hard

**Key concepts:** Contextual bandits, real-time features, notification fatigue, frequency capping, multi-armed decisions under budget.

**Expected components:**
- Candidate generation and scoring model predicting engagement per notification or module
- Contextual bandit or reinforcement learning layer for exploration
- Budget and frequency controls to avoid overwhelming users
- Real-time feature updates from streaming events
- Offline replay evaluation for bandit policies (counterfactual evaluation)
- Guardrail metrics: unsubscribe rate, opt-out, and long-term retention

**What to learn:** Exploration versus exploitation, off-policy evaluation (inverse propensity scoring, doubly robust estimation), and why short-term click gains can hurt long-term retention.

---

### 12. Content Moderation at Scale (Images, Video, or Text)
**Priority:** P1 | **Difficulty:** Hard

**Key concepts:** Multi-modal models, policy taxonomies, human review capacity, latency tiers (pre-publish versus post-publish), appeals, evolving policies.

**Expected components:**
- Tiered pipeline: cheap classifiers for high-volume filtering, expensive models for borderline cases, human review for the rest
- Multi-modal models combining text, image, and audio signals
- Policy taxonomy that maps labels to actions (remove, reduce distribution, label, no action)
- Human review tooling with quality checks and reviewer agreement measurement
- Feedback loop from appeals and audits back into training
- Monitoring of false-positive rates across languages and demographic groups

**What to learn:** Cascade architectures for cost control, inter-annotator agreement (Cohen's kappa), fairness auditing across subgroups, and how to handle policy changes without retraining from scratch.

---

### 13. Retrieval-Augmented Generation (RAG) Question Answering Over Company Data
**Priority:** P0 | **Difficulty:** Medium to Hard

**Key concepts:** Chunking, embeddings, vector search, reranking, grounding and citations, evaluation of generated answers, access control, latency and cost.

**Expected components:**
- Ingestion pipeline: document parsing, chunking strategy, metadata, and incremental re-indexing
- Retrieval: hybrid search combining keyword (BM25) and vector similarity, followed by a cross-encoder reranker
- Access control enforced at retrieval time, not after generation
- Generation with citations, with refusal behavior when retrieved context is weak
- Evaluation: retrieval recall@K, answer faithfulness, and human review on a fixed evaluation set
- Monitoring for stale indexes, unanswered queries, and user feedback

**What to learn:** Chunk size and overlap tradeoffs, hybrid retrieval, reranking, evaluation without ground truth (LLM-as-judge with calibration), and why permissions must be enforced at retrieval.

---

### 14. Multi-Tenant ML Feature Store and Training Platform (Platform-Adjacent)
**Priority:** P2 | **Difficulty:** Advanced

**Key concepts:** Point-in-time correctness, online and offline stores, feature reuse, versioning, data freshness SLAs, governance.

**Expected components:**
- Offline store for training data with point-in-time joins
- Online store for low-latency serving, kept consistent with offline definitions
- Feature registry with ownership, versioning, and documentation
- Ingestion pipelines for batch and streaming features
- Access control and lineage tracking
- Monitoring for feature freshness, null rates, and training-serving skew

**What to learn:** Training-serving skew and how to prevent it, point-in-time joins, feature backfills, and how a feature store reduces duplicated work across teams.

---

### 15. Experimentation Platform (A/B Testing at Scale)
**Priority:** P1 | **Difficulty:** Advanced

**Key concepts:** Randomization units, sample ratio mismatch, variance reduction (CUPED), network effects and interference, sequential testing, multiple comparisons.

**Expected components:**
- Assignment service with deterministic hashing for consistent bucketing
- Metric pipeline with guardrails and automated alerting
- Variance reduction using pre-experiment covariates (CUPED)
- Sequential testing or always-valid p-values for early stopping
- Diagnostics: sample ratio mismatch checks, balance checks, novelty effect detection
- Support for interference-aware designs (cluster or switchback randomization)

**What to learn:** Power analysis, CUPED, sample ratio mismatch as a debugging signal, and when standard A/B tests break down because of marketplace or social interference.

---

### 16. Ranking Under Constraints: Two-Sided Marketplace (Jobs, Lodging, or Gig Platforms)
**Priority:** P2 | **Difficulty:** Advanced

**Key concepts:** Two-sided objectives (seekers and providers), fairness, supply constraints, market equilibrium effects, exposure allocation.

**Expected components:**
- Relevance model for matching seekers to providers
- Exposure or allocation layer ensuring providers get fair visibility, especially new ones
- Constraint handling (capacity, geography, budget)
- Experimentation design that accounts for marketplace interference
- Metrics for both sides: match quality, fill rate, provider earnings distribution, and seeker satisfaction
- Monitoring for feedback loops that concentrate exposure on a few providers

**What to learn:** Two-sided marketplace dynamics, exposure fairness metrics, how ranking changes supply behavior over time, and interference-aware experiment design.

---

## Cross-cutting concepts checklist

Use this as a review list after each session. You should be able to explain each item with a concrete example from one of the problems above.

- [ ] **Metrics:** offline versus online, proxy versus north-star, guardrail metrics, and how they conflict
- [ ] **Labels:** implicit versus explicit feedback, position bias, selection bias, label delay, and label noise
- [ ] **Leakage:** point-in-time correct features, time-based splits, and future information in training data
- [ ] **Retrieval:** ANN indexes (HNSW, IVF), two-tower models, and hybrid lexical and semantic search
- [ ] **Ranking:** pointwise, pairwise, and listwise losses; multi-task learning; weighting objectives
- [ ] **Serving:** latency budgets, caching, precomputation, batch versus real-time inference, and fallbacks
- [ ] **Feature stores:** online and offline consistency, training-serving skew
- [ ] **Experimentation:** power, randomization units, CUPED, sequential testing, interference
- [ ] **Monitoring:** data drift, concept drift, calibration drift, and alert design
- [ ] **Feedback loops:** how model outputs change future training data, and how to break or measure them
- [ ] **Fairness and safety:** subgroup metrics, auditing, and policy constraints
- [ ] **Cost:** GPU and CPU budgets, model size versus quality, and cascade architectures

---

## Practice routine

A 12 to 14 week plan that covers the full sheet at about one problem per week, with review sessions in between:

| Weeks | Focus | Problems |
|---|---|---|
| 1 to 2 | Framework and beginner problems | 1, 2, 3 |
| 3 to 6 | Core recommendation and search | 4, 5, 6, 7 (one per week, plus review) |
| 7 to 10 | Advanced applied problems | 8, 9, 10, 11 |
| 11 to 12 | Modern ML and platform | 12, 13, 14 |
| 13 | Experimentation and marketplace | 15, 16 |
| 14 | Mock interviews | Re-do P0 problems (4, 5, 6, 7, 8, 13) under timed conditions |

**Each week:**
- Solve one problem in a timed 40-minute mock, speaking out loud
- Review your recording and list three things you would improve
- Re-read the cross-cutting checklist and tick off what you can now explain

**Mock interview tips:**
- Ask the interviewer clarifying questions before drawing anything
- State your assumptions and check them
- Keep a running "Parking lot" list of deeper topics to return to if time allows
- Finish with a summary of tradeoffs and what you would monitor after launch

---

*Note: Concept lists and components above reflect commonly discussed approaches. Real company designs vary, so treat them as starting points to adapt, not templates to memorize.*
