# Game crashes if you run out of cards see line 55 of models
# self.room_contents[-1] has "NoneType" and no attribute 'value' --> no card is drawn so room_contents are null?

import models
import engine
# import pygame
import os

# pygame.init()
# bounds = (1024, 768)
# window = pygame.display.set_mode(bounds)
# pygame.display.set_caption("Dungeon Crawl")
os.system('cls' if os.name == 'nt' else 'clear')
player = models.Player("Explorer")
player.direction = "decend into"

print(f"{player.name}, you are about to enter the dungeon!")

dungeon = models.Dungeon()
choice = ""

while player.health > 0:
    if player.direction == "decend into":
        message = f"Do you want to {player.direction} the dungeon [d] or leave [x]?"
        while True:
            choice = input(message)
            if choice == "x":
                player.direction = "ascend from"
                break
            if choice == "d":
                break

    print(f"You {player.direction} the dungeon!")

    dungeon.rooms.append(models.Room(dungeon, player))
    dungeon.rooms[-1].set_up_room()
    outcome: bool = False

    if dungeon.rooms[-1].event.suit == models.Suits.DIAMOND:
        print(f"You come to a {dungeon.rooms[-1].name}.")
        print(dungeon.rooms[-1].description)
        print()
        # print(dungeon.rooms[-1].event.face)
        # print(dungeon.rooms[-1].event.value)
        outcome = engine.resolve_trap(dungeon, player)

    if dungeon.rooms[-1].event.suit == models.Suits.CLUB:
        print(f"You come to a {dungeon.rooms[-1].name}.")
        print(dungeon.rooms[-1].description)
        print()
        # print(dungeon.rooms[-1].event.face)
        # print(dungeon.rooms[-1].event.value)
        outcome = engine.resolve_door(dungeon, player)

    if dungeon.rooms[-1].event.suit == models.Suits.SPADE:
        print(f"You come to a {dungeon.rooms[-1].name}.")
        print(dungeon.rooms[-1].description)
        print()
        # print(dungeon.rooms[-1].event.face)
        # print(dungeon.rooms[-1].event.value)
        outcome = engine.resolve_monster(dungeon, player)

    # process the Room
    if outcome == True:
        dungeon.rooms[-1].process_room(player)
    else:
        print("You didn't gain any treasure from that room!")

    print("-------------------------")
    print(f"Your current health is {player.health} hit points. Remaining torches: {4 - len(player.torches)}")
    player.list_stats()

    print()
    print()

    down, up = dungeon.player_depth(player)  # what level are we at
    print(f"You are at level {down - up} of the dungeon!")

    if (down - up) < 1:
        break

os.system('cls')
if player.health <= 0:
    print("You didn't make it out alive! YOU DIED!")
else:
    print("You escaped the dungeon!")
    print(f"The value of the loot you collected is {player.calculate_treasure()} gold pieces!")
    player.list_stats()

