from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from models import db, Plant
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

# ------------------ ROUTES ------------------ #

# READ all
@app.get("/plants")
def get_plants():
    plant = db.session.get(Plant, id)
    return jsonify([plant.to_dict() for plant in plants]), 200

# READ one
@app.get("/plants/<int:id>")
def get_plant(id):
    plant = db.session.get(Plant, id)
    if not plant:
        return make_response({"error": "Plant not found"}, 404)
    return jsonify(plant.to_dict()), 200

# CREATE new plant
@app.post("/plants")
def create_plant():
    data = request.get_json()
    if not data:
        return make_response({"error": "Invalid JSON"}, 400)

    try:
        new_plant = Plant(
            name=data.get("name"),
            image=data.get("image"),
            price=data.get("price"),
            is_in_stock=data.get("is_in_stock", True)  # default True
        )

        db.session.add(new_plant)
        db.session.commit()

        return jsonify(new_plant.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return make_response({"error": str(e)}, 400)

# UPDATE plant
@app.patch("/plants/<int:id>")
def update_plant(id):
    plant = db.session.get(Plant, id)
    if not plant:
        return make_response({"error": "Plant not found"}, 404)

    data = request.get_json()
    if "is_in_stock" in data:
        plant.is_in_stock = data["is_in_stock"]

    db.session.commit()
    return jsonify(plant.to_dict()), 200

# DELETE plant
@app.delete("/plants/<int:id>")
def delete_plant(id):
    plant = db.session.get(Plant, id)
    if not plant:
        return make_response({"error": "Plant not found"}, 404)

    db.session.delete(plant)
    db.session.commit()
    return "", 204

# ------------------ RUN SERVER ------------------ #
if __name__ == "__main__":
    app.run(port=5555, debug=True)
