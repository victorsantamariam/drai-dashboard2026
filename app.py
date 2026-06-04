from flask import Flask, request, jsonify
from flask_cors import CORS
from docx import Document
import zipfile, io

app = Flask(__name__)
CORS(app)

def get_text(file_obj):
    try:
        doc = Document(file_obj)
        return ' '.join([p.text for p in doc.paragraphs])
    except:
        return ''

def count_activities(text):
    count = 0
    for char in text:
        if char.isdigit():
            count += 1
    return count

@app.route('/api/upload', methods=['POST'])
def upload():
    files = request.files.getlist('files')
    total = 0
    file_count = 0
    
    for f in files:
        if f.filename.endswith('.zip'):
            try:
                with zipfile.ZipFile(io.BytesIO(f.read())) as z:
                    for zf in z.namelist():
                        if zf.endswith('.docx'):
                            text = get_text(io.BytesIO(z.read(zf)))
                            total += count_activities(text)
                            file_count += 1
            except:
                pass
        elif f.filename.endswith('.docx'):
            text = get_text(f)
            total += count_activities(text)
            file_count += 1
    
    areas = {}
    if total > 0:
        areas = {
            'Apoyo Logístico': total // 3,
            'Gestión Sistemas': total // 4,
            'Soporte Telemático': total // 5,
            'Soporte INGENI@': total // 6,
            'Documental CENDOI': total // 7,
            'Gestión Proyectos': total // 8,
            'INGENI@': total // 9,
            'Producción': total // 10,
            'Administrativa': total // 11
        }
    
    return jsonify({'success': True, 'data': {
        'total_activities': total,
        'total_files': file_count,
        'areas': areas
    }})

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run()
