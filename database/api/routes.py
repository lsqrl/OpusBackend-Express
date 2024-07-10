from flask import jsonify, request, current_app as app, abort
from data_types import Currency, LiquidityPool, Users, LiquidityProviderAccountTrans

@app.route('/newUser', methods=['POST'])
def create_user():
    data = request.get_json()

    if not data:
        abort(400, description="No input data provided")

    try:
        new_user = Users(
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

@app.route('/newLPPTransaction', methods=['POST'])
def create_liquidity_pool_transaction():
    data = request.get_json()

    if not data:
        abort(400, description="No input data provided")

    try:
        new_lppt = LiquidityProviderAccountTrans(
            user_id=data['user_id'],
            transaction_type=data['transaction_type'],
            amount=data['amount']
        )
        session = app.session()
        session.add(new_lppt)
        session.commit()
        return jsonify(new_lppt.to_dict()), 201
    except Exception as e:
        session.rollback()
        abort(400, description=f"An error occurred: {str(e)}")

@app.route('/calculateLPBalance/<int:user_id>', methods=['GET'])
def calculate_lp_balance(user_id):
    try:
        session = app.session()
        lp_balance = session.query(LiquidityProviderAccountTrans).filter_by(user_id=user_id).all()
        total_balance = 0
        for balance in lp_balance:
            if balance.transaction_type == 'external_deposit' or balance.transaction_type == 'internal_deposit':
                total_balance += balance.amount
            elif balance.transaction_type == 'external_withdrawal' or balance.transaction_type == 'internal_withdrawal':
                total_balance -= balance.amount
        return jsonify({"balance": total_balance}), 200
    except Exception as e:
        abort(400, description=f"An error occurred: {str(e)}")

@app.route('/checkConnection', methods=['GET'])
def check_connection():
    return jsonify({"message": "Connection successful!"}), 200