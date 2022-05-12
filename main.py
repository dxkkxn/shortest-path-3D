from home import AppController
from opengl_app import Render3D
from grid import Grid
import threading
import tkinter as tk

if __name__ == "__main__":
    grid = Grid(24, 1)
    grid.tuckey_smooth(1)
    app3D = Render3D(grid=grid, water_res=10)
    root = tk.Tk()
    app_tk = AppController(master=root, model=grid, opengl_app=app3D)
    # , opengl=app3D)
    # main.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)
    # main.create_grid(grid_)

    # path = dijkstra_matrix_sorted_dict(grid_.grid, (0, 11), (11, 0))
    # app3D.set_path(path)
    # app3D.mainloop()

    x = threading.Thread(target=app3D.mainloop)
    x.start()
    root.mainloop()
