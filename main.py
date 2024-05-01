import tkinter as tk
from tkinter import messagebox
import time
import threading


class PomodoroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Time")

        self.tempo_trabalho = tk.StringVar()
        self.tempo_descanso = tk.StringVar()
        self.ciclos = tk.StringVar()

        self.timer_thread = None

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Tempo de trabalho").grid(column=0, row=0, padx=5, pady=5)
        self.entry_tempo_trabalho = tk.Entry(self.root, textvariable=self.tempo_trabalho)
        self.entry_tempo_trabalho.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(self.root, text="Tempo de descanso").grid(column=0, row=1, padx=5, pady=5)
        self.entry_tempo_descanso = tk.Entry(self.root, textvariable=self.tempo_descanso)
        self.entry_tempo_descanso.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(self.root, text="Ciclos").grid(column=0, row=2, padx=5, pady=5)
        self.entry_ciclos = tk.Entry(self.root, textvariable=self.ciclos)
        self.entry_ciclos.grid(row=2, column=1, pady=5, padx=5)

        self.start_button = tk.Button(self.root, text="Iniciar Contador", command=self.start_timer)
        self.start_button.grid(row=3, column=0, columnspan=2, pady=5, padx=5)

        self.stop_button = tk.Button(self.root, text="Parar Contador", command=self.stop_timer, state=tk.DISABLED)
        self.stop_button.grid(row=4, column=0, columnspan=2, pady=5, padx=5, )

    def start_timer(self):
        try:
            tempo_trabalho = int(self.tempo_trabalho.get())
            tempo_descanso = int(self.tempo_descanso.get())
            ciclos = int(self.ciclos.get())
        except ValueError:
            messagebox.showerror("Formato Inválido", "Por favor, insira somente números inteiros")
            return

        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        self.timer_thread = threading.Thread(target=self.run_timer, args=(tempo_trabalho, tempo_descanso, ciclos))
        self.timer_thread.start()

    def run_timer(self, tempo_trabalho, tempo_descanso, ciclos):
        for ciclo in range(ciclos):
            self.work(tempo_trabalho)
            if ciclo < ciclos - 1:
                self.rest_timer(tempo_descanso)

        self.complete_pomodoro()

    def work(self, tempo):
        messagebox.showinfo("Pomodoro", "Trabalhando...")
        time.sleep(tempo * 60)

    def rest_timer(self, tempo):
        messagebox.showinfo("Pomodoro", "Hora do descanso")
        time.sleep(tempo * 60)

    def complete_pomodoro(self):
        messagebox.showinfo("Pomodoro", "Pomodoro completo!")
        self.reset()

    def stop_timer(self):
        if self.timer_thread and self.timer_thread.is_alive():
            self.timer_thread.join()
            self.reset()

    def reset(self):
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.tempo_trabalho.set("")
        self.tempo_descanso.set("")
        self.ciclos.set("")


if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroApp(root)
    root.geometry("400x400")
    root.mainloop()
