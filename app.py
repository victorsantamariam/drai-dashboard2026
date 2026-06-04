from flask import Flask, request, jsonify
from flask_cors import CORS
from docx import Document
import os
import zipfile
import io
import re
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)

# Configuración
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Base de datos simulada en memoria
database = {
    'reports': [],
    'files': []
}

def extract_numbers_from_text(text):
    """Extrae números del texto"""
    numbers = re.findall(r'\b(\d+)\b', text)
    return [int(n) for n in numbers if int(n) < 100000]

def process_docx_file(file_path):
    """Procesa un archivo DOCX y extrae datos"""
    try:
        doc = Document(file_path)
        data = {
            'tables': [],
            'paragraphs': [],
            'numbers': []
        }

        # Extraer tablas
        for table_idx, table in enumerate(doc.tables):
            table_data = []
            for row in table.rows:
                row_data = [cell.text.strip() for cell in row.cells]
                table_data.append(row_data)
            if table_data:
                data['tables'].append({
                    'index': table_idx,
                    'rows': table_data
                })

        # Extraer texto
        for para in doc.paragraphs:
            if para.text.strip():
                data['paragraphs'].append(para.text.strip())
                # Extraer números
                numbers = extract_numbers_from_text(para.text)
                data['numbers'].extend(numbers)

        return data
    except Exception as e:
        return {'error': str(e)}

def consolidate_data(files_data):
    """Consolida datos de múltiples archivos"""
    consolidated = {
        'total_files': len(files_data),
        'total_tables': sum(len(f['data']['tables']) for f in files_data),
        'areas': {
            'Apoyo Logístico': 0,
            'Gestión Sistemas': 0,
            'Soporte Telemático': 0,
            'Soporte INGENI@': 0,
            'Documental CENDOI': 0,
            'Gestión Proyectos': 0,
            'INGENI@': 0,
            'Producción': 0,
            'Administrativa': 0
        },
        'total_activities': 0,
        'files_processed': []
    }

    # Mapeo de palabras clave a áreas
    area_keywords = {
        'Apoyo Logístico': ['logístico', 'apoyo', 'infraestructura', 'transporte', 'almacén'],
        'Gestión Sistemas': ['sistemas', 'informática', 'it', 'técnico', 'servidor'],
        'Soporte Telemático': ['telemático', 'conferencia', 'videollamada', 'zoom', 'reunión'],
        'Soporte INGENI@': ['ingeni@', 'ingeniatica', 'software', 'aplicación'],
        'Documental CENDOI': ['documental', 'cendoi', 'documento', 'archivo', 'expediente'],
        'Gestión Proyectos': ['proyecto', 'gestión', 'planificación', 'cronograma'],
        'INGENI@': ['ingeni@', 'innovación'],
        'Producción': ['producción', 'manufactura', 'fabricación'],
        'Administrativa': ['administrativo', 'administración', 'rh', 'recursos']
    }

    # Procesar cada archivo
    for file_info in files_data:
        file_name = file_info['filename']
        data = file_info['data']
        text_content = ' '.join(data.get('paragraphs', [])).lower()
        numbers = data.get('numbers', [])

        # Contar actividades basándose en números encontrados
        file_activities = 0
        if numbers:
            file_activities = sum(numbers[:20]) if len(numbers) >= 5 else sum(numbers)
        else:
            # Si no hay números, estimar basándose en el contenido
            file_activities = len(data.get('paragraphs', [])) * 5 + len(data.get('tables', [])) * 10

        # Distribuir actividades entre áreas según palabras clave encontradas
        area_counts = {area: 0 for area in consolidated['areas'].keys()}
        found_areas = []

        for area, keywords in area_keywords.items():
            for keyword in keywords:
                if keyword in text_content:
                    found_areas.append(area)
                    break

        # Si se encontraron áreas, distribuir actividades
        if found_areas:
            activities_per_area = file_activities // len(found_areas)
            for area in found_areas:
                area_counts[area] = activities_per_area
            # Asignar el resto a la primera área
            remainder = file_activities % len(found_areas)
            area_counts[found_areas[0]] += remainder
        else:
            # Si no se detectan áreas, distribuir aleatoriamente
            default_areas = ['Apoyo Logístico', 'Gestión Sistemas', 'Soporte Telemático']
            activities_per_area = file_activities // len(default_areas)
            for area in default_areas:
                area_counts[area] = activities_per_area

        # Actualizar consolidado
        for area, count in area_counts.items():
            consolidated['areas'][area] += count

        consolidated['total_activities'] += file_activities
        consolidated['files_processed'].append({
            'name': file_name,
            'activities': file_activities
        })

    return consolidated

@app.route('/api/health', methods=['GET'])
def health():
    """Endpoint de salud"""
    return jsonify({'status': 'ok', 'message': 'Backend running'}), 200

@app.route('/api/upload', methods=['POST'])
def upload_files():
    """Endpoint para subir archivos DOCX o ZIP"""
    try:
        if 'files' not in request.files:
            return jsonify({'error': 'No files provided'}), 400

        files = request.files.getlist('files')
        results = []
        all_files_data = []

        for file in files:
            if file.filename == '':
                continue

            filename = file.filename

            # Procesar ZIP
            if filename.endswith('.zip'):
                with zipfile.ZipFile(io.BytesIO(file.read())) as zip_ref:
                    for zip_file in zip_ref.namelist():
                        if zip_file.endswith('.docx'):
                            with zip_ref.open(zip_file) as docx_file:
                                doc_data = process_docx_file(io.BytesIO(docx_file.read()))
                                all_files_data.append({
                                    'filename': zip_file,
                                    'data': doc_data
                                })
                                results.append({
                                    'filename': zip_file,
                                    'status': 'processed'
                                })

            # Procesar DOCX directo
            elif filename.endswith('.docx'):
                doc_data = process_docx_file(file)
                all_files_data.append({
                    'filename': filename,
                    'data': doc_data
                })
                results.append({
                    'filename': filename,
                    'status': 'processed'
                })

        # Consolidar datos
        consolidated = consolidate_data(all_files_data)

        # Guardar en base de datos
        report = {
            'id': len(database['reports']) + 1,
            'timestamp': datetime.now().isoformat(),
            'consolidated': consolidated,
            'files': results
        }
        database['reports'].append(report)

        return jsonify({
            'success': True,
            'report_id': report['id'],
            'data': consolidated,
            'files': results
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reports', methods=['GET'])
def get_reports():
    """Obtener todos los reportes"""
    return jsonify({
        'reports': database['reports']
    }), 200

@app.route('/api/reports/<int:report_id>', methods=['GET'])
def get_report(report_id):
    """Obtener un reporte específico"""
    for report in database['reports']:
        if report['id'] == report_id:
            return jsonify(report), 200
    return jsonify({'error': 'Report not found'}), 404

@app.route('/api/reports/<int:report_id>', methods=['DELETE'])
def delete_report(report_id):
    """Eliminar un reporte"""
    for i, report in enumerate(database['reports']):
        if report['id'] == report_id:
            database['reports'].pop(i)
            return jsonify({'success': True}), 200
    return jsonify({'error': 'Report not found'}), 404

@app.route('/api/export/<int:report_id>', methods=['GET'])
def export_report(report_id):
    """Exportar reporte como JSON"""
    for report in database['reports']:
        if report['id'] == report_id:
            return jsonify(report), 200
    return jsonify({'error': 'Report not found'}), 404

@app.route('/', methods=['GET'])
def index():
    """Página principal"""
    return jsonify({'message': 'DRAI Dashboard API', 'version': '1.0'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
