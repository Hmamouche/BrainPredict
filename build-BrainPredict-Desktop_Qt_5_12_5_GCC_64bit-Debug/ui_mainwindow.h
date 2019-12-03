/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 5.12.5
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QFrame>
#include <QtWidgets/QLabel>
#include <QtWidgets/QListWidget>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QTextBrowser>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralwidget;
    QWidget *confederate;
    QWidget *subject;
    QWidget *predictions;
    QLabel *label;
    QLabel *label_2;
    QWidget *animation;
    QLabel *label_3;
    QListWidget *listWidget;
    QFrame *line;
    QFrame *line_2;
    QLabel *label_4;
    QFrame *line_4;
    QFrame *line_6;
    QFrame *line_3;
    QTextBrowser *textBrowser;
    QPushButton *loadButton;
    QLabel *label_6;
    QWidget *audio;
    QPushButton *selectButton;
    QPushButton *pushButton_4;
    QPushButton *predictButton;
    QPushButton *simulationButton;
    QPushButton *predictorsButton;
    QLabel *predLabel;
    QLabel *generateLabel;
    QMenuBar *menubar;
    QStatusBar *statusbar;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QString::fromUtf8("MainWindow"));
        MainWindow->resize(1820, 913);
        MainWindow->setStyleSheet(QString::fromUtf8("border-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));"));
        centralwidget = new QWidget(MainWindow);
        centralwidget->setObjectName(QString::fromUtf8("centralwidget"));
        confederate = new QWidget(centralwidget);
        confederate->setObjectName(QString::fromUtf8("confederate"));
        confederate->setGeometry(QRect(220, 30, 311, 201));
        subject = new QWidget(centralwidget);
        subject->setObjectName(QString::fromUtf8("subject"));
        subject->setGeometry(QRect(670, 30, 151, 171));
        predictions = new QWidget(centralwidget);
        predictions->setObjectName(QString::fromUtf8("predictions"));
        predictions->setGeometry(QRect(190, 260, 761, 531));
        label = new QLabel(centralwidget);
        label->setObjectName(QString::fromUtf8("label"));
        label->setGeometry(QRect(230, 10, 81, 20));
        label_2 = new QLabel(centralwidget);
        label_2->setObjectName(QString::fromUtf8("label_2"));
        label_2->setGeometry(QRect(680, 10, 81, 20));
        animation = new QWidget(centralwidget);
        animation->setObjectName(QString::fromUtf8("animation"));
        animation->setGeometry(QRect(980, 50, 821, 741));
        label_3 = new QLabel(centralwidget);
        label_3->setObjectName(QString::fromUtf8("label_3"));
        label_3->setGeometry(QRect(20, 20, 151, 20));
        listWidget = new QListWidget(centralwidget);
        listWidget->setObjectName(QString::fromUtf8("listWidget"));
        listWidget->setGeometry(QRect(10, 40, 161, 151));
        line = new QFrame(centralwidget);
        line->setObjectName(QString::fromUtf8("line"));
        line->setGeometry(QRect(170, 10, 20, 811));
        line->setMaximumSize(QSize(20, 931));
        line->setFrameShape(QFrame::VLine);
        line->setFrameShadow(QFrame::Sunken);
        line_2 = new QFrame(centralwidget);
        line_2->setObjectName(QString::fromUtf8("line_2"));
        line_2->setGeometry(QRect(0, 810, 1821, 20));
        line_2->setFrameShape(QFrame::HLine);
        line_2->setFrameShadow(QFrame::Sunken);
        label_4 = new QLabel(centralwidget);
        label_4->setObjectName(QString::fromUtf8("label_4"));
        label_4->setGeometry(QRect(990, 20, 131, 20));
        line_4 = new QFrame(centralwidget);
        line_4->setObjectName(QString::fromUtf8("line_4"));
        line_4->setGeometry(QRect(180, 240, 791, 31));
        line_4->setFrameShape(QFrame::HLine);
        line_4->setFrameShadow(QFrame::Sunken);
        line_6 = new QFrame(centralwidget);
        line_6->setObjectName(QString::fromUtf8("line_6"));
        line_6->setGeometry(QRect(0, 0, 1821, 16));
        line_6->setFrameShape(QFrame::HLine);
        line_6->setFrameShadow(QFrame::Sunken);
        line_3 = new QFrame(centralwidget);
        line_3->setObjectName(QString::fromUtf8("line_3"));
        line_3->setGeometry(QRect(960, 10, 20, 811));
        line_3->setMaximumSize(QSize(20, 931));
        line_3->setFrameShape(QFrame::VLine);
        line_3->setFrameShadow(QFrame::Sunken);
        textBrowser = new QTextBrowser(centralwidget);
        textBrowser->setObjectName(QString::fromUtf8("textBrowser"));
        textBrowser->setGeometry(QRect(170, 830, 621, 31));
        loadButton = new QPushButton(centralwidget);
        loadButton->setObjectName(QString::fromUtf8("loadButton"));
        loadButton->setGeometry(QRect(810, 830, 51, 31));
        label_6 = new QLabel(centralwidget);
        label_6->setObjectName(QString::fromUtf8("label_6"));
        label_6->setGeometry(QRect(20, 830, 131, 31));
        audio = new QWidget(centralwidget);
        audio->setObjectName(QString::fromUtf8("audio"));
        audio->setGeometry(QRect(650, 210, 241, 21));
        selectButton = new QPushButton(centralwidget);
        selectButton->setObjectName(QString::fromUtf8("selectButton"));
        selectButton->setGeometry(QRect(10, 200, 141, 31));
        pushButton_4 = new QPushButton(centralwidget);
        pushButton_4->setObjectName(QString::fromUtf8("pushButton_4"));
        pushButton_4->setGeometry(QRect(10, 330, 142, 28));
        predictButton = new QPushButton(centralwidget);
        predictButton->setObjectName(QString::fromUtf8("predictButton"));
        predictButton->setGeometry(QRect(10, 400, 142, 28));
        simulationButton = new QPushButton(centralwidget);
        simulationButton->setObjectName(QString::fromUtf8("simulationButton"));
        simulationButton->setGeometry(QRect(10, 570, 142, 28));
        predictorsButton = new QPushButton(centralwidget);
        predictorsButton->setObjectName(QString::fromUtf8("predictorsButton"));
        predictorsButton->setGeometry(QRect(10, 610, 142, 28));
        predLabel = new QLabel(centralwidget);
        predLabel->setObjectName(QString::fromUtf8("predLabel"));
        predLabel->setGeometry(QRect(10, 440, 141, 21));
        generateLabel = new QLabel(centralwidget);
        generateLabel->setObjectName(QString::fromUtf8("generateLabel"));
        generateLabel->setGeometry(QRect(10, 370, 141, 21));
        MainWindow->setCentralWidget(centralwidget);
        menubar = new QMenuBar(MainWindow);
        menubar->setObjectName(QString::fromUtf8("menubar"));
        menubar->setGeometry(QRect(0, 0, 1820, 25));
        MainWindow->setMenuBar(menubar);
        statusbar = new QStatusBar(MainWindow);
        statusbar->setObjectName(QString::fromUtf8("statusbar"));
        MainWindow->setStatusBar(statusbar);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QApplication::translate("MainWindow", "MainWindow", nullptr));
        label->setText(QApplication::translate("MainWindow", "Interlocutor", nullptr));
        label_2->setText(QApplication::translate("MainWindow", "Participant", nullptr));
        label_3->setText(QApplication::translate("MainWindow", "Brain Regions", nullptr));
        label_4->setText(QApplication::translate("MainWindow", "Brain Visualization", nullptr));
        loadButton->setText(QApplication::translate("MainWindow", "Load", nullptr));
        label_6->setText(QApplication::translate("MainWindow", "Working directory:", nullptr));
        selectButton->setText(QApplication::translate("MainWindow", "Select/Deselect All", nullptr));
        pushButton_4->setText(QApplication::translate("MainWindow", "Generate Features", nullptr));
        predictButton->setText(QApplication::translate("MainWindow", "Prediction", nullptr));
        simulationButton->setText(QApplication::translate("MainWindow", "Simulation", nullptr));
        predictorsButton->setText(QApplication::translate("MainWindow", "Show Predictors ", nullptr));
        predLabel->setText(QString());
        generateLabel->setText(QString());
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
