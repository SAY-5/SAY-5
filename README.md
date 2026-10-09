<a href="https://sayportfolio.vercel.app"><img src="assets/banner.svg" alt="Sai Asish Y. Software engineer. Distributed systems, low latency infrastructure, databases." width="100%"></a>

<p>
  <a href="https://sayportfolio.vercel.app">Portfolio</a> &nbsp;&middot;&nbsp;
  <a href="https://showcases-lime.vercel.app">Live demos</a> &nbsp;&middot;&nbsp;
  <a href="https://www.linkedin.com/in/saiasishy/">LinkedIn</a> &nbsp;&middot;&nbsp;
  <a href="mailto:saiasish.cnp@gmail.com">saiasish.cnp@gmail.com</a>
</p>

Software engineer working on distributed systems, low latency infrastructure, and databases. MS in Computer Science from Stony Brook University, B.Tech from VIT. Previously at Nokia and in two research labs, CUBIT and the Data Management and Biomedical Analytics Lab. Open to SDE and SWE roles.

## Recent releases

The latest release of each repository, read from GitHub on 2026-10-09. GitHub did not answer for kernelcheck, rankfault; those entries show the release last read. Each title links to the write-up, or to the repository where there is no write-up yet.

- <a href="https://sayportfolio.vercel.app/p/modelgate"><b>ETA Model Serving</b></a><br><sub><a href="https://github.com/SAY-5/modelgate">modelgate</a> &middot; <a href="https://github.com/SAY-5/modelgate/releases/tag/v5.0.2">v5.0.2</a>, 2026-09-29</sub><br>FastAPI serving for a PyTorch ETA model: strict input validation, shadow runs, canaries with automatic rollback, and version swaps load-tested with 0 dropped requests.

- <a href="https://sayportfolio.vercel.app/p/dispatchgrid"><b>Streams Ride Matcher</b></a><br><sub><a href="https://github.com/SAY-5/dispatchgrid">dispatchgrid</a> &middot; <a href="https://github.com/SAY-5/dispatchgrid/releases/tag/v5.2.0">v5.2.0</a>, 2026-09-29</sub><br>Ride matching on Kafka Streams in Java 21 and Spring Boot 3, with trips in city-keyed MySQL shards, driver positions in Redis GEO and zero-downtime rolling updates on Kubernetes.

- <a href="https://sayportfolio.vercel.app/p/failsafe"><b>Resilient API Gateway</b></a><br><sub><a href="https://github.com/SAY-5/failsafe">failsafe</a> &middot; <a href="https://github.com/SAY-5/failsafe/releases/tag/v5.0.2">v5.0.2</a>, 2026-09-29</sub><br>Python API gateway with token-bucket rate limiting, per-replica circuit breakers, retries and failover; its chaos runs kill replicas under load with zero client-visible failures.

- <a href="https://sayportfolio.vercel.app/p/ledgermesh"><b>Order Saga With Chaos Proof</b></a><br><sub><a href="https://github.com/SAY-5/ledgermesh">ledgermesh</a> &middot; <a href="https://github.com/SAY-5/ledgermesh/releases/tag/v6.0.0">v6.0.0</a>, 2026-09-29</sub><br>Order saga across three Spring Boot services with Kafka, Redis and Resilience4j; in the recorded chaos run, 1200 orders under three service kills ended with none failed or stuck.

- <a href="https://sayportfolio.vercel.app/p/kernelcheck"><b>CUDA Kernel Fuzz Tester</b></a><br><sub><a href="https://github.com/SAY-5/kernelcheck">kernelcheck</a> &middot; <a href="https://github.com/SAY-5/kernelcheck/releases/tag/v4.0.0">v4.0.0</a>, 2026-09-29</sub><br>Differential fuzz tester for CUDA C++ kernels on a CPU execution model, never run on a GPU; it detected 156 of 171 seeded mutants, and the 15 it missed are equivalent under the kernels' contracts.

- <a href="https://sayportfolio.vercel.app/p/panelist"><b>Expert Grading And Delivery Platform</b></a><br><sub><a href="https://github.com/SAY-5/panelist">panelist</a> &middot; <a href="https://github.com/SAY-5/panelist/releases/tag/v6.0.0">v6.0.0</a>, 2026-09-28</sub><br>Expert grading platform: tasks routed by expertise tag, hidden attention checks, pay per approved task, and approved grades exported as versioned, checksummed JSONL datasets.

- <a href="https://sayportfolio.vercel.app/p/tradegraph"><b>Ownership And Exposure Graph</b></a><br><sub><a href="https://github.com/SAY-5/tradegraph">tradegraph</a> &middot; <a href="https://github.com/SAY-5/tradegraph/releases/tag/v5.1.1">v5.1.1</a>, 2026-09-28</sub><br>Counterparty knowledge graph from SEC filings: a Python ETL loads RDF into a SPARQL store, a Spring Boot API answers lineage and exposure queries, and an Angular explorer draws it.

- <a href="https://sayportfolio.vercel.app/p/conduit"><b>Declarative Connector Pipeline</b></a><br><sub><a href="https://github.com/SAY-5/conduit">conduit</a> &middot; <a href="https://github.com/SAY-5/conduit/releases/tag/v6.0.0">v6.0.0</a>, 2026-09-28</sub><br>Connector kit with one adapter interface for Slack, Jira and signed webhooks: idempotency keys, backoff, a circuit breaker per connector and an SQS dead-letter queue.

- <a href="https://sayportfolio.vercel.app/p/rankfault"><b>Collective Fault Injection Harness</b></a><br><sub><a href="https://github.com/SAY-5/rankfault">rankfault</a> &middot; <a href="https://github.com/SAY-5/rankfault/releases/tag/v5.0.0">v5.0.0</a>, 2026-09-28</sub><br>Fault injection for multi-rank PyTorch jobs: kills, freezes, link faults and ordering skew injected mid-collective; measured with gloo on CPU on Linux, 0 of 114 runs stalled, NCCL never run.

- <a href="https://sayportfolio.vercel.app/p/launchbridge"><b>Signed Webhook Integration Service</b></a><br><sub><a href="https://github.com/SAY-5/launchbridge">launchbridge</a> &middot; <a href="https://github.com/SAY-5/launchbridge/releases/tag/v5.1.0">v5.1.0</a>, 2026-09-27</sub><br>FastAPI and PostgreSQL integration service: signed inbound webhooks, deduplication, bounded retries, replay of failed events and secret rotation.

- <a href="https://sayportfolio.vercel.app/p/playbook"><b>Procedure To Agent Pipeline</b></a><br><sub><a href="https://github.com/SAY-5/playbook">playbook</a> &middot; <a href="https://github.com/SAY-5/playbook/releases/tag/v6.0.0">v6.0.0</a>, 2026-09-27</sub><br>Turns an expert's walkthrough and SOP into a tool-calling agent with Jira and Slack tools, grades its runs against the expert's rubric and feeds failures back as corrections.

- <a href="https://sayportfolio.vercel.app/p/spoofline"><b>Two-Stream Spoof Detection</b></a><br><sub><a href="https://github.com/SAY-5/spoofline">spoofline</a> &middot; <a href="https://github.com/SAY-5/spoofline/releases/tag/v5.1.0">v5.1.0</a>, 2026-09-27</sub><br>Audio and video spoof detection with a CNN-LSTM per stream, calibrated and fused, evaluated on attack families held out of training, on a deterministically generated corpus.

- <a href="https://sayportfolio.vercel.app/p/expertloop"><b>Notes To Agent Instructions</b></a><br><sub><a href="https://github.com/SAY-5/expertloop">expertloop</a> &middot; <a href="https://github.com/SAY-5/expertloop/releases/tag/v5.1.0">v5.1.0</a>, 2026-09-27</sub><br>Turns expert task notes into versioned agent instructions with linked sources, and gates approved workflows behind test cases before they reach business systems.

- <a href="https://sayportfolio.vercel.app/p/rideloop"><b>Ride Dispatch Platform</b></a><br><sub><a href="https://github.com/SAY-5/rideloop">rideloop</a> &middot; <a href="https://github.com/SAY-5/rideloop/releases/tag/v5.0.0">v5.0.0</a>, 2026-09-08</sub><br>Ride request, driver location and dispatch services in Python, with a geohash-partitioned DynamoDB driver index, PostgreSQL trips and a React rider map.

## Selected work

Each card opens the write-up; every one of these has a demo that runs in the browser.

<p>
<a href="https://sayportfolio.vercel.app/p/scanguard"><img src="assets/cards/scanguard.svg" alt="Scanner Preflight Service: Preflight and scan-sequence service for a research microPET scanner" width="49%"></a>
<a href="https://sayportfolio.vercel.app/p/cloudshift"><img src="assets/cards/cloudshift.svg" alt="Strangler Fig Migration Kit: Strangler-fig migration toolkit for a Spring Boot monolith with phased cutover" width="49%"></a>
<a href="https://sayportfolio.vercel.app/p/agentdesk"><img src="assets/cards/agentdesk.svg" alt="Customer Operations Agent: Customer-operations agent with tool-call resolution and low-confidence human handoff" width="49%"></a>
<a href="https://sayportfolio.vercel.app/p/taskboard"><img src="assets/cards/taskboard.svg" alt="Realtime Kanban Board: Collaborative Kanban board with real-time multi-user editing and WebSocket conflict resolution" width="49%"></a>
<a href="https://sayportfolio.vercel.app/p/shopflow"><img src="assets/cards/shopflow.svg" alt="E-Commerce Microservices: Spring Boot e-commerce microservices behind a REST gateway with database per service" width="49%"></a>
<a href="https://sayportfolio.vercel.app/p/gradeview"><img src="assets/cards/gradeview.svg" alt="Learning Analytics Dashboard: Learning-analytics dashboard with hand-rolled D3 visualizations over SQL-side aggregation" width="49%"></a>
<a href="https://sayportfolio.vercel.app/p/codelens"><img src="assets/cards/codelens.svg" alt="Go Symbol Reference Graph: Go AST code-intelligence tool backed by a symbol and reference graph" width="49%"></a>
<a href="https://sayportfolio.vercel.app/p/learnloop"><img src="assets/cards/learnloop.svg" alt="Elo-Rated Adaptive Practice: Adaptive practice web app with Elo-style difficulty and mastery tracking" width="49%"></a>
<a href="https://sayportfolio.vercel.app/p/scan-sequencer"><img src="assets/cards/scan-sequencer.svg" alt="PET Scan Sequencer: Hardware-verifying scan sequencer for a simulated small-animal PET scanner" width="49%"></a>
<a href="https://sayportfolio.vercel.app/p/diagkit"><img src="assets/cards/diagkit.svg" alt="Incident Root Cause Ranker: Diagnostic CLI that ranks the likely root cause of a distributed-service incident" width="49%"></a>
<a href="https://sayportfolio.vercel.app/p/snapvault"><img src="assets/cards/snapvault.svg" alt="Content-Addressed Backup: Distributed backup and restore with content-addressed dedup and verified parallel recovery" width="49%"></a>
</p>

<a href="https://sayportfolio.vercel.app/work"><img src="assets/stats.svg" alt="Numbers. Figures taken 2026-10-09. 166 public repositories, not counting 2298 forks; 1221 merged pull requests in projects outside this account; 167 projects in the portfolio catalog, 23 of them selected, each with a live demo. Catalog by category: Infra and Distributed 35, Agents and Language 31, Data and ML 27, Web and Full-stack 23, Systems and C++ 20, Developer Tools 16, Instrumentation and Test 13, Other 2." width="100%"></a>

## Open source

1221 merged pull requests in projects outside this account (as of 2026-10-09) across the JavaScript, Python, Go, and Rust ecosystems. Until May 2026 the approach was volume; since May 5, 2026 it is one issue at a time: reproduce it, fix it, test it, and land a single clean change. Apologies to the maintainers who dealt with duplicate or half-tested PRs before that.

## Contributions

<img src="https://raw.githubusercontent.com/SAY-5/SAY-5/output/github-snake-dark.svg" alt="Contribution graph for the past year, animated" width="100%">

<sub>Assets are generated from the portfolio's project data, the GitHub API and <code>data/recent-work.json</code> by <code>scripts/build.mjs</code> and refreshed daily.</sub>
