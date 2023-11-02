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


    def ejecutar_simulacion(self):
        quantum = 2
        tiempo_total = 0
        for proceso in lista_procesos_ordenados:
            print('Este es el tiempo de irrupcion', proceso.tiempo_irrupcion)
            tiempo_total = tiempo_total + proceso.tiempo_irrupcion
        print('la suma es ', tiempo_total)
        procesos_terminados = []
        tiempo_inicio_proceso_actual = 0

        self.proceso_en_ejecucion = self.cola_procesos_listos.popleft() #Inicio el primer proceso
        
        print("Contenido de self.cola_procesos_listos:")
        for proceso in self.cola_procesos_listos:
            print(str(proceso))

        while self.tiempo <= (tiempo_total - 1):
            # Realizar la ejecución del proceso actual
            for i in range(1, 3):
                print("¿Desea continuar?")
                print("1 - SI")
                opcion_continuar = int(input())

                if opcion_continuar == 1:
                    self.tiempo = self.tiempo + 1
                
                
                if self.proceso_en_ejecucion is not None:

                    tiempo_restante = self.proceso_en_ejecucion.tiempo_irrupcion - 1
                    self.proceso_en_ejecucion.tiempo_irrupcion = tiempo_restante

                    # Verificar si el proceso ha terminado su tiempo de irrupción
                    if self.proceso_en_ejecucion.tiempo_irrupcion == 0 or i == 2:
                        # tiempo_finalizacion = self.tiempo
                        # tiempo_retorno = tiempo_finalizacion - self.proceso_en_ejecucion.tiempo_arribo
                        # tiempo_espera = tiempo_retorno - self.proceso_en_ejecucion.tiempo_irrupcion   # Para estadisticas
                        
                        if self.proceso_en_ejecucion.tiempo_irrupcion == 0:   
                            #Aqui si el proceso termina se va a la cola de finalizados
                            procesos_terminados.append((self.proceso_en_ejecucion,))  
                        
                        if i==2 and self.proceso_en_ejecucion.tiempo_irrupcion != 0 :
                            # Aquí se devuelve el proceso en ejecución a la cola de listos
                            proceso_devuelto = self.proceso_en_ejecucion
                            self.cola_procesos_listos.append(proceso_devuelto)


                        # Ya sea por el quantum o porque termino, debe salir del procesador.
                        proceso_actual_id = self.proceso_en_ejecucion.proceso_id if self.proceso_en_ejecucion else "Ninguno"
                        print(f"El Proceso: {proceso_actual_id} abandono el procesador ")

                        self.proceso_en_ejecucion = None


                        if self.cola_procesos_listos: # Si hay procesos en cola de listos, se asigna el siguiente nuevamente
                            proceso_siguiente = self.cola_procesos_listos.popleft()
                            self.proceso_en_ejecucion = proceso_siguiente
                            print(f"El Proceso: {proceso_siguiente.proceso_id} se asigno al procesador ")
                    

                        # while len(simulador.cola_procesos_listos) < 5 and lista_procesos_ordenados: #Controlo multiprogramacion
                        #     proceso_pendiente = lista_procesos_ordenados.pop(0)
                        #     simulador.cola_procesos_listos.append(proceso_pendiente)

                
                
                # Imprimir el tiempo actual y el proceso en ejecución (o "Ninguno" si no hay proceso)
                proceso_actual_id = self.proceso_en_ejecucion.proceso_id if self.proceso_en_ejecucion else "Ninguno"
                print(f"Tiempo actual: {self.tiempo}, Proceso en ejecución: {proceso_actual_id}")

                # # Actualizar la cola de procesos listos (añadir procesos que llegan)
                # for proceso in list(self.cola_procesos_listos):
                #     if proceso.tiempo_arribo == self.tiempo:
                #         self.cola_procesos_listos.append(proceso)

           

        # Imprimir informe estadístico
        # total_retorno = sum(tiempo_retorno for (_, tiempo_retorno, _) in procesos_terminados)
        # total_espera = sum(tiempo_espera for (_, _, tiempo_espera) in procesos_terminados)
        # cantidad_procesos_terminados = len(procesos_terminados)
        
        # promedio_retorno = total_retorno / cantidad_procesos_terminados
        # promedio_espera = total_espera / cantidad_procesos_terminados

        # print("Informe estadístico:")
        # print(f"Tiempo de retorno promedio: {promedio_retorno}")
        # print(f"Tiempo de espera promedio: {promedio_espera}")
            

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
        tam_proceso = int(input())  # Corrección
        if tam_proceso <= 0:
            while (tam_proceso <= 0):
                print("ERROR: TAMAÑO NEGATIVO")
                tam_proceso = int(input())  # Corrección
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


lista_procesos_ordenados = sorted(todos_los_procesos, key=lambda proceso: (proceso.proceso_id, proceso.tiempo_arribo))

for proceso in lista_procesos_ordenados:
    print('este es el proceso')
    if len(simulador.cola_procesos_listos) < 5:
        simulador.cola_procesos_listos.append(proceso)
        todos_los_procesos.remove(proceso)

    
# Ejecutar la simulación
simulador.ejecutar_simulacion()
