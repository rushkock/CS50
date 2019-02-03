from room import Room
from room import Route
from items import Inventory
from items import Items
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
        #self.current_room = self.rooms[0]
        rooms_visited = []
        self.rooms_visited = rooms_visited
        #self.players_inventory = Inventory()

    def load_rooms(self, filename):
        """
        Load rooms from filename.
        Returns a collection of Room objects.
        """
        with open(filename, "r") as f:
            # read text file and put it in list seperated by line
            lines = f.read().splitlines()
            # add a new empty space in order to find the last room
            lines.append("")
           # this function will make one room
            def make_room(lines):
                # make a list of all the routes
                list_of_routes = []
                routes = lines[lines.index("-----") + 1: lines.index("")]
                for current_route in routes:
                    make_route = route(current_route)
                    list_of_routes.append(make_route)

                # make the room
                id, name, description = lines[0], lines[1], lines[2]
                room_inventory = Inventory()
                new_room = Room(id, name, description, list_of_routes, room_inventory)
                return new_room
            #lines = ["1", "room1", "hello", "-----", "WEST   2", "", "2", "room2", "description", "-----", "NORTH  1", ""]

            # this function will make one route with a direction and an id
            def route(line):
                direction = line[:line.find(" ")]
                id = line[line.rfind(" ") + 1: line.rfind(" ") + 2]
                conditional_item = line[line.rfind(" ") + 3:]
                new_route = Route(direction, id, conditional_item)
                #print (new_route)
                return new_route

            current, i = 0, 0
            list_of_rooms = []
            # make all the rooms by calling the make room function for every room
            for x in range(lines.count("")):
                index = 0
                # make a list with the places where the empty lines are
                end_of_room = []
                for each_line in lines:
                    if each_line == "":
                        end_of_room.append(index)
                    index = index + 1
                # seperate the lines list per room
                room = lines[current: end_of_room[i] + 1]
                current = end_of_room[i] + 1
                i = i + 1

                # call the make_room function for every room
                blah = make_room(room)
                list_of_rooms.append(blah)
            # for item in self.items:
            #     for room in list_of_rooms:
            #         if room.id == item.initial_room_id:
            #             room.inventory.add(item)
            #             #print(room)
            return list_of_rooms


    def load_items(self, filename):
        """
        Load items from filename.
        Returns a collection of item objects.
        """
        with open(filename, "r") as f:
            items_lines = f.read().splitlines()
            items_lines.append("")
            #print(items_lines)
            #this function will make one item
            def make_item(items_lines):
                new_item = Items(items_lines[0], items_lines[1], items_lines[2])
                return new_item

            current_pos, j = 0, 0
            list_of_items = []
            # make all the rooms by calling the make room function for every room
            for y in range(items_lines.count("")):
                items_index = 0
                # make a list with the places where the empty lines are
                end_of_items = []
                for each_item_line in items_lines:
                    if each_item_line == "":
                        end_of_items.append(items_index)
                    items_index = items_index + 1
                # seperate the lines list per room
                items = items_lines[current_pos: end_of_items[j] + 1]
                current_pos = end_of_items[j] + 1
                j = j + 1

                # call the make_item function for every room
                list_of_items.append(make_item(items))
                #print(make_item(items))
            return list_of_items



if __name__ == "__main__":
    adventure = Adventure("Tiny")