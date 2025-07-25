# 🏦 PoC Solution Design – CDW Drop Ship Order Automation

---

## 🔹 Use Case Overview

**Problem:**

- Drop ship POs with customer freight methods `KG` and `KC` are blocked from automation.
- Buyer team must manually review & release every PO with these methods – causes delays (2–3 hrs/PO).

**Goal:**

- Introduce a **modular automation engine** to evaluate and auto-release eligible POs based on supplier and ship method.
- Avoid modifying legacy iSeries and provide a bolt-on decision system.

---

## 🔍 System Context

- **Sales orders** are created in **iSeries**, typically triggered by Salesforce or SPS Commerce.
- iSeries then generates **purchase orders (POs)** for drop ship items.
- Buyer team reviews/interacts with POs in **iSeries**.
- PO data may feed into SPS/Salesforce, but the **core automation logic** starts **after PO creation**.
- Our modular engine evaluates POs **post-creation**, focusing on `KG/KC` scenarios.

---

## 🔹 Current Flow (Manual Touch)

1. Drop ship order placed → CDW systems process (OMS/AS400/etc.).
2. PO created in iSeries.
3. If `KG` or `KC` ship method → fails automation.
4. Routed to Buyer via Drop Ship Order Router.
5. Buyer manually reviews & releases.

⚠️ Result: Delays + buyer workload + inconsistent automation.

---

## 🔹 Why This Works – Design Rationale

### ❌ The Limitation with iSeries

- The existing **iSeries automation system** applies automation settings globally.

  - You can turn on automation for a ship method like `KG` or `KC` for **all suppliers**, or turn it off for everyone.
  - It **can’t make nuanced decisions** like:
    > “Supplier PDX allows KG, but Supplier ACME does not.”

- This **lack of granularity** forces CDW to block all KG/KC-based orders from automation, even if some suppliers are fully capable — leading to **unnecessary manual reviews** and delays.

### ✅ Our Modular Engine Solves This

You’re proposing a **standalone automation engine** — a smart, flexible microservice that works **alongside** iSeries, not inside it.

It:

🔄 **Hooks in after iSeries PO creation**

- Monitors or receives PO records (via polling, webhook, or file drop simulation).

🧠 **Evaluates each PO individually**

- Looks at the `supplier` and `ship_method`.
- Applies business logic from a lightweight config file (`suppliers.json`).

🚦 **Routes the PO appropriately**

- ✅ If supplier is approved → mark as “Auto-Released”.
- ❌ If not → send to existing Buyer review queue (no action needed by engine).

### 🧹 Key Design Advantages

- **Non-invasive:** No modification to iSeries.
- **Repeatable:** Anyone can run the PoC with mock JSON files and Python.
- **Realistic:** Mirrors enterprise decision flow without needing full backend access.
- **Scalable:** Easy to plug into Azure queues, databases, or API gateways later.
- **Smart:** Empowers CDW to automate only the **right** POs — reducing manual burden with **zero risk**.

---

## 🔹 Proposed Modular Automation Engine

**Introduce external engine to evaluate KG/KC POs based on supplier config.**

### ✅ New Logic:

- When PO is created:
  - If ship method is `KG` or `KC`:
    - Check if supplier is approved for auto-release.
    - If **yes** → auto-release to supplier via API flag/log.
    - If **no** → route PO to Buyer (no action by the engine).

### ✅ Benefits:

- Modular: No change to iSeries.
- Scalable: Easily onboard suppliers.
- Transparent: Configurable & traceable.

---

## 🔹 PoC Architecture

- **Language:** Python
- **Data:** Mock JSON files
- **Logic Entry Point:** PO created in iSeries with KG/KC method
- **Evaluation:** Supplier + ship method lookup
- **Output:** Log of release path (auto/manual)

```bash
- suppliers.json → { D1: allows KG/KC = true, ACME: false, ... }
- test_po.json → { po_id, supplier, ship_method }
```

---

## 🔹 Demo Flow (Walkthrough)

1. Load PO with KG method for supplier `PDX`.
2. Python script checks supplier settings.
3. Decision:
   - ✅ If supplier allows KG/KC → print "Auto Released"
   - ❌ If not → print "Needs Buyer Review"

```bash
python automate_po.py
>> PO123456 from PDX auto-released ✅
```

---

## 🔹 Results & Impact

- Built simple, repeatable decision engine.
- Operates **in parallel to iSeries**, non-disruptive.
- Potential for Azure Function + DB in prod.
- Measurable savings: \~2–3 hours per PO, thousands of POs/month.

---

## 🔹 GitHub Deliverables

- `automate_po.py` – Main logic
- `api_server.py` – Flask REST API (Azure-ready)
- `suppliers.json`, `test_po.json` – Mock data
- `requirements.txt` – Python dependencies
- `README.md` – Setup, usage, screenshots
- `Procfile` – for Azure App deployment
- Slide deck (this!)
- Demo walkthrough script

---

## 🔹 REST API Design (Azure-ready)

**POST /check\_po**

```json
Request Body:
{
  "supplier": "PDX",
  "ship_method": "KG"
}
Response:
{
  "po_status": "Auto Released"
}
```

Use this API for testing POs or integrating with CDW UI/OMS/Router.

---

## 🔹 Future Enhancements

- GUI dashboard for Buyer approvals
- Azure Cosmos DB for supplier config
- Slack/Teams notification on failures
- iSeries mock interface for PO status feedback

---

## 🔹 Thank You – Q&A

**Team:** [Your Names Here]\
**Project:** Drop Ship Order Automation Engine (Modular, KG/KC Focus)

📁 GitHub: [github.com/yourteam/drop-ship-automation](https://github.com/yourteam/drop-ship-automation)

---

