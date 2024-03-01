// Citation:https://blog.csdn.net/alal001/article/details/131225285
#pragma once
#include "common_func.cpp"

using namespace std;

class Graph
{
private:
    int vertex;    // vertex number
    int **matrix;  // matrix for directed graph
    bool *visited; // store whether the vertex is visited
    int *dist;     // store the weight from the begining
    int *pre;      // store the previous vertex

public:
    const int maxium = 10000; // max, stands for the edge that DNE
    Graph(const int edges, const int nodes, vector<vector<int>> arr)
    {
        vertex = nodes;
        visited = new bool[vertex];
        dist = new int[vertex];
        pre = new int[vertex];
        matrix = new int *[vertex]; // create matrix of directed graph
        for (int i = 0; i < vertex; i++)
        {
            pre[i] = -1;
            dist[i] = maxium;
            visited[i] = false;
            matrix[i] = new int[9];
            for (int j = 0; j < vertex; j++)
            {
                matrix[i][j] = maxium;
            }
        }
        for (int i = 0; i < edges; ++i)
        { // create relation of matrix of directed graph,maxium means doesn't connected
            matrix[arr[i][0]][arr[i][1]] = arr[i][2];
        }
    }

    ~Graph()
    {
        delete[] visited;
        delete[] matrix;
        delete[] pre;
        delete[] dist;
    }
    void dijkstra(int s, int end)
    {
        dist[s] = 0;
        visited[s] = true;
        for (int i = 0; i < vertex; i++)
        { // The distance from the vertex connect with the start vertex
            if (matrix[s][i] < maxium)
            {
                dist[i] = matrix[s][i];
                pre[i] = s;
            }
        }
        int curr = s;
        for (int i = 0; i < vertex; ++i)
        { // start seaching
            int tmp = maxium;
            for (int j = 0; j < vertex; j++)
            { // find the shortest distance from the start vertex, curr
                if (!visited[j] && dist[j] < tmp)
                {
                    tmp = dist[j];
                    curr = j;
                }
            }
            visited[curr] = true; // find curr
            for (int k = 0; k < vertex; ++k)
            {
                int new_dist = maxium; // update weight
                if (!visited[k] && matrix[curr][k] < maxium)
                {
                    new_dist = dist[curr] + matrix[curr][k];
                    if (new_dist < dist[k])
                    {
                        dist[k] = new_dist;
                        pre[k] = curr; // record the previous vertex of the current one
                    }
                }
            }
        }
        show(s, end);
    }

    void show(int start, int end)
    { // show the path
        stack<int> out;
        int n = end;
        while (n != start)
        {
            out.push(n);
            n = pre[n];
        }
        out.push(start);
        vector<int> path;
        while (out.size())
        {
            path.push_back(out.top());
            out.pop();
        }
        for (long long unsigned i = 0; i < path.size(); ++i)
        {
            cout << path[i] << "->";
        }
        cout << endl;
    }
    //end citation
    // int add_vertex(int from[],int to[]){
    //     vertex=vertex+1;
    //     return 0;
    // }
};
