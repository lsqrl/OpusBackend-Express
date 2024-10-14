from . import create_app

from flask import jsonify, request, current_app as app, abort
from database_prod.data_types import *
import datetime

app = create_app()

# Route to list all implemented API methods
@app.route('/methods', methods=['GET'])
def list_api_methods():
    """Endpoint to list all the implemented API methods"""
    output = []
    try:
        for rule in app.url_map.iter_rules():
            if rule.endpoint not in ['static', 'list_api_methods']:
                methods = ', '.join(rule.methods - {"OPTIONS", "HEAD"})
                output.append({
                    "endpoint": rule.endpoint,
                    "url": rule.rule,
                    "methods": methods
                })
        return jsonify(output)
    except Exception as e:
        return []

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)
