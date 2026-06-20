from flask import Flask, request, jsonify
import boto3
from datetime import datetime
import os
from decimal import Decimal
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# AWS connections
s3 = boto3.client('s3', region_name='us-east-1')
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('hitman-player-stats')

BUCKET = 'hitman-npc-data'
MODEL_KEY = 'rl_model/zombie_model.zip'

# ─────────────────────────────────────────────
# ENDPOINT 1: Health Check
# ─────────────────────────────────────────────
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'status': 'ok', 'message': 'Hitman API is running'}), 200

# ─────────────────────────────────────────────
# ENDPOINT 2: Upload RL Model
# ─────────────────────────────────────────────
@app.route('/upload-model', methods=['POST'])
def upload_model():
    if 'model' not in request.files:
        return jsonify({'error': 'No model file provided'}), 400
    file = request.files['model']
    s3.upload_fileobj(file, BUCKET, MODEL_KEY)
    return jsonify({'status': 'model uploaded successfully'}), 200

# ─────────────────────────────────────────────
# ENDPOINT 3: Get RL Model Download URL
# ─────────────────────────────────────────────
@app.route('/get-model-url', methods=['GET'])
def get_model_url():
    try:
        url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET, 'Key': MODEL_KEY},
            ExpiresIn=3600
        )
        return jsonify({'url': url}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ─────────────────────────────────────────────
# ENDPOINT 4: Save Player Session Stats
# ─────────────────────────────────────────────
@app.route('/save-session', methods=['POST'])
def save_session():
    data = request.json
    required = ['player_id', 'kills', 'health_left', 'weapon', 'session_time']
    for field in required:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
    table.put_item(Item={
        'player_id':    data['player_id'],
        'timestamp':    str(datetime.now()),
        'kills':        int(data['kills']),
        'health_left':  Decimal(str(data['health_left'])),
        'weapon':       data['weapon'],
        'session_time': Decimal(str(data['session_time'])),
        'ai_type':      data.get('ai_type', 'FSM')
    })
    return jsonify({'status': 'session saved'}), 200

    # ─────────────────────────────────────────────
# ENDPOINT 5: Get Player Stats
# Called by: Website dashboard
# ─────────────────────────────────────────────
@app.route('/get-stats', methods=['GET'])
def get_stats():
    try:
        response = table.scan()
        items = response.get('Items', [])
        def convert(obj):
            if isinstance(obj, Decimal):
                return float(obj)
            return obj
        cleaned = [{k: convert(v) for k, v in item.items()} for item in items]
        return jsonify({'sessions': cleaned, 'total': len(cleaned)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)