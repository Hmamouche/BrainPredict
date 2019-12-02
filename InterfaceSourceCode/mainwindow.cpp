/*
    Author: Youssef Hmamouche
    Year: 2019
*/

#include<QPixmap>
#include <QString>
#include "mainwindow.h"
#include "ui_mainwindow.h"
#include<vector>
#include <iterator>
#include<iostream>
#include <string>
#include<QDir>
#include<QAbstractItemModel>
#include<QListWidget>
#include<QVideoWidget>
#include<QMediaPlaylist>
#include<QResource>
#include<QFileDialog>
#include<iostream>
#include<QTableView>
#include<QStandardItemModel>
#include<QHeaderView>
#include<QThread>

#include<experimental/filesystem>
#include <QDebug>

namespace fs = std::experimental::filesystem;

using namespace  std;

MainWindow::MainWindow(QWidget *parent):
    QMainWindow(parent)
   , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    this->setFixedSize(this->size());

    this->setWindowTitle("BrainPredict");
    memory_alloc ();
    setWindows ();

    // read working directory, the default path is current dir of the application
    path = QDir::currentPath(). toStdString();

    connect (process, SIGNAL (started()), this, SLOT(this->ui->predLabel->setText("Running")));
    connect (process, SIGNAL (finished()), this, SLOT(this->ui->predLabel->setText("... Done")));
}

void MainWindow::memory_alloc ()
{
    // Memory allocation
    confederate  = new VideoPlayer (this);
    subject  = new VideoPlayer (this);
    participant = new QLabel (this);
    predictions  = new VideoPlayer (this);
    predictions  = new VideoPlayer (this);
    animation = new QLabel (this);
    brainvis = new VideoPlayer (this);
    selectionModel = new QItemSelectionModel (nullptr, this);

    tableWin = new QWidget;
    process = new QProcess (this);
}



// Set video players: video interlocutor, time series, and brain viskualisation
void MainWindow::setVideoPlayers ()
{
    // find subject audio file
    string filename = "";
    for (const auto & filepath : fs::directory_iterator(path + "/Inputs/speech")){
        string file  = split (filepath.path(), '/'). back ();
        if (file. find ("left") != string::npos and file. find (".wav") != string::npos)
        {
            filename = file;
            break;
        }
    }
    filename = path + "/Inputs/speech/" + filename;

    // set audio player of subject
    subject->setUrl (QUrl::fromLocalFile( QString::fromStdString (filename)));
    // set videos on players
    confederate->setUrl (QUrl::fromLocalFile( QString::fromStdString (path + "/Inputs/video/video_interlocutor.avi")));
    predictions->setUrl (QUrl::fromLocalFile(QString::fromStdString (path + "/Outputs/predictions_video.mp4")));
    brainvis->setUrl (QUrl::fromLocalFile(QString::fromStdString (path + "/Outputs/brain_activation.mp4")));
}

void MainWindow::setWindows ()
{
    QLabel* humanHead = new QLabel (this);

    humanHead->setGeometry (this->ui->subject->geometry().x(),
                            this->ui->subject->geometry().y(),
                            this->ui->subject->geometry().width(),
                            this->ui->subject->geometry().height());

    QPixmap pixmap(":/participant.jpeg");
    humanHead->setPixmap(pixmap.scaled (this->ui->subject->width(), this->ui->subject->height())) ; //, Qt::KeepAspectRatio));
    humanHead->setAlignment(Qt::AlignCenter);

    confederate->setGeometry (this->ui->confederate->geometry().x(),
                         this->ui->confederate->geometry().y(),
                         this->ui->confederate->geometry().width(),
                         this->ui->confederate->geometry().height() + 50);

    subject->setGeometry (this->ui->audio->geometry().x(),
                         this->ui->audio->geometry().y(),
                         this->ui->audio->geometry().width(),
                         this->ui->audio->geometry().height() + 50);


    predictions->setGeometry (this->ui->predictions->geometry().x(),
                              this->ui->predictions->geometry().y(),
                              this->ui->predictions->geometry().width(),
                              this->ui->predictions->geometry().height() + 50);

    brainvis->setGeometry (this->ui->animation->geometry().x(),
                           this->ui->animation->geometry().y(),
                           this->ui->animation->geometry().width(),
                           this->ui->animation->geometry().height() + 50);

    setRoisList ();
}

void MainWindow::setRoisList ()
{
    // read brain areas from csv file
    CMatString mat;
    QStringList strList;

    read_csv (mat, ":/brain_areas.tsv", '\t');
    for (unsigned i = 0; i < mat. size (); ++i)
        strList.push_back (QString::fromStdString (mat[i][0]));

    this->ui->listWidget->clear();
    this->ui->listWidget->addItems(strList);
    QListWidgetItem* item = 0;
    for(int i = 0; i < this->ui->listWidget->count(); ++i){
        item = this->ui->listWidget->item(i);
        item->setFlags(item->flags() | Qt::ItemIsUserCheckable);
        item->setCheckState(Qt::Unchecked);
    }
}

CVString MainWindow::getSelectedItems()
{
    CVString items;
    QListWidgetItem* item = 0;
    for(int i = 0; i < this->ui->listWidget->count(); ++i){
        item = this->ui->listWidget->item(i);
        if(item->checkState() == Qt::Checked)
            items.push_back( item->text().toStdString());
    }
    return items;
}

void MainWindow::on_loadButton_clicked()
{
    QString dirName = QFileDialog::getExistingDirectory(this);
    this->ui->textBrowser->setText(dirName);
    path = dirName.toStdString();
}

void MainWindow::on_simulationButton_clicked()
{
    setVideoPlayers();
    confederate->play ();
    subject->play();
    predictions-> play ();
    brainvis->play();
}

void MainWindow::on_predictorsButton_clicked()
{
    setPredTable ();
}

void MainWindow::on_selectButton_clicked()
{
    for(int i = 0; i < this->ui->listWidget->count(); ++i)
        this->ui->listWidget->item(i)->setCheckState(Qt::Checked);
}
void MainWindow::setPredTable()
{
    // read brain areas from csv file
    CMatString mat;
    QStringList strList;

    CVString rois =  read_csv (mat, path + "/Outputs/predictors.csv", ';');

    for (auto roi:rois)
                 strList. push_back (QString::fromStdString(roi));

    tableWin->setWindowTitle("Predictors Table");

    QTableView * tableWidget = new QTableView;
    QStandardItemModel* model = new QStandardItemModel(1,rois.size(),this);


    model->setHorizontalHeaderLabels(strList);
    for (unsigned i = 0; i < mat.size(); ++i)
        for (unsigned j = 0; j < mat[i].size(); ++j){
            model->setItem(i, j, new QStandardItem(QString::fromStdString(mat[i][j])));
        }

    //QGridLayout *layout = new QGridLayout;
    tableWidget->setWindowTitle("Predictors Table");
    tableWidget->setModel(model);
    //tableWidget->setEditTriggers(QAbstractItemView::NoEditTriggers);
    //tableWidget->horizontalHeader()->setSectionResizeMode(QHeaderView::Stretch);
    /*layout->addWidget(tableWidget);
    tableWin->setLayout(layout);
    layout->setSizeConstraint(QLayout::SetMinAndMaxSize);*/
    tableWidget-> show ();
}

void MainWindow::on_predictButton_clicked()
{
    QString ex = QString::fromStdString ("sh predict.sh");
    process->setWorkingDirectory (QString::fromStdString (path));

    qDebug () << ex << endl;
    process->start (ex);
    process->waitForStarted();

    qDebug () << "Running" << endl;
    //this->ui->predLabel->setText("Running");
    process->waitForFinished();
    qDebug () << process->readAll() << endl;
    qDebug () << "Done" << endl;
    this->ui->predLabel->setText("Done ...");

    process->close();
}

void MainWindow :: disp()
{
    /*int t;
    t = process->readAllStandardOutput(). toInt();
    // this->ui->progressBar->setValue (t);
    cout << t <<endl;
   // this->ui->progressBar->setValue (t);*/
    this->ui->predLabel->clear();
    this->ui->predLabel->setText("Running ...");
    this->ui->predLabel->update();

    //this->ui->text->setText("Running ...");
}
