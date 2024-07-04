from flask import jsonify, request, current_app as app, abort
from dataTypes import Currency, LiquidityPool, User

@app.route('/currencies', methods=['GET'])
def get_currencies():
    session = app.session
    currencies = session.query(Currency).all()
    return jsonify([currency.to_dict() for currency in currencies])

@app.route('/users', methods=['GET'])
def get_users():
    session = app.session
    users = session.query(User).all()
    return jsonify([user.to_dict() for user in users])

@app.route('/insertUser', methods=['POST'])
def create_user():
    data = request.get_json()

    if not data:
        abort(400, description="No input data provided")

    try:
        new_user = User(
            role_id=data['role_id'],
            wallet_address=bytes.fromhex(data['wallet_address']),
            name=data['name'],
            password=data['password'],
            address=data['address'],
            age=data['age'],
            gender=data['gender'],
            email=data['email'],
            kyc_aml_id=bytes.fromhex(data['kyc_aml_id'])
        )
        session = app.session()
        session.add(new_user)
        session.commit()
        return jsonify(new_user.to_dict()), 201
    except Exception as e:
        session.rollback()
        abort(400, description=f"An error occurred: {str(e)}")

@app.route('/liquidityPools', methods=['GET'])
def get_liquidity_pools():
    session = app.session
    pools = session.query(LiquidityPool).all()
    return jsonify([pool.to_dict() for pool in pools])

@app.route('/currencies/<string:abbreviation>', methods=['GET'])
def get_currency(abbreviation):
    session = app.session()
    currency = session.query(Currency).filter_by(abbreviation=abbreviation).first()
    if not currency:
        abort(404, description="Currency not found")
    return jsonify(currency.to_dict())
