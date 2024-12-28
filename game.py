import win32console
import RPGObjects
import win32con
import time
import msvcrt
import random

class Game:
    def __init__(self, char, width=120, height=30, pos=[0, 0], scene_fix=False):
        self.width = width
        self.height = height
        self.char = char
        self.pos = pos
        self.scene_fix = scene_fix
        self.player = None
        self.objects = dict()
        self.other_objects = []
        self.coliseum = []
        self.scene = [[char for j in range(width)] for i in range(height)]

    def set_char(self, char):
        self.char = char
        self.scene = [[char for j in range(self.width)] for i in range(self.height)]

    def add_object(self, obj, name=None):

        if name not in self.objects.keys():
            self.objects[name] = obj

            if type(obj) == RPGObjects.Player and self.player is None:
                self.player = name

        elif name is None:
            self.other_objects.append(obj)
        else:
            raise Exception(f"name \"{name}\" already exists")

    def redraw(self, key, w, h):
        if self.player and self.scene_fix:
            self._move_pos(w, h)

        self.set_char(self.char)
        self.coliseum = []
        
        for obj in list(self.objects.values()) + self.other_objects:
            
            if obj.coliseum:
                self.coliseum += obj.get_coliseum()

        for obj in self.other_objects + list(self.objects.values()):

            if obj.request_move(key):
                coord = obj.request_move(key)
                if coord not in self.coliseum:
                    obj.set_coord(coord)

            self._draw_object(obj)

    def _draw_object(self, obj):
        matrix = obj.matrix
        for iInd, i in enumerate(matrix):
            for jInd, j in enumerate(i):
                if j !=" ":
                    self.scene[iInd + obj.coord[1]][jInd + obj.coord[0]] = j

    def move_object(self, name, coord=None, proection=None):
        if coord is not None:
            self.objects[name].set_coord(coord)

        if proection is not None:
            self.objects[name].set_proection(proection)

    def _move_pos(self, width, height):
        if self.objects[self.player].coord[0] - self.pos[0] < width // 4:
            self.pos[0] -= (width // 4) - (self.objects[self.player].coord[0] - self.pos[0])
        if self.objects[self.player].coord[0] - self.pos[0] > (width * 3) // 4:
            self.pos[0] += (self.objects[self.player].coord[0] - self.pos[0]) - ((width * 3) // 4)
        if self.objects[self.player].coord[1] - self.pos[1] < height // 4:
            self.pos[1] -= (height // 4) - (self.objects[self.player].coord[1] - self.pos[1])
        if self.objects[self.player].coord[1] - self.pos[1] > (height * 3) // 4:
            self.pos[1] += (self.objects[self.player].coord[1] - self.pos[1]) - ((height * 3) // 4)
        
    def random_filling(self, proection, raito, coliseum=False):
        for i in range(int(self.width * self.height * raito)):
            self.add_object(RPGObjects.Object(coord=(random.randint(1, self.width - 1 - len(max(proection.split("\n")))),
                                                     random.randint(1, self.height - 1 - len(proection.split("\n")))),
                                              proection=proection,
                                              coliseum=coliseum))

class ConsoleRender:
    def __init__(self, fps=60, width=120, height=30):
        self.console = win32console.CreateConsoleScreenBuffer(
            DesiredAccess=win32con.GENERIC_READ | win32con.GENERIC_WRITE,
            ShareMode=0,
            SecurityAttributes=None,
            Flags=0
        )
        self.console.SetConsoleActiveScreenBuffer()
        self.console.SetConsoleCursorInfo(Size=1, Visible=False)
        self.fps = fps
        self.width = width
        self.height = height

    def render(self, scene):
        key = self.read_input()
        scene.redraw(key, self.width, self.height)
        matrix = scene.scene
        
        output = ""

        for lineInd in range(scene.pos[1], scene.pos[1] + self.height):
            for columnInd in range(scene.pos[0], scene.pos[0] + self.width):
                if 0 < lineInd < scene.height and 0 < columnInd < scene.width: 
                    output += matrix[lineInd][columnInd]
                else:
                    output += " "

        self.console.WriteConsoleOutputCharacter(Characters=output, WriteCoord=win32console.PyCOORDType(0, 0))

        time.sleep(1/ self.fps)

        if key == 'q':
            exit()

    def read_input(self):
        event = msvcrt.kbhit()
        if event:
            key = chr(ord(msvcrt.getch()))
            return key
        return None
