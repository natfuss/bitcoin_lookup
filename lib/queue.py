# -*- coding: utf-8 -*-

from collections import deque

class Queue:
    
    def __init__(self):
        self.elements = deque()

    def enqueue(self, elt):
        self.elements.append(elt)

    def dequeue(self):
        return self.elements.popleft()

    def isempty(self):
        return len(self.elements) == 0
