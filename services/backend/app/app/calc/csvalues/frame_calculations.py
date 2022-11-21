""" dit und dat."""
from logging import Logger

import networkx as nx

from . import cs_inertia, cs_torsion


class FrameCalculations:
    """main module."""

    def __init__(self, graph, logger: Logger):
        self.graph = graph
        logger.info(self.graph.nodes())
        self.ordered_cycles = None
        # self.mapping = {val: val.p_id for key, val in self.twod_frame_points.items()}
        # self.vis_graph: nx.DiGraph = nx.relabel_nodes(self.graph, self.mapping)
        self.cs_inertia = None
        self.cs_torsion = None
        self.update(logger)

    def update(self, logger):
        self.update_only_inertia(logger)
        self.cs_torsion = cs_torsion.CrossSectionTorsionValues(self.graph, self.ordered_cycles, self.cs_inertia)

    def update_only_inertia(self, logger):
        self.ordered_cycles = self._get_ordered_cycles()
        for cell in self.ordered_cycles:
            G: nx.Graph = nx.subgraph(self.graph, cell)
            for (u, v) in G.edges():
                # print("in cell", u, v)
                self.graph[u][v]['open'] = 0
        # self.mapping = {val: val.p_id for key, val in self.twod_frame_points.items()}
        # self.vis_graph: nx.DiGraph = nx.relabel_nodes(self.graph, self.mapping)
        self.cs_inertia = cs_inertia.CrossSectionInertiaValues(self.graph, logger)

    @staticmethod
    def _order_nodes_in_cycle(graph, nodes):
        order, = nx.cycle_basis(graph.subgraph(nodes))
        return order

    def _get_ordered_cycles(self):
        cycles = nx.minimum_cycle_basis(self.graph)
        ordered_cycles = [self._order_nodes_in_cycle(self.graph, nodes) for nodes in cycles]
        return ordered_cycles
