/*
    Author: Youssef Hmamouche
    Year: 2019
*/

#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QPushButton>
#include <QLabel>
#include <QItemSelectionModel>
#include <QMovie>
#include <QTableWidget>
#include<QtMultimediaWidgets/qgraphicsvideoitem.h>
#include<QProcess>

#include "videoplayer.h"
#include"charger_csv.h"

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

private:
    string path;
    QPushButton* button;
    QItemSelectionModel* selectionModel;
    QLabel* participant;
    QLabel * animation;
    // vodeis
    //QMediaPlayer* player;
    VideoPlayer* confederate;
    VideoPlayer* subject;
    /*VideoPlayer* audioConfederate;
    VideoPlayer* audioParticipant;*/
    VideoPlayer* predictions;
    VideoPlayer* brainvis;
    QMovie *movie;
    QTableWidget * tableWidget;

    QWidget * tableWin;

    QProcess * process;

    Ui::MainWindow *ui;

    CVString getSelectedItems ();

public:
    MainWindow (QWidget *parent = nullptr);
    void setWindows ();
    void memory_alloc ();
    void setPredTable ();
    void setVideoPlayers ();
    void setRoisList ();
    ~MainWindow()
    {
        delete button;
        delete selectionModel;
        delete confederate;
        delete subject;
        delete participant;
        delete predictions;
        delete animation;
        delete brainvis;
        delete movie;
        delete tableWidget;
        delete ui;

        delete tableWin;
        delete process;
    }

private slots:
    void on_loadButton_clicked();
    void on_simulationButton_clicked();
    void on_predictorsButton_clicked();
    void on_selectButton_clicked();
    void on_predictButton_clicked();
    void disp();
};
#endif // MAINWINDOW_H
