from . import create_app

app = create_app()

# Route to list all implemented API methods
@app.route('/methods', methods=['GET'])
def list_api_methods():
    """Endpoint to list all the implemented API methods"""
    output = []
    try:
        for rule in app.url_map.iter_rules():
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
    app.run(debug=True)
