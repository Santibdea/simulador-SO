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
rta = 0
while rta != 1 and rta != 2:
    print("SELECCIONE COMO QUIERE CARGAR EL PROCESO:")
    print("1 - INGRESAR PROCESO POR TERMINAL")
    print("2 - LEER ARCHIVO CON PROCESOS")
    rta = int(input())

# SI EL USUARIO INGRESA LOS PROCESOS POR TERMINAL
if rta == 1:
    estado_carga = True
    while (cont <= 10 and estado_carga is True):
        print("------------------------------------------------------")
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
        if tiempo_llegada < 0:
            while (tiempo_llegada < 0):
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
        print("------------------------------------------------------")
        print("¿DESEA CONTINUAR?")
        print("1 - SI")
        print("2 - NO")
        rta = 0
        cont += 1
        while rta != 1 and rta != 2:
            rta = int(input())
        if rta == 2:
            estado_carga = False
            cont -= 1

# ORDENA POR TIEMPO DE LLEGADA
lista_proceso = sorted(lista_proceso, key=lambda x: x[2])
print("LISTA ORDENADA:", lista_proceso)

# PRESENTACIONES DE SALIDA
proceso_en_ejecucion = []
cola_listos = []
opcion_seguimiento = True
t = lista_proceso[0][2]
quantum = 0
z = 0
y = 0

while opcion_seguimiento is True:
    # SE PREGUNTA SI NO HAY MAS PROCESOS EN COLA DE LISTOS Y EN LISTA DE PROCESOS:
    if (len(cola_listos) == 0 and len(lista_proceso) == 0):
        opcion_seguimiento = False
        # SI HAY UN PROCESO EJECUTANDOSE:
        # SE PREGUNTA SI YA SE TERMINO DE EJECUTAR EL PROCESO
    if len(proceso_en_ejecucion) != 0:
        if proceso_en_ejecucion[0][3] == 0:
            proceso_en_ejecucion = []
            if (len(proceso_en_ejecucion) == 0 and len(cola_listos) == 0 and len(lista_proceso) == 0):
                y = 1
            quantum = 0

    # CARGA DE PROCESOS A COLA DE LISTOS
    if len(lista_proceso) != 0:
        while t == lista_proceso[0][2]:
            cola_listos.append(lista_proceso[0])
            tamaño = len(lista_proceso) - 1
            lista_proceso[0] = [0, 0, 0, 0]
            for i in range(0, tamaño):
                lista_proceso[i] = lista_proceso[i+1]
                lista_proceso[i+1] = 0
            # UNA VEZ SE PASA UN PROCESO A COLA DE LISTOS, SE ELIMINA DICHO PROCESO DE ESTA LISTA
            lista_proceso.pop(tamaño)
            if len(lista_proceso) == 0:
                lista_proceso.append([0, 0, 0, 0])
                z = 1

    if z == 1:
        lista_proceso.pop(0)
    z = 0

    if quantum == 2:
        if (len(proceso_en_ejecucion) != 0 and y == 0):
            cola_listos.append(proceso_en_ejecucion[0])
            proceso_en_ejecucion.pop(0)
        quantum = 0

    # SE PREGUNTAR SI SE PUEDE EJECUTAR UN PROCESO
    if (len(proceso_en_ejecucion) == 0 and y == 0):
        proceso_en_ejecucion.append(cola_listos[0])
        # MOVEMOS UNA POSICION A LA IZQUIERDA CADA PROCESO DE LA COLA DE LISTOS
        tamaño = len(cola_listos) - 1
        for i in range(0, tamaño):
            cola_listos[i] = cola_listos[i+1]
            cola_listos[i+1] = 0
        cola_listos.pop(tamaño)
    if y == 0:
        print("----------------------------------------------------------")
        print("INSTANTE:", t)
        print("ESTADO DEL PROCESADOR:", proceso_en_ejecucion)
        print("COLA DE LISTOS:", cola_listos)
        print("----------------------------------------------------------")
        t += 1
        quantum += 1
        proceso_en_ejecucion[0][3] = proceso_en_ejecucion[0][3] - 1

    if y == 0:
        print("¿DESEA CONTINUAR?")
        print("1 - SI")
        print("2 - NO")
        rta = 0
        while rta != 1 and rta != 2:
            rta = int(input())
        if rta == 2:
            opcion_seguimiento = False
    else:
        opcion_seguimiento = False

print("FIN")
