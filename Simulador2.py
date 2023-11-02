from collections import deque

# Clase para representar un proceso
class Proceso:
    def __init__(self, proceso_id, tamano, tiempo_arribo, tiempo_irrupcion):
        self.proceso_id = proceso_id
        self.tamano = tamano
        self.tiempo_arribo = tiempo_arribo
        self.tiempo_irrupcion = tiempo_irrupcion

    def __str__(self):
        return f"Proceso ID: {self.proceso_id}, Tamaño: {self.tamano}, Tiempo de Arribo: {self.tiempo_arribo}, Tiempo de Irrupción: {self.tiempo_irrupcion}"

# Clase para representar una partición de memoria
class ParticionMemoria:
    def __init__(self, id_particion, tamano, proceso_asignado=None):
        self.id_particion = id_particion
        self.tamano = tamano
        self.proceso_asignado = proceso_asignado
        self.fragmentacion_interna = 0

# Clase para el simulador
class Simulador:
    def __init__(self):
        self.memoria = [
            ParticionMemoria(1, 100),  # Memoria para el Sistema Operativo
            ParticionMemoria(2, 250),  # Memoria para trabajos grandes
            ParticionMemoria(3, 120),  # Memoria para trabajos medianos
            ParticionMemoria(4, 60),   # Memoria para trabajos pequeños
        ]
        self.cola_procesos_listos = deque()
        self.proceso_en_ejecucion = None
        self.tiempo = 0

    def cargar_proceso(self, proceso):
        # Implementar la carga de procesos y asignación de memoria con el algoritmo Best-Fit
        best_fit_partition = None
        for partition in self.memoria:
            if partition.proceso_asignado is None and partition.tamano >= proceso.tamano:
                if best_fit_partition is None or partition.tamano < best_fit_partition.tamano:
                    best_fit_partition = partition

        if best_fit_partition:
            best_fit_partition.proceso_asignado = proceso
            best_fit_partition.fragmentacion_interna = best_fit_partition.tamano - proceso.tamano

    def ejecutar_simulacion(self, quantum):
        procesos_terminados = []
        tiempo_inicio_proceso_actual = 0

        while self.cola_procesos_listos or self.proceso_en_ejecucion:
            # Verificar si hay procesos en cola de listos
            if self.cola_procesos_listos:
                proceso_siguiente = self.cola_procesos_listos.popleft()
                if self.proceso_en_ejecucion:
                    self.cola_procesos_listos.append(self.proceso_en_ejecucion)
                self.proceso_en_ejecucion = proceso_siguiente

            if self.proceso_en_ejecucion:
                proceso_actual_id = self.proceso_en_ejecucion.proceso_id
                print(f"Tiempo actual: {self.tiempo}, Proceso en ejecución: {proceso_actual_id}")
                tiempo_restante = self.proceso_en_ejecucion.tiempo_irrupcion

                if tiempo_restante > quantum:
                    tiempo_restante -= quantum
                else:
                    tiempo_restante = 0

                self.proceso_en_ejecucion.tiempo_irrupcion = tiempo_restante

                if tiempo_restante == 0:
                    tiempo_finalizacion = self.tiempo + 1
                    tiempo_retorno = tiempo_finalizacion - self.proceso_en_ejecucion.tiempo_arribo
                    tiempo_espera = tiempo_retorno - self.proceso_en_ejecucion.tiempo_irrupcion

                    procesos_terminados.append((self.proceso_en_ejecucion, tiempo_retorno, tiempo_espera))

                    print(f"El Proceso: {proceso_actual_id} ha terminado")

                    self.proceso_en_ejecucion = None
            else:
                print(f"Tiempo actual: {self.tiempo}, Proceso en ejecución: Ninguno")

            self.tiempo += 1

        # Imprimir informe estadístico
        total_retorno = sum(tiempo_retorno for (_, tiempo_retorno, _) in procesos_terminados)
        total_espera = sum(tiempo_espera for (_, _, tiempo_espera) in procesos_terminados)
        cantidad_procesos_terminados = len(procesos_terminados)

        promedio_retorno = total_retorno / cantidad_procesos_terminados
        promedio_espera = total_espera / cantidad_procesos_terminados

        print("Informe estadístico:")
        print(f"Tiempo de retorno promedio: {promedio_retorno}")
        print(f"Tiempo de espera promedio: {promedio_espera}")

# Ejemplo de uso del simulador
simulador = Simulador()

print("SELECCIONE UNA OPCION:")
print("1 - CARGAR PROCESOS")
opcion = int(input())

# USUARIO SELECCIONA CARGAR PROCESOS
if opcion == 1:
    print("OPCION ELEGIDA CON EXITO")

lista_procesos = []
todos_los_procesos = []

cont = 1

# EL USUARIO DEFINE LA MANERA DE CARGAR EL PROCESO
print("SELECCIONE COMO QUIERE CARGAR EL PROCESO:")
print("1 - INGRESAR PROCESO POR TERMINAL")
print("2 - LEER ARCHIVO CON PROCESOS")
opcion_carga = int(input())

aux = 0
# SI EL USUARIO INGRESA LOS PROCESOS POR TERMINAL
if opcion_carga == 1:
    estado_carga = True
    while (cont <= 10 and estado_carga is True):
        print("CARGANDO EL PROCESO:", cont)
        print("INGRESE EL ID DEL PROCESO:")
        id = int(input())
        if id <= 0:
            while (id <= 0):
                print("ERROR: ID NEGATIVO:")
                id = int(input())
        print("INGRESE EL TAMAÑO DEL PROCESO:")
        tam_proceso = int(input())
        if tam_proceso <= 0:
            while (tam_proceso <= 0):
                print("ERROR: TAMAÑO NEGATIVO")
                tam_proceso = int(input())
        print("INGRESE EL TIEMPO DE LLEGADA DEL PROCESO:")
        tiempo_llegada = int(input())
        if tiempo_llegada < 0:
            while (tiempo_llegada < 0):
                print("ERROR: TIEMPO DE LLEGADA NEGATIVO")
                tiempo_llegada = int(input())
        print("INGRESE EL TIEMPO DE IRRUPCIÓN DEL PROCESO:")
        tiempo_irrupcion = int(input())
        if tiempo_irrupcion <= 0:
            while (tiempo_irrupcion <= 0):
                print("ERROR: TIEMPO DE IRRUPCIÓN NEGATIVO")
                tiempo_irrupcion = int(input())
        nuevoProceso = Proceso(id, tam_proceso, tiempo_llegada, tiempo_irrupcion)
        todos_los_procesos.append(nuevoProceso)

        print("¿DESEA CONTINUAR?")
        print("1 - SI")
        print("2 - NO")
        opcion_continuar = int(input())
        cont += 1
        if opcion_continuar == 2:
            estado_carga = False
            cont -= 1

lista_procesos_ordenados = sorted(todos_los_procesos, key=lambda proceso: (proceso.tiempo_arribo, proceso.proceso_id))

for proceso in lista_procesos_ordenados:
    if len(simulador.cola_procesos_listos) < 5:
        simulador.cola_procesos_listos.append(proceso)
        todos_los_procesos.remove(proceso)

# Ejecutar la simulación con un quantum de 2
quantum = 2
simulador.ejecutar_simulacion(quantum)
