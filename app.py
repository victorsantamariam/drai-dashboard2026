from flask import Flask, request, jsonify
from flask_cors import CORS
from docx import Document
import zipfile, io, re

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

def extract_numbers(text):
    nums = re.findall(r'\b(\d+)\b', text)
    return [int(n) for n in nums if int(n) < 100000]

def process_docx(file_obj):
    try:
        doc = Document(file_obj)
        total = 0
        for para in doc.paragraphs:
            if para.text.strip():
                nums = extract_numbers(para.text)
                if nums:
                    total += sum(nums[:5])
        return total
    except:
        return 0
@app.route('/api/upload', methods=['OPTIONS'])
def handle_preflight():
    return '', 204
@app.route('/api/upload', methods=['POST'])
def upload():
    files = request.files.getlist('files')
    if not files:
        return jsonify({'error': 'No files'}), 400
    
    total = 0
    files_list = []
    
    for file in files:
        name = file.filename
        count = 0
        
        if name.endswith('.zip'):
            try:
                with zipfile.ZipFile(io.BytesIO(file.read())) as z:
                    for f in z.namelist():
                        if f.endswith('.docx'):
                            c = process_docx(io.BytesIO(z.read(f)))
                            count += c
                            total += c
            except:
                pass
        elif name.endswith('.docx'):
            count = process_docx(file)
            total += count
        
        if count > 0:
            files_list.append({'name': name, 'activities': count})
    
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
    
    return jsonify({
        'success': True,
        'data': {
            'total_activities': total,
            'total_files': len(files_list),
            'areas': areas,
            'files': files_list
        }
    })

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run()
