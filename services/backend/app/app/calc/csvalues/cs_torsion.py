"""functionality to calc warping torsion"""
from itertools import cycle

import networkx as nx
import numpy as np
from sympy.geometry import Polygon, Point

from .cs_inertia import CrossSectionInertiaValues
from ...db.models import FramePoint


class CrossSectionTorsionValues:
    def __init__(self, graph, cycles, inertia: CrossSectionInertiaValues):
        self.graph: nx.Graph = graph
        self.inertia = inertia
        self.cycles = cycles
        self.cycles_graphs = []
        # self.is_open = np.full_like(self.inertia.length_mat, 1)
        self.coef_mat = np.zeros((len(self.cycles), len(self.cycles)))
        self.a_mat = np.zeros((len(self.cycles), 1))
        self.center_mat = []
        # self.ori_mat = np.zeros((len(self.cycles), 1))
        self._get_cell_matrices()
        self.it = self._get_venant()
        self._get_phi()
        self._get_omega_help()
        self.omega_null = self._get_omega_null()
        self._get_omega_s()
        self._calc_shear_center()
        self._calc_omega_m()
        self._calc_mom_inert_sec()

    def _get_cell_matrices(self):
        # print(len(self.cycles))
        for ii, cell in enumerate(self.cycles):
            # print("cell", cell)
            cycle_graph = nx.DiGraph()
            nx.add_cycle(cycle_graph, cell)
            G = nx.subgraph(self.graph, cell)
            # print(G.edges.data())
            length_mat = np.triu(nx.to_numpy_array(G))
            # print(length_mat)
            thick_mat = np.triu(nx.to_numpy_array(G, weight='thick'))
            shear_flow_mat = np.divide(length_mat, thick_mat, out=np.zeros_like(length_mat), where=thick_mat != 0)
            # print(shear_flow_mat)
            shear_flow = np.sum(shear_flow_mat)
            self.coef_mat[ii][ii] = shear_flow
            points = []
            for node in cell:
                # print("blub", node, self.graph.nodes[node])
                qpoint: FramePoint = node
                p = Point(qpoint.y, qpoint.z)
                # print(type(p))
                points.append(p)
            poly = Polygon(*tuple(points))
            self.a_mat[ii][0] = 2 * poly.area
            # print(poly.area)
            # ori = np.sign(poly.area)
            # print(nx.find_cycle(cycle_graph, list(cycle_graph.nodes)[0], 'reverse'))
            if np.sign(poly.area) == -1:
                print('turn')
                # print(cycle_graph.edges())
                cycle_graph = cycle_graph.reverse(copy=False)
                # print(list(nx.find_cycle(cycle_graph, list(cycle_graph.nodes)[0], 'original')))
                reverse_cycle = [(u, v) for (u, v, d) in
                                 list(nx.find_cycle(cycle_graph, list(cycle_graph.nodes)[0], 'original'))]
                # print(reverse_cycle)
                cycle_graph = nx.DiGraph()
                cycle_graph.add_edges_from(reverse_cycle)
                cycle_graph.graph['reverse'] = True
                # print(cycle_graph.edges())
                # print(nx.find_cycle(cycle_graph, list(cycle_graph.nodes)[0], 'reverse'))
            # cycle_graph.graph['ori'] = self.ori_mat[ii][0]
            self.center_mat.append(poly.centroid)
            # self.ori_mat = np.sign(self.a_mat)
            self.a_mat = np.absolute(self.a_mat)
            # print(float(poly.area))
            # hull = ConvexHull(points)
            # print(float(hull.area))
            self.cycles_graphs.append(cycle_graph)
            for jj, next_cell in enumerate(self.cycles):
                shear_flow_minus = 0
                if next_cell != cell:
                    H = nx.subgraph(self.graph, next_cell)
                    R = G.copy()
                    R.remove_nodes_from(n for n in G if n not in H)
                    length_mat = np.triu(nx.to_numpy_array(R))
                    thick_mat = np.triu(nx.to_numpy_array(R, weight='thick'))
                    shear_flow_mat = np.divide(length_mat, thick_mat, out=np.zeros_like(length_mat),
                                               where=thick_mat != 0)
                    shear_flow_minus -= np.sum(shear_flow_mat)
                    # print(R.edges())
                    self.coef_mat[ii][jj] = shear_flow_minus
                    # print(shear_flow_minus)
        # self.phi_mat = self.ori_mat * np.linalg.solve(self.coef_mat, self.a_mat)
        self.phi_mat = np.linalg.solve(self.coef_mat, self.a_mat)
        # print(self.ori_mat)
        print(self.coef_mat)
        print(self.a_mat)
        print(self.phi_mat)

    def _get_venant(self):
        it = 0
        # for ii, [arr] in enumerate(self.a_mat):
        #     it += self.a_mat[ii][0] * self.phi_mat[ii][0]
        it += np.sum(self.a_mat * self.phi_mat)
        print("it_1", it)
        print(self.inertia.length_mat, self.inertia.thick_mat, self.inertia.open_mat)
        it += np.sum(np.multiply(np.multiply(self.inertia.length_mat, self.inertia.open_mat), np.power(self.inertia.thick_mat, 3))) / 3
        print("it_2", it)
        return it

    def _get_phi(self):
        # fi_cells = np.zeros_like(self.cycles)
        # print(fi_cells)
        # print(self.cycles)
        cell_graph: nx.DiGraph
        for ii, cell_graph in enumerate(self.cycles_graphs):
            # print(cell_graph.edges())
            # G: nx.Graph = nx.subgraph(self.graph, cell)
            for edge in cell_graph.edges:
                u, v = edge
                # phi = 0
                # if 'phi' in G[u][v]:
                #     phi = G[u][v]['phi']
                # cell_graph[u][v]['phi'] = self.ori_mat[ii]*self.phi_mat[ii]
                cell_graph[u][v]['phi'] = - self.phi_mat[ii]
                # print(cell_graph[u][v]['phi'])
            for jj, next_cell in enumerate(self.cycles_graphs):
                if next_cell != cell_graph:
                    R: nx.DiGraph = cell_graph.copy()
                    R.remove_nodes_from(n for n in cell_graph if n not in next_cell)
                    # print(R.edges())
                    for u, v in R.edges():
                        # print(cell_graph.edges(u))
                        phi = cell_graph[u][v]['phi']
                        # cell_graph[u][v]['phi'] = phi - self.ori_mat[jj]*self.phi_mat[jj]
                        cell_graph[u][v]['phi'] = phi + self.phi_mat[jj]

            # if cell_graph.to_undirected().has_edge('4', '69'):
            # print(cell_graph.edges('4'))
            # print(cell_graph.edges.data('phi'))
        # print(self.graph['67']['37'].get('phi'))

    def _get_omega_help(self):
        cell_graph: nx.DiGraph
        g = self.graph
        start_at = list(g.nodes())[0]
        g.nodes[start_at]['omega_h'] = 0
        open_segs: nx.Graph = g.copy()
        # cycles = self.cycles_graphs.copy()
        while len(self.cycles_graphs) > 0:
            # cy_cycle = cycle(self.cycles_graphs)
            cy_iter = iter(self.cycles_graphs)
            # start_node = None
            cell_graph = next(cy_iter)
            while True:
                start_node = self.check_omega(cell_graph)
                if start_node:
                    # print(start_node)
                    break
                cell_graph = next(cy_iter)
            print(cell_graph.edges())
            cy_cycle = cycle(cell_graph.edges())

            u, v = next(cy_cycle)
            # print(u, v)
            while u != start_node[0]:
                u, v = next(cy_cycle)
                # print(u, v)
            while v != start_node[0]:
                if open_segs.has_edge(u, v):
                    open_segs.remove_edge(u, v)
                length = g[u][v]['weight']
                # print(length)
                thick = g[u][v]['thick']
                # seg: QLineF = G[u][v]['edge']
                # print(G.nodes[u])
                # p1: QPointF = g.nodes[u]['point']
                # p2: QPointF = g.nodes[v]['point']
                # omeg = p1.x() * (p2.y() - p1.y()) - p1.y() * (p2.x() - p1.x())
                omeg = self.calc_omeg(u, v)
                # phi = 0
                # if 'phi' in G[u][v]:
                phi = cell_graph[u][v]['phi']
                # print(int(u)+1, int(v)+1, omeg, phi, thick, length)
                # print(length)
                if 'omega_h' in g.nodes[v]:
                    u, v = next(cy_cycle)
                    continue
                g.nodes[v]['omega_h'] = g.nodes[u]['omega_h'] + omeg + phi / thick * length
                #print(v, g.nodes[v]['omega_h'])
                u, v = next(cy_cycle)
            if open_segs.has_edge(u, v):
                open_segs.remove_edge(u, v)
            self.cycles_graphs.remove(cell_graph)
        print(open_segs.edges())
        for u, v in open_segs.edges():
            # p1: QPointF = g.nodes[u]['point']
            # p2: QPointF = g.nodes[v]['point']
            # omeg = p1.x() * (p2.y() - p1.y()) - p1.y() * (p2.x() - p1.x())
            omeg = self.calc_omeg(u, v)
            omega_h = g.nodes[u]['omega_h']
            g.nodes[v]['omega_h'] = omega_h + omeg
        # print(open_segs.edges())
        print(g.nodes.data('omega_h'))

    def calc_omeg(self, u, v):
        """
        calculates the omega term for the given segment

        Parameters
        ----------
        u
        v

        Returns
        -------
        omeg
        """
        p1: FramePoint = u
        p2: FramePoint = v
        omeg = p1.y * (p2.z - p1.z) - p1.z * (p2.y - p1.y)
        # print("omeg", omeg)
        return omeg

    def check_omega(self, g: nx.Graph):
        # print(g.nodes())
        # check = None
        check = [node for node in g.nodes() if 'omega_h' in self.graph.nodes[node]]
        # print(check)
        return check

    def _get_omega_null(self):
        g = self.graph
        aw = 0
        for u, v in g.edges():
            aw_edge = g[u][v]['thick'] * g[u][v]['weight'] * (g.nodes[v]['omega_h'] + g.nodes[u]['omega_h']) / 2
            # print(int(u) + 1, int(v) + 1, g[u][v]['thick'], g[u][v]['weight'], g.nodes[u]['omega_h'],
            #       g.nodes[v]['omega_h'], aw_edge)
            aw += aw_edge
        omega_null = - aw / self.inertia.a_vals.a
        print("omega_null: ", omega_null)
        return omega_null

    def _get_omega_s(self):
        g = self.graph
        for u in g.nodes():
            p1: FramePoint = u
            g.nodes[u]['omega_s'] = self.omega_null + float(p1.y) * self.inertia.a_vals.z_s - \
                float(p1.z) * self.inertia.a_vals.y_s + g.nodes[u]['omega_h']
        for u, v, wt in g.edges.data():
            g[u][v]['oms1'] = g.nodes[u]['omega_s'][0]
            g[u][v]['oms2'] = g.nodes[v]['omega_s'][0]
        print(g.edges.data('oms1'))
        print(g.edges.data('oms2'))
        self.oms1_mat = np.triu(nx.to_numpy_array(self.graph, weight='oms1'))
        self.oms2_mat = np.triu(nx.to_numpy_array(self.graph, weight='oms2'))
        # print(g.nodes.data('omega_s'))

    def _calc_shear_center(self):
        # graph = self.graph
        inertia = self.inertia
        a_vals = inertia.a_vals
        # for u, v, wt in graph.edges.data():
        #    length = wt['weight']
        #    thick = wt['thick']
        #    ayw += 1/6 * length * thick
        ayw = np.sum(1 / 6 * inertia.a_mat * (
                inertia.y1_mat * (2 * self.oms1_mat + self.oms2_mat) + inertia.y2_mat * (
                    self.oms1_mat + 2 * self.oms2_mat)))
        azw = np.sum(1 / 6 * inertia.a_mat * (
                inertia.z1_mat * (2 * self.oms1_mat + self.oms2_mat) + inertia.z2_mat * (
                    self.oms1_mat + 2 * self.oms2_mat)))
        self.y_m_s = -(a_vals.ayzs * ayw - a_vals.ayys * azw) / (a_vals.azzs * a_vals.ayys - a_vals.ayzs ** 2)
        self.z_m_s = (-a_vals.azzs * ayw + a_vals.ayzs * azw) / (a_vals.azzs * a_vals.ayys - a_vals.ayzs ** 2)

        self.y_m = self.y_m_s + inertia.a_vals.y_s
        self.z_m = self.z_m_s + inertia.a_vals.z_s
        print(ayw, self.y_m_s, self.z_m_s, self.y_m, self.z_m)

    def _calc_omega_m(self):
        g = self.graph
        a_vals = self.inertia.a_vals
        for u in g.nodes():
            p1: FramePoint = u
            g.nodes[u]['omega_m'] = g.nodes[u]['omega_s'] + (float(p1.y) - a_vals.y_s) * self.z_m_s \
                - (float(p1.z) - a_vals.z_s) * self.y_m_s
        for u, v, wt in g.edges.data():
            g[u][v]['omm1'] = g.nodes[u]['omega_m'][0]
            g[u][v]['omm2'] = g.nodes[v]['omega_m'][0]
        self.omm1_mat = np.triu(nx.to_numpy_array(self.graph, weight='omm1'))
        self.omm2_mat = np.triu(nx.to_numpy_array(self.graph, weight='omm2'))
        # print(g.nodes.data('omega_m'))

    def _calc_mom_inert_sec(self):
        self.awwm = np.sum(
            1 / 3 * self.inertia.a_mat * (self.omm1_mat ** 2 + self.omm2_mat ** 2 + self.omm2_mat * self.omm1_mat))
        print(self.awwm)
