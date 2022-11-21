"""Storing and Calculation of cross sectional values"""

# from mpmath import *
import math
from logging import Logger

import networkx as nx
import numpy as np
from sympy import pi, Point2D, Segment2D

from ...db.models import FramePoint


class AVals:
    # noinspection PyTypedDict,PyTypeChecker
    def __init__(self):
        self.a: float = None
        self.aqy: float = None
        self.aqz: float = None
        self.ay: float = None
        self.az: float = None
        self.ayy: float = None
        self.ayys: float = None
        self.azz: float = None
        self.azzs: float = None
        self.ayz: float = None
        self.ayzs: float = None
        self.y_s: float = None
        self.z_s: float = None


class MainAxisVals:
    # noinspection PyTypedDict,PyTypeChecker
    def __init__(self):
        self.phi: float = None
        self.I1: float = None
        self.I2: float = None
        self.i1: float = None
        self.i2: float = None


class CrossSectionInertiaValues:
    """Storing and Calculation of cross-sectional values"""

    def __init__(self, graph: nx.Graph, logger: Logger):
        self.num_zero = 1e-6
        self.graph = graph
        self.a_vals = AVals()
        self.main_axis_vals = MainAxisVals()
        self.length_mat = None
        self.thick_mat = None
        self.open_mat = None
        self.a_mat = None
        self.cos_mat = None
        self.sin_mat = None
        self.aqy_mat = None
        self.aqz_mat = None
        self.y_mat = None
        self.ay_mat = None
        self.y1_mat = None
        self.y2_mat = None
        self.z1_mat = None
        self.z2_mat = None
        self.ayy_mat = None
        self.z_mat = None
        self.az_mat = None
        self.azz_mat = None
        self.ayz_mat = None

        self._process_segments(logger)
        self.calc_moments()
        # print('avals', vars(self.a_vals))
        self.calc_main_axis()
        print('avals', vars(self.a_vals))

        # self.mid_points = []
        # for k, v in self.a_vals.items():
        #     print(k, v)
        # for k, v in self.main_axis_vals.items():
        #     print(k, v)
        # self._segments_mat = nx.to_numpy_array(self.graph, weight='segment')

    def _process_segments(self, logger: Logger):
        # y_axis = Ray2D(Point2D(0, 0), angle=0)
        u: FramePoint
        v: FramePoint
        logger.info(self.graph.edges.data())
        for (u, v, wt) in self.graph.edges.data():
            # seg: QLineF = wt['edge']
            print(wt)
            # p1: FramePoint = self.graph.nodes[u]
            # p2: FramePoint = self.graph.nodes[v]
            x1: float = u.y
            x2: float = v.y
            y1: float = u.z
            y2: float = v.z
            print(x1, y1, x2, y2)
            p1 = Point2D(x1, y1)
            p2 = Point2D(x2, y2)
            seg = Segment2D(p1, p2)
            # p1.distance(p2)
            # length = p1.distance(p2)
            length = seg.length
            midpoint: Point2D = seg.midpoint
            print(length)
            self.graph[u][v]['weight'] = length
            self.graph[u][v]['y'] = midpoint.x
            self.graph[u][v]['z'] = midpoint.y
            # length: float = float(wt['weight'])
            # print("bla", x1, type(x1))
            self.graph[u][v]['y1'] = x1
            self.graph[u][v]['y2'] = x2
            self.graph[u][v]['z1'] = y1
            self.graph[u][v]['z2'] = y2
            self.graph[u][v]['cos'] = (x2 - x1) / length
            # print("cos", x1,x2,length,(x1 - x2) / length)
            # self.graph[u][v]['sin'] = abs(sin(float(angle)))
            self.graph[u][v]['sin'] = (y2 - y1) / length
            if 'open' not in wt:
                print(u, v, "open")
                self.graph[u][v]['open'] = 1

    def calc_moments(self):
        self.length_mat = np.triu(nx.to_numpy_array(self.graph))
        self.thick_mat = np.triu(nx.to_numpy_array(self.graph, weight='thick'))
        self.open_mat = np.triu(nx.to_numpy_array(self.graph, weight='open'))
        self.a_mat = self.length_mat * self.thick_mat
        self.a_vals.a = np.sum(self.a_mat)
        self.cos_mat = np.triu(nx.to_numpy_array(self.graph, weight='cos'))
        self.sin_mat = np.triu(nx.to_numpy_array(self.graph, weight='sin'))
        self.aqy_mat = self.a_mat * abs(self.cos_mat)
        self.a_vals.aqy = np.sum(self.aqy_mat)
        self.aqz_mat = self.a_mat * abs(self.sin_mat)
        self.a_vals.aqz = np.sum(self.aqz_mat)
        self.y_mat = np.triu(nx.to_numpy_array(self.graph, weight='y'))
        self.ay_mat = self.a_mat * self.y_mat
        self.a_vals.ay = np.sum(self.ay_mat)
        self.y1_mat = np.triu(nx.to_numpy_array(self.graph, weight='y1'))
        self.y2_mat = np.triu(nx.to_numpy_array(self.graph, weight='y2'))
        self.z1_mat = np.triu(nx.to_numpy_array(self.graph, weight='z1'))
        self.z2_mat = np.triu(nx.to_numpy_array(self.graph, weight='z2'))
        self.ayy_mat = self.a_mat * (self.y1_mat ** 2 + self.y2_mat ** 2 + self.y1_mat * self.y2_mat) / 3
        self.a_vals.ayy = np.sum(self.ayy_mat)
        self.z_mat = np.triu(nx.to_numpy_array(self.graph, weight='z'))
        self.az_mat = self.a_mat * self.z_mat
        self.a_vals.az = np.sum(self.az_mat)
        self.azz_mat = self.a_mat * (self.z1_mat ** 2 + self.z2_mat ** 2 + self.z1_mat * self.z2_mat) / 3
        self.a_vals.azz = np.sum(self.azz_mat)
        self.ayz_mat = self.a_mat * (self.y1_mat * self.z1_mat
                                     + self.length_mat / 2 * (self.z1_mat * self.cos_mat + self.y1_mat * self.sin_mat)
                                     + (self.length_mat ** 2) / 3 * self.cos_mat * self.sin_mat)
        self.a_vals.ayz = np.sum(self.ayz_mat)
        self.a_vals.y_s = self.a_vals.ay / self.a_vals.a
        self.a_vals.z_s = self.a_vals.az / self.a_vals.a
        self.a_vals.ayys = self.a_vals.ayy - self.a_vals.y_s ** 2 * self.a_vals.a
        self.a_vals.azzs = self.a_vals.azz - self.a_vals.z_s ** 2 * self.a_vals.a
        self.a_vals.ayzs = self.a_vals.ayz - self.a_vals.z_s * self.a_vals.y_s * self.a_vals.a

    def calc_main_axis(self):
        if self.a_vals.ayz < self.num_zero:
            self.main_axis_vals.phi = 0
            self.main_axis_vals.I1 = self.a_vals.ayys
            self.main_axis_vals.I2 = self.a_vals.azzs
            self.main_axis_vals.i1 = math.sqrt(self.a_vals.ayys / self.a_vals.a)
            self.main_axis_vals.i2 = math.sqrt(self.a_vals.azzs / self.a_vals.a)
        else:
            phi_sector = 0
            sector = 0
            check_phi = abs((self.a_vals.ayys - self.a_vals.azzs) / (2 * self.a_vals.ayzs))
            if check_phi > 0:
                sector = 1
            elif check_phi < self.num_zero:
                sector = 0
            elif check_phi < 0:
                sector = -1
            check_phi_1 = abs(self.a_vals.ayys - self.a_vals.azzs)
            if check_phi_1 < self.num_zero < abs(self.a_vals.ayzs):
                phi_sector = pi / 4
            elif 2 * abs(self.a_vals.ayzs) >= check_phi_1:
                phi_sector = 1 / 2 * (sector * (pi / 2) - math.atan(
                    (self.a_vals.ayys - self.a_vals.azzs) / (2 * self.a_vals.ayzs)))
            elif 2 * abs(self.a_vals.ayzs) < check_phi_1:
                phi_sector = 1 / 2 * math.atan((2 * self.a_vals.ayzs) / (self.a_vals.ayys - self.a_vals.azzs))
            self.main_axis_vals.phi = phi_sector
            self.main_axis_vals.I1 = (1 / 2 * (self.a_vals.ayys + self.a_vals.azzs) + 1 / 2 * math.sqrt(
                (self.a_vals.ayys - self.a_vals.azzs) ** 2 + 4 * self.a_vals.ayzs ** 2)
                                      )
            self.main_axis_vals.I2 = (1 / 2 * (self.a_vals.ayys + self.a_vals.azzs) - 1 / 2 * math.sqrt(
                (self.a_vals.ayys - self.a_vals.azzs) ** 2 + 4 * self.a_vals.ayzs ** 2)
                                      )
            self.main_axis_vals.i1 = math.sqrt(self.main_axis_vals.I1 / self.a_vals.a)
            self.main_axis_vals.i2 = math.sqrt(self.main_axis_vals.I2 / self.a_vals.a)
