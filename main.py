from tkinter_app import AppController
from opengl_app import Render3D
from grid import Grid
import threading
import tkinter as tk

if __name__ == "__main__":
    grid = Grid(size=15, seed=1)
    grid.tuckey_smooth(radius=1)
    app3D = Render3D(grid=grid, water_res=16)
    root = tk.Tk()
    app_tk = AppController(master=root, model=grid, opengl_app=app3D)
    x = threading.Thread(target=app3D.mainloop)
    x.start()
    root.mainloop()
