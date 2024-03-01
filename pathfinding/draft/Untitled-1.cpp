#include "Graph.cpp"
#include "parse_data.cpp"
#include "common_func.cpp"
int main()
{
    vector<vector<int>> arr;
    arr= {{0,1,8},{0,3,16,},{0,4,7},{1,3,9},{3,1,9},{1,5,5},{2,9,2},
                   {3,2,1},{3,6,10},{3,8,12},{4,7,5},{4,3,9},{4,8,7},{5,3,2},
                   {5,2,11},{6,2,13},{6,9,2},{7,6,8},{8,7,1},{8,6,6}};
    string f = "Map.txt";
    read_graph_from_file(f,arr);
    int edges=20;
    cout<<edges<<endl;
    int nodes=10;
    Graph temp_graph(edges,nodes,arr);
    temp_graph.dijkstra(1,9);
    return 0;
}
