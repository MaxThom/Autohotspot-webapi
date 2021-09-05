
from flask import Blueprint, request, jsonify, render_template

hotspot_bp = Blueprint('hotspot', __name__)

incomes = [
  { 'description': 'salary', 'amount': 5000 }
]

@hotspot_bp.route('/')
def get():
    hotspot = {'status': 'WIFI'}
    return render_template('hotspot.html',hotspot=hotspot)

@hotspot_bp.route('/api', methods=['GET'])
def api_get():
    data = request.get_json()
    print(data)
    print(data["ssid"])
    print(data["password"])
    return jsonify(request.get_json())