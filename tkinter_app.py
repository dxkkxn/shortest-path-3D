"""MVC pattern for tk application."""
import tkinter as tk
from tkinter import ttk
from dijkstra import dijkstra_matrix_sorted_dict
from a_star import a_star_matrix_sorted_dict
from grid import Grid
import random

inf = float('inf')


class TkSettingsView(tk.Toplevel):
    """Tk toplevel window for the settings."""

    def __init__(self, *args, **kwargs):
        """Initialise the settings toplevel."""
        super().__init__(*args, **kwargs)
        self.grid_size_scale = tk.Scale(self, from_=2, to_=50,
                                        label="Grid size",
                                        orient=tk.HORIZONTAL, tickinterval=10)
        self.grid_size_scale.set(20)
        self.grid_size_scale.pack(side=tk.TOP, fill=tk.X, anchor=tk.W)
        smooth_algorithm = tk.Label(self, text="Smoothing algorithm:",
                                    anchor=tk.W)
        smooth_algorithm.pack(side=tk.TOP, fill=tk.X)
        self.phone = tk.StringVar()
        frame = tk.Frame(self, bg="red")
        self.tuckey = tk.Radiobutton(frame, text="Tuckey",
                                     variable=self.phone, value="Tuckey",
                                     anchor=tk.CENTER, indicatoron=0)
        self.average = tk.Radiobutton(frame, text="Average", variable=self.phone,
                                      value="Average", anchor=tk.CENTER,
                                      indicatoron=0)
        self.tuckey.pack(side=tk.LEFT)
        self.average.pack(side=tk.LEFT)
        frame.pack(side=tk.TOP)  #,fill=tk.X, expand=tk.TRUE)

        self.radius_smooth_scale = tk.Scale(self, from_=0, to_=10,
                                            label="Smooth radius",
                                            orient=tk.HORIZONTAL,
                                            tickinterval=2)
        self.radius_smooth_scale.pack(side=tk.TOP, fill=tk.X)
        self.radius_smooth_scale.set(1)

        self.water_res_scale = tk.Scale(self, from_=0, to_=64,
                                        label="Water resolution (3D)",
                                        orient=tk.HORIZONTAL, tickinterval=16)
        self.water_res_scale.set(10)
        self.water_res_scale.pack(side=tk.TOP, fill=tk.X)
        self.phone.set("Tuckey")
        self.seed_scale = tk.Scale(self, from_=0, to_=1000,
                                   label="Seed",
                                   orient=tk.HORIZONTAL, tickinterval=400)
        self.seed_scale.set(random.randint(0,1000))
        self.seed_scale.pack(side=tk.TOP, fill=tk.X)
        self.validate = tk.Button(self, text="Create")
        self.validate.pack(side=tk.TOP)
        self.grab_set()


class TkSettingsController():
    """Controller for the TkSettingsView."""

    def __init__(self, *args, **kwargs):
        """Bind events to widgets."""
        self.view = TkSettingsView()
        self.view.validate.config(command=self.get_and_destroy)

    def get_and_destroy(self):
        """Get all settings and destroy the window."""
        self.size = self.view.grid_size_scale.get()
        self.phone = self.view.phone.get()
        self.radius = self.view.radius_smooth_scale.get()
        self.res = self.view.water_res_scale.get()
        self.seed = self.view.seed_scale.get()
        self.view.destroy()

    def get(self):
        """Get values set."""
        return (self.size, self.phone, self.radius, self.res, self.seed)


class TkView(tk.Frame):
    """View for the tkinter application."""

    def __init__(self, master, *args, **kwargs):
        """Initialise les widgets sur l'application."""
        super().__init__(master, *args, **kwargs)
        top_frame = tk.Frame(master)
        self.change_grid = tk.Button(top_frame, text="Change grid")
        top_frame.pack(side=tk.TOP, fill=tk.X)
        self.change_grid.pack(side=tk.LEFT)

        self.canvas = tk.Canvas(self, width=512, height=512)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)
        self.settings = tk.Frame(self)
        self.settings.pack(side=tk.TOP, fill=tk.BOTH)

        self.phone_algo = tk.StringVar()
        subframe = tk.Frame(self.settings)
        self.dijkstra = tk.Radiobutton(subframe, text="Dijkstra",
                                       variable=self.phone_algo, value="Dijkstra",
                                       anchor=tk.W)
        self.a_star = tk.Radiobutton(subframe, text="A-star",
                                     variable=self.phone_algo,
                                     value="A-star", anchor=tk.W)

        subframe2 = tk.Frame(self.settings)
        self.phone_dimen = tk.StringVar()
        self.two_d = tk.Radiobutton(subframe2, text="2D",
                                    variable=self.phone_dimen,
                                    value="2D", anchor=tk.W)
        self.three_d = tk.Radiobutton(subframe2, text="3D",
                                      variable=self.phone_dimen,
                                      value="3D", anchor=tk.W)

        self.two_d.pack(side=tk.TOP, fill=tk.X, padx=10)
        self.three_d.pack(side=tk.TOP, fill=tk.X, padx=10)
        self.three_d.invoke()

        label = tk.Label(self.settings, text="Water level :")
        label.pack(side=tk.LEFT, fill=tk.BOTH)
        # self.water = IntVar()
        self.water_sb = tk.Spinbox(self.settings, from_=-1, to=10, increment=1,
                                   width=2, state="readonly")
        self.water_sb.pack(side=tk.LEFT, fill=tk.BOTH, padx=10)

        sep = ttk.Separator(self.settings, orient=tk.VERTICAL)
        sep.pack(side=tk.LEFT, fill=tk.BOTH, padx=10)

        self.dijkstra.pack(side=tk.TOP, fill=tk.X, padx=10)
        self.a_star.pack(side=tk.TOP, fill=tk.X, padx=10)
        subframe.pack(side=tk.LEFT, padx=10)
        subframe2.pack(side=tk.LEFT, padx=10)

        sep = ttk.Separator(self.settings, orient=tk.VERTICAL)
        sep.pack(side=tk.LEFT, fill=tk.BOTH, padx=10)

        self.animate = tk.Button(self.settings, text="Animate")
        self.animate.pack(side=tk.LEFT, fill=tk.BOTH, padx=10)


class AppController():
    """Controller for the tkinter and opengl applications."""

    def __init__(self, master, model, opengl_app):
        """Initialise the viegrid."""
        self.view = TkView(master)
        self.view.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)
        self.grid = model
        self.width = self.view.canvas.winfo_width()
        self.height = self.view.canvas.winfo_height()
        self.view.canvas.bind("<Configure>", self.resize)
        self.view.water_sb.config(command=self.update_grid)
        # dict to store link the ids of rectangles to their coord
        self.dico = {}
        self.create_grid()
        self.opengl = opengl_app
        self.selected = []  # vertex selected in canvas
        self.view.dijkstra.invoke()
        self.view.animate.config(command=self.animate)
        self.view.change_grid.config(command=self.open_settings)
        self.view.three_d.config(command=self.change_dimen)
        self.view.two_d.config(command=self.change_dimen)
        self.view.a_star.config(command=self.change_algorithm)
        self.view.dijkstra.config(command=self.change_algorithm)
        self.master = master
        return

    def change_algorithm(self):
        # update path
        p = self.path
        self.path = self.compute_path()
        print(p == self.path)
        self.draw_path()
        self.opengl.set_path(self.path)
        self.opengl.display_path = True


    def change_dimen(self):
        """Change the dimension in opengl app."""
        if self.view.phone_dimen.get() == "2D":
            self.view.water_sb.insert(0, "-1")
            self.opengl.set_2D()
            self.view.water_sb.config(state="disabled")
        else:
            self.view.water_sb.config(state="readonly")
            assert(self.view.phone_dimen.get() == "3D")
            self.opengl.set_3D()
            self.update_grid()

    def open_settings(self):
        """Create a topleve with all avaible settings."""
        settings = TkSettingsController()
        self.opengl.stop = True
        self.master.wait_window(settings.view)
        size, phone, radius, res, seed = settings.get()
        self.grid = Grid(size, seed)
        if phone == "Tuckey":
            self.grid.tuckey_smooth(radius)
        else:
            assert(phone == "Average")
            self.grid.smooth(radius)
        self.view.canvas.delete("all")
        self.dico = {}  # reset dico
        self.selected = []
        self.create_grid()
        self.opengl.set_water_resolution(res)
        self.opengl.set_grid(self.grid)
        self.opengl.stop = False
        self.opengl.redisplay()


    def animate(self, event=None):
        """Strats the animation in the opengl window."""
        self.opengl.display_path = False
        self.opengl.start_animation()

    def resize(self, event=None):
        """If window size changed adapt the canvas rectangles."""
        width = self.view.canvas.winfo_width()
        height = self.view.canvas.winfo_height()
        self.dico = {}
        if width != self.width or height != self.height:
            self.width, self.height = width, height
            self.view.canvas.delete("all")
            self.create_grid()

    def create_grid(self):
        """Draw the rectangles in the canvas."""
        n = len(self.grid)
        x_step = self.width / n
        y_step = self.height / n
        for i in range(n):
            for j in range(n):
                # draw of main square
                x_0 = i * x_step
                y_0 = j * y_step
                color = self.grid.color(j, i)
                str_col = self.to_hex_rgb(*color)
                rect = self.view.canvas.\
                    create_rectangle(x_0, y_0, x_0 + x_step, y_0 + y_step,
                                     fill=str_col, width=2)  #,tags="main")
                self.dico[rect] = (j, i)
                self.view.canvas.tag_bind(rect, sequence="<ButtonRelease-1>",
                                          func=self.select_square)
        self.view.canvas.addtag_all("all")

    @staticmethod
    def to_hex_rgb(r, g, b) -> str:
        """Return de color in 8bits hexadecimal (str)."""
        color = [r, g, b]
        hex_rgb_list = []
        for x in color:
            hex_x = hex(x)[2:]
            if len(hex_x) == 1:
                hex_x = "0" + hex_x
            hex_rgb_list.append(hex_x)
        return "#" + "".join(hex_rgb_list)

    def draw_path(self):
        """Draw the path with green rectangles."""
        n = len(self.grid)
        x_step = self.width / n
        y_step = self.height / n
        x_small_sq_len = x_step / 3
        y_small_sq_len = y_step / 3
        for j, i in self.path:
            x_0 = i * x_step + x_small_sq_len
            y_0 = j * y_step + y_small_sq_len
            self.view.canvas.create_oval(x_0, y_0, x_0 + x_small_sq_len,
                                         y_0 + y_small_sq_len, fill="red",
                                         width=2, tags="path")

    def select_square(self, event=None):
        """Change square color when a square has been clicked."""
        id_ = self.view.canvas.find_withtag("current")[0]
        self.view.canvas.itemconfigure(id_, fill="purple")
        self.view.canvas.tag_bind(id_, sequence="<ButtonRelease-3>",
                                  func=self.deselect_square)

        self.selected.append(self.dico[id_])

        if len(self.selected) >= 2:
            self.path = self.compute_path()
            self.draw_path()
            self.opengl.set_path(self.path)
            self.opengl.display_path = True
        self.view.water_sb.configure(state=tk.DISABLED)
        self.view.two_d.configure(state=tk.DISABLED)
        self.view.three_d.configure(state=tk.DISABLED)
        self.view.change_grid.configure(state=tk.DISABLED)

    def compute_path(self):
        if self.view.phone_algo.get() == "Dijkstra":
            return self.compute_dijkstra()
        else:
            assert(self.view.phone_algo.get() == "A-star")
            return self.compute_a_star()

    def compute_dijkstra(self):
        """Compute the dijkstra path for self.selected points."""
        path = []
        for i in range(1, len(self.selected)):
            start = self.selected[i - 1]
            target = self.selected[i]
            if len(path) != 0:
                path.pop(-1)  # Eliminate last vertex to avoid repetion
                # last vertex of previous path is the first vertex of next path
            path.extend(dijkstra_matrix_sorted_dict(self.grid, start, target))
        return path

    def compute_a_star(self):
        """Compute the A* path for self.selected points."""
        path = []
        for i in range(1, len(self.selected)):
            start = self.selected[i - 1]
            target = self.selected[i]
            if len(path) != 0:
                path.pop(-1)  # Eliminate last vertex to avoid repetion
                # last vertex of previous path is the first vertex of next path
            path.extend(a_star_matrix_sorted_dict(self.grid, start, target))
        return path

    def deselect_square(self, event=None):
        """Deselect a square and delete it from selected."""
        id_ = self.view.canvas.find_withtag("current")[0]
        self.view.canvas.tag_unbind(id_, sequence="<ButtonRelease-3>")
        self.selected.remove(self.dico[id_])
        color = self.grid.color(*self.dico[id_])
        str_col = self.to_hex_rgb(*color)
        self.view.canvas.itemconfigure(id_, fill=str_col)
        self.view.canvas.delete("path")
        self.view.water_sb.configure(state="disabled")
        self.view.two_d.configure(state=tk.DISABLED)
        self.view.three_d.configure(state=tk.DISABLED)
        if len(self.selected) >= 2:
            self.path = self.compute_path()
            self.draw_path()
        if len(self.selected) == 0:
            self.view.water_sb.configure(state="readonly")
            self.view.two_d.configure(state=tk.ACTIVE)
            self.view.three_d.configure(state=tk.ACTIVE)
            self.view.change_grid.configure(state=tk.ACTIVE)

    def _get_rect_id_in(self, pos):
        for id_, coord in self.dico.items():
            if coord == pos:
                return id_
        raise KeyError("Not found")

    def update_grid(self, event=None):
        """Update colors in grid in relation to water level."""
        assert(len(self.selected) == 0)
        self.view.update_idletasks()
        lvl = int(self.view.water_sb.get())
        self.opengl.set_water_height(lvl)
        for i in range(len(self.grid)):
            for j in range(len(self.grid)):
                y = self.grid.height(j, i)
                id_ = self._get_rect_id_in((j, i))
                if y <= lvl:
                    self.view.canvas.itemconfig(id_, fill="#007577")
                    self.view.canvas.tag_unbind(id_,
                                                "<ButtonRelease-1>")
                    self.grid[j, i] = inf
                else:
                    self.grid[j, i] = self.grid.old(j, i)
                    color = self.grid.color(j, i)
                    str_col = self.to_hex_rgb(*color)
                    self.view.canvas.itemconfig(id_, fill=str_col)
                    self.view.canvas.tag_bind(id_,
                                              "<ButtonRelease-1>",
                                              func=self.select_square)
                                              # func=self.select_square)
