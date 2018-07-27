#!/usr/bin/python

"""
Simple graph implementation compatible with BokehGraph class.
"""

from collections import namedtuple
Vertex = namedtuple('Vertex', ['label', 'component'])


class Vertex:
    """ Represent a vertex with a label and possible connected component"""
    def __init__(self, label, component=-1):
        self.label = label
        self.component = component


class Graph:
    """Represent a graph as a dictionary of vertices mapping labels to edges."""

    def __init__(self):
      self.vertices = {}
      
    def add_vertex(self,vertex, edges=()):
        """Add a new vertex, optionally with edges to other vertices"""
        if not set(edges).issubset(self.vertices):
            raise Exception('Error: cannot have edge to nonexistent vertices')
        if vertex in self.vertices:
            raise Exception('Error: adding vertext that already exists')
        self.vertices[vertex] = set(edges)
        
    def add_edge(self, start, end, bidirectional=True):
        """ Add a edge (default bidirectional) between two vertices """
        if start not in self.vertices or end not in self.vertices:
            raise Exception('Vertices to connect not in graph!')
        self.vertices[start].add(end)
        if bidirectional:
            self.vertices[end].add(start)

    # def bfs(self, start, target=None):
    #     queue = [start]
    #     visited = set()

    #     while queue:
    #         current = queue.pop(0)
    #         if current == target:
    #             break
    #         visited.add(current)
    #         # add possible (unvisited) vertices to queue
    #         queue.extend(self.vertices[current] - visited)

    #     return visited

    # def dfs(self, start, target=None):
    #     stack = [start]
    #     visited = set()

    #     while stack:
    #         current = stack.pop(0)
    #         if current == target:
    #             break
    #         visited.add(current)
    #         # add possible (unvisited) vertices to queue
    #         stack.extend(self.vertices[current] - visited)

    #     return visited

    def search(self, start, target=None, method='dfs'):
        """ search the graph using BFS or DFS. """
        quack = [start]    # queue or stack, depending on method
        pop_index = 0 if method == 'bfs' else -1
        visited = set()

        while quack:
            current = quack.pop(pop_index)
            if current == target:
                break
            visited.add(current)
            # add possible (unvisited) vertices to queue
            quack.extend(self.vertices[current] - visited)

        return visited

    def find_components(self):
        """ Identify components and update vertex component IDs. """
        visited = set()
        current_component = 0

        for vertex in self.vertices:
            if vertex not in visited:
                reachable = self.search(vertex)
                for other_vertex in reachable:
                    other_vertex.component = current_component
                current_component += 1
                visited.update(reachable)
        self.components = current_component