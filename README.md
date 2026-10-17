# 🛡️ Decision Layer Agent (Decision Architect Challenge)

An explicit decision layer designed for real-world AI systems. Instead of executing every instruction blindly, this architecture acts as a safety and trust firewall, deciding whether to act based on **confidence, risk score, evidence used, missing information, and reversibility**.

---

## 🚀 What We Built
1. **Decision Engine:** Evaluates proposed actions against context and returns one of five strict verdicts: `execute`, `ask`, `defer`, `escalate`, or `refuse`.
2. **Rich Metadata Surface:** Every decision includes confidence scores, risk metrics, reversibility levels, and tracked missing information.
3. **Audit Trail:** Comprehensive logging (`audit_trail.jsonl`) capturing inputs, signals, reasoning, and final outcomes.
4. **Multi-Domain Support:** Wired with 3 core example domains:
   - **Financial Refunds** (Threshold & receipt validation)
   - **DevOps Code Deployments** (Environment & test-suite verification)
   - **Support Ticket Triage** (Priority & authorization checks)
5. **Deliberate Failure Test:** A test case designed to challenge input manipulation and unverified privileges.

---

## 📂 Project Structure
```text
decision-layer-agent/
│
├── models.py           # Pydantic data models (Verdict, Reversibility, Action, Context)
├── engine.py           # Core decision matrix and signal calculation logic
├── main.py             # Entry point running domain tests & failure scenarios
└── audit_trail.jsonl   # Automated audit log output
🛠️ Installation & Running
Clone the repository:

Bash
git clone [https://github.com/GhufranSolyman/decision-layer-agent.git](https://github.com/GhufranSolyman/decision-layer-agent.git)
cd decision-layer-agent
Install dependencies:

Bash
pip install pydantic
Run the test suite:

Bash
python main.py
🏗️ Architecture Snapshot
Plaintext
[User / Agent Action + Context] 
              │
              ▼
   [Signals & Risk Engine]
   - Confidence Score Calculation
   - Risk Assessment & Reversibility Check
   - Missing Information Detection
              │
              ▼
     [Decision Matrix]
 (Execute / Ask / Defer / Escalate / Refuse)
              │
              ▼
  [Audit Trail Logger (.jsonl)]
🔮 Two-Year Thesis (2026–2028)
Over the next two years, AI systems will transition from uncritical instruction-executors to autonomous, collaborative entities requiring strict governance layers. The primary bottleneck in agentic systems is no longer tool invocation, but liability, risk management, and operational safety. Decision layers will evolve into mandatory decentralized firewalls sitting between agent intent and real-world impact. Powered by formal verification and cryptographic trust signals, whoever masters the decision layer owns the institutional trust of the automated era.