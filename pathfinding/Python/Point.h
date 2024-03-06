#pragma once
#include<string>
#include<iostream>
using namespace std;
class Point{
    friend std::ostream& operator<<(std::ostream&, const Point&);
    protected:
    int number;
    string latitude;
    string longitude;
    char NS;
    char EW;
    public:
    //constructors
    Point(int,string,char,string,char);
    ~Point();
    //member functions
    string print_coordinate();
    double get_latitude();
    double get_longitude();
    bool operator<(const Point&) const;
};
std::ostream& operator<<(std::ostream&, const Point&);