from models import *


# def set_up_room(dungeon: Dungeon, player: Player) -> Room:
#     return Room(dungeon, player)


def resolve_door(dungeon, player) -> bool:
    message = "Draw a card [d] to break down the barrier! "

    if player.hand.skills_contains(Suits.CLUB):
        # TODO: get rid of the used scroll!
        message = "Draw a card [d] or use the 'Open ALL Doors' scroll [s] "

    while dungeon.rooms[-1].event.value > 0:  # as long as the door still has health draw cards
        choice = input(message)

        if choice == "s" and player.hand.skills_contains(Suits.CLUB):
            dungeon.rooms[-1].event.value = 0
            print("The scroll 'Open ALL Doors' worked!")
            return True

        if choice == "d":
            dungeon.rooms[-1].draw_card()
        print(f"You did {dungeon.rooms[-1].room_contents[-1].value} damage to the barrier!")

    print("You've broken through!")
    return True


def resolve_monster(dungeon, player):
    message = "Draw a card [d] to attack the monster! "

    if player.hand.skills_contains(Suits.SPADE):
        message = "Draw a card [d] or use the 'Incinerate' scroll [s] "

    while dungeon.rooms[-1].event.value > 0:  # as long as the monster still has health draw cards
        choice = input(message)

        if choice == "s" and player.hand.skills_contains(Suits.SPADE):
            dungeon.rooms[-1].event.value = 0
            # TODO: get rid of the used scroll!
            print("The scroll 'Incinerate' worked!")
            return True

        if choice == "d":
            dungeon.rooms[-1].draw_card()
            print(dungeon.rooms[-1].room_contents[-1].value)
            if dungeon.rooms[-1].event.value <= 0:
                print("You defeated the monster!")
            else:
                print(f"You did {dungeon.rooms[-1].room_contents[-1].value} damage to the monster!")
                print(f"You've taken {dungeon.rooms[-1].event.value} damage!")
                player.health -= (dungeon.rooms[-1].event.value)
                if player.health < 1:
                    print("You Died!")
                    return False
                print(f"Your health is now {player.health} hit points.")

    return True


def resolve_trap(dungeon, player):
    # print(dungeon.rooms[-1].description)
    message = "Draw a card [d] to disarm the trap! "

    if player.hand.skills_contains(Suits.DIAMOND):
        message = "Draw a card [d] or use the 'Disarm All Traps' scroll [s] "

    choice = input(message)

    if choice == "s" and player.hand.skills_contains(Suits.DIAMOND):
        dungeon.rooms[-1].event.value = 0
        # TODO: get rid of the used scroll!
        print("The scroll 'Disarm All Traps' worked!")
        return True

    if choice == "d":
        dungeon.rooms[-1].draw_card()
        if dungeon.rooms[-1].event.value <= 0:
            if dungeon.rooms[-1].devine_intervention != True:
                print("You've disarmed the trap!")
                return True
            print("The goddess has saved you!")
            return True
        else:
            print(f"You failed to disarm the trap! You took damage! {dungeon.rooms[-1].event.value} damage!")
            player.health -= dungeon.rooms[-1].event.value
            if player.health < 1:
                print("You Died!")
                return False

            return False

    #     # print(dungeon.rooms[-1].event.value, dungeon.rooms[-1].room_contents[-1].value)
    # print(f"Your health is now {player.health}")
    # return False
