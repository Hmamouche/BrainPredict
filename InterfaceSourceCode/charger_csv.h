/************************************
 **
 ** charger_csv.h
 ** Author: Youssef Hmamouche
 ** Year: 2018
 ** description: Read a csv file with header in the first line
 **
 *************************************/

#pragma once

#include <vector>
#include<string>
using namespace std;

typedef vector<string> CVString;
typedef vector <vector<string> > CMatString;

CVString split (const string &, const char &);
CVString read_csv (CMatString &mat, const string & fileName, const char & sep);
