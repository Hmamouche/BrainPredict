/*
    charger_csv.h
    Author: Youssef Hmamouche
    Year: 2018
*/
#include "charger_csv.h"
#include <QDebug>
#include<QFile>

CVString split (const string &line, const char & sep)
{
     CVString out;
     string value = "";
     unsigned inc(0);
     for (auto c = line.begin(); c != (line.end()); ++c)
     {
        if (*c != sep)
           value.push_back(*c);
        if( *c == sep || (inc == (line.size() - 1)))
        {
            out.push_back(value);
            value.clear();
        }
        ++ inc;
     }
     return out;
}

CVString read_csv (CMatString &mat, const string & fileName, const char & sep)
{
    QString data;
    QFile file(QString::fromStdString (fileName));
    if(!file.open(QIODevice::ReadOnly)) {
        qDebug()<<"file of brain areas names not opened"<<endl;
    }
    else
    {
        //qDebug()<<"file opened"<<endl;
        data = file.readAll();
    }

    CVString lines = split (data.toStdString(), '\n');
    CVString header = split (lines [0], sep);

    mat.clear();
    mat.reserve (lines. size () - 1);

    for (unsigned i = 1; i < lines. size (); ++i)
        mat.push_back (split (lines [i], sep));

    file.close();
    return header;
}
