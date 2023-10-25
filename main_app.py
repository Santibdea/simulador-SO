import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, messagebox
from PIL import Image
# Sets the appearance mode of the application
# "System" sets the appearance same as that of the system
ctk.set_appearance_mode("Dark")        
 
# Sets the color of the widgets
# Supported themes: green, dark-blue, blue
ctk.set_default_color_theme("dark-blue")  

class ComputerProcess:
    def __init__(self, id, size,arrival_time,execution_time,location = None):
        self.id = id
        self.size = size
        self.arrival_time = arrival_time
        self.execution_time = execution_time
        self.location = location

class Simulator:
    def __init__(self, master):
        self.master = master
        self.master.title("Simulador de Asignación de Memoria y Planificación de Procesos")
        self.process_ids = 1
        self.memory_partitions = [250, 120, 60,100]
        self.ready_queue = []
        self.titles = ['Memory Partition', 'Process ID', 'Process Size', 'Arrival Time', 'Execution Time']
        self.quantum = 2

        # Add GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Label to enter process information
        self.frame = tk.Frame(self.master,bg="#00008B")
        self.process_size_label = ctk.CTkLabel(self.master, text="Tamaño de Proceso:")
        self.process_size_label.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        self.process_size_entry = ctk.CTkEntry(self.master)
        self.process_size_entry.grid(row=0, column=1, padx=5, pady=5)
        
        self.process_ta_label = ctk.CTkLabel(self.master, text="Tiempo de arribo:")
        self.process_ta_label.grid(row=1, column=0, padx=50, pady=5, sticky="ew")
        self.process_ta_entry = ctk.CTkEntry(self.master)
        self.process_ta_entry.grid(row=1, column=1, padx=5, pady=5)

        self.process_ti_label = ctk.CTkLabel(self.master, text="Tiempo de irrupción:")
        self.process_ti_label.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        self.process_ti_entry = ctk.CTkEntry(self.master)
        self.process_ti_entry.grid(row=2, column=1, padx=5, pady=5)

        # Button to load a new process
        self.cargar_proceso_btn = ctk.CTkButton(self.master, text="Cargar Proceso", command=self.load_process)
        self.cargar_proceso_btn.grid(row=3, column=0, columnspan=2, pady=10)
        # Label for the state of the ready process queue
        ctk.CTkLabel(self.master, text="Cola de Procesos Listos:").grid(row=5, column=0, padx=5, pady=5, sticky="ew")

        # Listbox to display the ready process queue
        self.ready_queue_listbox = ctk.CTkTextbox(self.master)
        self.ready_queue_listbox.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

        # Button to start the simulation
        self.iniciar_btn = ctk.CTkButton(self.master, text="Iniciar Simulación", command=self.start_simulation)
        self.iniciar_btn.grid(row=7, column=0, columnspan=2, pady=10)

        # Button to finish the simulation
        ctk.CTkButton(self.master, text="Finalizar Simulación", command=self.finish_simulation).grid(row=8, column=0, columnspan=2, pady=10)

    def load_process(self):
        process_size = self.process_size_entry.get()
        process_ta = self.process_ta_entry.get()
        process_ti = self.process_ti_entry.get()
        if not process_ta or not process_size or not process_ti:
            messagebox.showerror("Error", "Por favor, ingrese el tiempo de arribo, el tiempo de irrupción y el tamaño del proceso.")
            return
        
        self.process_ta_entry.delete(0, tk.END)
        self.process_ti_entry.delete(0, tk.END)
        self.process_size_entry.delete(0, tk.END)

        try:
            process_size = int(process_size)
            process_id = self.process_ids
            process = ComputerProcess(process_id, process_size, process_ta, process_ti)
            self.ready_queue.append(process)
            self.process_ids += 1
            self.ready_queue_listbox.insert(tk.END, f"ID: {process.id}, TA: {process.arrival_time}, TI: {process.execution_time}\n")
        except ValueError:
            messagebox.showerror("Error", "El tamaño del proceso debe ser un número entero.")
            return


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

    def start_simulation(self):
        # Table to display memory partition information

        #Reutilizar variable. Ahora representa la row de la lista de finalizados
        self.process_ids = 1

        frame = self.frame
        frame.grid(row=1, column=1)
        self.delete_buttons()
        for index, partition in enumerate(self.memory_partitions):
            ctk.CTkLabel(frame, text=self.titles[index]).grid(row=0, column=index, padx=5, pady=5)
            ctk.CTkLabel(frame, text=f"Tamaño de Partición: {partition}K").grid(row=1+index, column=0, padx=5, pady=5)
            for i in range(0,3):
                process = self.ready_queue[i]
                process.location = i + 1
                ctk.CTkLabel(frame, text=process.id).grid(row=i+1, column=1, padx=5, pady=5)
                ctk.CTkLabel(frame, text=process.size).grid(row=i+1, column=2, padx=5, pady=5)
                ctk.CTkLabel(frame, text=process.arrival_time).grid(row=i+1, column=3, padx=5, pady=5)
                ctk.CTkLabel(frame, text=process.execution_time).grid(row=i+1, column=4, padx=5, pady=5)
        ctk.CTkLabel(frame, text=self.titles[4]).grid(row=0, column=4, padx=5, pady=5)
        ctk.CTkLabel(self.master, text="Procesos finalizados").grid(row=0, column=5, padx=100, pady=5)
        
        ctk.CTkButton(self.master, text="Continuar simulación", command=self.continue_simulation).grid(row=8, column=3, columnspan=2, pady=10)

    def continue_simulation(self):
        if self.ready_queue:
            self.quantum -= 1
            process = self.ready_queue[0]
            process.execution_time = str(int(process.execution_time) - 1)
            print(self.ready_queue)
            if process.execution_time == '0':
                ctk.CTkLabel(self.master, text=str(process.id)).grid(row=self.process_ids, column=5, padx=5, pady=5)
                ctk.CTkLabel(self.frame, text=process.execution_time).grid(row=process.location, column=4, padx=5, pady=5)
                self.process_ids += 1
                del self.ready_queue[0]
                self.quantum = 2
            else:
                if self.quantum == 0:
                    self.quantum = 2
                    self.ready_queue = self.ready_queue[1:] + [self.ready_queue[0]]
                ctk.CTkLabel(self.frame, text=process.execution_time).grid(row=process.location, column=4, padx=5, pady=5)
        else:
            self.finish_simulation()
            

    def finish_simulation(self):
        messagebox.showinfo("Simulación Finalizada", "La simulación ha finalizado.")
        # Call the function to update the GUI after finishing the simulation
        self.master.destroy()


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
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
    root.mainloop()
