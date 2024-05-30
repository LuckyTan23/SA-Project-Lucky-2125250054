import tkinter as tk
import time

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
            start_time = time.time()
            self.hybrid_sort(self.array)
            end_time = time.time()
            elapsed_time = end_time - start_time
            self.time_label.config(text=f"Estimasi waktu sorting: {elapsed_time:.4f} detik")
        except ValueError:
            tk.messagebox.showerror("Input Error", "Masukkan hanya angka yang dipisahkan oleh spasi.")

    def heapify(self, arr, n, i, color_array):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and arr[i] < arr[left]:
            largest = left

        if right < n and arr[largest] < arr[right]:
            largest = right

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            self.draw_array(arr, color_array)
            time.sleep(0.5)
            self.heapify(arr, n, largest, color_array)

    def heap_sort(self, arr):
        n = len(arr)
        color_array = ['gray'] * len(arr)

        for i in range(n // 2 - 1, -1, -1):
            self.heapify(arr, n, i, color_array)

        for i in range(n-1, 0, -1):
            arr[i], arr[0] = arr[0], arr[i]
            color_array[i] = 'green'
            self.draw_array(arr, color_array)
            time.sleep(0.5)
            self.heapify(arr, i, 0, color_array)

    def merge_sort(self, arr, l=0, r=None):
        if r is None:
            r = len(arr) - 1

        if l < r:
            m = l + (r - l) // 2
            self.merge_sort(arr, l, m)
            self.merge_sort(arr, m + 1, r)
            self.merge(arr, l, m, r)

    def merge(self, arr, l, m, r):
        n1 = m - l + 1
        n2 = r - m

        L = arr[l:l + n1]
        R = arr[m + 1:m + 1 + n2]

        i = j = 0
        k = l

        while i < n1 and j < n2:
            if L[i] <= R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
            self.draw_array(arr, ['gray' if x != k else 'yellow' for x in range(len(arr))])
            time.sleep(0.5)

        while i < n1:
            arr[k] = L[i]
            i += 1
            k += 1
            self.draw_array(arr, ['gray' if x != k else 'yellow' for x in range(len(arr))])
            time.sleep(0.5)

        while j < n2:
            arr[k] = R[j]
            j += 1
            k += 1
            self.draw_array(arr, ['gray' if x != k else 'yellow' for x in range(len(arr))])
            time.sleep(0.5)

    def hybrid_sort(self, arr):
        if len(arr) <= 10:
            self.merge_sort(arr)
        else:
            self.heap_sort(arr)
            self.merge_sort(arr)
        self.draw_array(arr, ['green'] * len(arr))

if __name__ == "__main__":
    root = tk.Tk()
    visualizer = SortingVisualizer(root)
    root.mainloop()
