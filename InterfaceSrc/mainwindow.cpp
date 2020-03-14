/*
 ** This file is part of BrainPredict.
 ** Author: Youssef Hmamouche
 ** Year: 2019
*/

#include<QPixmap>
#include <QString>
#include<QListWidget>

#include<QFileDialog>
#include<QTableView>
#include<QStandardItemModel>
#include<QHeaderView>

#include <QDebug>
#include<experimental/filesystem>

#include<vector>
#include <iterator>
#include <string>

#include "mainwindow.h"
#include "ui_mainwindow.h"

#include<iostream>

using namespace std;
namespace fs = std::experimental::filesystem;

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
    path = this->ui->textBrowser->toPlainText().toStdString();
    if (path.length() == 0){
        path = QDir::currentPath(). toStdString();
    }
    //path = QDir::currentPath(). toStdString();
    //setVideoPlayers();

}

void MainWindow::memory_alloc ()
{
    // Memory allocation
    confederate  = new VideoPlayer (this);
    subject  = new VideoPlayer (this);

    confederate_audio  = new VideoPlayer (this);

    participant = new QLabel (this);
    predictions  = new VideoPlayer (this);
    predictions  = new VideoPlayer (this);
    animation = new QLabel (this);
    brainvis = new VideoPlayer (this);
    tableWin = new QWidget;
    process = new QProcess (this);


}



// Set video players: video interlocutor, time series, and brain viskualisation
void MainWindow::setVideoPlayers ()
{
    // find subject audio file
    string filename_left = "", filename_right = "";
    for (const auto & filepath : fs::directory_iterator(path + "/Inputs/speech")){
        string file  = split (filepath.path(), '/'). back ();
        if (file. find ("left") != string::npos and file. find (".wav") != string::npos)
        {
            filename_left = file;
        }
        if (file. find ("right") != string::npos and file. find (".wav") != string::npos)
        {
            filename_right = file;
        }
    }
    filename_left = path + "/Inputs/speech/" + filename_left;
    filename_right = path + "/Inputs/speech/" + filename_right;

    // set audio player of subject
    subject->setUrl (QUrl::fromLocalFile( QString::fromStdString (filename_left)));
    // set videos on players
    confederate->setUrl (QUrl::fromLocalFile( QString::fromStdString (path + "/Inputs/video/video_interlocutor.avi")));

    confederate_audio->setUrl (QUrl::fromLocalFile( QString::fromStdString (filename_right)));

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

    confederate_audio->setGeometry (this->ui->audio_2->geometry().x(),
                         this->ui->audio_2->geometry().y(),
                         this->ui->audio_2->geometry().width(),
                         this->ui->audio_2->geometry().height() + 50);


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
    QListWidgetItem* item = nullptr;

    for(int i = 0; i < this->ui->listWidget->count(); ++i){
        item = this->ui->listWidget->item(i);
        item->setFlags(item->flags() | Qt::ItemIsUserCheckable);
        item->setCheckState(Qt::Unchecked);
    }
}

CVString MainWindow::getSelectedItems()
{
    CMatString mat;
    CVString header = read_csv (mat, ":/brain_areas.tsv", '\t');
    CVString areasNumbers;

    CVString items;
    QListWidgetItem* item = nullptr;
    for(int i = 0; i < this->ui->listWidget->count(); ++i){
        item = this->ui->listWidget->item(i);
        if(item->checkState() == Qt::Checked)
            items.push_back( item->text().toStdString());
    }

    for (string &item:items)
    {
        for (unsigned i = 0; i < mat.size(); ++i)
        {
            if (mat[i][0] == item)
                areasNumbers. push_back (mat[i][1]);
        }
     }
    return areasNumbers;
}

void MainWindow::on_simulationButton_clicked()
{
    confederate->play ();
    confederate_audio->play ();
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
    QStandardItemModel* model = new QStandardItemModel(1, int (rois.size()),this);


    model->setHorizontalHeaderLabels(strList);
    for (unsigned i = 0; i < mat.size(); ++i)
        for (unsigned j = 0; j < mat[i].size(); ++j){
            model->setItem(int (i), int (j), new QStandardItem(QString::fromStdString(mat[i][j])));
        }

    tableWidget->setWindowTitle("Predictors Table");
    tableWidget->setModel(model);

    tableWidget->horizontalHeader()->setSectionResizeMode(QHeaderView::Stretch);
    tableWidget->verticalHeader()->setSectionResizeMode(QHeaderView::Stretch);

    /*tableWidget->setWordWrap(true);
    tableWidget->setTextElideMode(Qt::ElideLeft);
    tableWidget->resizeColumnsToContents();
    tableWidget->resizeRowsToContents();

    //tableWidget->resizeRowsToContents();*/

    tableWidget-> show ();
}

void MainWindow :: disp()
{
    this->ui->predLabel->clear();
    this->ui->predLabel->setText("Running ...");
    this->ui->predLabel->update();
}

void MainWindow::on_loadButton_clicked()
{
    QString dirName = QFileDialog::getExistingDirectory(this);
    this->ui->textBrowser->setText(dirName);
    path = dirName.toStdString();

    setVideoPlayers();

}
void MainWindow::on_loadButton_2_clicked()
{
    QString dirName = QFileDialog::getExistingDirectory(this);
    this->ui->textBrowser_2->setText(dirName);
    path = dirName.toStdString();
}

//  Make predictions when clicked
void MainWindow::on_predictButton_clicked()
{
    // Get number of selected regions, and join them with space
    CVString selectedAreas = getSelectedItems();
    string areas ("");
    for (auto area : selectedAreas)
            areas += area + " ";

    // get the conversation type from the combobox
    string conversType = this->ui->comboBox->currentText(). toStdString();
    if (conversType == "Human-human")
        conversType = "h";
    else if (conversType == "Human-robot")
        conversType = "r";

    // Construct the argument for predict.py file
    QString script = QString::fromStdString  ("python src/predict.py -rg " + areas +
                    " -t " + conversType +
                    "-pmp PredictionModule -in " + path);

    // Execute the script
    qDebug () << script << endl;
    process->execute (script);
    process->waitForFinished();
    qDebug () << "Done" << endl;
    this->ui->predLabel->setText("Done ...");
    process->close();
}

// Generate time series when clicked
void MainWindow::on_pushButton_4_clicked()
{
    QString ex = QString::fromStdString ("sh test.sh");

    // Get number of selected regions, and join them with space
    CVString selectedAreas = getSelectedItems();
    string areas ("");
    for (auto area : selectedAreas)
            areas += area + " ";

    // Get OpenFace path from textbrowser
    string openFacePath = this->ui->textBrowser_2->toPlainText().toStdString();

    // Construct the argument for predict.py file
    QString script = QString::fromStdString  ("python src/generate_time_series.py -rg " + areas +
                    " -ofp " + openFacePath +
                    " -pmp PredictionModule -in " + path);

    // Execute the script
    qDebug () << script << endl;
    process->execute (script);
    process->waitForStarted();
    process->waitForFinished();
    qDebug () << process->readAll() << endl;
    this->ui->generateLabel->setText("Done ...");
    process->close();
}

