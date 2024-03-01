#pragma once
#include <iostream>
#include <vector>
#include <stack>
#include <string>
#include <fstream>
#include <sstream>
using namespace std;
void print_2dv(vector<vector<int>> arr){
for (vector<int> i : arr)
    {
        for (int j : i)
        {
            cout << j << " ";
        }
        cout << endl;
    }
}