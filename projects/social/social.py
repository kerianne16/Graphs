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


class User:
    def __init__(self, name):
        self.name = name


class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}  # vertices - indexed by ID
        self.friendships = {}  # edges between users

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}
        # !!!! IMPLEMENT ME

        # Add users
        for i in range(numUsers):
            self.addUser(f"User {i + 1}")

        # Create friendships

        # Generate every possible combination of friendships, shuffle it, then slice off exactly how many friendships we need to generate
        possibleFriendships = []

        # Generate all possible friendship combinations
        for userID in self.users:  # get all the keys in the users dictionary
            for friendID in range(userID + 1, self.lastID + 1):
                possibleFriendships.append((userID, friendID))

        # Shuffle the friendship combinations
        random.shuffle(possibleFriendships)

        # Slice off exactly how many friendships we need to generate
        for friendship_index in range(avgFriendships * numUsers // 2):
            friendship = possibleFriendships[friendship_index]
            self.addFriendship(friendship[0], friendship[1])

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set
        # !!!! IMPLEMENT ME
        # UserID is the starting vertex
        # Friendship node is the target vertex

        # Create an empty queue
        q = Queue()

        # Create an empty visited dictionary to store visited vertices and their paths
        visited = {}  # Note that this is a dictionary, not a set

        # Add a path to the starting vertex to the Queue
        q.enqueue([userID])

        # While the queue is not empty...
        while q.size() > 0:

            path = q.dequeue()

            # Grab the last vertex/friend from the path
            friend = path[-1]

            # if the key is not in the dictinoary already
            if friend not in visited:
                # When we reach an unvisited user, append the path to the visited dictionary
                visited[friend] = path

                for neighbor in self.friendships[friend]:
                    path_copy = path.copy()
                    path_copy.append(neighbor)
                    q.enqueue(path_copy)
        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2)
    print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    print(connections)
