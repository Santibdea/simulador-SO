import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename

# Sets the appearance mode of the application
# "System" sets the appearance same as that of the system
ctk.set_appearance_mode("Dark")

# Sets the color of the widgets
# Supported themes: green, dark-blue, blue
ctk.set_default_color_theme("dark-blue")


# Estados posibles de un proceso: ready, ready and suspended, in execution, y finished

class ComputerProcess:
    def __init__(self, id, size, arrival_time, execution_time, state=None, location=None):
        self.id = id
        self.size = size
        self.arrival_time = arrival_time
        self.execution_time = execution_time
        self.state = state
        self.location = location


class Partition:
    def __init__(self, size, not_busy=True):
        self.size = size
        self.not_busy = not_busy


class Simulator:
    def __init__(self, master):
        self.master = master
        self.master.title(
            "Simulador de Asignación de Memoria y Planificación de Procesos")
        self.process_ids = 1
        self.memory_partitions = [Partition(250), Partition(
            120), Partition(60), Partition(100)]
        self.ready_queue = []
        self.titles = ['Memory Partition', 'Process ID',
                       'Process Size', 'Arrival Time', 'Execution Time']
        self.quantum = 2
        self.total_execution = 0
        self.total_execution_inverse = 0

        self.max_quantum = 2
        self.multiprog_degree = 5

        # Create a dictionary to store label references
        self.label_references = {}
        # Add GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Label to enter process information
        self.matrix = tk.Frame(self.master, bg="#00008B")
        self.cola_finalizados = tk.Frame(self.master, bg="#00008B")
        self.frame3 = tk.Frame(self.master, bg="#00008B")
        # Adjust the row and column values as needed
        self.frame3.grid(row=4, column=0, columnspan=2)

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
        ctk.CTkLabel(self.frame3, text="Cola de Procesos Listos:").grid(
            row=1, column=0, padx=5, pady=5)

        # Listbox to display the ready process queue
        self.ready_queue_listbox = ctk.CTkTextbox(self.frame3)
        self.ready_queue_listbox.grid(row=1, column=1, padx=5, pady=5)

        # self.ready_queue_listbox = ctk.CTkScrollableFrame(self.frame3, width=200, height=200, orientation="horizontal")
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
            self.save_process(self, int(process_size),
                              int(process_ta), int(process_ti))
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

        process_id = self.process_ids
        process = ComputerProcess(process_id, p_size, p_ta, p_ti)

        self.total_execution += int(p_ti)
        self.ready_queue.append(process)
        self.process_ids += 1

        self.ready_queue_listbox.insert(
            tk.END, f"ID: {process.id}, TA: {process.arrival_time}, TI: {process.execution_time}\n")

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

    def best_partition(self, process_size):
        if process_size < self.memory_partitions[2].size:
            return 2
        elif process_size < self.memory_partitions[1].size:
            return 1
        elif process_size < self.memory_partitions[0].size:
            return 0

    def load_to_memory(self):
        matrix = self.matrix
        for i in range(0, len(self.ready_queue)):
            if i < self.multiprog_degree:
                process = self.ready_queue[i]
                if i < len(self.memory_partitions) - 1:
                    location = self.best_partition(process.size)
                    if self.memory_partitions[location].not_busy:
                        process.location = location
                        process.state = 'ready'
                        self.memory_partitions[location].not_busy = False

                        ctk.CTkLabel(matrix, text=process.id).grid(
                            row=location+1, column=1, padx=5, pady=5)
                        ctk.CTkLabel(matrix, text=process.size).grid(
                            row=location+1, column=2, padx=5, pady=5)
                        ctk.CTkLabel(matrix, text=process.arrival_time).grid(
                            row=location+1, column=3, padx=5, pady=5)
                        ctk.CTkLabel(matrix, text=process.execution_time).grid(
                            row=location+1, column=4, padx=5, pady=5)
                    else:
                        process.state = 'ready and suspended'

                else:
                    process.state = 'ready and suspended'
            else:
                break

    def start_simulation(self):
        # Ordenar por tiempo de arribo:
        self.ready_queue = sorted(
            self.ready_queue, key=lambda x: x.arrival_time)

        # Limpiar lo ingresado y reordenarlo por tiempo de arribo
        self.ready_queue_listbox.delete("1.0", "end")
        for queue_process in self.ready_queue:
            self.ready_queue_listbox.insert(
                tk.END, f"ID: {queue_process.id}, TA: {queue_process.arrival_time}, TI: {queue_process.execution_time}\n")

        # Reutilizar variable. Ahora representa la row de la lista de finalizados
        self.process_ids = 1

        matrix = self.matrix
        matrix.grid(row=1, column=0)

        cola_finalizados = self.cola_finalizados
        cola_finalizados.grid(row=1, column=1, sticky="ne")

        self.delete_buttons()

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
        ctk.CTkLabel(matrix, text=self.titles[4]).grid(
            row=0, column=4, padx=5, pady=5)
        self.load_to_memory()

        ctk.CTkLabel(cola_finalizados, text="Procesos finalizados").grid(
            row=0, padx=100, pady=5)

        ctk.CTkButton(self.frame3, text="Finalizar Simulación",
                      command=self.finish_simulation).grid(row=2, column=0, pady=10)
        ctk.CTkButton(self.frame3, text="Continuar simulación",
                      command=self.continue_simulation).grid(row=2, column=1, pady=10)
        self.progress_bar = ctk.CTkProgressBar(
            self.master, orientation="horizontal")
        self.progress_bar.grid(row=9, pady=10, columnspan=2)
        self.progress_bar.set(0)

    def next_execution(self):
        queue = self.ready_queue
        if len(queue) > 2:
            queue[0], queue[1], queue[2] = queue[2], queue[0], queue[1]
        elif len(queue) == 2:
            queue[0], queue[1] = queue[1], queue[0]

    def end_process(self):
        matrix = self.matrix
        process = self.ready_queue[0]
        location = process.location
        ctk.CTkLabel(matrix, text="     -    ").grid(
            row=location+1, column=1, padx=5, pady=5)
        ctk.CTkLabel(matrix, text="     -    ").grid(
            row=location+1, column=2, padx=5, pady=5)
        ctk.CTkLabel(matrix, text="     -    ").grid(
            row=location+1, column=3, padx=5, pady=5)
        ctk.CTkLabel(matrix, text="     -    ").grid(
            row=location+1, column=4, padx=5, pady=5)
        ctk.CTkLabel(self.cola_finalizados, text=str(process.id)).grid(
            row=self.process_ids, padx=5, pady=5)
        self.memory_partitions[process.location].not_busy = True
        del self.ready_queue[0]

    def continue_simulation(self):
        if self.ready_queue:
            self.total_execution_inverse += 1
            self.progress_bar.set(
                self.total_execution_inverse / self.total_execution)
            self.quantum -= 1

            process = self.ready_queue[0]
            # Se almacena como string porque para mostrarlo en la ventana necesita ser string
            process.execution_time = str(int(process.execution_time) - 1)

            if process.execution_time == '0':  # '0' no es falsy >:(
                self.end_process()
                self.load_to_memory()
                self.process_ids += 1
                self.quantum = self.max_quantum
            else:
                if not self.quantum:
                    self.quantum = self.max_quantum

                    self.next_execution()

                ctk.CTkLabel(self.matrix, text=process.execution_time).grid(
                    row=process.location+1, column=4, padx=5, pady=5)

        else:
            self.finish_simulation()

    def finish_simulation(self):
        # custom_box = tk.Toplevel(root)
        # custom_box.title("Custom Messagebox")
        top = tk.Toplevel()
        top.title('Simulación finalizada')
        # # Load your image
        image_path = "images/libertad.webp"
        img = Image.open(image_path)
        img = ImageTk.PhotoImage(img)

        # # Display the image
        image_label = tk.Label(top, image=img)
        image_label.image = img  # To prevent garbage collection
        image_label.pack()

        # # Additional text or buttons can be added as needed
        # message_label = tk.Label(top, text="Cerrar")
        # message_label.pack()

        # Change here to root.destroy
        ok_button = tk.Button(top, text="OK", command=root.destroy)
        ok_button.pack()


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
    root.configure(bg="#00008B")
    # Configure column weight to make elements expand horizontally
    # root.columnconfigure(0, weight=1)  # Assumes you are using column 0, adjust if necessary
    app = MainApp(root)
    root.mainloop()
