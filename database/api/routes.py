from flask import jsonify, request, current_app as app, abort
from data_types import Currency, LiquidityPool, LiquidityPoolTrans, Users, LiquidityProviderAccountTrans

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

@app.route('/calculatePoolBalance/<string:currency>', methods=['GET'])
def calculate_pool_balance(currency):
    try:
        session = app.session()
        currency_id = session.query(Currency).filter_by(abbreviation=currency).first().id
        liquidity_pool_id = session.query(LiquidityPool).filter_by(currency_id=currency_id).first().id
        pool_rows = session.query(LiquidityPoolTrans).filter_by(pool_id=liquidity_pool_id).all()
        total_balance = 0
        for row in pool_rows:
            total_balance += row.amount
        return jsonify({"balance": total_balance}), 200
    except Exception as e:
        abort(400, description=f"An error occurred: {str(e)}")

@app.route('/calculateUserShares/<string:currency>/<int:user_id>', methods=['GET'])
def calculate_user_shares(currency, user_id):
    try:
        session = app.session()
        currency_id = session.query(Currency).filter_by(abbreviation=currency).first().id
        liquidity_pool_id = session.query(LiquidityPool).filter_by(currency_id=currency_id).first().id
        pool_rows = session.query(LiquidityPoolTrans).filter_by(pool_id=liquidity_pool_id).filter_by(user_id=user_id).all()
        
        user_shares = 0
        for row in pool_rows:
            user_shares += row.user_shares

        return jsonify({"shares": user_shares}), 200
    except Exception as e:
        abort(400, description=f"An error occurred: {str(e)}")

@app.route('/allocate', methods=['POST'])
def allocate():
    data = request.get_json()

    if not data:
        abort(400, description="No input data provided")

    currency = data['currency']
    # Get the pool's total balance
    session = app.session()
    print(f"Currency: {currency}")
    currency_id = session.query(Currency).filter_by(abbreviation=currency).first().id
    liquidity_pool_id = session.query(LiquidityPool).filter_by(currency_id=currency_id).first().id
    pool_rows = session.query(LiquidityPoolTrans).filter_by(pool_id=liquidity_pool_id).all()
    
    total_pool_balance = 0
    for row in pool_rows:
        total_pool_balance += row.amount

    total_pool_shares = 0
    for row in pool_rows:
        total_pool_shares += row.user_shares

    user_shares = 0
    if total_pool_balance == 0:
        user_shares = data['amount']
    else: user_shares = (data['amount'] * total_pool_shares) / total_pool_balance

    try:
        new_allocation = LiquidityPoolTrans(
            user_id=data['user_id'],
            pool_id=liquidity_pool_id,
            transaction_type='user_allocation',
            user_shares=user_shares,
            amount=data['amount']
        )

        new_lp_balance = LiquidityProviderAccountTrans(
            user_id=data['user_id'],
            transaction_type='internal_withdrawal',
            amount=data['amount']
        )
        
        session.add(new_allocation)
        session.add(new_lp_balance)
        session.commit()
        return jsonify(new_allocation.to_dict()), 201
    except Exception as e:
        session.rollback()
        abort(400, description=f"An error occurred: {str(e)}")


@app.route('/deallocate', methods=['POST'])
def deallocate():
    data = request.get_json()

    if not data:
        abort(400, description="No input data provided")

    currency = data['currency']
    # Get the pool's total balance
    session = app.session()
    currency_id = session.query(Currency).filter_by(abbreviation=currency).first().id
    liquidity_pool_id = session.query(LiquidityPool).filter_by(currency_id=currency_id).first().id
    pool_rows = session.query(LiquidityPoolTrans).filter_by(pool_id=liquidity_pool_id).all()
    
    total_pool_balance = 0
    for row in pool_rows:
        total_pool_balance += row.amount

    total_pool_shares = 0
    for row in pool_rows:
        total_pool_shares += row.user_shares

    user_shares = 0
    if total_pool_balance == 0:
        user_shares = data['amount']
    else: user_shares = (data['amount'] * total_pool_shares) / total_pool_balance

    try:
        new_allocation = LiquidityPoolTrans(
            user_id=data['user_id'],
            pool_id=liquidity_pool_id,
            transaction_type='user_deallocation',
            user_shares=-user_shares,
            amount=-data['amount']
        )

        new_lp_balance = LiquidityProviderAccountTrans(
            user_id=data['user_id'],
            transaction_type='internal_deposit',
            amount=data['amount']
        )
        
        session.add(new_allocation)
        session.add(new_lp_balance)
        session.commit()
        return jsonify(new_allocation.to_dict()), 201
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

@app.route('/calculateAllocatedBalance/<int:user_id>', methods=['GET'])
def calculate_allocated_balance(user_id):
    try:
        session = app.session()
        lp_balance = session.query(LiquidityProviderAccountTrans).filter_by(user_id=user_id).all()
        total_balance = 0
        for balance in lp_balance:
            if balance.transaction_type == 'internal_withdrawal':
                total_balance += balance.amount
            elif balance.transaction_type == 'internal_deposit':
                total_balance -= balance.amount
        return jsonify({"balance": total_balance}), 200
    except Exception as e:
        abort(400, description=f"An error occurred: {str(e)}")

@app.route('/checkConnection', methods=['GET'])
def check_connection():
    return jsonify({"message": "Connection successful!"}), 200