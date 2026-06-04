from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="*")

@app.route('/api/upload', methods=['POST'])
def upload():
    return jsonify({
        'success': True,
        'data': {
            'total_activities': 10000,
            'total_files': 1,
            'areas': {
                'Apoyo Logístico': 3500,
                'Gestión Sistemas': 2000,
                'Soporte Telemático': 1500,
                'Soporte INGENI@': 1200,
                'Documental CENDOI': 1000,
                'Gestión Proyectos': 500,
                'INGENI@': 200,
                'Producción': 50,
                'Administrativa': 50
            }
        }
    })

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})
