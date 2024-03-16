from S07_TP14_01 import *
from S08_TP15 import PlanetTk
import tkinter as tk
import random


class Conway(PlanetTk):
    NORTH, EAST, SOUTH, WEST = (-1, 0), (0, 1), (1, 0), (0, -1)
    NORTH_EAST, SOUTH_EAST, SOUTH_WEST, NORTH_WEST = (
        -1, 1), (1, 1), (1, -1), (-1, -1)
    WIND_ROSE = (NORTH, NORTH_EAST, EAST, SOUTH_EAST,
                 SOUTH, SOUTH_WEST, WEST, NORTH_WEST)

    def __init__(self, root, name, lattitude_cells_count, longitude_cells_count, background_color='white', foreground_color='dark blue', gridlines_color='maroon',  cell_size=20, gutter_size=0, margin_size=0, show_content=True, show_grid_lines=True, **kw):
        super().__init__(root, name, lattitude_cells_count, longitude_cells_count, {Human}, background_color='white',
                         foreground_color='dark blue', gridlines_color='maroon',  cell_size=20, gutter_size=0, margin_size=0, show_content=True, show_grid_lines=True, **kw)
        self.__prev_grid = None
        self.__b_quit = tk.Button(self.get_root(), text='Close', command=self.quit)
        self.__b_quit.pack(side=tk.BOTTOM)
        for cell_number in range(self.get_cells_count()):
            def func_with_args(event, num=cell_number): return self.born_on_click(num)
            self.tag_bind(f'c_{cell_number}', '<Button-1>', func_with_args)
            self.tag_bind(f't_{cell_number}', '<Button-1>', func_with_args)

        self.draw()

    def copy_grid(self):
        copied_grid = [[cell for cell in row] for row in self.get_grid()]
        return copied_grid

    def set_prev_grid(self, grid):
        self.__prev_grid = grid

    def get_prev_grid(self):
        return self.__prev_grid

    def populate_random_neighborhood(self):
        random_neighborhood_cells_number = self.get_cell_neighborhood_numbers(
            random.randint(0, self.get_cells_count()-1), Conway.WIND_ROSE, True)
        for i in random_neighborhood_cells_number:
            self.born(i, Human())

    def init_population(self):
        n = self.get_columns_count() * 7 + 15
        c = self.get_columns_count()
        self.born(n, Human())
        self.born(n+1, Human())
        self.born(n+2, Human())
        self.born(n+2 - c, Human())
        self.born(n+2 - 2*c - 1, Human())

    def born_on_click(self, cell_number):
        self.born(cell_number, Human())
        self.itemconfigure(f't_{cell_number}', text=Human())
        self.itemconfigure(f'c_{cell_number}', fill='yellow')

    def next_generation(self):
        temp_grid = self.copy_grid()
        self.set_prev_grid(self.copy_grid())

        for i in self.get_same_value_cell_numbers(Human()):
            neighborhood = self.get_cell_neighborhood_numbers(i, Conway.WIND_ROSE, False)
            neighbors = [neighbor for neighbor in neighborhood if isinstance(self.get_cell(neighbor), Human)]
            if (len(neighbors) < 2 or len(neighbors) > 3):
                l, c = self.get_coordinates_from_cell_number(i)
                temp_grid[l][c] = Ground()
            # if len(neighbors) == 3 || 2 do nothing

        for j in self.get_same_value_cell_numbers(Ground()):
            free_cell_neighborhood = self.get_cell_neighborhood_numbers(j, Conway.WIND_ROSE, False)
            human_neighbors = [neighbor for neighbor in free_cell_neighborhood if isinstance(
                self.get_cell(neighbor), Human)]
            if (len(human_neighbors) == 3):
                l, c = self.get_coordinates_from_cell_number(j)
                temp_grid[l][c] = Human()

        for k in range(self.get_cells_count()):
            l, c = self.get_coordinates_from_cell_number(k)
            if (temp_grid[l][c] == Human()):
                self.born(k, Human())
            else:
                self.die(k)

    def update_canvas(self):
        self.next_generation()

        for cell_number in range(self.get_cells_count()):
            l, c = self.get_coordinates_from_cell_number(cell_number)
            if (self.get_cell(cell_number) != self.get_prev_grid()[l][c]):
                cell_type = self.get_cell(cell_number)
                color = "yellow" if cell_type == Human() else "white"
                self.itemconfigure(f't_{cell_number}', text=cell_type)
                self.itemconfigure(f'c_{cell_number}', fill=color)

        self.after(400, self.update_canvas)


if __name__ == '__main__':

    root = tk.Tk()
    LINES_COUNT = 30
    COLUMNS_COUNT = 60
    CELL_SIZE = 20
    GUTTER_SIZE = 0
    MARGIN_SIZE = 10
    elements_types = {Lion, Cow, Water, Herb, Dragon}
    app = Conway(root, "Terre", LINES_COUNT, COLUMNS_COUNT, elements_types,
                 CELL_SIZE, GUTTER_SIZE, MARGIN_SIZE, width=80, height=50)

    app.populate_random_neighborhood()
    app.populate_random_neighborhood()
    app.populate_random_neighborhood()
    app.populate_random_neighborhood()
    app.populate_random_neighborhood()
    app.init_population()

    app.update_canvas()

    app.mainloop()
