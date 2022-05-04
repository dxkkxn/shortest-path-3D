import tkinter as tk
from tkinter import ttk
from grid import Grid
from dijkstra import dijkstra_matrix_sorted_dict

inf = float('inf')

class App(tk.Frame):
    def __init__(self, master, opengl, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.opengl_app = opengl
        self.canvas = tk.Canvas(self, width=1024, height=1024)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)
        self.settings = tk.Frame(self, bg="red")
        self.settings.pack(side=tk.TOP, fill=tk.BOTH)

        phone = tk.StringVar()
        subframe = tk.Frame(self.settings)
        dijkstra = tk.Radiobutton(subframe, text="Dijkstra",
                                  variable=phone, value="Dijkstra", anchor=tk.W)
        a_star = tk.Radiobutton(subframe, text="A-star", variable=phone,
                                value="A-star", anchor=tk.W)

        subframe2 = tk.Frame(self.settings)
        phone = tk.StringVar()
        two_d = tk.Radiobutton(subframe2, text="2D",
                            variable=phone, value="2D", anchor=tk.W)

        three_d = tk.Radiobutton(subframe2, text="3D", variable=phone,
                                value="3D", anchor=tk.W)
        two_d.pack(side=tk.TOP, fill=tk.X, padx=10)
        three_d.pack(side=tk.TOP, fill=tk.X,  padx=10)

        label = tk.Label(self.settings, text="Water level :")
        label.pack(side=tk.LEFT, fill=tk.BOTH)
        self.water_sb = tk.Spinbox(self.settings, from_=0, to=10, increment=1, width=2,
                            command=self.update_grid, state="readonly")
        self.water_sb.pack(side=tk.LEFT, fill=tk.BOTH, padx=10)

        sep = ttk.Separator(self.settings, orient=tk.VERTICAL)
        sep.pack(side=tk.LEFT, fill=tk.BOTH, padx=10)

        dijkstra.pack(side=tk.TOP, fill=tk.X, padx=10)
        a_star.pack(side=tk.TOP, fill=tk.X,  padx=10)
        subframe.pack(side=tk.LEFT, padx=10)
        subframe2.pack(side=tk.LEFT, padx=10)

        sep = ttk.Separator(self.settings, orient=tk.VERTICAL)
        sep.pack(side=tk.LEFT, fill=tk.BOTH, padx=10)

        animate = tk.Button(self.settings, text="Animate")
        animate.pack(side=tk.LEFT, fill=tk.BOTH, padx=10)

    def create_grid(self, grid):
        self.grid = grid
        n = len(self.grid)
        self.dico = {}
        self.width = self.canvas.winfo_width()
        self.height = self.canvas.winfo_height()
        x_step = self.width/n
        y_step = self.height/n
        for i in range(n):
            for j in range(n):
                #draw of main square
                x_0 = i * x_step
                y_0 = j * y_step
                color = grid.color(j, i)
                str_col = self.to_hex_rgb(*color)
                self.dico[j, i] = self.canvas.create_rectangle(x_0, y_0, x_0 + x_step, y_0 + y_step,
                                        fill=str_col, width=2, tags="main")
        self.canvas.tag_bind("main", sequence="<ButtonRelease-1>",
                             func=self.select_square)
        self.canvas.addtag_all("all")
        self.selected = []

    @staticmethod
    def to_hex_rgb(r, g, b):
        print(r, g, b)
        """
        Returns de color in 8bits hexadecimal form in str format
        """
        color = [r,g,b]
        hex_rgb_list = []
        for x in color:
            hex_x = hex(x)[2:]
            if len(hex_x) == 1:
                hex_x = "0" + hex_x
            hex_rgb_list.append(hex_x)
        return "#" + "".join(hex_rgb_list)

    def draw_path(self):
        """Draws the path with green rectangles"""
        x_step = self.width / 12
        y_step = self.height / 12
        x_small_sq_len = x_step/3
        y_small_sq_len = y_step/3
        for j, i in self.path:
            x_0 = i * x_step + x_small_sq_len
            y_0 = j * y_step + y_small_sq_len
            self.canvas.create_rectangle(x_0, y_0, x_0 + x_small_sq_len,
                                         y_0 + y_small_sq_len, fill="green",
                                         width=2, tags="path")

    def select_square(self, event=None):
        """Change square color when a square has been clicked."""
        n = len(self.selected)
        if n < 2:
            id_ = self.canvas.find_withtag("current")[0]
            self.canvas.itemconfigure(id_, fill="purple")
            self.canvas.tag_bind(id_, sequence="<ButtonRelease-3>",
                                 func=self.deselect_square)
            for coord, iden in self.dico.items():
                if iden == id_:
                    self.selected.append(coord)
                    break
            if len(self.selected) == 2:
                start = self.selected[0]
                target = self.selected[1]
                self.path = dijkstra_matrix_sorted_dict(self.grid.grid,
                                                        start, target)
                self.opengl_app.set_path(self.path)
                self.opengl_app.display_path = True

                self.draw_path()
                self.water_sb.configure(state=tk.DISABLED)

    def deselect_square(self, event=None):
        id_ = self.canvas.find_withtag("current")[0]
        self.canvas.tag_unbind(id_, sequence="<ButtonRelease-3>")
        i = 0 if self.dico[self.selected[0]] == id_ else 1
        print(i)
        j, k = self.selected[i]
        color = self.grid.color(j, k)
        str_col = self.to_hex_rgb(*color)
        self.canvas.itemconfigure(id_, fill=str_col)
        self.selected.pop(i)
        self.water_sb.configure(state="readonly")
        self.canvas.delete("path")

    def update_grid(self):
        if len(self.selected) > 0:
            assert(len(self.selected) == 1)
            id_ = self.dico[self.selected[0]]
            self.canvas.tag_unbind(id_, sequence="<ButtonRelease-3>")
        self.selected = []
        lvl = int(self.water_sb.get())
        self.opengl_app.set_water_height(lvl)
        for i in range(len(self.grid)):
            for j in range(len(self.grid)):
                y = self.grid.calculate_height(j, i)
                if y <= lvl:
                    if len(self.selected) > 0:
                        if (j, i) != self.selected[0]:
                            self.canvas.itemconfig(self.dico[j, i], fill="cyan")
                            self.grid[j, i] = inf
                    else:
                        self.canvas.itemconfig(self.dico[j, i], fill="cyan")
                        self.grid[j, i] = inf
                else:
                    self.grid[j, i] = self.grid.old_grid[j][i]
                    color = self.grid.color(j, i)
                    str_col = self.to_hex_rgb(*color)
                    self.canvas.itemconfig(self.dico[j, i], fill=str_col)
