import json
from flask import Flask, request, jsonify, send_from_directory
from pymongo import MongoClient
import os
from dash import Dash, dcc, html, Input, Output
import dash_table
import pandas as pd

# ---------------------- Load Configuration ---------------------- #

# Load MongoDB configuration from a JSON file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

mongo_username = config['mongo_username']
mongo_password = config['mongo_password']
mongo_host = config['mongo_host']
mongo_port = config['mongo_port']
mongo_auth_db = config['mongo_auth_db']

# ---------------------- Flask API Setup ---------------------- #

# Initialize Flask app
api_app = Flask(__name__)

# MongoDB configuration
mongo_uri = f"mongodb://{mongo_username}:{mongo_password}@{mongo_host}:{mongo_port}/?authSource={mongo_auth_db}"
client = MongoClient(mongo_uri)
db = client["robot_data"]
tofahat_collection = db["tofahat"]

# Directory to save images
IMAGE_SAVE_PATH = "./static/images/"
os.makedirs(IMAGE_SAVE_PATH, exist_ok=True)

@api_app.route('/api/robot/tofahat', methods=['POST'])
def receive_tofaha_data():
    try:
        # Parse data from request
        robot_id = request.form['robot_id']
        tree_id = request.form['tree_id']
        tofaha_id = request.form['tofaha_id']
        status = request.form['status']
        timestamp = request.form['timestamp']

        # Save image if available
        image_url = None
        if 'image' in request.files:
            image = request.files['image']
            image_name = f"{tofaha_id}_{timestamp.replace(':', '_')}.jpg"
            image_path = os.path.join(IMAGE_SAVE_PATH, image_name)
            image.save(image_path)
            image_url = f"/static/images/{image_name}"

        # Insert data into MongoDB
        tofaha_data = {
            "robot_id": robot_id,
            "tree_id": tree_id,
            "tofaha_id": tofaha_id,
            "status": status,
            "timestamp": timestamp,
            "image_url": image_url
        }
        tofahat_collection.insert_one(tofaha_data)

        return jsonify({"message": "Data received successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@api_app.route('/static/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(IMAGE_SAVE_PATH, filename)

# ---------------------- Dash Dashboard Setup ---------------------- #

# Initialize Dash app
dash_app = Dash(__name__, server=api_app, url_base_pathname='/dashboard/')

# Fetch data from MongoDB
def fetch_data():
    data = list(tofahat_collection.find({}, {"_id": 0}))
    return pd.DataFrame(data)

# Layout for the dashboard
dash_app.layout = html.Div([
    html.H1("Tofaha Inspection Dashboard", style={"text-align": "center"}),

    # Data table for tofaha records
    dash_table.DataTable(
        id="tofaha-table",
        columns=[
            {"name": "Robot ID", "id": "robot_id"},
            {"name": "Tree ID", "id": "tree_id"},
            {"name": "Tofaha ID", "id": "tofaha_id"},
            {"name": "Status", "id": "status"},
            {"name": "Timestamp", "id": "timestamp"},
            {"name": "Image", "id": "image_url", "presentation": "markdown"}
        ],
        style_table={"overflowX": "auto"},
        style_cell={"textAlign": "left", "padding": "5px"},
        style_header={"backgroundColor": "#f4f4f4", "fontWeight": "bold"},
        style_data_conditional=[
            {"if": {"filter_query": "{status} = 'rotten'", "column_id": "status"},
             "backgroundColor": "#ffcccc", "color": "#b30000"},
            {"if": {"filter_query": "{status} = 'healthy'", "column_id": "status"},
             "backgroundColor": "#ccffcc", "color": "#006600"}
        ]
    ),

    # Graph for inspection statistics
    dcc.Graph(id="inspection-stats"),

    # Interval for real-time updates
    dcc.Interval(id="interval-update", interval=5000, n_intervals=0)
])

# Callbacks for dynamic updates
@dash_app.callback(
    [Output("tofaha-table", "data"), Output("inspection-stats", "figure")],
    [Input("interval-update", "n_intervals")]
)
def update_dashboard(n):
    df = fetch_data()
    print("Fetched DataFrame:")
    print(df)

    # Ensure 'status' column exists
    if "status" not in df.columns:
        df["status"] = []

    # Update DataTable
    table_data = df.to_dict("records")

    # Generate inspection statistics
    fig = {
        "data": [
            {"x": df["status"].value_counts().index.tolist(),
             "y": df["status"].value_counts().values.tolist(),
             "type": "bar", "name": "Tofaha Status"}
        ],
        "layout": {
            "title": "Inspection Statistics",
            "xaxis": {"title": "Status"},
            "yaxis": {"title": "Count"}
        }
    }

    return table_data, fig

# ---------------------- Run the App ---------------------- #

if __name__ == "__main__":
    api_app.run(host="0.0.0.0", port=5000, debug=True)
