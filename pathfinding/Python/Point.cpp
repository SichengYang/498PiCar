#include "Point.h"

using namespace std;
Point::Point(int num, string la,char ns, string lo,char ew) : number(num), latitude(la), NS(ns), longitude(lo), EW(ew)
{
    cout << "Constructing Point Object: " << num << " " << la <<ns<< " " << lo <<ew<< endl;
}
Point::~Point()
{
    cout << "~Point()" << endl;
}

string Point::print_coordinate()
{
    return this->latitude + " " + this->longitude;
}
double Point::get_latitude()
{
    return stod(this->latitude);
}
double Point::get_longitude()
{
    return stod(this->longitude);
}