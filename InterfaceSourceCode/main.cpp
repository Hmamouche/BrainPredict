/************************************************************************
** Copyright (C) 2019 Youssef Hmamouche.
**
** This file is part of BrainPredict.

** BrainPredict is free software: you can redistribute it and/or modify
** it under the terms of the GNU General Public License as published by
** the Free Software Foundation, either version 3 of the License, or
** (at your option) any later version.

** BrainPredict is distributed in the hope that it will be useful,
** but WITHOUT ANY WARRANTY; without even the implied warranty of
** MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
** GNU General Public License for more details.

** You should have received a copy of the GNU General Public License
** along with Foobar.  If not, see <https://www.gnu.org/licenses/>. 2
*****************************************************************************/
#include <QApplication>
#include <QtWidgets/QApplication>
#include "mainwindow.h"

int main(int argc, char *argv[])
{

    QApplication app (argc, argv);
    MainWindow *mw = new MainWindow;
    mw->show();

    return app.exec();
}
