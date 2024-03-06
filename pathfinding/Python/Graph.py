import numpy as np
# Class Map initiate a Map object contains the cost matrix built from parsing a file
# Vertex must be consecutive integers
class Map:
    def __init__(self, file_name):
        MAX = np.inf
        readin = []
        with open(file_name) as f:
            for line in f.readlines():
                temp=(line.strip()).split()
                readin.append(temp)
        edge_num=len(readin)
        temp_list=[]
        for i in range(0, edge_num):
            temp_list.append(readin[i][0])
            temp_list.append(readin[i][1])
        vertex_num=len(set(temp_list))
        self.matrix = [[MAX for x in range(vertex_num)] for y in range(vertex_num)]
        # self.vertex=list(range(1,vertex_num+1))
        self.vertex=[]
        for i in range(vertex_num):
            self.vertex.append(str(i+1))
        for i in range(edge_num):
            self.matrix[int(readin[i][0])-1][int(readin[i][1])-1]=int(readin[i][2])
            self.matrix[int(readin[i][1])-1][int(readin[i][0])-1]=int(readin[i][2])





