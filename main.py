import tkinter as tk
from tkinter import messagebox
import time
from multiprocessing import Process, Pipe
from sorting import hybrid_sort_with_timing

class SortingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Hybrid Sort Visualization")

        self.canvas = tk.Canvas(root, width=800, height=400)
        self.canvas.pack()

        self.entry_label = tk.Label(root, text="Masukkan elemen array (dipisahkan oleh spasi):")
        self.entry_label.pack(pady=5)

        self.entry = tk.Entry(root, width=50)
        self.entry.pack(pady=5)

        self.sort_button = tk.Button(root, text="Urutkan", command=self.start_sort)
        self.sort_button.pack(pady=5)

        self.time_label = tk.Label(root, text="")
        self.time_label.pack(pady=5)

        self.array = []

    def draw_array(self, arr, color_array):
        self.canvas.delete("all")
        canvas_height = 400
        canvas_width = 800
        bar_width = canvas_width / (len(arr) + 1)
        offset = 30
        spacing = 10

        normalized_array = [i / max(arr) for i in arr]
        for i, height in enumerate(normalized_array):
            x0 = i * bar_width + offset + spacing
            y0 = canvas_height - height * 360
            x1 = (i + 1) * bar_width + offset
            y1 = canvas_height
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color_array[i])
            self.canvas.create_text(x0 + 2, y0, anchor=tk.SW, text=str(arr[i]))

        self.root.update_idletasks()

    def start_sort(self):
        try:
            self.array = list(map(int, self.entry.get().split()))
            parent_conn, child_conn = Pipe()
            process = Process(target=hybrid_sort_with_timing, args=(self.array, child_conn))
            process.start()
            self.root.after(100, self.check_process, process, parent_conn)
        except ValueError:
            messagebox.showerror("Input Error", "Masukkan hanya angka yang dipisahkan oleh spasi.")

    def check_process(self, process, parent_conn):
        if process.is_alive():
            self.root.after(100, self.check_process, process, parent_conn)
        else:
            process.join()
            if parent_conn.poll():
                result = parent_conn.recv()
                elapsed_time = result['time']
                sorted_array = result['array']
                self.draw_array(sorted_array, ['green'] * len(sorted_array))
                self.time_label.config(text=f"Estimasi waktu sorting: {elapsed_time:.4f} ms")

if __name__ == "__main__":
    root = tk.Tk()
    visualizer = SortingVisualizer(root)
    root.mainloop()
