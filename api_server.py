# api_server.py
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Load supplier config once at startup
with open('suppliers.json') as f:
    supplier_config = json.load(f)

# Shared evaluation function
def evaluate_po(po, config):
    supplier = po['supplier']
    ship_method = po['ship_method']
    po_id = po['po_id']

    allowed_methods = config.get(supplier, {}).get('allowed_methods', [])
    if ship_method in allowed_methods:
        return {
            "po_id": po_id,
            "status": "auto-released",
            "message": f" PO {po_id} from {supplier} (Method: {ship_method}) auto-released"
        }
    else:
        return {
            "po_id": po_id,
            "status": "buyer-review",
            "message": f" PO {po_id} from {supplier} (Method: {ship_method}) needs Buyer Review"
        }

# POST endpoint
@app.route('/evaluate', methods=['POST'])
def evaluate():
    pos = request.get_json()
    if not isinstance(pos, list):
        return jsonify({"error": "Expected a list of POs"}), 400

    results = [evaluate_po(po, supplier_config) for po in pos]
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
