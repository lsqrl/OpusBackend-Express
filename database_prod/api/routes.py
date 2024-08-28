from flask import jsonify, current_app as app, abort
from database_prod.data_types import *

def get_class_by_name(class_name):
    try:
        model_class = globals()[class_name]
        return model_class
    except KeyError:
        return None
    
@app.route('/checkConnection', methods=['GET'])
def check_connection():
    return jsonify({"message": "Connection successful!"}), 200


@app.route('/getUsers', methods=['GET'])
def get_users():
    try:
        session = app.session()        
        users = session.query(Users).all()
        users_list = [user.to_dict() for user in users] 

        return jsonify(users_list) 
    except Exception as e:
        abort(400, description=f"An error occurred: {str(e)}")

@app.route('/getClass/<class_name>', methods=['GET'])
def get_class(class_name):
    try:
        model_class = get_class_by_name(class_name)
        
        if model_class is None:
            abort(404, description=f"Class '{class_name}' not found.")

        session = app.session()
        results = session.query(model_class).all()
        
        results_list = [result.to_dict() for result in results]

        return jsonify(results_list)

    except Exception as e:
        abort(400, description=f"An error occurred: {str(e)}")