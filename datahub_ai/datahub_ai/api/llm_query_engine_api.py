import json
from bson import json_util

from flask import Flask, request, jsonify
from flask_cors import CORS

from llama_index.core.storage.chat_store import SimpleChatStore

from datahub_ai.logic import data_description_logic, query_logic
import os




# initialize the Flask application with the module name
app = Flask(__name__)


# enable cors for all api calls from django
CORS(app, resources={"/api/*": {"origins": ["http://localhost:8000"]}})


# route for quering the datahub ai
@app.route('/api/query', methods=['POST'])
def query_post():

    # get requst json data
    data = request.json

    # extract different elements from the json data
    query_string = data.get("query")
    is_verbose = data.get("is_verbose")
    chat_store_json = data.get("chat_store_json", None)

    # initialize chat store from request data if available
    chat_store = None
    if chat_store_json is not None:
        chat_store = SimpleChatStore.from_json(chat_store_json)


    # return error if query string is not available
    if not query_string:
        return jsonify({"error": "Missing 'query' parameter"}), 400

    # set is_verbose to False if not available
    if not is_verbose:
        is_verbose = False


    # query the datahub ai
    result = query_logic.query_ai(query_string, is_verbose, chat_store=chat_store)


    # get the chat store from the ai query result used for providing context to the next query
    chat_store_out = result.get("chat_store", None)
    # convert chat store to json
    chat_store_out_json = None
    if chat_store_out is not None:
        chat_store_out_json = chat_store_out.json()


    # Return the JSON response
    return jsonify({
        "query": query_string,
        "response": result.get("response"),
        "verbose_output": result.get("verbose_output"),
        "chat_store_json": chat_store_out_json,
    })



# route for getting the names of the inactive tables, that are not allowed to be used by the datahub ai
@app.route('/api/data-description/inactive-table-names', methods=['GET'])
def data_description_inactive_table_names_get():

    # get the names of the inactive tables
    inactive_table_names = data_description_logic.get_inactive_table_names()

    # Return the JSON response
    return jsonify({
        "inactive-table-names": inactive_table_names,
    })


# route for getting the names of the active tables, that are used by the datahub ai
@app.route('/api/data-description/active-tables', methods=['GET'])
def data_description_active_tables_get():

    # get the names of the active tables
    active_tables = data_description_logic.get_active_tables()


    # Return the JSON response
    return jsonify({
        "active-tables": parse_json(active_tables)
    })

# route for adding a table to the active tables
@app.route('/api/data-description/active-tables', methods=['POST'])
def data_description_active_tables_post():

    # get the request json data
    data = request.json

    # extract the table name from the json data
    table_name = data.get("table_name")


    # return error if table name is not available
    if not table_name:
        return jsonify({"error": "Missing 'table_name' parameter"}), 400


    # add the table to the active tables
    response = data_description_logic.add_table_without_description(table_name)


    # Return the JSON response
    return jsonify({
        "table_name": table_name,
    })

# route for updating the description of a table in the active tables
@app.route('/api/data-description/active-tables', methods=['PUT'])
def data_description_active_tables_put():

    # get the request json data
    data = request.json

    # extract the table name and table description from the json data
    table_name = data.get("table_name")
    table_description = data.get("table_description")


    # return error if table name or table description is not available
    if not table_name:
        return jsonify({"error": "Missing 'table_name' parameter"}), 400

    # return error if table description is not available
    if not table_description:
        return jsonify({"error": "Missing 'table_description' parameter"}), 400


    # update the table description
    response = data_description_logic.update_table(table_name, table_description)


    # Return the JSON response
    return jsonify({
        "table_name": table_name,
        "table_description": table_description,
    })

# route for deleting a table from the active tables
@app.route('/api/data-description/active-tables', methods=['DELETE'])
def data_description_active_tables_delete():

    # get the request json data
    data = request.json

    # extract the table name from the json data
    table_name = data.get("table_name")


    # return error if table name is not available
    if not table_name:
        return jsonify({"error": "Missing 'table_name' parameter"}), 400


    # delete the table from the active tables
    response = data_description_logic.remove_table(table_name)


    # Return the JSON response
    return jsonify({
        "table_name": table_name,
    })


# route for importing the active tables from a file
@app.route('/api/data-description/active-tables/import', methods=['POST'])
def data_description_active_tables_import():

    # get the request json data
    data = request.json
    file_data = data.get("file_data")


    # return error if file data is not available
    if not file_data:
        return jsonify({"error": "Missing 'file_data' parameter"}), 400


    # import the active tables from the file
    response = data_description_logic.import_active_tables(file_data)


    # Return the JSON response
    return jsonify({
        "response": response,
    })




def parse_json(data):
    return json.loads(json_util.dumps(data))


# if this is the main thread of execution start the server
if __name__ == '__main__':
    # start the server listening on port 8001 and allow all incoming requests
    app.run(host='0.0.0.0', port=8001)
