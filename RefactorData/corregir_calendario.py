import pandas as pd
import re
from datetime import datetime

def estandarizar_nombre_equipo(nombre):
    """
    Estandariza nombres de equipos para coincidir con los datos históricos.
    
    Args:
        nombre: Nombre del equipo que puede estar en diversos formatos
    
    Returns:
        Nombre estandarizado que coincide con el formato del CSV histórico
    """
    # Primero limpiamos el nombre para manejar posibles espacios extras
    nombre = nombre.strip()
    
    # Mapeo completo y actualizado de todos los equipos
    mapeo_equipos = {
        # Junior
        'Atlético Junior': 'Junior',
        'Junior': 'Junior',
        
        # Atlético Nacional
        'Nacional': 'Atlético Nacional',
        'Atlético Nacional': 'Atlético Nacional',
        
        # Pereira
        'Deportivo Pereira': 'Pereira',
        'Pereira': 'Pereira',
        'Pererira': 'Pereira',  # Corrección de error tipográfico
        
        # Bucaramanga
        'Atlético Bucaramanga': 'Bucaramanga',
        'Bucaramanga': 'Bucaramanga',
        
        # Independiente Santa Fe
        'Santa Fe': 'Independiente Santa Fe',
        'Independiente Santa Fe': 'Independiente Santa Fe',
        
        # Deportivo Cali
        'Cali': 'Deportivo Cali',
        'Deportivo Cali': 'Deportivo Cali',
        
        # América de Cali
        'América': 'América de Cali',
        'América de Cali': 'América de Cali',
        
        # Millonarios
        'Millonarios': 'Millonarios',
        
        # Once Caldas
        'Once Caldas': 'Once Caldas',
        
        # Rionegro (Águilas Doradas)
        'Águilas Doradas': 'Rionegro',
        'Rionegro': 'Rionegro',
        
        # La Equidad
        'La Equidad': 'La Equidad',
        'Equidad': 'La Equidad',
        
        # Envigado
        'Envigado': 'Envigado',
        
        # Fortaleza
        'Fortaleza': 'Fortaleza CEIF',
        'Fortaleza CEIF': 'Fortaleza CEIF',
        
        # Unión Magdalena
        'Unión Magdalena': 'Unión Magdalena',
        
        # Deportivo Pasto
        'Pasto': 'Deportivo Pasto',
        'Deportivo Pasto': 'Deportivo Pasto',
        
        # Deportes Tolima
        'Tolima': 'Deportes Tolima',
        'Deportes Tolima': 'Deportes Tolima',
        
        # Alianza FC
        'Alianza': 'Alianza FC',
        'Alianza FC': 'Alianza FC',
        
        # Independiente Medellín (corregido)
        'Independiente': 'Independiente Medellín',
        'Medellín': 'Independiente Medellín',
        'Independiente Medellín': 'Independiente Medellín',
        'DIM': 'Independiente Medellín',
        
        # Boyacá Chicó
        'Chicó': 'Boyacá Chicó',
        'Boyacá Chicó': 'Boyacá Chicó',
        
        # Llaneros
        'Llaneros': 'Llaneros'
    }
    
    # Retornar el nombre estandarizado, o el nombre original si no está en el mapeo
    return mapeo_equipos.get(nombre, nombre)

def calendario_txt_a_csv(ruta_calendario, ruta_salida):
    """
    Convierte el archivo de calendario.txt a un CSV estructurado.
    
    Args:
        ruta_calendario: Ruta al archivo de calendario en formato texto
        ruta_salida: Ruta donde se guardará el archivo CSV procesado
    
    Returns:
        DataFrame con el calendario procesado
    """
    # Leer el archivo de texto
    with open(ruta_calendario, 'r', encoding='utf-8') as f:
        lineas = f.read().splitlines()
    
    # Variables para el procesamiento
    partidos = []
    fecha_numero = None
    fecha_texto = None
    fecha_completa = None
    
    # Diccionario para convertir nombres de meses
    meses = {
        'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4,
        'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,
        'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
    }
    
    # Fechas específicas para jornadas sin fecha explícita (basadas en el calendario)
    # Para las fechas 16-20 que no tienen la línea con la fecha
    fechas_jornadas = {
        16: "2025-04-26",  # Estimación para la Fecha 16 (una semana después de la Fecha 15)
        17: "2025-05-03",  # Estimación para la Fecha 17
        18: "2025-05-10",  # Estimación para la Fecha 18
        19: "2025-05-17",  # Estimación para la Fecha 19
        20: "2025-05-24"   # Estimación para la Fecha 20
    }
    
    # Procesar líneas
    i = 0
    while i < len(lineas):
        linea = lineas[i].strip()
        
        # Detectar línea de fecha (jornada)
        match_fecha = re.match(r'Fecha (\d+)', linea)
        if match_fecha:
            fecha_numero = int(match_fecha.group(1))
            fecha_texto = None
            fecha_completa = fechas_jornadas.get(fecha_numero, None)  # Valor por defecto en caso de no encontrar en la siguiente línea
            
            # Buscar la siguiente línea con la fecha
            if i + 1 < len(lineas):
                fecha_linea = lineas[i + 1].strip()
                # Verificar si la siguiente línea contiene un día de la semana
                if any(dia in fecha_linea.lower() for dia in ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']):
                    fecha_texto = fecha_linea
                    
                    # Extraer información de fecha
                    try:
                        # Patrón para extraer el día y mes
                        match_dia_mes = re.search(r'(\d+) de ([a-zA-ZáéíóúÁÉÍÓÚ]+)', fecha_texto)
                        if match_dia_mes:
                            dia = int(match_dia_mes.group(1))
                            mes_nombre = match_dia_mes.group(2).lower()
                            mes = meses.get(mes_nombre, None)
                            
                            if mes:
                                fecha_completa = f"2025-{mes:02d}-{dia:02d}"
                    except Exception:
                        pass  # Mantener el valor por defecto de fecha_completa
        
        # Detectar línea de partido
        elif linea.startswith('-') and 'vs.' in linea:
            # Extraer equipos
            match_partido = re.match(r'-([^-]+)\s+vs\.\s+([^-]+)', linea)
            if match_partido and fecha_numero is not None:
                local = match_partido.group(1).strip()
                visitante = match_partido.group(2).strip()
                
                # Estandarizar nombres
                local_estandarizado = estandarizar_nombre_equipo(local)
                visitante_estandarizado = estandarizar_nombre_equipo(visitante)
                
                # Añadir a la lista de partidos
                partidos.append({
                    'Fecha_Numero': fecha_numero,
                    'Fecha': fecha_completa,
                    'Local': local_estandarizado,
                    'Visitante': visitante_estandarizado
                })
        
        i += 1
    
    # Crear DataFrame
    df_calendario = pd.DataFrame(partidos)
    
    # Convertir la columna de fecha a datetime si es posible
    if 'Fecha' in df_calendario.columns:
        df_calendario['Fecha'] = pd.to_datetime(df_calendario['Fecha'], errors='coerce')
    
    # Guardar a CSV
    df_calendario.to_csv(ruta_salida, index=False)
    
    return df_calendario

def main():
    """Función principal para ejecutar la conversión"""
    # Rutas de archivos
    ruta_calendario = 'calendario_2025.txt'
    ruta_salida = '../data/calendario_2025.csv'
    
    # Procesar el calendario
    df_calendario = calendario_txt_a_csv(ruta_calendario, ruta_salida)
    
    # Imprimir información
    print(f"Calendario procesado exitosamente.")
    print(f"Total de partidos: {len(df_calendario)}")
    print(f"Archivo guardado en: {ruta_salida}")
    
    # Mostrar las primeras filas para verificación
    print("\nPrimeras 5 filas del calendario procesado:")
    print(df_calendario.head(5))
    
    # Verificar la distribución de partidos por jornada
    partidos_por_fecha = df_calendario.groupby('Fecha_Numero').size()
    print("\nPartidos por fecha:")
    for fecha, cantidad in partidos_por_fecha.items():
        print(f"Fecha {fecha}: {cantidad} partidos")
    
    # Verificar la estandarización
    equipos_locales = set(df_calendario['Local'])
    equipos_visitantes = set(df_calendario['Visitante'])
    todos_equipos = equipos_locales.union(equipos_visitantes)
    
    print(f"\nTotal de equipos únicos: {len(todos_equipos)}")
    print(f"Equipos en el calendario: {sorted(todos_equipos)}")
    
    # Verificar fechas
    fechas_presentes = df_calendario['Fecha'].dropna().unique()
    print(f"\nFechas en el calendario: {len(fechas_presentes)}")
    print(f"Rango de fechas: {min(fechas_presentes)} a {max(fechas_presentes)}")
    
    # Verificar que todos los equipos juegan tanto de local como de visitante
    print("\nVerificación de equipos local/visitante:")
    for equipo in sorted(todos_equipos):
        juegos_local = len(df_calendario[df_calendario['Local'] == equipo])
        juegos_visitante = len(df_calendario[df_calendario['Visitante'] == equipo])
        total_juegos = juegos_local + juegos_visitante
        print(f"{equipo}: {total_juegos} partidos ({juegos_local} local, {juegos_visitante} visitante)")

if __name__ == '__main__':
    main()