# Ruchella Kock
# 12460796
# This file defines the Adventure class

from room import Room
from room import Route
from item import Items
from inventory import Inventory
import sys


class Adventure():
    """
    This is your Adventure game class. It should contains
    necessary attributes and methods to setup and play
    Crowther's text based RPG Adventure.
    """

    def __init__(self, game):
        """
        Create rooms and items for the appropriate 'game' version.
        """
        self.items = self.load_items(f"data/{game}Items.txt")
        self.rooms = self.load_rooms(f"data/{game}Rooms.txt")
        self.current_room = self.rooms[0]
        rooms_visited = []
        rooms_visited.append("1")
        self.rooms_visited = rooms_visited
        self.players_inventory = Inventory()

    def load_items(self, filename):
        """
        Load items from filename.
        Returns a collection of item objects.
        """
        # open the right adventure file
        with open(filename, "r") as f:
            list_of_items = []
            # go over the file and make a new_item everytime
            while(True):
                item_name = f.readline().strip()
                # stop if end of file
                if item_name == "":
                    break
                item_description = f.readline().strip()
                initial_room_id = f.readline().strip()
                # this is the empty line
                f.readline()
                new_item = Items(item_name, item_description, initial_room_id)
                list_of_items.append(new_item)
            return list_of_items

    def load_rooms(self, filename):
        """
        Load items from filename.
        Returns a collection of item objects.
        """
        with open(filename, "r") as f:
            list_of_rooms = []
            while(True):
                list_of_routes = []
                id = f.readline().strip()
                # stop if end of file
                if id == "":
                    break
                name = f.readline().strip()
                description = f.readline().strip()
                # read the -----
                f.readline()
                current_route = "initialize"
                # make a route class for every route and add it to a list of routes
                while(current_route != "" and current_route != "\n"):
                    current_route = f.readline().strip()
                    direction = current_route[:current_route.find(" ")]
                    # check if there is a conditional item and make the route accordingly
                    slash = current_route.find("/")
                    if slash != -1:
                        route_id = current_route[current_route.rfind(" ") + 1: slash]
                        conditional_item = current_route[slash + 1:]
                    else:
                        route_id = current_route[current_route.rfind(" ") + 1:]
                        conditional_item = ""
                    new_route = Route(direction, route_id, conditional_item)
                    list_of_routes.append(new_route)
                del list_of_routes[-1]
                # make the room and add it to list of rooms
                room_inventory = Inventory()
                room = Room(id, name, description, list_of_routes, room_inventory)
                for item in self.items:
                    if room.id == item.initial_room_id:
                        room.inventory.add(item)
                list_of_rooms.append(room)

            return list_of_rooms

    def won(self):
        """
        Check if the game is won.
        Returns a boolean.
        """
        return self.current_room.won()

    def move(self, direction):
        """
        Moves to a different room in the specified direction.
        """
        # check if it is a valid move if it is then move to that room
        current_room_id = self.current_room.valid_move(direction, self.players_inventory)
        if current_room_id != None:
            for room in self.rooms:
                if room.id == current_room_id:
                    self.current_room = room
                    self.rooms_visited.append(self.current_room.id)
                    break
        else:
            return False

        # if its a forced movement then print description and move to the room
        if self.current_room.forced_movement() and not self.current_room.won():
            self.current_room.look()
            adventure.move("FORCED")
        return True

    def play(self):
        """
        Play an Adventure game
        """
        print(f"Welcome, to the Adventure games.\n"
              "May the randomly generated numbers be ever in your favour.\n")
        self.current_room.printing(self.rooms_visited)

        # Prompt the user for commands until they've won the game.
        while not self.won():
            command = input("> ")
            command = command.upper()
            dictionary_directions = {"E": "EAST", "EAST": "EAST", "W": "WEST", "WEST": "WEST", "S": "SOUTH", "SOUTH": "SOUTH",
                                     "N": "NORTH", "NORTH": "NORTH", "U": "UP", "UP": "UP", "D": "DOWN", "DOWN": "DOWN",
                                     "IN": "IN", "OUT": "OUT", "WAVE": "WAVE", "XYZZY": "XYZZY", "PLUGH": "PLUGH", "WAVE": "WAVE",
                                     "JUMP": "JUMP", "WATER": "WATER", "SWIM": "SWIM"}
            # Check if the command is a movement or not.
            if command in dictionary_directions:
                # if its a valid move then move to that room
                if adventure.move(dictionary_directions[command]):
                    self.current_room.printing(self.rooms_visited)
                else:
                    self.print_invalid_command()
            # will print the description of the room the player is in
            elif command == "LOOK" or command == "L":
                self.current_room.look()
            # will remind player how to play
            elif command == "HELP" or command == "H":
                print("You can move by typing directions such as EAST/WEST/IN/OUT"
                      "QUIT quits the game.\n"
                      "HELP prints instructions for the game.\n"
                      "INVENTORY lists the item in your inventory.\n"
                      "LOOK lists the complete description of the room and its contents.\n"
                      "TAKE <item> take item from the room.\n"
                      "DROP <item> drop item from your inventory.\n")
            # will show player what is in the inventory
            elif command == "INVENTORY" or command == "I":
                # checks if players's inventory is empty
                if self.players_inventory.is_empty():
                    print("Your inventory is empty.")
                else:
                    print(self.players_inventory)
            # player can take an item and add it to their inventory
            elif command[0:4] == "TAKE":
                command_item = command.split()
                if len(command_item) != 2:
                    self.print_invalid_command()
                else:
                    adventure.take_or_drop(command_item[1], self.players_inventory, self.current_room.inventory, "taken.")
            # player can drop an item and it will go back to the intitial room
            elif command[0:4] == "DROP":
                command_item = command.split()
                if len(command_item) != 2:
                    self.print_invalid_command()
                else:
                    adventure.take_or_drop(command_item[1], self.current_room.inventory, self.players_inventory, "dropped.")
            # with the quit command the program will stop running thus ending the game
            elif command == "QUIT" or command == "Q":
                print("Thanks for playing!")
                sys.exit()
            else:
                self.print_invalid_command()

    def take_or_drop(self, command, destination, origin, string):
        """
        Take an item from the room inventory and add it to the players inventory
        Drop an item from the player inventory and add it to the room_inventory
        """
        # check if the item is in the inventory
        item = origin.find_item(command)
        # if it is then move it from one inventory to the other
        if item != None:
            destination.add(item)
            origin.remove(item)
            print(f"{command} {string}")
        else:
            print("No such item.")

    def print_invalid_command(self):
        print("Invalid command")


if __name__ == "__main__":
    adventure = Adventure("Tiny")

    adventure.play()