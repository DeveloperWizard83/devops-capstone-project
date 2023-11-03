from flask import jsonify, request, make_response, abort, url_for
from .model import Account, db
from . import app

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

