from logic import generateClimateHistory, PrintClimateHistory, BuildTransitionMatrixk, RegisterDay,print_transition_matrix,loadClimateHistoryFromFile,forecastClimateSequence,forecastNextClimate,index_to_climate
from UserDesign import menu, Credits

def RunApp():
    arrayClimates = []
    HistoryGenerate = False
    dayN = 0
    matriz_transicion = []

    while True:
        opcion = menu()

        match opcion:
            case 1:
                dayN = RegisterDay()
                arrayClimates = generateClimateHistory(arrayClimates, dayN)
                HistoryGenerate = True
                print(f"Historial de {dayN} días generado aleatoriamente.")
                matriz_transicion = BuildTransitionMatrixk(arrayClimates, dayN)
            case 2:
                if HistoryGenerate:
                    PrintClimateHistory(arrayClimates)
                else:
                    print("Primero se debe generar el historial de climas (Opción 1).")
            case 3:
                if HistoryGenerate:
                    matriz = BuildTransitionMatrixk(arrayClimates, dayN)
                    print_transition_matrix(matriz)
                else:
                    print("Primero se debe generar el historial de climas (Opción 1).")
            case 4:
                filepath = "historial_climatico.json"
                loaded_data = loadClimateHistoryFromFile(filepath)
                if loaded_data:
                    arrayClimates = loaded_data
                    dayN = len(arrayClimates)
                    HistoryGenerate = True
                    print(f"Historial de {dayN} días cargado desde '{filepath}'.")
                    matriz_transicion = BuildTransitionMatrixk(arrayClimates, dayN)
                else:
                    print("No se pudo cargar el historial desde el archivo.")
            case 5:
                if HistoryGenerate and matriz_transicion:
                    try:
                        num_forecast_days = int(input("¿Cuántos días desea pronosticar?: "))
                        if num_forecast_days > 0:
                            
                            if arrayClimates:
                                forecasted_sequence = forecastClimateSequence(arrayClimates, matriz_transicion, num_forecast_days)
                                if forecasted_sequence:
                                    print(f"\n--- Pronóstico para los próximos {num_forecast_days} días ---")
                                    for i, clima_index in enumerate(forecasted_sequence):
                                        clima_nombre = index_to_climate.get(clima_index, "Desconocido")
                                        print(f"Día {i+1} (pronosticado): {clima_nombre}")
                                    print("--------------------------------------------------\n")
                                else:
                                    print("No se pudo generar el pronóstico.")
                            else:
                                print("El historial de climas está vacío. Genere o cargue un historial primero.")
                        else:
                            print("El número de días a pronosticar debe ser mayor que cero.")
                    except ValueError:
                        print("Entrada inválida. Por favor, ingrese un número entero para los días a pronosticar.")
                else:
                    print("Primero debe generar o cargar el historial de climas y calcular la matriz de transición (Opciones 1, 3 o 4).")
            case 6:
                Credits()
            case 7:
                print("Saliendo de la aplicación. ¡Hasta luego!")
                exit(0)
            case _:
                print("Opción inválida. Por favor, seleccione una opción válida.")