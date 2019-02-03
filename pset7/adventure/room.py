# Ruchella Kock
# 12460796
# This file defines the Route and the Room class


from inventory import Inventory


class Route(object):
    def __init__(self, direction, adjacent_room, conditional_item):
        self.direction = direction
        self.adjacent_room = adjacent_room
        self.conditional_item = conditional_item

    def __str__(self):
        return self.direction + "," + self.adjacent_room


class Room(object):
    """
    Representation of a room in Adventure
    """

    def __init__(self, id, name, description, routes, inventory):
        """
        Initialize a Room
        give it an id, name and description
        """
        self.id = id
        self.name = name
        self.description = description
        self.routes = routes
        self.inventory = inventory

    def valid_move(self, command, players_inventory):
        """
        Check if the move is a valid move
        Check if there is a conditional item required to make the move
        Return the id of the room where the player should move to
        """
        for current_route in self.routes:
            if current_route.direction == command:
                if current_route.conditional_item != "":
                    item_found = players_inventory.find_item(current_route.conditional_item)
                    if item_found != None:
                        return current_route.adjacent_room
                else:
                    return current_route.adjacent_room

    def forced_movement(self):
        """
        Check if there is a forced movement
        Returns a boolean
        """
        for current_route in self.routes:
            return current_route.direction == "FORCED"

    def won(self):
        """
        Check if the game is won
        Returns a boolean
        """
        for current_route in self.routes:
            return current_route.adjacent_room == "0"

    def printing(self, rooms_visited):
        """
        Check if the room has been visited if not then print the description
        If the room has been visited print the name
        """
        if self.id in rooms_visited[:len(rooms_visited) - 1]:
            print(self.name)
            if not self.inventory.is_empty():
                print(self.inventory)
        else:
            self.look()

    def look(self):
        """
        Will always print the description regardless if room has been visited or not
        """
        print(self.description)
        if not self.inventory.is_empty():
            print(self.inventory)