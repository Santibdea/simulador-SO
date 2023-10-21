# EL SISTEMA MUESTRA LAS OPCIONES
print("SELECCIONE UNA OPCION:")
print("1 - CARGAR PROCESOS")
opcion = int(input())

# USUARIO SELECCIONA CARGAR PROCESOS
if opcion == 1:
    print("OPCION ELEGIDA CON EXITO")

lista_proceso = []
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
                tam_proceso = input()
        print("INGRESE EL TIEMPO DE LLEGADA DEL PROCESO:")
        tiempo_llegada = int(input())
        if tiempo_llegada <= 0:
            while (tiempo_llegada <= 0):
                print("ERROR: TAMAÑO NEGATIVO")
                tiempo_llegada = int(input())
        print("INGRESE EL TIEMPO DE IRRUPCION DEL PROCESO:")
        tiempo_irrupcion = int(input())
        if tiempo_irrupcion <= 0:
            while (tiempo_irrupcion <= 0):
                print("ERROR: TAMAÑO NEGATIVO")
                tiempo_irrupcion = int(input())
        lista_proceso.append(
            [id, tam_proceso, tiempo_llegada, tiempo_irrupcion])
        print("¿DESEA CONTINUAR?")
        print("1 - SI")
        print("2 - NO")
        opcion_continuar = int(input())
        cont += 1
        if opcion_continuar == 2:
            estado_carga = False
            cont -= 1
print(lista_proceso)

# ORDENA POR TIEMPO DE LLEGADA
cola_procesos = sorted(lista_proceso, key=lambda x: x[2])
print(cola_procesos)

cola_listos = []
cola_finalizados = []
quantum = 2
particiones = [60, 120, 250]

asignacion = [60, 120, 250]
fi = [0, 0, 0]

# PRESENTACIONES DE SALIDA
print("¿DESEA VISUALIZAR LAS PRESENTACIONES DE SALIDA")
print("1 - SI")
print("2 - NO")
opcion_inicio = int(input())

t = 0
aux = 0
if opcion_inicio == 1:
    opcion_seguimiento = True
    while (opcion_seguimiento is True):
        if (t == lista_proceso[aux][2]):
            cola_listos.append(lista_proceso[aux])
            aux += 1
            if (cola_listos[0][1] <= 60 and asignacion[0] == 60):
                asignacion[0] = cola_listos[0][1]
                fi[0] = 60 - asignacion[0]
                cola_listos[0] = 0
                for i in range(0, 8):
                    cola_listos[i] = cola_listos = [i + 1]
                    cola_listos[i+1] = 0
            else:
                if (cola_listos[0][1] <= 120 and asignacion[1] == 120):
                    asignacion[1] = cola_listos[0][1]
                    fi[1] = 120 - asignacion[1]
                    cola_listos[0] = 0
                    for i in range(0, 8):
                        cola_listos[i] = cola_listos = [i + 1]
                        cola_listos[i+1] = 0
                else:
                    if (cola_listos[0][1] <= 150 and asignacion[2] == 150):
                        asignacion[2] = cola_listos[0][1]
                        fi[2] = 150 - asignacion[2]
                        cola_listos[0] = 0
                        for i in range(0, 8):
                            cola_listos[i] = cola_listos = [i + 1]
                            cola_listos[i+1] = 0
    print("¿DESEA CONTINUAR?")
    print("1 - SI")
    print("2 - NO")
    if opcion_continuar == 2:
        opcion_seguimiento = False
