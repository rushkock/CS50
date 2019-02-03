# Ruchella Kock
# 12460796
# This file defines the Items class


class Items(object):
    """
    Representation of an item in Adventure
    """

    def __init__(self, name, description, initial_room_id):
        self.name = name
        self.description = description
        self.initial_room_id = initial_room_id

    def __str__(self):
        return self.name + ": " + self.description