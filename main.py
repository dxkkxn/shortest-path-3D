from home import App
from opengl_app import Render3D
from grid import Grid
import threading
import tkinter as tk

if __name__ == "__main__":
    grid_ = Grid(12, 1)
    grid_.tuckey_smooth(2)

    app3D = Render3D()
    app3D.set_grid(grid_)

    root = tk.Tk()
    main = App(master=root, opengl=app3D)
    main.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)
    root.update_idletasks()
    main.create_grid(grid_)

    # # path = dijkstra_matrix_sorted_dict(grid_.grid, (0, 11), (11, 0))
    # app3D.set_path(path)
    # app3D.mainloop()

    x = threading.Thread(target=app3D.mainloop)
    x.start()
    root.mainloop()
