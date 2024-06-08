import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd


class EditableTableApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Szerkeszthető táblázat")

        self.create_table()
        self.populate_table()
        self.create_generate_button()

    def create_table(self):
        self.tree = ttk.Treeview(
            self.root, columns=("Sorszám", "Téma", "Óraszám"), show="headings"
        )
        self.tree.heading("Sorszám", text="Sorszám")
        self.tree.heading("Téma", text="Téma")
        self.tree.heading("Óraszám", text="Óraszám")
        self.tree.pack(pady=20)

        self.tree.column("Sorszám", width=70)
        self.tree.column("Téma", width=500)
        self.tree.column("Óraszám", width=100)

        self.tree.bind("<Double-1>", self.on_double_click)

    def populate_table(self):
        # Add sample data
        self.data = [
            ["Bolygónk élővilága", 4],
            ["Összefoglalás", 2],
            ["Számonkérés", 1],
        ]

        for i in range(10):  # Ensure there are at least 10 rows
            if i < len(self.data):
                self.tree.insert(
                    "", "end", values=(i + 1, self.data[i][0], self.data[i][1])
                )
            else:
                self.tree.insert("", "end", values=(i + 1, "", ""))

    def on_double_click(self, event):
        item = self.tree.selection()[0]
        column = self.tree.identify_column(event.x)
        column_index = int(column.replace("#", "")) - 1

        # Prevent editing the "Sorszám" column
        if column_index == 0:
            return

        # Get the item and column index
        selected_item = self.tree.item(item, "values")

        # Get cell coordinates
        x, y, width, height = self.tree.bbox(item, column)

        # Create an entry widget at the location of the selected cell
        entry = tk.Entry(self.tree)
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, selected_item[column_index])
        entry.focus_set()

        entry.bind(
            "<Return>", lambda e: self.save_edit(item, column_index, entry.get(), entry)
        )
        entry.bind("<FocusOut>", lambda e: entry.destroy())

    def save_edit(self, item, column_index, value, entry):
        # Get the current values of the selected item
        values = list(self.tree.item(item, "values"))

        # Update the value in the specific column
        values[column_index] = value

        # Update the item with the new values
        self.tree.item(item, values=values)

        # Destroy the entry widget
        entry.destroy()

    def create_generate_button(self):
        self.generate_button = tk.Button(
            self.root, text="Generálás", command=self.generate
        )
        self.generate_button.pack(pady=20)

    def generate(self):
        data = []
        for item in self.tree.get_children():
            row = self.tree.item(item)["values"]
            sorszam, tema, oraszam = row
            try:
                oraszam = int(oraszam)
                for i in range(oraszam):
                    data.append([i + 1, tema])
            except ValueError:
                continue

        # Convert to DataFrame and save as Excel
        df = pd.DataFrame(data, columns=["Óraszám", "Téma"])
        df.to_excel("output.xlsx", index=False)

        messagebox.showinfo("Info", "Excel fájl generálva: output.xlsx")


if __name__ == "__main__":
    root = tk.Tk()
    app = EditableTableApp(root)
    root.mainloop()
