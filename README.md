# AegisOps

---

# 🚀 Project Roadmap: Autonomous AI DevOps Engineer

This roadmap breaks down the development of the *Self-Healing & Auto-Scaling Infrastructure Agent* into progressive, manageable engineering tasks.

---

## 📂 Repository File Structure Matrix

Ensure your repository follows this microservices architecture layout before writing configurations:

```text
self-healing-infra/
├── .github/
│   └── workflows/              # CI/CD pipelines
├── protobuf/
│   └── telemetry.proto         # Shared gRPC service definitions
├── demo-app/
│   ├── app.py                  # Vulnerable application logic
│   └── Dockerfile
├── service-a/                  # Ingestion Layer (FastAPI + gRPC Client)
│   ├── main.py
│   ├── telemetry_pb2.py        # Generated from compiler
│   ├── telemetry_pb2_grpc.py   # Generated from compiler
│   └── Dockerfile
├── service-b/                  # AI Detection Layer (gRPC Server + Deep Learning)
│   ├── main.py
│   ├── model.py                # PyTorch/PyOD Anomaly Core
│   ├── telemetry_pb2.py
│   ├── telemetry_pb2_grpc.py
│   └── Dockerfile
├── otel-collector-config.yaml  # OpenTelemetry scraping configurations
└── docker-compose.yml          # Local infrastructure mesh

```

---

## 📋 Step-by-Step Development Checklists

### 🟩 Step 1: The Vulnerable Mock Environment (`demo-app/`)

*Goal: Build a target container that can be intentionally broken on demand.*

* [ ] **1.1 Base Application Setup:** Initialize a lightweight web application inside `demo-app/app.py`.
* [ ] **1.2 Create Global Leak State:** Declare a global scope Python collection array to act as a persistent memory trap.
* [ ] **1.3 Add `/leak` Endpoint:** Write a route that injects heavy, raw byte blocks or massive strings into the global collection array every time it is pinged.
* [ ] **1.4 Add `/slow-query` Endpoint:** Write a route that executes a heavy, multi-layered nested calculation loop to pin the container CPU usage at 100%.
* [ ] **1.5 Set Up Unbuffered Logs:** Write standard print strings with explicit keywords (`[INFO]`, `[ERROR]`) and ensure `PYTHONUNBUFFERED=1` is passed in the environment to keep streams live.
* [ ] **1.6 Containerize:** Build a minimalist `Dockerfile` utilizing a `python-slim` base image exposing the application port.

### 🟩 Step 2: Telemetry Scraper & Ingestion Mesh (`otel` & `service-a/`)

*Goal: Capture data automatically and send it to your first microservice.*

* [ ] **2.1 Configure OTel Scraper:** Author the `otel-collector-config.yaml` file. Add the `hostmetrics` receiver and set a rapid 2-second collection interval.
* [ ] **2.2 Configure OTel Exporters:** Direct the output pipes (`otlphttp`) to send data packets downstream to `http://service-a:5000/v1/metrics` and `/v1/logs`.
* [ ] **2.3 Build FastAPI Ingestion Base:** Initialize `service-a/main.py` using asynchronous endpoint declarations (`async def`) matching the OTel payload paths.
* [ ] **2.4 Parse Metrics Arrays:** Write data-extraction logic to parse incoming nested telemetry JSON structures into flat, floating-point variables representing system RAM and CPU percentages.

### 🟩 Step 3: Define the Data Contract (`protobuf/`)

*Goal: Enforce strict, high-speed serialization parameters between services.*

* [ ] **3.1 Author Protobuf Schema:** Write `protobuf/telemetry.proto`. Define message structures for `MetricPayload` (CPU, RAM fields) and `LogPayload` (level, message fields).
* [ ] **3.2 Declare RPC Streams:** Add an `AnomalyDetector` service block containing bidirectional or unary streaming endpoints (e.g., `rpc StreamMetrics (MetricPayload) returns (AnomalyResponse)`).
* [ ] **3.3 Compile Protocol Files:** Execute the `grpcio-tools` compiler command in your terminal to output the python interface files.
* [ ] **3.4 Sync Interface Stubs:** Copy the generated `telemetry_pb2.py` and `telemetry_pb2_grpc.py` scripts directly into the directories of both **Service A** and **Service B**.

### 🟩 Step 4: The Deep Learning Anomaly Core (`service-b/`)

*Goal: Build the machine learning brain that detects patterns of architectural failure.*

* [ ] **4.1 Build Unsupervised ML Model:** Write `service-b/model.py`. Use an Autoencoder (PyTorch) or an Isolation Forest (PyOD) to dynamically grade incoming metrics.
* [ ] **4.2 Code the Reconstruction Threshold:** Define mathematical rules to trigger warnings when metric variance shifts multiple standard deviations away from the calibrated mean baseline.
* [ ] **4.3 Build Async gRPC Server:** Set up `service-b/main.py` using `grpc.aio` to listen for network queries on internal port `50051`.
* [ ] **4.4 Connect Inference Pipeline:** Link the active data ingestion loops coming from the gRPC stream channel to process features instantly through your ML engine, outputting an alert payload whenever the score flags a critical anomaly.

### 🟩 Step 5: Bridge Services & Network Orchestration (`docker-compose.yml`)

*Goal: Tie the entire network together and run validation stress tests.*

* [ ] **5.1 Update Service A to gRPC Client:** Integrate a gRPC communication channel stub inside Service A’s FastAPI routes to pass data downstream to Service B immediately upon ingestion.
* [ ] **5.2 Wire up `docker-compose.yml`:** Declare all container contexts (`demo-app`, `otel-collector`, `service-a`, `service-b`) on a shared private subnet mask.
* [ ] **5.3 Establish Dependency Orders:** Attach `depends_on` constraints so the ingestion systems wait for the gRPC detection servers to be completely healthy before accepting external metrics.

---

## 🧪 Verification Plan (Run this to verify success)

Once these 5 steps are checked off, run the following validation pipeline to test your work:

```bash
# 1. Spin up the entire infrastructure mesh
docker compose up --build

# 2. In a separate terminal, trigger the intentional memory leak
curl http://localhost:8000/leak

# 3. Validation Check
# Open the console logs for service-a and service-b. 
# You should see the OTel collector pass metrics to Service A, 
# Service A stream them via gRPC to Service B, 
# and Service B print: [ANOMALY DETECTED] Reconstruction error exceeded threshold!

```

---

## ⏭️ Next System Milestones (For Future Phases)

* **Phase 4:** Setup **LangGraph** orchestrator core logic and state models.
* **Phase 5:** Implement secure Linux sandboxing utilizing **E2B MicroVMs** to test generated diagnostic scripts safely.
