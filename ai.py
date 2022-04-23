from __future__ import absolute_import, division, print_function
import copy, random
from game import Game

MOVES = {0: 'up', 1: 'left', 2: 'down', 3: 'right'}
MAX_PLAYER, CHANCE_PLAYER = 0, 1

# Tree node. To be used to construct a game tree.
class Node:
    # Recommended: do not modify this __init__ function
    def __init__(self, state, player_type):
        self.state = (copy.deepcopy(state[0]), state[1])

        # to store a list of (direction, node) tuples
        self.children = []

        self.player_type = player_type

    # returns whether this is a terminal state (i.e., no children)
    def is_terminal(self):
        return len(self.children) == 0

# AI agent. Determine the next move.
class AI:
    # Recommended: do not modify this __init__ function
    def __init__(self, root_state, search_depth=3):
        self.root = Node(root_state, MAX_PLAYER)
        self.search_depth = search_depth
        self.simulator = Game(*root_state)

    # (Hint) Useful functions:
    # self.simulator.current_state, self.simulator.set_state, self.simulator.move

    # Build a game tree from the current node up to the given depth
    def build_tree(self, node = None, depth = 0):
        # Base case
        if depth == 0:
            return

        # Recursive case - 2 alternatives
        # Max player
        if node.player_type == MAX_PLAYER:
            for move in MOVES.keys():
                # create a child game from the current state and take the move there
                child_game = Game(*node.state)
                moved = child_game.move(move)

                # if not moved: skip this move, will have one less child
                if moved == False:
                    continue

                # create child node and add it to the list of children
                child_node = Node(child_game.current_state(), 1 - node.player_type)
                node.children.append((move, child_node))

                # recursively build subtree
                self.build_tree(child_node, depth - 1)

        # Chance player
        else:
            # create a game starting from the root state...
            root_game = Game(*node.state)

            # ...to get the list of its open tiles
            for open_tile in root_game.get_open_tiles():

                # Copy tile matrix and put a 2-tile on the open tile spot
                child_tile_matrix = copy.deepcopy(node.state[0])
                i = open_tile[0]
                j = open_tile[1]
                child_tile_matrix[i][j] = 2

                # create child node and add it to the list of children
                child_node = Node((child_tile_matrix, node.state[1]), 1 - node.player_type)
                node.children.append((None, child_node))

                # recursively build subtree
                self.build_tree(child_node, depth - 1)


    # Expectimax calculation.
    # Return a (best direction, expectimax value) tuple if node is a MAX_PLAYER
    # Return a (None, expectimax value) tuple if node is a CHANCE_PLAYER
    def expectimax(self, node = None):
        # Base case
        if node.is_terminal():
            score = node.state[1]
            if node.player_type == MAX_PLAYER:
                return random.randint(0,3), score
            else:
                return None, score

        # Recursive case - 2 alternatives
        # compute expectimax on children first
        children_expmax = [(move, self.expectimax(child)) for move, child in node.children]

        # Max player
        if node.player_type == MAX_PLAYER:
            # children_expmax consists of (move, (None, value))
            max_pair = max(children_expmax, key=lambda x: x[1][1])
            return max_pair[0], max_pair[1][1]

        # Chance player
        else:
            # children_expmax consists of (None, (move, value))
            return None, sum(x[1][1] for x in children_expmax) / len(node.children)


    # Return decision at the root
    def compute_decision(self):
        self.build_tree(self.root, self.search_depth)
        direction, _ = self.expectimax(self.root)
        return direction

    # Implement method for extra credits
    # Improved decision computation
    def compute_decision_ec(self):
        self.build_tree(self.root, self.search_depth + 1)
        direction, _ = self.expectimax(self.root)
        return direction
