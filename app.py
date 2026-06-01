from flask import Flask, request, jsonify
from flask_cors import CORS
from docx import Document
import zipfile, io, re, json
from datetime import datetime

app = Flask(__name__)
CORS(app)
database = {'reports': [], 'files': []}

def extract_numbers(text):
    return [int(n) for n in re.findall(r'\b(\d+)\b', text) if int(n) < 100000]

def process_docx(file_path):
    try:
        doc = Document(file_path)
        data = {'tables': [], 'paragraphs': [], 'numbers': []}
        for idx, table in enumerate(doc.tables):
            rows = [[cell.text.strip() for cell in row.cells] for row in table.rows]
            if rows:
                data['tables'].append({'index': idx, 'rows': rows})
        for para in doc.paragraphs:
            if para.text.strip():
                data['paragraphs'].append(para.text.strip())
                data['numbers'].extend(extract_numbers(para.text))
        return data
    except:
        return {'error': 'error'}

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'message': 'Backend running'})

@app.route('/api/upload', methods=['POST'])
def upload():
    if 'files' not in request.files:
        return jsonify({'error': 'No files'}), 400
    results, all_data = [], []
    for file in request.files.getlist('files'):
        if file.filename.endswith('.zip'):
            with zipfile.ZipFile(io.BytesIO(file.read())) as z:
                for f in z.namelist():
                    if f.endswith('.docx'):
                        data = process_docx(io.BytesIO(z.read(f)))
                        all_data.append({'filename': f, 'data': data})
                        results.append({'filename': f, 'status': 'ok'})
        elif file.filename.endswith('.docx'):
            data = process_docx(file)
            all_data.append({'filename': file.filename, 'data': data})
            results.append({'filename': file.filename, 'status': 'ok'})
    total_activities = sum(sum(d['data'].get('numbers', [])[:10]) for d in all_data)
    report = {'id': len(database['reports'])+1, 'timestamp': datetime.now().isoformat(), 'consolidated': {'total_files': len(all_data), 'total_tables': sum(len(d['data']['tables']) for d in all_data), 'total_activities': total_activities, 'files_processed': [{'name': d['filename'], 'activities': sum(d['data'].get('numbers', [])[:10])} for d in all_data]}, 'files': results}
    database['reports'].append(report)
    return jsonify({'success': True, 'report_id': report['id'], 'data': report['consolidated']})

@app.route('/api/reports', methods=['GET'])
def get_reports():
    return jsonify({'reports': database['reports']})

@app.route('/api/reports/<int:id>', methods=['GET'])
def get_report(id):
    return jsonify(next((r for r in database['reports'] if r['id']==id), {'error': 'not found'}))

if __name__ == '__main__':
    app.run()
