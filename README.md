# 🚀 Drop Ship PO Automation Engine – Hackathon Submission

## 🧩 Team: Code, Ship, Repeat  
**Contributors:** Olena Noda, Emily Teter, Brendon Pagel

---

## 🔍 Problem
Drop ship POs using freight methods `KG` or `KC` are excluded from automation due to iSeries system limitations — all must be manually reviewed by the Buyer team (2–3 hrs per PO). This is inefficient and blocks suppliers that could otherwise be fully automated.

---

## 🎯 Solution – Modular PO Automation Engine
We created a lightweight, standalone engine that:
- Hooks into the flow **after iSeries PO creation**
- Checks if the supplier + ship method is eligible
- If eligible → auto-releases
- If not → flags for buyer manual review

> ✅ iSeries remains untouched.  
> ✅ Logic is fully config-driven (`suppliers.json`)  
> ✅ Ready for API deployment in Azure

---

## 📂 Files
| File | Description |
|------|-------------|
| `PoC_Solution_Design.md` | Full technical design of the solution |
| `automate_po.py` | Python script to simulate PO evaluation |
| `suppliers.json` | Mock supplier automation config |
| `test_po.json` | Sample PO data |
| `api_server.py` | Optional Flask API |
| `Procfile` | Needed for Azure App deployment |
| `requirements.txt` | Python dependencies |

---

## ▶️ How to Run
Install dependencies:

```bash
pip install -r requirements.txt
