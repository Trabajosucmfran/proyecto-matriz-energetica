import pandas as pd
import numpy as np

# 1. Configuración inicial
# Fijamos una semilla para que los datos aleatorios sean reproducibles (siempre den el mismo resultado)
np.random.seed(42)

# Definimos los años (2014 al 2024) y los países de la muestra
anios = np.arange(2014, 2025)
paises = ['Chile', 'País_A', 'País_B', 'País_C']

# Creamos listas vacías para ir guardando los datos generados
datos_lista = []

# 2. Generación de los datos país por país
for pais in paises:
    n_anios = len(anios)
    
    # Simulamos el Consumo de Energía en GWh (Crecimiento sostenido con un poco de ruido)
    # Partimos de una base aleatoria para cada país y le sumamos un crecimiento anual
    consumo_base = np.random.randint(60000, 80000)
    crecimiento_anual = np.linspace(1, 1.25, n_anios) # Crece un 25% en la década
    ruido_consumo = np.random.normal(0, 500, n_anios)
    consumo_gwh = (consumo_base * crecimiento_anual) + ruido_consumo
    
    if pais == 'Chile':
        # --- DATOS PARA CHILE ---
        # Importación fósil: Mantenemos la media en torno al 98.5% histórico oficial
        importacion_fosil = np.random.normal(98.5, 0.6, n_anios)
        
        # Capacidad Solar MW: Simulamos el "boom solar" de Chile
        # Empieza bajo en 2014 y crece exponencialmente hacia 2024
        capacidad_solar = np.linspace(400, 9000, n_anios) + np.random.normal(0, 150, n_anios)
        
    else:
        # --- DATOS PARA PAÍSES DE CONTRASTE (Transiciones exitosas) ---
        # Importación fósil: Comienzan dependientes (ej. 70%) pero bajan con el tiempo (ej. hasta 40%)
        tendencia_baja = np.linspace(np.random.uniform(65, 75), np.random.uniform(35, 45), n_anios)
        importacion_fosil = tendencia_baja + np.random.normal(0, 2, n_anios)
        
        # Capacidad Solar MW: Crecimiento más constante y maduro desde el principio
        capacidad_solar = np.linspace(3000, 12000, n_anios) + np.random.normal(0, 300, n_anios)
    
    # 3. Ensamblaje de los datos
    # Iteramos sobre cada año para guardar el registro correspondiente
    for i in range(n_anios):
        datos_lista.append({
            'Año': anios[i],
            'País': pais,
            'Consumo_Energia_GWh': round(consumo_gwh[i], 2),
            'Importacion_Fosil_Porcentaje': round(importacion_fosil[i], 2),
            'Capacidad_Solar_MW': round(capacidad_solar[i], 2)
        })

# 4. Creación del DataFrame y exportación
df_energia = pd.DataFrame(datos_lista)

# Limitamos el porcentaje máximo a 100% por lógica matemática
df_energia['Importacion_Fosil_Porcentaje'] = df_energia['Importacion_Fosil_Porcentaje'].clip(upper=100.0)

# Exportamos a CSV (este es el archivo que subirán a GitHub)
nombre_archivo = 'dataset_sintetico_energia.csv'
df_energia.to_csv(nombre_archivo, index=False, encoding='utf-8')

print(f"¡Base de datos '{nombre_archivo}' generada con éxito!")
print("\nVista previa de los datos de Chile:")
print(df_energia[df_energia['País'] == 'Chile'].head())
