from room import Room
from player import Player
from world import World

import random
from ast import literal_eval
'''
1. Check the starting node and add its neighbours to the queue.
2. Mark the starting node as explored.
3. Get the first node from the queue / remove it from the queue
4. Check if node has already been visited.
5. If not, go through the neighbours of the node.
6. Add the neighbour nodes to the queue.
7. Mark the node as explored.
8. Loop through steps 3 to 7 until the queue is empty.
'''
'''
if player is in room then turn around leave the room (adding that room to the queue) to explore a new room until player has gone inside every room 
'''
# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


def reverse_directions(direction):
    if direction == "n":
        return "s"
    elif direction == "s":
        return "n"
    elif direction == "w":
        return "e"
    elif direction == "e":
        return "w"

# create queue


class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)

# create stack


class Stack():
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None

    def size(self):
        return len(self.stack)


# hold the graph
graph = {}

# Breadth First Search


def bfs(graph, starting_room):
    # Create an empty Queue
    q = Queue()
    path = []
    # Create an empty visited to store visited rooms
    visited = set()
    # enqueue to the starting_room into the queue
    q.enqueue([starting_room])
    # While the queue is not empty
    while q.size() > 0:
        # Dequeue the first PATH from the front of the array
        path = q.dequeue()
        # Grab the last vertex of the path
        currentRoom = path[-1]
        # if the currentRoom has not been visited
        if currentRoom not in visited:
            # then add current room to visited
            visited.add(currentRoom)
            for room in graph[currentRoom]:
                if graph[currentRoom][room] == "?":
                    return path
            # enqueue each path to each room in the queue
            for exits in graph[currentRoom]:
                path.append(exits)
                next_room = graph[currentRoom][exits]
            # set to path.copy()
                tempPath = path.copy()
                # add to the next room
                tempPath.append(next_room)
                q.enqueue(tempPath)  # add the temp path copy to the queue


# while the graph is smaller
while len(graph) < len(world.rooms):
    currentRoom = player.current_room
    # if the current room is not in graph yet
    if currentRoom not in graph:
        # Add room to graph without exits
        graph[currentRoom] = {}
        for end in player.current_room.get_exits():
            # set to value to ? first time visiting the room
            graph[currentRoom][end] = "?"
    for path in graph[currentRoom]:
        if path not in graph[currentRoom]:
            break
        if graph[currentRoom][path] == "?":
            tempPath = path
            # if theres an exit
            if tempPath is not None:
                # add temp path to trav path, move player to room, set room to player.current
                traversal_path.append(tempPath)
                player.travel(tempPath)
                newRoom = player.current_room
                # if the new room not in our graph yet
                if newRoom not in graph:
                    graph[newRoom] = {}
                    for exiT in player.current_room.get_exits():
                        # update exits key and value
                        graph[player.current_room][exiT] = "?"
            graph[currentRoom][tempPath] = newRoom
            graph[newRoom][reverse_directions(tempPath)] = currentRoom
            currentRoom = newRoom
    # No exits left
    paths = bfs(graph, currentRoom)
    if paths != None:
        # for each room in the paths
        for roomID in paths:
            for room in graph[currentRoom]:
                # if the exit value is the room
                if graph[currentRoom][room] == roomID:
                    # add this exit to our traversal
                    traversal_path.append(room)
                    player.travel(room)
    # reset current room to room we just traveled to
    currentRoom = player.current_room


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

#######
# UNCOMMENT TO WALK AROUND
#######
'''
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
'''
