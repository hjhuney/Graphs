"""
General drawing methods for graphs using Bokeh.
"""

from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import (GraphRenderer, StaticLayoutProvider, Circle, LabelSet,
                          ColumnDataSource)


class BokehGraph:
    """Class that takes a graph and exposes drawing methods."""
    def __init__(self, graph, title='Graph', width=10, height=10, show_axis=False, show_grid=False, circle_size=35, draw_components=False):
        if not graph.vertices:
            raise Exception('graph should contain vertices!')
        self.graph = graph
        self.width = width
        self.height = height
        self.pos = {}
        # set up plot, canvas space
        self.plot = figure(title=title, x_range=(0, width), y_range=(0, height)
        self.plot.axis.visible = show_axis
        self.plot.grid.visible = show_grid
        self._setup_graph_renderer(circle_size, draw_components)
        self._setup_labels()

    def _setup_graph_renderer(self, circle_size, draw_components=False):
        # render will have actual logic for drawing
        graph_renderer = GraphRenderer()
        # saving vertices in arbitrar but persistent order
        self.vertex_keys = list(self.graph.vertices.keys())

        # add vertex data as instructions for drawing nodes
        graph_renderer.node_renderer.data_source.add(self.vertex_keys, 'index')
        if draw_components:
            # components will be random colors
            graph_renderer.node_renderer_data_source.add(
                self._get_connected_component_colors(), 'color')
        else: 
            # nodes will be random colors
            graph_renderer.node_renderer.data_source.add(
                self._get_random_colors(), 'color')

    def _get_random_colors(self, num_colors=None):
        colors =[]
        num_colors = num_colors or (len(self.graph.vertices))
        for _ in range(num_colors):
            color = '#' + ''.join([choice('0123456789ABCDEF') for j in range(6)])
            colors.append(color)
        return colors

    def _get_edge_indexes(self):
        start_indices = []
        end_indices = []
        checked = set()

        for vertex, edges in self.graph.vertices.items():
            if vertex not in checked:
                for destination in edges:
                    start_indices.append(vertex)
                    end_indices.append(destination)
                checked.add(vertex)

        return dict(start=start_indices, end=end_indices)


    def _setup_labels(self):
        label_data = {'x': [], 'y': [], 'names': []}
        for vertex, position in self.pos.items():
            label_data['x'].append(position[0])
            label_data['y'].append(position[1])
            label_data['names'].append(vertex.label)
        label_source = ColumnDataSource(label_data)
        labels = LabelSet(x='x', y='y', text='names', level='glyph', text_align='center', text_baseline='middle', source=label_source, render_mode='canvas')
        self.plot.add_layout(labels)

    def show(self.output_path='./graph.html'):
        output_file(output_path)
        show(self.plot)

    def randomize(self):
        """ randomize vertex positions """
        for vertex in self.graph.vertices:
            # TODO make boundds and random draws less hacky
            self.pos[vertex] = (1+ random() * (self.width -2), 
            1 + random() * (self.height -2))

    def _color_connected_components(self):
        """ return same colors for vertices in connected components """
        self.graph.find_components()
        component_colors = self._get_random_colors(self.graph.components)
        vertex_colors = []
        for vetex in self.vertex_keys:
            vertex_colors.append(component_colors[vertex.component])
        return vertex_colors