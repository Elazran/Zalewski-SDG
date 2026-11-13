import tkinter as tk
from tkinter import filedialog, messagebox

from src.data_service import get_layer


def simple_operations():
    layer = get_layer()

    if layer is None:
        return

    window = tk.Toplevel()
    window.title("Proste operacje")
    window.geometry("400x300")

    operation = tk.StringVar(value="buffer")
    threshold = tk.StringVar()
    buffer_distance = tk.StringVar()
    simplify_tolerance = tk.StringVar()

    tk.Label(window, text="Operacja:").pack()

    tk.OptionMenu(
        window,
        operation,
        "buffer",
        "convex hull",
        "simplify",
        "centroid",
        command=lambda x: show_inputs()
    ).pack()


    inputs_frame = tk.Frame(window)
    inputs_frame.pack(pady=10)

    buffer_frame = tk.Frame(inputs_frame)
    tk.Label(
        buffer_frame,
        text="Szerokość bufora (w jednostkach układu warstwy):"
    ).pack()
    tk.Entry(buffer_frame, textvariable=buffer_distance).pack()

    simplify_frame = tk.Frame(inputs_frame)
    tk.Label(
        simplify_frame,
        text="Tolerancja uproszczenia (im większa, tym mniej punktów w geometrii):"
    ).pack()
    tk.Entry(simplify_frame, textvariable=simplify_tolerance).pack()

    def show_inputs():
        for frame in (buffer_frame, simplify_frame):
            frame.pack_forget()

        selected = operation.get()

        if selected == "buffer":
            buffer_frame.pack()
        elif selected == "simplify":
            simplify_frame.pack()

    show_inputs()

    def execute():
        selected = operation.get()

        result = layer.copy()
        try:
            if selected == "buffer":
                result["geometry"] = layer.geometry.buffer(
                    float(buffer_distance.get())
                )

            elif selected == "convex hull":
                result["geometry"] = layer.geometry.convex_hull

            elif selected == "simplify":
                result["geometry"] = layer.geometry.simplify(
                    float(simplify_tolerance.get())
                )

            elif selected == "centroid":
                result["geometry"] = layer.geometry.centroid

        except ValueError:
            messagebox.showerror(
                "Błąd",
                "Wprowadź poprawną wartość liczbową w polu parametru.",
                parent=window
            )
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".geojson",
            filetypes=[("GeoJSON", "*.geojson")]
        )

        if path:
            result.to_file(path)
            window.destroy()

    tk.Button(
        window,
        text="Wykonaj",
        command=execute
    ).pack()