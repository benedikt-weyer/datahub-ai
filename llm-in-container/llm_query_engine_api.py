from flask import Flask, request, jsonify, Response
from flask_cors import CORS, cross_origin

from advanced_sql_query_engine import submit_query
from data_description_access import get_table_names

# Initialize the Flask application and the LLMQueryEngine instance
app = Flask(__name__)

CORS(app,resources={r"/api/*": {"origins": "http://localhost:8000"}})

@app.route('/api/query', methods=['GET'])
def query_get():
    # Access the query parameter from the URL
    query_string = request.args.get("query")

    if not query_string:
        return jsonify({"error": "Missing 'query' parameter"}), 400

    # Create a response using the query string
    response = f'You just submitted the query: {query_string}'

    # Return the JSON response
    return jsonify({
        "query": query_string,
        "response": response
    })

@app.route('/api/query', methods=['POST'])
def query_post():
    data = request.json
    query_string = data.get("query")
    
    if not query_string:
        return jsonify({"error": "Missing 'query' parameter"}), 400
    
    response = submit_query(query_string)
    return jsonify({
        "query": query_string,
        "response": response,
    })



@app.route('/api/data-description', methods=['GET'])
def data_description_get():
    # Access the query parameter from the URL
    #query_string = request.args.get("query")

    #if not query_string:
    #    return jsonify({"error": "Missing 'query' parameter"}), 400

    # Create a response using the query string
    #response = f'You just submitted the query: {query_string}'
    table_names = get_table_names()

    # Return the JSON response
    return jsonify({
        "table-names": table_names,
    })






if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
