from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ecommerce.db"

db = SQLAlchemy(app)
CORS(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)


@app.route("/api/products/add", methods=["POST"])
def add_product():
    data = request.json

    if data is None:
        return jsonify({"error": "JSON ausente ou invalido"}), 400

    if "name" in data and "price" in data:
        product = Product(
            name=data["name"],
            price=data["price"],
            description=data.get("description", ""),
        )

        db.session.add(product)
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Produto criado com sucesso",
                    "product": {
                        "id": product.id,
                        "name": product.name,
                        "price": product.price,
                        "description": product.description,
                    },
                }
            ),
            201,
        )

    return jsonify({"error": "Campos obrigatórios: name, price"}), 400


@app.route("/api/products/delete/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Produto deletado com sucesso"})
    return jsonify({"message": "Produto nao encontrado ou nao existe na base"}), 404


@app.route("/api/products/<int:product_id>", methods=["GET"])
def get_product_details(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify(
            {
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "description": product.description,
            }
        )
    return jsonify({"message": "Produto nao encontrado ou nao existe"}), 404


@app.route("/api/products/update/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return "Produto nao encontrado ou nao existe"

    data = request.json
    if "name" in data:
        product.name = data["name"]

    if "price" in data:
        product.price = data["price"]

    if "description" in data:
        product.description = data["description"]

    db.session.commit()
    return jsonify(
        {
            "message": "Produto atualizadom com sucesso",
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description,
        }
    )


@app.route("/api/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    product_list = []
    for product in products:
        product_data = {
            "id": product.id,
            "name": product.name,
            "price": product.price,
        }
        product_list.append(product_data)
    return jsonify(product_list)


@app.route("/")
def helloWorld():
    return "Hello World!"


if __name__ == "__main__":
    app.run(debug=True)
