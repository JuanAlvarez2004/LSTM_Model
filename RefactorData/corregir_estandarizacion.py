import pandas as pd

def corregir_estandarizacion(archivo_entrada, archivo_salida):
    """
    Corrige la estandarización de equipos en el CSV, cambiando específicamente
    'Independiente' que fue estandarizado incorrectamente como 'Independiente Santa Fe' 
    a 'Independiente Medellín'.
    
    La función realiza las siguientes correcciones:
    1. Cambia 'Independiente Santa Fe' a 'Independiente Medellín' para los registros donde
       el equipo/oponente original es 'Independiente'
    2. Actualiza las columnas booleanas correspondientes
    3. Verifica y mantiene la estandarización correcta de 'Santa Fe' como 'Independiente Santa Fe'
    
    Args:
        archivo_entrada: Ruta del archivo CSV de entrada
        archivo_salida: Ruta donde se guardará el archivo CSV corregido
    
    Returns:
        Dict: Diccionario con estadísticas de las correcciones realizadas
    """
    # Cargar el CSV
    print(f"Cargando archivo: {archivo_entrada}")
    df = pd.read_csv(archivo_entrada)
    
    # Contar registros antes de la corrección
    registros_totales = len(df)
    print(f"Total de registros en el archivo: {registros_totales}")
    
    # Contar casos específicos antes de la corrección
    equipos_a_corregir = len(df[
        (df['Equipo'] == 'Independiente') & 
        (df['Equipo_Estandarizado'] == 'Independiente Santa Fe')
    ])
    
    oponentes_a_corregir = len(df[
        (df['Oponente'] == 'Independiente') & 
        (df['Oponente_Estandarizado'] == 'Independiente Santa Fe')
    ])
    
    print(f"Registros con Equipo='Independiente' y Equipo_Estandarizado='Independiente Santa Fe': {equipos_a_corregir}")
    print(f"Registros con Oponente='Independiente' y Oponente_Estandarizado='Independiente Santa Fe': {oponentes_a_corregir}")
    
    # Primero crear la columna para Independiente Medellín si no existe
    if 'Equipo_Independiente Medellín' not in df.columns:
        df['Equipo_Independiente Medellín'] = 0  # Usando 0 para False, ya que las columnas booleanas usan valores numéricos
    
    if 'Oponente_Independiente Medellín' not in df.columns:
        df['Oponente_Independiente Medellín'] = 0  # Usando 0 para False
    
    # Realizar correcciones en la estandarización
    # 1. Corregir "Independiente" a "Independiente Medellín" en la columna Equipo_Estandarizado
    df.loc[df['Equipo'] == 'Independiente', 'Equipo_Estandarizado'] = 'Independiente Medellín'
    
    # 2. Corregir "Independiente" a "Independiente Medellín" en la columna Oponente_Estandarizado
    df.loc[df['Oponente'] == 'Independiente', 'Oponente_Estandarizado'] = 'Independiente Medellín'
    
    # Actualizar columnas booleanas
    # Para equipos
    df.loc[df['Equipo_Estandarizado'] == 'Independiente Medellín', 'Equipo_Independiente Medellín'] = 1
    
    # Para oponentes
    df.loc[df['Oponente_Estandarizado'] == 'Independiente Medellín', 'Oponente_Independiente Medellín'] = 1
    
    # Actualizar la columna Oponente_Independiente Santa Fe para revertir la asignación incorrecta
    # Cambiar a 0 (False) donde el oponente ha sido reasignado como Independiente Medellín
    df.loc[df['Oponente'] == 'Independiente', 'Oponente_Independiente Santa Fe'] = 0
    
    # Verificar correcciones
    equipos_corregidos = len(df[
        (df['Equipo'] == 'Independiente') & 
        (df['Equipo_Estandarizado'] == 'Independiente Medellín')
    ])
    
    oponentes_corregidos = len(df[
        (df['Oponente'] == 'Independiente') & 
        (df['Oponente_Estandarizado'] == 'Independiente Medellín')
    ])
    
    print(f"Registros con Equipo='Independiente' y Equipo_Estandarizado='Independiente Medellín' después de la corrección: {equipos_corregidos}")
    print(f"Registros con Oponente='Independiente' y Oponente_Estandarizado='Independiente Medellín' después de la corrección: {oponentes_corregidos}")
    
    # Verificar que las columnas booleanas se actualizaron correctamente
    oponentes_bool_corregidos = len(df[
        (df['Oponente'] == 'Independiente') & 
        (df['Oponente_Estandarizado'] == 'Independiente Medellín') &
        (df['Oponente_Independiente Santa Fe'] == 0) &
        (df['Oponente_Independiente Medellín'] == 1)
    ])
    
    print(f"Registros con Oponente='Independiente' donde las columnas booleanas se corrigieron correctamente: {oponentes_bool_corregidos}")
    
    # Verificar que Santa Fe sigue correctamente mapeado a Independiente Santa Fe
    santa_fe_equipo = len(df[
        (df['Equipo'] == 'Santa Fe') & 
        (df['Equipo_Estandarizado'] == 'Independiente Santa Fe')
    ])
    
    santa_fe_oponente = len(df[
        (df['Oponente'] == 'Santa Fe') & 
        (df['Oponente_Estandarizado'] == 'Independiente Santa Fe')
    ])
    
    print(f"Registros con Equipo='Santa Fe' y Equipo_Estandarizado='Independiente Santa Fe': {santa_fe_equipo}")
    print(f"Registros con Oponente='Santa Fe' y Oponente_Estandarizado='Independiente Santa Fe': {santa_fe_oponente}")
    
    # Verificar si hay algún registro que aún tenga un problema de coherencia
    problematicos = len(df[
        (df['Oponente'] == 'Independiente') & 
        (df['Oponente_Estandarizado'] == 'Independiente Medellín') &
        (df['Oponente_Independiente Santa Fe'] == 1)
    ])
    
    if problematicos > 0:
        print(f"ADVERTENCIA: Hay {problematicos} registros con inconsistencias en las columnas booleanas.")
    
    # Guardar el archivo corregido
    df.to_csv(archivo_salida, index=False)
    print(f"Archivo corregido guardado como: {archivo_salida}")
    
    return {
        'total_registros': registros_totales,
        'equipos_corregidos': equipos_corregidos,
        'oponentes_corregidos': oponentes_corregidos,
        'oponentes_bool_corregidos': oponentes_bool_corregidos
    }

# Ejemplo de uso
if __name__ == "__main__":
    # Rutas de archivos
    archivo_entrada = "Goleadores_Procesados.csv"
    archivo_salida = "../data/Goleadores_Procesados.csv"
    
    # Ejecutar la corrección
    resultado = corregir_estandarizacion(archivo_entrada, archivo_salida)
    
    print("\nResumen:")
    print(f"Total de registros procesados: {resultado['total_registros']}")
    print(f"Equipos corregidos: {resultado['equipos_corregidos']}")
    print(f"Oponentes corregidos: {resultado['oponentes_corregidos']}")
    print(f"Oponentes con columnas booleanas corregidas: {resultado['oponentes_bool_corregidos']}")