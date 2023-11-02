class Proceso:
    def __init__(self, proceso_id, tamano, tiempo_arribo, tiempo_irrupcion):
        self.proceso_id = proceso_id  # ID del proceso
        self.tamano = tamano  # Tamaño del proceso en memoria
        self.tiempo_arribo = tiempo_arribo  # Tiempo de arribo
        self.tiempo_irrupcion = tiempo_irrupcion  # Tiempo de irrupción

    def __str__(self):
        return f"Proceso ID: {self.proceso_id}, Tamaño: {self.tamano}, Tiempo de Arribo: {self.tiempo_arribo}, Tiempo de Irrupción: {self.tiempo_irrupcion}"

# Ejemplo de uso:
# Crear un proceso
proceso1 = Proceso(1, 50, 0, 5)
print(proceso1)
