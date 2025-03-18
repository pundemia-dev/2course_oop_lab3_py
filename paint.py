import customtkinter
from tkinter import Canvas
from math import sqrt


class CCircle:
    def __init__(self, x:int, y:int, canvas):
        self.x = x
        self.y = y
        self.radius = 35
        self.color = "#6B8E23"
        self.selected = False
        self.canvas = canvas
    def checkPoint(self, x:int, y:int)->bool:
        return ((x - self.x)**2 + (y - self.y)**2) <= self.radius**2
    def distPoint(self, x:int, y:int):
        return sqrt((x - self.x)**2 + (y - self.y)**2)
    def select(self):
        self.selected = not(self.selected)
    def unselect(self):
        self.selected = False
    def paint(self):
        x1, y1 = (self.x - self.radius), (self.y - self.radius)
        x2, y2 = (self.x + self.radius), (self.y + self.radius)
        border_color = "#1f6aa5" if self.selected else self.color
        self.canvas.create_oval(x1, y1, x2, y2, 
                                fill=self.color, 
                                width=5, 
                                outline=border_color) #negative
    def selfDestruct(self):
        if self.selected:
            del self
            return True


class Container:
    def __init__(self, canvas):
        self.objects = list()
        self.canvas = canvas
    def newCircle(self, event):
        self.objects.append(CCircle(event.x, event.y, self.canvas))
    def __getattribute__(self, name): # paint
        attr = super().__getattribute__(name)
        if callable(attr):
            def wrapper(*args, **kwargs):
                result = attr(*args, **kwargs)
                self.canvas.delete("all")
                for obj in self.objects:
                    obj.paint()
                return result 
            return wrapper
        return attr     
    def selectObjects(self, event):
        sel_objects = list(filter(lambda p:p.checkPoint(event.x, event.y), self.objects))
        sel_objects.sort(key=lambda p:p.distPoint(event.x, event.y)) #[0]
        for obj in sel_objects:
            obj.select()
    def unselectObjects(self, *args):
        for obj in self.objects:
            obj.unselect()
    def deleteObjects(self, *args):
        self.objects = [obj for obj in self.objects if not obj.selfDestruct()]
            


class Paint(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.default_color = "#6B8E23" #CD5C5C
        self.brush_size = 40
        self.configure(fg_color="#242424")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.canvas = Canvas(self, bg="#242424", highlightbackground = "#242424")
        self.canvas.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.container = Container(self.canvas)
        self.canvas.bind("<Button-1>", self.container.newCircle)
        self.canvas.bind("<Button-3>", self.container.selectObjects)
        self.canvas.bind_all("<Delete>", self.container.deleteObjects)
        self.canvas.bind_all("<BackSpace>", self.container.deleteObjects)
        self.canvas.bind_all("<Escape>", self.container.unselectObjects)
        
        


