#pragma once
#include "Graph.cpp"
#include "return_values.h"
int readin_graph(ifstream &f, vector<vector<int>> &arr)
{
    string line;
    int temp_i = 0;
    int temp_j = 0;
    int weight = 0;
    vector<int> temp = {0, 0, 0};
    int count = 0;
    if (getline(f, line))
    {
        istringstream iss(line);
        if (iss >> temp_i >> temp_j >> weight)
        {
            temp = {temp_i, temp_j, weight};
            arr.push_back(temp);
            count++;
            return parse_data_success;
        }
        else
        {
            return parse_data_fail;
        }
    }
    else
    {
        return parse_data_end_of_file;
    }
}

int read_graph_from_file(string &f,vector<vector<int>> &arr){
    ifstream ifs;
    ifs.open(f);
    if (ifs.is_open())
    {
        while(readin_graph(ifs, arr)!=parse_data_end_of_file){}
    }
    ifs.close();
    return 0;
}