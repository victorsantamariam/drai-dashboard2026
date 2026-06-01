import xml.etree.ElementTree as ET
import re
import os
from pathlib import Path

# Namespaces
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

# Diccionario para almacenar datos por semana y área
datos_consolidados = {}

# Procesar archivos 09-18
for num_archivo in range(9, 19):
    filename = f"{num_archivo:02d}- Informe Semanal de Actividades.docx"
    print(f"\n{'='*80}")
    print(f"PROCESANDO: {filename}")
    print(f"{'='*80}")
    
    try:
        # Desempaquetar DOCX
        folder = f"docx_{num_archivo:02d}"
        if not os.path.exists(folder):
            os.system(f'unzip -q "{filename}" -d {folder} 2>/dev/null')
        
        # Parsear XML
        tree = ET.parse(f'{folder}/word/document.xml')
        root = tree.getroot()
        
        # Extraer texto completo
        full_text = []
        for t_elem in root.findall('.//w:t', ns):
            if t_elem.text:
                full_text.append(t_elem.text)
        
        combined_text = ' '.join(full_text)
        
        # Buscar números en contextos específicos
        patterns = {
            'aulas_programadas': r'aulas? programadas?.*?(\d+)',
            'aulas_reservas': r'aulas? por reservas?.*?(\d+)',
            'videoconferencias': r'videoconferencia.*?(\d+)',
            'sesiones': r'sesiones?.*?(\d+)',
            'transmisiones': r'transmisiones?.*?(\d+)',
            'emails': r'email.*?(\d+)',
            'solicitudes': r'solicitudes?.*?(\d+)',
        }
        
        print(f"\nNúmeros encontrados en {filename}:")
        for pattern_name, pattern in patterns.items():
            matches = re.findall(pattern, combined_text, re.IGNORECASE)
            if matches:
                print(f"  {pattern_name}: {matches[:10]}")  # Primeros 10 matches
        
        # Contar palabras clave por área
        areas = {
            'Logístico': ['aula', 'reserva', 'infraestructura', 'logístico'],
            'Sistemas': ['mantenimiento', 'parche', 'backup', 'sistemas'],
            'Telemático': ['soporte técnico', 'incidente', 'telemático'],
            'Académico INGENI@': ['email', 'talento tech', 'campista', 'ingeni@'],
            'Documental CENDOI': ['documento', 'solicitud', 'documental', 'cendoi'],
            'Proyectos UGP': ['reunión', 'ugp', 'proyecto', 'paua'],
            'INGENI@': ['ingeni@', 'asesoría', 'seguimiento'],
            'Producción': ['diseño', 'video', 'gráfico', 'producción'],
            'Administrativa': ['contratación', 'compra', 'administrativa', 'trámite']
        }
        
        print(f"\nÁreas detectadas:")
        for area_name, keywords in areas.items():
            area_count = sum(combined_text.lower().count(kw) for kw in keywords)
            if area_count > 0:
                print(f"  {area_name}: {area_count} menciones")
        
    except Exception as e:
        print(f"ERROR procesando {filename}: {e}")

print("\n" + "="*80)
print("EXTRACCIÓN COMPLETADA")
print("="*80)

