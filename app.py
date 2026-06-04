from flask import Flask, request, jsonify
from flask_cors import CORS
from docx import Document
import os, zipfile, io, re, json
from datetime import datetime

app = Flask(__name__)
CORS(app)

database = {'reports': []}

AREAS = ['Apoyo Logístico', 'Gestión Sistemas', 'Soporte Telemático', 
         'Soporte INGENI@', 'Documental CENDOI', 'Gestión Proyectos', 
         'INGENI@', 'Producción', 'Administrativa']

def extract_numbers(text):
    return [int(n) for n in re.findall(r'\b(\d+)\b', text) if int(n) < 100000]

def process_docx(file_path):
    try:
        doc = Document(file_path)
        total = 0
        for para in doc.paragraphs:
            text = para.text.strip()
            if text:
                numbers = extract_numbers(text)
                if numbers:
                    total += sum(numbers[:5])
        return total
    except:
        return 0

@app.route('/api/upload', methods=['POST'])
def upload():
    if 'files' not in request.files:
        return jsonify({'error': 'No files'}), 400
    
    files = request.files.getlist('files')
    total_activities = 0
    files_processed = []
    
    for file in files:
        filename = file.filename
        file_count = 0
        
        if filename.endswith('.zip'):
            with zipfile.ZipFile(io.BytesIO(file.read())) as z:
                for f in z.namelist():
                    if f.endswith('.docx'):
                        count = process_docx(io.BytesIO(z.read(f)))
                        file_count += count
                        total_activities += count
            files_processed.append({'name': filename, 'activities': file_count})
        
        elif filename.endswith('.docx'):
            file_count = process_docx(file)
            total_activities += file_count
            files_processed.append({'name': filename, 'activities': file_count})
    
    areas = {area: total_activities // len(AREAS) for area in AREAS}
    
    response_data = {
        'total_activities': total_activities,
        'total_files': len(files_processed),
        'areas': areas,
        'files': files_processed
    }
    
    return jsonify({'success': True, 'data': response_data})

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run()
