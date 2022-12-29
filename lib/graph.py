# -*- coding: utf-8 -*-


class Graph:

    def __init__(self, order, directed, labels=None):
        self.order = order
        self.directed = directed
        self.adjlists = []
        for _ in range(order):
            self.adjlists.append([])
        self.labels = labels

    def addedge(self, src, dst):
        if src >= self.order or src < 0:
            raise IndexError("Invalid src index")
        if dst >= self.order or dst < 0:
            raise IndexError("Invalid dst index")

        self.adjlists[src].append(dst)
        if not self.directed and dst != src:
            self.adjlists[dst].append(src)


    def addvertex(self, number=1, labels=None):
        self.order += number
        for _ in range(number):
            self.adjlists.append([])
        if labels:
            self.labels.append(labels)


def todot(G):
    link = " -> "
    dot = "digraph {\nrankdir=LR\nnodesep=1;\n"
    for s in range(G.order):
        if G.labels:
            dot += "  " + str(s) + '[label = "' + G.labels[s] + '"]\n'
        else:
            dot += "  " + str(s) + '\n'
        for adj in G.adjlists[s]:
            if G.directed or adj <= s:
                dot += str(s) + link + str(adj) + "\n"

    dot += "}"
    return dot