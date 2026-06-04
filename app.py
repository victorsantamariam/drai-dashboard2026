from flask import Flask, request, jsonify
from flask_cors import CORS
from docx import Document
import os, zipfile, io, re, json
from datetime import datetime

app = Flask(__name__)
CORS(app)

database = {'reports': []}

AREAS = {
    'Apoyo Logístico': ['apoyo', 'logístico', 'logistica'],
    'Gestión Sistemas': ['gestión', 'sistemas', 'gestion'],
    'Soporte Telemático': ['soporte', 'telemático', 'telematico'],
    'Soporte INGENI@': ['ingeni@', 'ingenia'],
    'Documental CENDOI': ['documental', 'cendoi'],
    'Gestión Proyectos': ['proyecto', 'proyectos'],
    'INGENI@': ['innovación', 'innovacion'],
    'Producción': ['producción', 'produccion'],
    'Administrativa': ['administrativa', 'admin']
}

def extract_numbers(text):
    return [int(n) for n in re.findall(r'\b(\d+)\b', text) if int(n) < 100000]

def detect_area(text):
    text_lower = text.lower()
    for area, keywords in AREAS.items():
        for keyword in keywords:
            if keyword in text_lower:
                return area
    return 'Otro'

def process_docx(file_path):
    try:
        doc = Document(file_path)
        activities = {area: 0 for area in AREAS}
        activities['Otro'] = 0
        
        for para in doc.paragraphs:
            text = para.text.strip()
            if text:
                numbers = extract_numbers(text)
                if numbers:
                    area = detect_area(text)
                    activities[area] += sum(numbers[:5])
        
        return activities
    except:
        return {area: 0 for area in AREAS}

@app.route('/api/upload', methods=['POST'])
def upload():
    if 'files' not in request.files:
        return jsonify({'error': 'No files'}), 400
    
    files = request.files.getlist('files')
    all_activities = {area: 0 for area in AREAS}
    all_activities['Otro'] = 0
    files_processed = []
    
    for file in files:
        filename = file.filename
        
        if filename.endswith('.zip'):
            with zipfile.ZipFile(io.BytesIO(file.read())) as z:
                for f in z.namelist():
                    if f.endswith('.docx'):
                        activities = process_docx(io.BytesIO(z.read(f)))
                        for area in all_activities:
                            all_activities[area] += activities.get(area, 0)
                        files_processed.append({'name': f, 'areas': activities})
        
        elif filename.endswith('.docx'):
            activities = process_docx(file)
            for area in all_activities:
                all_activities[area] += activities.get(area, 0)
            files_processed.append({'name': filename, 'areas': activities})
    
    total = sum(all_activities.values())
    
    report = {
        'id': len(database['reports'])+1,
        'timestamp': datetime.now().isoformat(),
        'total_activities': total,
        'areas': all_activities,
        'files': files_processed
    }
    database['reports'].append(report)
    
    return jsonify({'success': True, 'data': report})

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run()
