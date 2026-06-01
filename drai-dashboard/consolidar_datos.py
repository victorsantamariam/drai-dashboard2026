import re

# Leer archivo raw con todos los contenidos de archivos 09-18
with open('/sessions/great-fervent-euler/mnt/outputs/drai-data-raw.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Dividir por archivo
archivos = re.split(r'=== ARCHIVO (\d+) ===', content)[1:]  # Evitar la primera división vacía

# Crear pares (número, contenido)
datos_por_archivo = {}
for i in range(0, len(archivos), 2):
    if i+1 < len(archivos):
        num = int(archivos[i])
        texto = archivos[i+1]
        datos_por_archivo[num] = texto

print("Archivos procesados:")
for num in sorted(datos_por_archivo.keys()):
    lines = len(datos_por_archivo[num].split('\n'))
    print(f"  Archivo {num:02d}: {lines} líneas")

# Extraer datos por área de cada archivo
areas_mapping = {
    'Apoyo Logístico': ['apoyo logístico', 'logístico', 'aulas programadas', 'aulas por reservas', 'videoconferencia'],
    'Gestión Sistemas': ['gestión de sistemas', 'sistemas de información', 'mantenimientos', 'parches'],
    'Soporte Telemático': ['soporte telemático', 'soportes técnicos', 'incidentes'],
    'Soporte INGENI@': ['soporte académico ingeni@', 'talento tech', 'campistas', 'ingeni@'],
    'Documental CENDOI': ['documental cendoi', 'cendoi', 'documentos procesados'],
    'Gestión Proyectos': ['gestión de proyectos', 'ugp', 'reuniones ugp'],
    'INGENI@': ['ingeni@', 'pties', 'estudia', 'ava'],
    'Producción': ['producción', 'diseños gráficos', 'videos', 'producciones'],
    'Administrativa': ['gestión administrativa', 'contratación', 'compras', 'licencias']
}

# Procesar cada archivo
print("\n" + "="*80)
print("DATOS CONSOLIDADOS POR ARCHIVO Y ÁREA")
print("="*80)

for num_archivo in sorted(datos_por_archivo.keys()):
    texto = datos_por_archivo[num_archivo]
    
    print(f"\nARCHIVO {num_archivo:02d}:")
    print("-" * 80)
    
    # Extraer números del texto
    numeros = re.findall(r'\d+', texto)
    
    # Buscar áreas y extracto números
    for area_name, keywords in areas_mapping.items():
        found = False
        for kw in keywords:
            if kw.lower() in texto.lower():
                found = True
                break
        
        if found:
            # Extraer contexto alrededor del área
            idx = next((i for i, kw in enumerate(keywords) if kw.lower() in texto.lower()), -1)
            if idx >= 0:
                pattern = keywords[idx]
                # Encontrar posición del patrón
                pos = texto.lower().find(pattern.lower())
                if pos >= 0:
                    context = texto[max(0, pos-100):min(len(texto), pos+300)]
                    # Extraer números del contexto
                    context_nums = re.findall(r'\d+', context)
                    print(f"  ✓ {area_name}: números encontrados = {context_nums[:5]}")

print("\n" + "="*80)
print("ANÁLISIS COMPLETADO - Datos listos para consolidación")
print("="*80)

