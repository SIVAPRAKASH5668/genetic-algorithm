import tkinter as tk
from tkinter import ttk
import random
from location import Location
from genetic_algorithm import GeneticAlgorithm


class VRPSolver(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Vehicle Routing Problem Solver")
        self.geometry("1200x800")
        self.configure(bg="#eaf2f8")  # Light background color

        self.colors = [
            "#FF5733", "#F8C471", "#1ABC9C", "#1E8449", "#85C1E9",
            "#3498DB", "#E74C3C", "#8E44AD", "#34495E", "#EC7063",
            "#A569BD", "#16A085", "#F39C12", "#2C3E50", "#D7BDE2",
        ]

        self.locations = []
        self.setup_ui()
        self.generate_initial_locations(limit=20)

    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas for visualization
        self.canvas = tk.Canvas(
            main_frame, width=1000, height=600, bg="white", borderwidth=2, relief="solid"
        )
        self.canvas.grid(row=0, column=0, columnspan=2, pady=10)

        # Left panel for controls
        control_frame = ttk.Frame(main_frame, padding=10)
        control_frame.grid(row=1, column=0, sticky="nw")

        # Add location controls (in a single line)
        ttk.Label(control_frame, text="Add Location", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=3, pady=5)

        ttk.Label(control_frame, text="X:").grid(row=1, column=0, padx=5, sticky="e")
        self.x_entry = ttk.Entry(control_frame, width=5)
        self.x_entry.grid(row=1, column=1, padx=5)

        ttk.Label(control_frame, text="Y:").grid(row=1, column=2, padx=5, sticky="e")
        self.y_entry = ttk.Entry(control_frame, width=5)
        self.y_entry.grid(row=1, column=3, padx=5)

        ttk.Button(control_frame, text="Add Location", command=self.add_location).grid(row=1, column=4, padx=10)

        # Delete location controls
        ttk.Label(control_frame, text="Delete Location", font=("Arial", 12, "bold")).grid(row=2, column=0, columnspan=3, pady=10)

        self.location_dropdown = ttk.Combobox(control_frame, state="readonly", width=15)
        self.location_dropdown.grid(row=3, column=0, columnspan=3, pady=5)
        ttk.Button(control_frame, text="Delete", command=self.delete_location).grid(row=3, column=4, padx=10)

        # Solve VRP controls
        ttk.Label(control_frame, text="Solve VRP", font=("Arial", 12, "bold")).grid(row=4, column=0, columnspan=3, pady=10)

        ttk.Label(control_frame, text="Vehicles:").grid(row=5, column=0, sticky="e", padx=5)
        self.vehicle_count = ttk.Entry(control_frame, width=5)
        self.vehicle_count.insert(0, "3")
        self.vehicle_count.grid(row=5, column=1, pady=5)

        ttk.Button(control_frame, text="Solve", command=self.solve_vrp).grid(row=5, column=4, padx=10)

        # Right panel for information
        info_frame = ttk.Frame(main_frame, padding=10)
        info_frame.grid(row=1, column=1, sticky="ne")

        ttk.Label(info_frame, text="Information Panel", font=("Arial", 12, "bold")).pack()

        self.info_text = tk.Text(info_frame, width=40, height=10, wrap=tk.WORD, state=tk.DISABLED)
        self.info_text.pack(pady=5)

    def generate_initial_locations(self, limit=20):
        for _ in range(limit):
            x = random.randint(0, 49)
            y = random.randint(0, 29)

            if not any(loc.x == x and loc.y == y for loc in self.locations):
                is_depot = not self.locations  # First location is the depot
                location = Location(x, y, is_depot)
                self.locations.append(location)

        self.update_dropdown()
        self.draw_locations()

    def draw_locations(self):
        self.canvas.delete("all")
        for location in self.locations:
            location.draw_location(self.canvas)

    def draw_route(self, from_loc, to_loc, color):
        x1, y1 = from_loc.x * 20, from_loc.y * 20
        x2, y2 = to_loc.x * 20, to_loc.y * 20
        self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2)

    def update_dropdown(self):
        options = [f"({loc.x}, {loc.y})" for loc in self.locations if not loc.depot]
        self.location_dropdown['values'] = options
        if options:
            self.location_dropdown.current(0)

    def add_location(self):
        try:
            x = int(self.x_entry.get())
            y = int(self.y_entry.get())

            if 0 <= x <= 49 and 0 <= y <= 29:
                if not any(loc.x == x and loc.y == y for loc in self.locations):
                    location = Location(x, y)
                    self.locations.append(location)
                    self.update_dropdown()
                    self.draw_locations()

            self.x_entry.delete(0, tk.END)
            self.y_entry.delete(0, tk.END)
        except ValueError:
            pass

    def delete_location(self):
        selected = self.location_dropdown.get()
        if selected:
            x, y = map(int, selected.strip("()").split(", "))
            self.locations = [loc for loc in self.locations if loc.x != x or loc.y != y]
            self.update_dropdown()
            self.draw_locations()

    def solve_vrp(self):
        try:
            vehicle_count = int(self.vehicle_count.get())
            if vehicle_count < 1:
                return

            depot = next(loc for loc in self.locations if loc.depot)
            locations_no_depot = [loc for loc in self.locations if not loc.depot]

            solutions = []
            locations_per_vehicle = len(locations_no_depot) // vehicle_count

            for i in range(vehicle_count):
                start_idx = i * locations_per_vehicle
                end_idx = start_idx + locations_per_vehicle
                if i == vehicle_count - 1:
                    end_idx = len(locations_no_depot)

                pool = locations_no_depot[start_idx:end_idx]
                if pool:
                    ga = GeneticAlgorithm(pool, depot)
                    solution = ga.solve()[-1]
                    solutions.append(solution)

            self.draw_locations()
            for i, solution in enumerate(solutions):
                color = self.colors[i % len(self.colors)]
                genes = solution.genes
                for j in range(1, len(genes)):
                    self.draw_route(genes[j - 1], genes[j], color)
                    genes[j].draw_location(self.canvas, color)

            self.display_summary(solutions)
        except ValueError:
            pass

    def display_summary(self, solutions):
        self.info_text.configure(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)

        for i, solution in enumerate(solutions):
            self.info_text.insert(tk.END, f"Vehicle {i + 1} Route:\n")
            for loc in solution.genes:
                self.info_text.insert(tk.END, f"({loc.x}, {loc.y}) -> ")
            self.info_text.insert(tk.END, "END\n\n")

        self.info_text.configure(state=tk.DISABLED)


if __name__ == "__main__":
    app = VRPSolver()
    app.mainloop()
