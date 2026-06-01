import re

# Leer archivo raw
with open('/sessions/great-fervent-euler/mnt/outputs/drai-data-raw.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Dividir por archivos
archivos = re.split(r'=== ARCHIVO \d+ ===', content)

# Inicializar estructura de datos
areas_data = {
    'Apoyo Logístico y Videoconferencia': {},
    'Gestión de Sistemas de Información': {},
    'Soporte Telemático': {},
    'Soporte Técnico y Académico INGENI@': {},
    'Gestión Documental CENDOI': {},
    'Unidad de Gestión de Proyectos': {},
    'INGENI@': {},
    'Producción': {},
    'Gestión Administrativa': {}
}

# Procesar cada archivo
for idx, archivo_content in enumerate(archivos[1:], 9):  # Comenzar en archivo 09
    print(f"\n{'='*60}")
    print(f"PROCESANDO ARCHIVO {idx}")
    print(f"{'='*60}")
    
    # Buscar números en el contenido
    # Patrones comunes: "Aulas Programadas: 827" o "827 aulas"
    numeros = re.findall(r'(\d+)', archivo_content)
    if numeros:
        print(f"Números encontrados: {numeros[:20]}")  # Mostrar primeros 20
    
    # Buscar nombres de áreas
    for area in areas_data.keys():
        if area.lower() in archivo_content.lower():
            print(f"✓ Encontrado: {area}")

print("\n" + "="*60)
print("ANÁLISIS COMPLETADO")
print("="*60)
