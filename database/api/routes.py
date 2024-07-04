from flask import jsonify, current_app as app, abort
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
