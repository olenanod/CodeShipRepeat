# automate_po.py
# This script simulates evaluating multiple drop ship POs for auto-release

import json

# Load supplier configuration
def load_supplier_config():
    with open('suppliers.json') as f:
        return json.load(f)

# Load list of POs
def load_pos():
    with open('test_po.json') as f:
        return json.load(f)

# Evaluate a single PO
def evaluate_po(po, config):
    supplier = po['supplier']
    ship_method = po['ship_method']
    po_id = po['po_id']

    allowed_methods = config.get(supplier, {}).get('allowed_methods', [])

    if ship_method in allowed_methods:
        return f" PO {po_id} from {supplier} (Method: {ship_method}) auto-released"
    else:
        return f" PO {po_id} from {supplier} (Method: {ship_method}) needs Buyer Review"

if __name__ == '__main__':
    config = load_supplier_config()
    pos = load_pos()

    print("=== PO Evaluation Results ===")
    for po in pos:
        result = evaluate_po(po, config)
        print(result)
