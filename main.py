from RPGObjects import *
import random
import game

app = game.ConsoleRender(width=85, height=21, fps=60)
my_game = game.Game(char='.', width=500, height=300, scene_fix=True)

player = Player(coord=(40, 10))

wallY = 30

my_game.random_filling(proection=",", raito=0.03)
my_game.random_filling(proection=" ^ \n/^\\\n | ", raito=0.01, coliseum=1)

for i in range(0, 497, 3):
    if i == 108:
        continue
    if wallY > 1:
        wallY += random.randint(0, 8) // 8 * random.choice([-1, 1])
    my_game.add_object(Object(coord=(i, wallY), proection="===\n###\n###\n###", coliseum=True))

my_game.add_object(Object(coord=(1, 1), proection="%" * 499, coliseum=True))
my_game.add_object(Object(coord=(1, 2), proection="%\n" * 298, coliseum=True))
my_game.add_object(Object(coord=(1, 299), proection="%" * 499, coliseum=True))
my_game.add_object(Object(coord=(499, 1), proection="%\n" * 298, coliseum=True))

my_game.add_object(player, "hero")

while True:
    app.render(my_game)
