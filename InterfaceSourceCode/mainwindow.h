/*
    Author: Youssef Hmamouche
    Year: 2019
*/

#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QPushButton>
#include <QLabel>
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
    QLabel* participant;
    QLabel * animation;

    /* 4 Video Players */
    VideoPlayer* confederate;
    VideoPlayer* subject;
    VideoPlayer* predictions;
    VideoPlayer* brainvis;

    /* Widget for tableView */
    QWidget * tableWin;

    /* Process to execute external scripts */
    QProcess * process;

    Ui::MainWindow *ui;

    /* Private functions */
    CVString getSelectedItems ();
    void setWindows ();
    void memory_alloc ();
    void setPredTable ();
    void setVideoPlayers ();
    void setRoisList ();

public:
    MainWindow (QWidget *parent = nullptr);

    ~MainWindow()
    {
        delete button;
        delete confederate;
        delete subject;
        delete participant;
        delete predictions;
        delete animation;
        delete brainvis;
        //delete ui;

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
    void on_loadButton_2_clicked();
    void on_pushButton_4_clicked();
};
#endif // MAINWINDOW_H
