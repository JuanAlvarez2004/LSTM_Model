import pandas as pd
import glob

# Lista de archivos CSV a unir
archivos_csv = [
    '../BackupResultados/predicciones_lstm_Carlos_Bacca_mejorado.csv',
    '../BackupResultados/predicciones_lstm_Dayro_Moreno_mejorado.csv',
    '../BackupResultados/predicciones_lstm_Hugo_Rodallega_mejorado.csv',
    '../BackupResultados/predicciones_lstm_Leonardo_Castro_mejorado.csv',
    '../BackupResultados/predicciones_lstm_Marco_Perez_mejorado.csv'
]

# Leer y concatenar todos los DataFrames
dataframes = []
for archivo in archivos_csv:
    df = pd.read_csv(archivo)
    dataframes.append(df)

df_completo = pd.concat(dataframes, ignore_index=True)

# Renombrar las columnas especificadas
df_completo = df_completo.rename(columns={
    'Prediccion_Goles': 'Prediccion_Entero',
    'Prediccion_Continua': 'Prediccion_Decimal',
    'Promedio_Historico_vs_Oponente': 'Promedio_Goles_vs_Oponente',
    'Confianza': 'Confianza_Modelo'
})

# Guardar el DataFrame unido y renombrado en un nuevo archivo CSV
df_completo.to_csv('../BackupResultados/predicciones_torneo2025_lstm.csv', index=False)

print("Proceso completado. Archivo 'predicciones_torneo2025_lstm.csv' creado con éxito.")