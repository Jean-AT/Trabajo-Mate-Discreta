import random

PossibleClimates = [
    "Nublado",
    "Parcialmente Nublado",
    "Soleado",
    "Parcialmente Soleado"
]

climate_to_index = {
    "Nublado": 0,
    "Parcialmente Nublado": 1,
    "Soleado": 2,
    "Parcialmente Soleado": 3
}

index_to_climate = {
    0: "Nublado",
    1: "Parcialmente Nublado",
    2: "Soleado",
    3: "Parcialmente Soleado"
}

def RegisterDay():
    while True:
        try:
            dayN = int(input("Ingrese un numero de dias (20-30): "))
            if 20 <= dayN <= 30:
                return dayN
            else:
                print("Por favor, ingrese un número entre 20 y 30.")
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número entero.")

def generateClimateHistory(arrayClima, dayN):
    arrayClima = []
    for i in range(dayN):
        temp_climate_name = random.choice(PossibleClimates)
        arrayClima.append(climate_to_index[temp_climate_name])
    return arrayClima

def PrintClimateHistory(arrayClimates_indices):
    print("El historial del clima en los ultimos dias:\n")
    print("Pronóstico simulado:")
    for dia, clima_index in enumerate(arrayClimates_indices, start=1):
        clima_nombre = index_to_climate.get(clima_index, "Desconocido")
        print(f"Día {dia}: {clima_nombre}")

def BuildTransitionMatrixk(historial, dias):
    conteoMatriz = [[0 for _ in range(4)] for _ in range(4)]
    for i in range(1, dias):
        conteoMatriz[historial[i - 1]][historial[i]] += 1
    matriz = [[0.0 for _ in range(4)] for _ in range(4)]
    for i in range(4):
        transicionesTotales = 0
        for j in range(4):
            transicionesTotales += conteoMatriz[i][j]

        for j in range(4):
            if transicionesTotales > 0:
                matriz[i][j] = float(conteoMatriz[i][j]) / transicionesTotales
            else:
                matriz[i][j] = 0.0
                
    return matriz

def print_transition_matrix(matrix):
    print("\n--- Matriz de Transición ---")
    print("      0       1       2       3")
    print("---------------------------------")
    for i, row in enumerate(matrix):
        row_str = f"{i} | "
        for val in row:
            row_str += f"{val:.2f}    "
        print(row_str)
    print("---------------------------------\n")

def loadClimateHistoryFromFile(filepath):
    loaded_history_indices = []
    try:
        if filepath.endswith('.csv'):
            import csv
            with open(filepath, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    clima_nombre = row.get('clima')
                    if clima_nombre in climate_to_index:
                        loaded_history_indices.append(climate_to_index[clima_nombre])
                    else:
                        print(f"Advertencia: Clima desconocido '{clima_nombre}' en el archivo. Ignorando.")
        elif filepath.endswith('.json'):
            import json
            with open(filepath, mode='r', encoding='utf-8') as file:
                data = json.load(file)
                for entry in data:
                    clima_nombre = entry.get('clima')
                    if clima_nombre in climate_to_index:
                        loaded_history_indices.append(climate_to_index[clima_nombre])
                    else:
                        print(f"Advertencia: Clima desconocido '{clima_nombre}' en el archivo. Ignorando.")
        else:
            print("Formato de archivo no soportado. Use .csv o .json.")
            return []
    except FileNotFoundError:
        print(f"Error: El archivo '{filepath}' no fue encontrado.")
        return []
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {e}")
        return []

    return loaded_history_indices

def forecastNextClimate(current_climate_index, transition_matrix):
    if not (0 <= current_climate_index < 4):
        print("Error: Índice de clima actual inválido para el pronóstico.")
        return -1

    probabilities = transition_matrix[current_climate_index]
    next_climate_index = random.choices(range(4), weights=probabilities, k=1)[0]
    
    return next_climate_index

def forecastClimateSequence(historial_inicial, transition_matrix, num_days_to_forecast):
    if not historial_inicial:
        print("Error: El historial inicial está vacío. No se puede pronosticar.")
        return []

    forecast_sequence = []
    current_state = historial_inicial[-1]

    for _ in range(num_days_to_forecast):
        next_state = forecastNextClimate(current_state, transition_matrix)
        if next_state == -1:
            break
        forecast_sequence.append(next_state)
        current_state = next_state 
    
    return forecast_sequence