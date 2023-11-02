"""
Account Service

This microservice handles the lifecycle of Accounts
"""
# pylint: disable=unused-import
from flask import jsonify, request, make_response, abort, url_for   # noqa; F401
from service.models import Account, db
from service.common import status  # HTTP Status Codes
from . import app  # Import Flask application


@app.route("/accounts", methods=["POST"])
def create_account():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid data"}), 400

    account = Account()
    account.deserialize(data)
    db.session.add(account)
    db.session.commit()
    
    location_url = url_for("get_account", account_id=account.id, _external=True)
    
    return make_response(jsonify(account.serialize()), 201, {"Location": location_url})

@app.route("/accounts/<int:account_id>", methods=["GET"])
def get_account(account_id):
    account = Account.query.get(account_id)
    if not account:
        return jsonify({"error": "Account not found"}), 404

    return jsonify(account.serialize()), 200

@app.route("/accounts", methods=["GET"])
def list_accounts():
    accounts = Account.query.all()
    account_list = [account.serialize() for account in accounts]

    return jsonify(account_list), 200

@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_account(account_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid data"}), 400

    account = Account.query.get(account_id)
    if not account:
        return jsonify({"error": "Account not found"}), 404

    # Update the account details based on the provided data
    account.deserialize(data)
    db.session.commit()

    return jsonify(account.serialize()), 200

@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_account(account_id):
    account = Account.query.get(account_id)
    if not account:
        return jsonify({"error": "Account not found"}), 404

    db.session.delete(account)
    db.session.commit()
    
    return "", 204

if __name__ == '__main__':
    app.run(debug=True)
