#!/usr/bin/env python
# coding: utf-8

# [Citation: (modified from the original version)
# -*- coding: utf-8 -*-
# @Time    : 2019/4/11
# @Author  : Zhao huilin
# @FileName: dijkstra.py
# @Software: PyCharm
# @Blog    ：https://me.csdn.net/nominior
import numpy as np
class Dijkstra:
    def __init__(self,matrix,vertexs,src_vertex):
        self.matrix = matrix
        self.vertexs = vertexs
        self.src_vertex = src_vertex
        self.set = self.get_set()
        self.unsearch = self.get_unsearch()
        self.dis = self.get_dis()
        self.path = self.get_path()
        self.point = self.get_point()
 
 
    def get_set(self):
        return [self.src_vertex]
    def get_unsearch(self):
        unsearch = self.vertexs[:]
        unsearch.remove(self.src_vertex)
        return unsearch
    def get_dis(self):
        dis = {}
        vertexs = self.vertexs
        index = vertexs.index(self.src_vertex)
        for i,distance in enumerate(self.matrix[index]):
            dis[vertexs[i]] = distance
        print(dis)
        return dis
    def get_path(self):
        path = {}
        vertexs = self.vertexs
        index = vertexs.index(self.src_vertex)
        for i,distance in enumerate(self.matrix[index]):
            path[vertexs[i]] = []
            if distance != np.inf:
                path[vertexs[i]].append(self.src_vertex)
        return path
 
    def get_point(self):
        return self.src_vertex
 
    def update_point(self,index):
        dis_sort = list(self.dis.values())
        dis_sort.sort()
        point_dis = dis_sort[index]
        for key,distance in self.dis.items():
            if distance == point_dis and key not in self.set:
                self.point = key
                break
            
    def update_dis_path(self):
        new_dis = {}
        index_point = self.vertexs.index(self.point)
        for i,key in enumerate(self.dis.keys()):
            new_dis[key] = self.dis[self.point] + self.matrix[index_point][i]
            if new_dis[key]<self.dis[key]:
                self.dis[key] = new_dis[key]
                # self.path[key] = self.path[self.point].append(self.point)
                self.path[key] =self.path[self.point].copy()
                self.path[key].append(self.point)
 
 
    def find_shortestPath(self,dst_vertex=None,info_show=False):
        count = 1
        if info_show:
            print('*' * 10, 'initialize', '*' * 10)
            self.show()
        while self.unsearch:
            self.update_point(count)
            self.set.append(self.point)
            self.unsearch.remove(self.point)
            self.update_dis_path()
            if info_show:
                print('*' * 10, 'produce', count, '*' * 10)
                self.show()
            count+=1
            if dst_vertex != None and dst_vertex in self.set:
                result = self.path[dst_vertex].copy()
                result.append(dst_vertex)
                return result
        return self.path
 
 
 
    def show(self):
        print('set:',self.set)
        print('unsearch:',self.unsearch)
        print('point:',self.point)
        print('dis:',self.dis.values())
        print('path:',self.path.values())




