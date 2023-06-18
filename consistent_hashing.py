
from bisect import bisect_right, insort


class ConsistentHashing:
    """
    Implements consistent hashing -  
    thanks : https://github.com/wasimusu/distcache/blob/master/distcache/consistent_hashing.py
    """

    def __init__(self, nodes=None, weights=None):
        """
        Initially we will make as may replicas as weight

        :param nodes: list of servers
        :param weights: the servers with higher usable capacity should have weights.
        """
        self.ring = []  # (position, server) in sorted order
        self.occupied = set()
        self.weight = 5
        if nodes and not weights:
            weights = [self.weight] * len(nodes)
        # The user can keep adding servers as the user discovers servers
        if nodes and len(nodes):
            self._generate_ring(nodes, weights)

    def _generate_ring(self, nodes, weights):
        for id, node in enumerate(nodes):
            for i in range(weights[id]):
                key = "{}_{}".format(node, i)
                position = hash(key)
                # If the position already exists hash again.
                while position in self.occupied:
                    key = "{}_{}".format(key, i)
                    position = hash(key)
                self.occupied.add(position)
                insort(self.ring, (position, node))

    def add_node(self, node, weight=5):
        """
        Add node to the HashRing of consistent hashing scheme.

        :param node: new node to be added (ip address in this case)
        :param weight: weight of the new node to be added.
        :return: None
        """
        self._generate_ring([node], [weight])

    def remove_node(self, node):
        """
        Remove node from the ring because it is dead or unavailable.

        :param node: node to be removed from the consistent hashing scheme.
        It will no longer be considered while hashing.

        :return: None
        """
        temp = []
        for position, server in self.ring:
            if server != node:
                temp.append((position, server))
                self.occupied.remove(position)
        self.ring = temp.copy()
        del temp

    def get_node(self, key):
        """
        Get the node/server where the key is or should be.

        :param key: key whose node/server is to be computed.
        :return: node where the key should be stored or retrived from.
        """
        position = bisect_right(self.ring, (hash(key), None))
        if position == len(self.ring):
            position = 0
        return self.ring[position][1]
