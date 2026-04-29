from flask import Flask, jsonify

app = Flask(__name__)

inventario = {
    "1": {"titulo": "Clean Code", "stock": 10},
    "2": {"titulo": "SOLID Principles", "stock": 5}
}

@app.route('/api/v2/inventario/<id>', methods=['GET'])
def consultar_stock(id):
    item = inventario.get(id)
    return jsonify(item) if item else (jsonify({"error": "No encontrado"}), 404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)