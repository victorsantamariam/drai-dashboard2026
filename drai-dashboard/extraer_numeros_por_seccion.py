import re

# Leer el archivo raw
with open('/sessions/great-fervent-euler/mnt/outputs/drai-data-raw.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Dividir por archivo
archivos = {}
current_archivo = None
current_content = []

for line in content.split('\n'):
    match = re.match(r'=== ARCHIVO (\d+) ===', line)
    if match:
        if current_archivo is not None:
            archivos[current_archivo] = '\n'.join(current_content)
        current_archivo = int(match.group(1))
        current_content = []
    else:
        current_content.append(line)

if current_archivo is not None:
    archivos[current_archivo] = '\n'.join(current_content)

# Procesar archivos 15-18 (nuevos)
print("="*80)
print("EXTRAYENDO DATOS DE ARCHIVOS 15-18 (NUEVOS)")
print("="*80)

for num_archivo in [15, 16, 17, 18]:
    if num_archivo in archivos:
        texto = archivos[num_archivo]
        
        print(f"\n{'─'*80}")
        print(f"ARCHIVO {num_archivo:02d}")
        print(f"{'─'*80}")
        
        # Buscar secciones con palabras clave y números
        secciones = {
            'Apoyo Logístico': [
                r'Aulas? Programadas?[:\s]+(\d+)',
                r'Aulas? por Reservas?[:\s]+(\d+)',
                r'Videoconferencias?[:\s]+(\d+)',
                r'Total Apoyo[:\s]+(\d+)'
            ],
            'Gestión Sistemas': [
                r'Mantenimientos?[:\s]+(\d+)',
                r'Parches?[:\s]+(\d+)',
                r'Backups?[:\s]+(\d+)',
            ],
            'Soporte Telemático': [
                r'Soportes? Técnicos?[:\s]+(\d+)',
                r'Incidentes?[:\s]+(\d+)',
            ],
            'INGENI@ - Talento Tech': [
                r'Campistas?[:\s]+(\d+)',
                r'Matrículas?[:\s]+(\d+)',
                r'Pruebas[:\s]+(\d+)',
            ],
            'Producción': [
                r'Diseños? Gráficos?[:\s]+(\d+)',
                r'Videos?[:\s]+(\d+)',
                r'Producciones?[:\s]+(\d+)',
            ],
        }
        
        for seccion, patterns in secciones.items():
            found_any = False
            for pattern in patterns:
                matches = re.findall(pattern, texto, re.IGNORECASE)
                if matches:
                    if not found_any:
                        print(f"\n  {seccion}:")
                        found_any = True
                    print(f"    {pattern[:40]}: {matches}")

