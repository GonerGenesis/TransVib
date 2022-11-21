import networkx as nx
import plotly.graph_objects as go

from ...db.models import FramePoint


# from PySide2.QtCore import QPointF


class OmegaPlot:

    def __init__(self, graph: nx.Graph):
        self.x = []
        self.y = []
        self.z = []
        self.i = []
        self.j = []
        self.k = []
        self.omm_max = 0
        vertices = {}
        print('edges', graph.edges().data())
        vertex_count = 0

        for u, v in graph.edges():
            p1: FramePoint = u
            print(p1)
            # p1_obj = p1.toTuple()
            p2: FramePoint = v
            # p2_obj = p2.toTuple()
            omm1 = graph.nodes[u]['omega_m']
            omm2 = graph.nodes[v]['omega_m']
            self.omm_max = max(abs(self.omm_max), abs(omm1), abs(omm2))
            if p1 not in vertices:
                vertices[p1] = len(self.x)
                self.y.append(float(p1.y))
                self.z.append(float(p1.z))
                self.x.append(0)
                # self.intensity.append(0)
                self.y.append(float(p1.y))
                self.z.append(float(p1.z))
                self.x.append(float(omm1))
                # self.intensity.append(float(omm1))
            if p2 not in vertices:
                vertices[p2] = len(self.x)
                self.y.append(float(p2.y))
                self.z.append(float(p2.z))
                self.x.append(0)
                # self.intensity.append(0)
                self.y.append(float(p2.y))
                self.z.append(float(p2.z))
                self.x.append(float(omm2))
                # self.intensity.append(omm2)

            self.i.append(vertices[p1])
            self.j.append(vertices[p2])
            self.k.append(vertices[p1]+1)
            self.i.append(vertices[p1]+1)
            self.j.append(vertices[p2])
            self.k.append(vertices[p2]+1)
        # print(self.x)
        # print(self.y)
        # print(self.z)
        # print(self.i)
        # print(self.j)
        # print(self.k)
        self.omm_max = self.omm_max[0]
        self.fig = go.Figure(data=[
            go.Mesh3d(x=self.x, y=self.y, z=self.z,
                      # alphahull=1,
                      #colorbar_title='z',
                      # color='x',
                      # colorscale=[[0, 'gold'],[0.5*self.omm_max, 'mediumturquoise'], [self.omm_max, 'magenta']],
                      colorscale='icefire',
                      intensity=self.x,
                      i=self.i,
                      j=self.j,
                      k=self.k,
                      #name='y',
                      #showscale=True
                      )]
        )
        print(len(self.x))
        # self.fig.show()
