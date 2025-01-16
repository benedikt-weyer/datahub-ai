import json

from flask import Flask, request, jsonify, Response
from flask_cors import CORS, cross_origin
from bson import json_util


from logic import data_description_logic, query_logic

# Initialize the Flask application and the LLMQueryEngine instance
app = Flask(__name__)

CORS(app,resources={r"/api/*": {"origins": ["http://localhost:8000"]}})


@app.route('/api/query', methods=['POST'])
def query_post():
    data = request.json
    query_string = data.get("query")
    is_verbose = data.get("is_verbose")
    
    if not query_string:
        return jsonify({"error": "Missing 'query' parameter"}), 400
    
    if not is_verbose:
        is_verbose = False
    
    result = query_logic.query_ai(query_string, is_verbose)

    return jsonify({
        "query": query_string,
        "response": result.get("response"),
        "verbose_output": result.get("verbose_output"),
    })



@app.route('/api/data-description/inactive-table-names', methods=['GET'])
def data_description_inactive_table_names_get():
    # Access the query parameter from the URL
    #query_string = request.args.get("query")

    #if not query_string:
    #    return jsonify({"error": "Missing 'query' parameter"}), 400

    # Create a response using the query string
    #response = f'You just submitted the query: {query_string}'
    inactive_table_names = data_description_logic.get_inactive_table_names()

    # Return the JSON response
    return jsonify({
        "inactive-table-names": inactive_table_names,
    })


@app.route('/api/data-description/active-tables', methods=['GET'])
def data_description_active_tables_get():

    active_tables = data_description_logic.get_active_tables()

    # Return the JSON response
    return jsonify({
        "active-tables": parse_json(active_tables)
    })

@app.route('/api/data-description/active-tables', methods=['POST'])
def data_description_active_tables_post():
    data = request.json
    table_name = data.get("table_name")
    
    if not table_name:
        return jsonify({"error": "Missing 'table_name' parameter"}), 400
    
    response = data_description_logic.add_table_without_description(table_name)
    return jsonify({
        "table_name": table_name,
    })

@app.route('/api/data-description/active-tables', methods=['PUT'])
def data_description_active_tables_put():
    data = request.json
    table_name = data.get("table_name")
    table_description = data.get("table_description")
    
    if not table_name:
        return jsonify({"error": "Missing 'table_name' parameter"}), 400
    
    if not table_description:
        return jsonify({"error": "Missing 'table_description' parameter"}), 400
    
    response = data_description_logic.update_table(table_name, table_description)

    return jsonify({
        "table_name": table_name,
        "table_description": table_description,
    })

@app.route('/api/data-description/active-tables', methods=['DELETE'])
def data_description_active_tables_delete():
    data = request.json
    table_name = data.get("table_name")
    
    if not table_name:
        return jsonify({"error": "Missing 'table_name' parameter"}), 400
    
    response = data_description_logic.remove_table(table_name)
    return jsonify({
        "table_name": table_name,
    })


@app.route('/api/data-description/active-tables/import', methods=['POST'])
def data_description_active_tables_import():
    data = request.json
    file_data = data.get("file_data")
    
    if not file_data:
        return jsonify({"error": "Missing 'file_data' parameter"}), 400
    
    response = data_description_logic.import_active_tables(file_data)
    return jsonify({
        "response": response,
    })




def parse_json(data):
    return json.loads(json_util.dumps(data))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
