# Ruchella Kock
# 12460796
# This file defines the Inventory class


class Inventory(object):
    """
    Keeping an inventory of items
    """

    def __init__(self):
        self.inventory = []

    def add(self, item):
        """
        Add an item to the inventory (list)
        """
        self.inventory.append(item)

    def remove(self, item):
        """
        Remove an item from the inventory (list)
        """
        self.inventory.remove(item)

    def __str__(self):
        list_of_string_items = []
        for item in self.inventory:
            list_of_string_items.append(str(item))
        return "\n".join(list_of_string_items)

    def find_item(self, item_name):
        """
        Check if item is in inventory and if it is return that item
        """
        for item in self.inventory:
            if item.name == item_name:
                return item

    def is_empty(self):
        """
        Check if the inventory is empty
        """
        return len(self.inventory) == 0