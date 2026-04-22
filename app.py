from flask import Flask, render_template, jsonify, request
import requests
import redis
import json
import os

app   = Flask(__name__)
r     = redis.Redis(host=os.getenv('REDIS_HOST', 'redis'), port=6379, decode_responses=True)
ITEMS = os.getenv('ITEM_SVC_URL', 'http://item-service:5001')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/items', methods=['GET'])
def get_items():
    try:
        return jsonify(requests.get(f'{ITEMS}/items', timeout=3).json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/items', methods=['POST'])
def post_item():
    try:
        resp = requests.post(f'{ITEMS}/items', json=request.json, timeout=3)
        return jsonify(resp.json()), resp.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/notifications', methods=['GET'])
def get_notifications():
    try:
        raw = r.lrange('notifications', 0, 19)
        return jsonify([json.loads(n) for n in raw])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
