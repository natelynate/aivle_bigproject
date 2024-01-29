import tkinter as tk
from tkinter import filedialog

class ClickRecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Click Recorder App")

        self.coordinates = []

        # Set the canvas size to match the desired screen resolution (1920x1080)
        self.canvas = tk.Canvas(root, width=1920, height=1080, bg="white")
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        # Place the "Export Coordinates" button at (100, 100) on the canvas
        self.export_button = tk.Button(self.canvas, text="Export Coordinates", command=self.export_coordinates)
        self.export_button.place(x=20, y=20)

        # Add label to display the count of points
        self.point_count_label = tk.Label(self.canvas, text="Points: 0")
        self.point_count_label.place(x=200, y=20)

        self.canvas.bind("<Button-1>", self.record_click)

    def record_click(self, event):
        # Scale the coordinates to fit within the canvas size
        x = (event.x / self.canvas.winfo_width()) * 1920
        y = (event.y / self.canvas.winfo_height()) * 1080

        self.coordinates.append((x, y))
        self.canvas.create_oval(event.x - 5, event.y - 5, event.x + 5, event.y + 5, fill="red")

        # Update the point count label
        self.update_point_count_label()

        if len(self.coordinates) == 100:
            self.export_coordinates()

    def export_coordinates(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])

        if file_path:
            with open(file_path, "w") as file:
                for x, y in self.coordinates:
                    file.write(f"{x},{y}\n")

            self.coordinates = []
            self.canvas.delete("all")
            self.update_point_count_label()  # Update the point count label after exporting
            print("Coordinates exported successfully.")

    def update_point_count_label(self):
        # Update the point count label text
        self.point_count_label.config(text=f"Points: {len(self.coordinates)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ClickRecorderApp(root)
    root.mainloop()
