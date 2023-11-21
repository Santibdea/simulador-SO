import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename
from collections import deque

# Sets the appearance mode of the application
# "System" sets the appearance same as that of the system
ctk.set_appearance_mode("Dark")

# Sets the color of the widgets
# Supported themes: green, dark-blue, blue
ctk.set_default_color_theme("dark-blue")

# Se deberia definir el estado del proceso por la cola en la cual se encuentra.

# Estados posibles de un proceso: ready, ready and suspended, in execution, y finished


class ComputerProcess:
    def __init__(self, id, size, arrival_time, execution_time, initial_ex_time=0, state=None, location=None, return_time=0, internal_fragmentation=0):
        self.id = id
        self.size = size
        self.arrival_time = arrival_time
        self.execution_time = execution_time
        self.initial_ex_time = initial_ex_time
        self.internal_fragmentation = internal_fragmentation
        self.state = state
        self.location = location
        self.return_time = return_time


class Partition:
    def __init__(self, partition_id, size, proccess_asigned=None,):
        self.partition_id = partition_id
        self.size = size
        self.proccess_asigned = proccess_asigned


class Simulator:
    def __init__(self, master):
        self.master = master
        self.master.title(
            "Simulador de Asignación de Memoria y Planificación de Procesos")
        self.process_ids = 1
        OS = ComputerProcess(0, 100, 0, 0, )
        OS_partition = Partition(4, 100, OS)

        self.memory_partitions = [Partition(1, 60), Partition(
            2, 120), Partition(3, 250), OS_partition]
        self.ready_queue = deque()
        self.proccess_in_execution = None
        self.titles = ['Memory Partition', 'Process ID',
                       'Process Size', 'Arrival Time', 'Ex. Time', 'Int. Frag.']
        self.all_processes = []
        self.finished_queue = []
        self.total_execution = 0
        self.total_execution_inverse = 0

        # Add GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Label to enter process information
        self.matrix = tk.Frame(self.master, bg="#5B5E61")
        self.cola_finalizados = tk.Frame(self.master, bg="#5B5E61")
        self.cola_listos = tk.Frame(self.master, bg="#5B5E61")
        self.bottom_frame = tk.Frame(self.master, bg="#5B5E61")
        # Adjust the row and column values as needed
        self.bottom_frame.grid(row=4, column=0, columnspan=2)

        self.process_size_label = ctk.CTkLabel(
            self.master, text="Tamaño de Proceso:")
        self.process_size_label.grid(row=0, column=0, padx=5, pady=5)

        self.process_size_entry = ctk.CTkEntry(self.master)
        self.process_size_entry.grid(row=0, column=1, padx=5, pady=5)

        self.process_ta_label = ctk.CTkLabel(
            self.master, text="Tiempo de arribo:")
        self.process_ta_label.grid(row=1, column=0, padx=50, pady=5)
        self.process_ta_entry = ctk.CTkEntry(self.master)
        self.process_ta_entry.grid(row=1, column=1, padx=5, pady=5)

        self.process_ti_label = ctk.CTkLabel(
            self.master, text="Tiempo de irrupción:")
        self.process_ti_label.grid(row=2, column=0, padx=5, pady=5)
        self.process_ti_entry = ctk.CTkEntry(self.master)
        self.process_ti_entry.grid(row=2, column=1, padx=5, pady=5)

        # Button to load a new process
        self.cargar_proceso_btn = ctk.CTkButton(
            self.master, text="Cargar Proceso", command=self.load_process)
        self.cargar_proceso_btn.grid(row=3, column=0, pady=10)

        self.cargar_archivo_btn = ctk.CTkButton(
            self.master, text="Cargar Archivo", command=self.load_file)
        self.cargar_archivo_btn.grid(row=3, column=1,  pady=10)

        # Label for the state of the ready process queue
        self.procesos_nuevos = ctk.CTkLabel(
            self.bottom_frame, text="Procesos nuevos:")
        self.procesos_nuevos.grid(row=1, column=0, padx=5, pady=5)

        # Listbox to display the ready process queue
        self.ready_queue_listbox = ctk.CTkTextbox(self.bottom_frame)
        self.ready_queue_listbox.grid(row=1, column=1, padx=5, pady=5)

        # self.ready_queue_listbox = ctk.CTkScrollableFrame(self.bottom_frame, width=200, height=200, orientation="horizontal")
        # self.ready_queue_listbox.grid(row=1, column=1, padx=5, pady=5)

        # Button to start the simulation
        self.iniciar_btn = ctk.CTkButton(
            self.master, text="Iniciar Simulación", command=self.start_simulation)
        self.iniciar_btn.grid(row=5, pady=10, columnspan=2)

        # Button to finish the simulation

    def load_process(self):
        process_size = self.process_size_entry.get()
        process_ta = self.process_ta_entry.get()
        process_ti = self.process_ti_entry.get()

        if not process_ta or not process_size or not process_ti:
            messagebox.showerror(
                "Error", "Por favor, ingrese el tiempo de arribo, el tiempo de irrupción y el tamaño del proceso.")
            return

        self.process_ta_entry.delete(0, tk.END)
        self.process_ti_entry.delete(0, tk.END)
        self.process_size_entry.delete(0, tk.END)

        try:
            self.save_process(int(process_size), int(
                process_ta), int(process_ti))
        except ValueError:
            messagebox.showerror(
                "Error", "El tamaño del proceso debe ser un número entero.")
            return

    def load_file(self):
        filename = askopenfilename(initialdir="./",
                                   title="UTN - FRRE - SO 2023 - GRUPO EPSILON - Elija un archivo",
                                   filetypes=[("text files", "*.txt")])
        with open(filename, "r", encoding="utf8") as f:
            for line in f:
                line = line.split(':')[1].split(',')
                line = [int(element.strip()) for element in line]
                self.save_process(line[0], line[1], line[2])

    def save_process(self, p_size, p_ta, p_ti):
        if len(self.all_processes) >= 10:
            messagebox.showerror(
                "Error", "No es posible cargar mas de 10 procesos")
            return
        process_id = self.process_ids
        process = ComputerProcess(process_id, p_size, p_ta, p_ti)
        process.initial_ex_time = process.execution_time
        self.total_execution += int(p_ti)
        self.all_processes.append(process)
        self.process_ids += 1
        self.ready_queue_listbox.insert(
            tk.END, f"ID: {process.id}, TA: {process.arrival_time}, TI: {process.execution_time}, TAMAÑO: {p_size} \n")

    def delete_buttons(self):
        # Destroy the button
        self.process_ta_entry.destroy()
        self.process_ti_entry.destroy()
        self.process_size_entry.destroy()
        self.process_size_label.destroy()
        self.process_ta_label.destroy()
        self.process_ti_label.destroy()
        self.cargar_proceso_btn.destroy()
        self.iniciar_btn.destroy()
        self.cargar_archivo_btn.destroy()
        self.procesos_nuevos.destroy()
        self.ready_queue_listbox.destroy()

    def release_partition(self, partition_id):
        for partition in self.memory_partitions:
            if partition.partition_id == partition_id:
                partition.proccess_asigned = None
                ctk.CTkLabel(self.matrix, text='        ').grid(
                    row=partition.partition_id, column=1, padx=5, pady=5)
                ctk.CTkLabel(self.matrix, text='        ').grid(
                    row=partition.partition_id, column=2, padx=5, pady=5)
                ctk.CTkLabel(self.matrix, text='        ').grid(
                    row=partition.partition_id, column=3, padx=5, pady=5)
                ctk.CTkLabel(self.matrix, text='        ').grid(
                    row=partition.partition_id, column=4, padx=5, pady=5)
                ctk.CTkLabel(self.matrix, text='        ').grid(
                    row=partition.partition_id, column=5, padx=5, pady=5)

    def best_fit_partition(self, process_size):
        for partition in self.memory_partitions:
            if partition.partition_id != 4 and (not partition.proccess_asigned) and partition.size >= process_size:
                return partition

        return None

    def start_simulation(self):
        # Limpiar lo ingresado y reordenarlo por tiempo de arribo
        self.all_processes = sorted(self.all_processes, key=lambda proceso: (
            proceso.id, proceso.arrival_time))

        for proceso in self.all_processes:
            print("process id: ", proceso.id)
            if (len(self.ready_queue) < 6) and (proceso.arrival_time <= self.total_execution_inverse):
                print('arribo el proceso', proceso.id,
                      'en el tiempo', self.total_execution_inverse)
                self.ready_queue.append(proceso)
                self.all_processes.remove(proceso)
                self.update_ready_queue_GUI()

        self.ready_queue_listbox.delete("1.0", "end")

        # Reutilizar variable. Ahora representa la row de la lista de finalizados
        self.process_ids = 1

        matrix = self.matrix
        matrix.grid(row=1, column=0)

        cola_finalizados = self.cola_finalizados
        cola_listos = self.cola_listos

        for proceso in self.ready_queue:
            print(f"proceso id {proceso.id}")

        num_processes_to_allocate = min(3, len(self.ready_queue))
        processes_to_allocate = list(self.ready_queue)[
            :num_processes_to_allocate]

        for process in processes_to_allocate:
            best_partition = self.best_fit_partition(process.size)
            if best_partition:
                print('sss', best_partition.partition_id)
                best_partition.proccess_asigned = process
                process.internal_fragmentation = best_partition.size - process.size
                process.location = best_partition.partition_id
                process.state = 'ready'
                ctk.CTkLabel(self.matrix, text=process.id).grid(
                    row=(best_partition.partition_id), column=1, padx=5, pady=5)
                ctk.CTkLabel(self.matrix, text=process.size).grid(
                    row=(best_partition.partition_id), column=2, padx=5, pady=5)
                ctk.CTkLabel(self.matrix, text=process.arrival_time).grid(
                    row=(best_partition.partition_id), column=3, padx=5, pady=5)
                ctk.CTkLabel(self.matrix, text=process.execution_time).grid(
                    row=(best_partition.partition_id), column=4, padx=5, pady=5)
                ctk.CTkLabel(self.matrix, text=process.internal_fragmentation).grid(
                    row=(best_partition.partition_id), column=5, padx=5, pady=5)
            else:
                process.state = 'ready and suspended'
        if self.ready_queue:
            self.proccess_in_execution = self.ready_queue.popleft()  # Inicio el primer proceso

        cola_finalizados.grid(row=1, column=1, sticky="ne")
        cola_listos.grid(row=1, column=5, sticky="ne")
        # Limpiar la GUI antes de actualizarla
        for widget in self.cola_listos.winfo_children():
            widget.destroy()

        # Encabezado de la cola de listos
        ctk.CTkLabel(self.cola_listos, text="Cola de listos: ").grid(
            row=0, column=0, padx=10, pady=5)

        # Mostrar los procesos en la cola de listos
        for i, process in enumerate(self.ready_queue, start=1):
            ctk.CTkLabel(self.cola_listos, text=str(process.id)).grid(
                row=i, column=0, padx=5, pady=5)

        self.delete_buttons()

        self.right_frame = tk.Frame(
            self.bottom_frame, bg="#00448B", borderwidth=10)
        self.right_frame.grid(row=1, column=0, padx=5, pady=5)

        self.procces_enter = ctk.CTkLabel(self.right_frame, text="Proceso que se asigno a ejecucion").grid(
            row=0, column=1, padx=10, pady=10)

        for index, partition in enumerate(self.memory_partitions):

            # Poner títulos de la matriz
            ctk.CTkLabel(matrix, text=self.titles[index]).grid(
                row=0, column=index, padx=5, pady=5)

            # Poner la partición a la que pertenece la row
            ctk.CTkLabel(matrix, text=f"Partición {partition.size}K").grid(
                row=1+index, column=0, padx=5, pady=5)

            # Poner "-" en la partición del SO
            ctk.CTkLabel(matrix, text="-").grid(row=4,
                                                column=index+1, padx=5, pady=5)
        ctk.CTkLabel(matrix, text=self.titles[-2]).grid(
            row=0, column=4, padx=5, pady=5)
        ctk.CTkLabel(matrix, text=self.titles[-1]).grid(
            row=0, column=5, padx=5, pady=5)

        ctk.CTkLabel(cola_finalizados, text="Procesos finalizados").grid(
            row=0, padx=10, pady=5)

        ctk.CTkLabel(cola_listos, text="Cola de listos: ").grid(
            row=0, padx=10, pady=5)

        ctk.CTkButton(self.bottom_frame, text="Finalizar Simulación",
                      command=self.finish_simulation).grid(row=2, column=0, pady=10)

        ctk.CTkButton(self.bottom_frame, text="Continuar simulación",
                      command=self.continue_simulation).grid(row=2, column=1, pady=10)

        self.progress_bar = ctk.CTkProgressBar(
            self.master, orientation="horizontal")
        self.progress_bar.grid(row=9, pady=10, columnspan=2)
        self.progress_bar.set(0)
        ctk.CTkLabel(self.master, text="Tiempo actual: ").grid(
            row=10, pady=10, column=0)
        self.tiempo_actual = ctk.CTkLabel(self.master, text="").grid(
            row=10, pady=10, column=1)

    def is_memory_full(self):
        for partition in self.memory_partitions:
            if (partition.proccess_asigned == None):
                return False
        return True

    def is_proccess_loaded_in_memory(self, proceso):
        for partition in self.memory_partitions:
            if (partition.proccess_asigned != None):
                if (partition.proccess_asigned.id == proceso.id):
                    return True
        return False

    def update_ready_queue_GUI(self):
        # Limpiar la GUI antes de actualizarla
        for widget in self.cola_listos.winfo_children():
            widget.destroy()

    # Encabezado de la cola de listos
        ctk.CTkLabel(self.cola_listos, text="Cola de listos: ").grid(
            row=0, column=0, padx=10, pady=5)

    # Mostrar los procesos en la cola de listos
        for i, process in enumerate(self.ready_queue, start=1):
            ctk.CTkLabel(self.cola_listos, text=str(process.id)).grid(
                row=i, column=0, padx=5, pady=5)

    def continue_simulation(self, ):

        if self.proccess_in_execution is not None:

            for quantum in range(1, 3):
                # Verifico si hay algun proceso que se pueda añadir a la cola de listos
                self.verifyReadyQueue()
                # self.verifyIfNextProcessIsInMemoryAndLoad()
                self.total_execution_inverse += 1
                self.progress_bar.set(
                    self.total_execution_inverse / self.total_execution)
                self.tiempo_actual = ctk.CTkLabel(self.master, text=str(
                    self.total_execution_inverse)).grid(row=10, pady=10, column=1)
                self.proccess_in_execution.execution_time -= 1

                if not self.is_memory_full():  # Caso en el cual la memoria no este llena y haya procesos para asignar

                    print(
                        "La memoria puede ser cargada con algun proceso y hay algun proceso asignable")
                    # Crear una lista de particiones libres
                    free_partitions = [
                        partition for partition in self.memory_partitions if partition.proccess_asigned is None]

                    # Ordenar las particiones libres por tamaño (de menor a mayor)
                    free_partitions.sort(key=lambda partition: partition.size)

                    # Obtener los primeros tres procesos de la cola de listos
                    num_processes_to_allocate = min(3, len(self.ready_queue))
                    processes_to_allocate = list(self.ready_queue)[
                        :num_processes_to_allocate]

                    unassigned_processes = []

                    # Itera a través de los procesos para asignar
                    for process in processes_to_allocate:
                        # Variable para rastrear si el proceso está asignado en alguna partición
                        is_assigned = False

                        # Itera a través de las particiones para verificar si el proceso está asignado
                        for partition in self.memory_partitions:
                            if partition.proccess_asigned is not None and partition.proccess_asigned.id == process.id:
                                is_assigned = True
                                break

                        # Si el proceso no está asignado, agrégalo al array de procesos no asignados
                        if not is_assigned:
                            unassigned_processes.append(process)

                    for process in unassigned_processes:
                        print(
                            'se distinguio un proceso que esta en la cola de listos, pero no en memoria')
                        best_fit_partition = None

                        for partition in free_partitions:
                            if partition.size >= process.size and (best_fit_partition is None or partition.size < best_fit_partition.size):
                                best_fit_partition = partition

                        if best_fit_partition:
                            process.internal_fragmentation = best_fit_partition.size - process.size

                            best_fit_partition.proccess_asigned = process
                            process.location = best_fit_partition.partition_id
                            process.state = 'ready'

                            self.update_memory_GUI(
                                process, best_fit_partition)
                # Veo si la memoria esta llena, el caso en el que el siguiente proceso que se deba procesar no este en memoria, debe cargarse por bestFit, pero sin sacar de memoria el proceso que esta actualmente en ejecucion
                else:
                    self.verifyIfNextProcessIsInMemoryAndLoad()
                if self.proccess_in_execution.execution_time == 0 or quantum == 2:
                    # tiempo_finalizacion = self.tiempo
                    # tiempo_retorno = tiempo_finalizacion - self.proceso_en_ejecucion.tiempo_arribo
                    # tiempo_espera = tiempo_retorno - self.proceso_en_ejecucion.tiempo_irrupcion   # Para estadisticas

                    if self.proccess_in_execution.execution_time == 0:

                        print('un proceso termino')
                        # Aqui si el proceso termina se va a la cola de finalizados
                        self.release_partition(
                            self.proccess_in_execution.location)
                        self.finished_queue.append(self.proccess_in_execution)
                        print(
                            f"El proceso {self.proccess_in_execution.id} termino")
                        proceso_actual_id = self.proccess_in_execution.id if self.proccess_in_execution else "Ninguno"

                        self.proccess_exit = ctk.CTkLabel(
                            self.right_frame, text="Proceso que abandono el procesador: {}".format(proceso_actual_id))
                        self.proccess_exit.grid(
                            row=0, column=1, padx=10, pady=10)
                        ctk.CTkLabel(self.cola_finalizados, text=str(proceso_actual_id)).grid(
                            row=self.process_ids, padx=5, pady=5)
                        self.process_ids = self.process_ids + 1

                        self.proccess_in_execution = None
                        if not self.is_memory_full():  # Caso en el cual la memoria no este llena y haya procesos para asignar

                            print(
                                "La memoria puede ser cargada con algun proceso y hay algun proceso asignable")
                            # Crear una lista de particiones libres
                            free_partitions = [
                                partition for partition in self.memory_partitions if partition.proccess_asigned is None]

                            # Ordenar las particiones libres por tamaño (de menor a mayor)
                            free_partitions.sort(
                                key=lambda partition: partition.size)

                            # Obtener los primeros tres procesos de la cola de listos
                            num_processes_to_allocate = min(
                                3, len(self.ready_queue))
                            processes_to_allocate = list(self.ready_queue)[
                                :num_processes_to_allocate]

                            unassigned_processes = []

                            # Itera a través de los procesos para asignar
                            for process in processes_to_allocate:
                                # Variable para rastrear si el proceso está asignado en alguna partición
                                is_assigned = False

                                # Itera a través de las particiones para verificar si el proceso está asignado
                                for partition in self.memory_partitions:
                                    if partition.proccess_asigned is not None and partition.proccess_asigned.id == process.id:
                                        is_assigned = True
                                        break

                                # Si el proceso no está asignado, agrégalo al array de procesos no asignados
                                if not is_assigned:
                                    unassigned_processes.append(process)

                            for process in unassigned_processes:
                                print(
                                    'se distinguio un proceso que esta en la cola de listos, pero no en memoria')
                                best_fit_partition = None

                                for partition in free_partitions:
                                    if partition.size >= process.size and (best_fit_partition is None or partition.size < best_fit_partition.size):
                                        best_fit_partition = partition

                                if best_fit_partition:
                                    process.internal_fragmentation = best_fit_partition.size - process.size
                                    best_fit_partition.proccess_asigned = process
                                    process.location = best_fit_partition.partition_id
                                    process.state = 'ready'

                                    self.update_memory_GUI(
                                        process, best_fit_partition)

                        if self.ready_queue:  # Si hay procesos en cola de listos, se asigna el siguiente nuevamente
                            proceso_siguiente = self.ready_queue.popleft()
                            self.proccess_in_execution = proceso_siguiente
                            self.procces_enter = ctk.CTkLabel(
                                self.right_frame, text="Proceso que se asigno al procesador: {}".format(proceso_siguiente.id))
                            self.procces_enter.grid(
                                row=0, column=2, padx=10, pady=10)
                            self.update_ready_queue_GUI()

                        break

                    if quantum == 2 and self.proccess_in_execution.execution_time != 0:
                        self.verifyReadyQueue()  # Primero veo si arribo algun proceso y lo agrego, luego recien devuelvo el que se estaba ejecutando para darle prioridad al que arriba
                        for proceso in self.ready_queue:
                            print(proceso.id)

                        if len(self.ready_queue) > 0:
                            proceso_siguiente = self.ready_queue[0]
                            if proceso_siguiente != None and not self.is_proccess_loaded_in_memory(proceso_siguiente):
                                print('el proceso siguiente',
                                      proceso_siguiente.id, ' No esta en memoria')
                                best_partition = self.best_fit_partition(
                                    proceso_siguiente.size)
                                if best_partition != None:
                                    best_partition.proccess_asigned = proceso_siguiente
                                    proceso_siguiente.location = best_partition
                                    self.update_memory_GUI(
                                        proceso_siguiente, best_partition)
                                # Si es none es un caso especial en el cual se debe reemplazar si o si por el proceso en ejecucion que este en memoria, ya q no hay otra opcion.
                                if (best_partition == None):
                                    best_fit_partition = None
                                    for partition in self.memory_partitions:  # Encuentro la mejor particion teniendo en cuenta que no puede reemplazar aquella particion que tiene el proceso en ejecucion
                                        if partition.partition_id != 4 and partition.size >= proceso_siguiente.size:
                                            if best_fit_partition is None or partition.size < best_fit_partition.size:
                                                best_fit_partition = partition
                                    best_fit_partition.proccess_asigned = proceso_siguiente
                                    proceso_siguiente.location = best_fit_partition.partition_id
                                    self.update_memory_GUI(
                                        proceso_siguiente, best_fit_partition)
                        else:
                            print("La cola de listos está vacía.")
                        # proceso_siguiente = self.ready_queue[0]

                        # Aquí se devuelve el proceso en ejecución a la cola de listos
                        proceso_devuelto = self.proccess_in_execution
                        self.ready_queue.append(proceso_devuelto)
                        proceso_actual_id = self.proccess_in_execution.id if self.proccess_in_execution else "Ninguno"

                        self.proccess_exit = ctk.CTkLabel(
                            self.right_frame, text="Proceso que abandono el procesador: {}".format(proceso_actual_id))
                        self.proccess_exit.grid(
                            row=0, column=1, padx=10, pady=10)

                        self.proccess_in_execution = None
                        self.update_ready_queue_GUI()
                        if self.ready_queue:  # Si hay procesos en cola de listos, se asigna el siguiente nuevamente
                            proceso_siguiente = self.ready_queue.popleft()
                            self.proccess_in_execution = proceso_siguiente
                            self.procces_enter = ctk.CTkLabel(
                                self.right_frame, text="Proceso que se asigno al procesador: {}".format(proceso_siguiente.id))
                            self.procces_enter.grid(
                                row=0, column=2, padx=10, pady=10)
                            self.update_ready_queue_GUI()
                        break

                    # Ya sea por el quantum o porque termino, debe salir del procesador.

                    # while len(simulador.cola_procesos_listos) < 5 and lista_procesos_ordenados: #Controlo multiprogramacion
                    #     proceso_pendiente = lista_procesos_ordenados.pop(0)
                    #     simulador.cola_procesos_listos.append(proceso_pendiente)

    def verifyReadyQueue(self):

        for process in self.ready_queue:
            process.return_time += 1

        for proceso in self.all_processes:
            print("process id: ", proceso.id)
            if (len(self.ready_queue) < 5) and (proceso.arrival_time <= self.total_execution_inverse):
                print('arribo el proceso', proceso.id,
                      'en el tiempo', self.total_execution_inverse)
                self.ready_queue.append(proceso)
                self.all_processes.remove(proceso)
                self.update_ready_queue_GUI()

    def update_memory_GUI(self, process, best_fit_partition):
        process.internal_fragmentation = best_fit_partition.size - process.size
        ctk.CTkLabel(self.matrix, text=process.id).grid(
            row=best_fit_partition.partition_id, column=1, padx=5, pady=5)
        ctk.CTkLabel(self.matrix, text=process.size).grid(
            row=best_fit_partition.partition_id, column=2, padx=5, pady=5)
        ctk.CTkLabel(self.matrix, text=process.arrival_time).grid(
            row=best_fit_partition.partition_id, column=3, padx=5, pady=5)
        ctk.CTkLabel(self.matrix, text=process.execution_time).grid(
            row=best_fit_partition.partition_id, column=4, padx=5, pady=5)
        ctk.CTkLabel(self.matrix, text=process.internal_fragmentation).grid(
            row=(best_fit_partition.partition_id), column=5, padx=5, pady=5)

    def verifyIfNextProcessIsInMemoryAndLoad(self):
        print("La memoria esta llena")
        proceso_siguiente = self.ready_queue[0]
        if proceso_siguiente != None and not self.is_proccess_loaded_in_memory(proceso_siguiente):
            print("el siguiente proceso no esta en memoria, se debe cargar, sin reemplazar el proceso q se esta ejecutando")

            best_fit_partition = None

            for partition in self.memory_partitions:  # Encuentro la mejor particion teniendo en cuenta que no puede reemplazar aquella particion que tiene el proceso en ejecucion
                if partition.partition_id != 4 and partition.proccess_asigned.id != self.proccess_in_execution.id and partition.size >= proceso_siguiente.size:
                    # hasta aca todo correcto
                    if best_fit_partition is None or partition.size < best_fit_partition.size:
                        best_fit_partition = partition
            print('aa', best_fit_partition)

            if (best_fit_partition != None and not self.is_proccess_loaded_in_memory(proceso_siguiente)):
                best_fit_partition.proccess_asigned = proceso_siguiente
                proceso_siguiente.location = best_fit_partition.partition_id
             # Actualiza la interfaz o los datos necesarios
                ctk.CTkLabel(self.matrix, text=proceso_siguiente.id).grid(
                    row=best_fit_partition.partition_id, column=1, padx=5, pady=5)
                ctk.CTkLabel(self.matrix, text=proceso_siguiente.size).grid(
                    row=best_fit_partition.partition_id, column=2, padx=5, pady=5)
                ctk.CTkLabel(self.matrix, text=proceso_siguiente.arrival_time).grid(
                    row=best_fit_partition.partition_id, column=3, padx=5, pady=5)
                ctk.CTkLabel(self.matrix, text=proceso_siguiente.execution_time).grid(
                    row=best_fit_partition.partition_id, column=4, padx=5, pady=5)
                ctk.CTkLabel(self.matrix, text=proceso_siguiente.internal_fragmentation).grid(
                    row=(best_fit_partition.partition_id), column=5, padx=5, pady=5)
            # Si es none es un caso especial en el cual se debe reemplazar si o si por el proceso en ejecucion que este en memoria, ya q no hay otra opcion.
            if (best_fit_partition == None):
                for partition in self.memory_partitions:  # Encuentro la mejor particion teniendo en cuenta que no puede reemplazar aquella particion que tiene el proceso en ejecucion
                    if partition.partition_id != 4 and partition.size >= proceso_siguiente.size:
                        if best_fit_partition is None or partition.size < best_fit_partition.size:
                            best_fit_partition = partition
                best_fit_partition.proccess_asigned = proceso_siguiente
                proceso_siguiente.location = best_fit_partition.partition_id
             # Actualiza la interfaz o los datos necesarios
                ctk.CTkLabel(self.matrix, text=proceso_siguiente.id).grid(
                    row=best_fit_partition.partition_id, column=1, padx=5, pady=5)
                ctk.CTkLabel(self.matrix, text=proceso_siguiente.size).grid(
                    row=best_fit_partition.partition_id, column=2, padx=5, pady=5)
                ctk.CTkLabel(self.matrix, text=proceso_siguiente.arrival_time).grid(
                    row=best_fit_partition.partition_id, column=3, padx=5, pady=5)
                ctk.CTkLabel(self.matrix, text=proceso_siguiente.execution_time).grid(
                    row=best_fit_partition.partition_id, column=4, padx=5, pady=5)
                ctk.CTkLabel(self.matrix, text=proceso_siguiente.internal_fragmentation).grid(
                    row=(best_fit_partition.partition_id), column=5, padx=5, pady=5)

    def finish_simulation(self):
        # custom_box = tk.Toplevel(root)
        # custom_box.title("Custom Messagebox")
        top = tk.Toplevel()
        top.title('Simulación finalizada')
        titles = ['Process ID', 'Process Size', 'Arrival Time',
                  'Execution Time', 'Return Time', 'Wait Time']
        self.finished_queue = sorted(self.finished_queue, key=lambda proceso: (
            proceso.id, proceso.arrival_time))
        for i, title in enumerate(titles):
            # Poner títulos de la matriz
            tk.Label(top, text=title).grid(
                row=0, column=i, padx=5, pady=5)
        for i, process in enumerate(self.finished_queue, start=1):
            tk.Label(top, text=str(process.id)).grid(
                row=i, column=0, padx=5, pady=5)
            tk.Label(top, text=str(process.size)).grid(
                row=i, column=1, padx=5, pady=5)
            tk.Label(top, text=str(process.arrival_time)).grid(
                row=i, column=2, padx=5, pady=5)
            tk.Label(top, text=str(process.initial_ex_time)).grid(
                row=i, column=3, padx=5, pady=5)
            tk.Label(top, text=str(process.return_time)).grid(
                row=i, column=4, padx=5, pady=5)
            tk.Label(top, text=str(process.return_time - process.initial_ex_time)).grid(
                row=i, column=5, padx=5, pady=5)

        ok_button = tk.Button(top, text="OK", command=root.destroy)
        ok_button.grid(columnspan=6, pady=10)


# Add other necessary functions for the simulation logic

class MainApp(ctk.CTk):
    def __init__(self, master):
        self.master = master
        self.master.title("Main Application")

        # Create an instance of the Simulator class
        self.simulator = Simulator(self.master)


        # Add other elements to the main application if needed
        # ...
# Crea la aplicación y ejecútala
if __name__ == "__main__":
    root = tk.Tk()
    # Change the background color of the window to light gray
    root.configure(bg="#5B5E61")
    # Configure column weight to make elements expand horizontally
    # root.columnconfigure(0, weight=1)  # Assumes you are using column 0, adjust if necessary
    app = MainApp(root)
    root.mainloop()
