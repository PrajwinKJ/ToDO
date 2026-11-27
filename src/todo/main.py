from PySide6.QtWidgets import (QApplication,QMainWindow,QPushButton,QLineEdit,QWidget,QStackedWidget,QVBoxLayout,QHBoxLayout,QLabel,QTableWidget,QTableWidgetItem,QHeaderView,QCheckBox,QTableView)
import sys
from PySide6.QtGui import QIcon
from pathlib import Path
from PySide6.QtCore import QSize

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        mainWidget=QWidget()
        mainLayout=QHBoxLayout(mainWidget)
        self.resize(600,800)

        self.iconPath=str(Path(__file__).resolve().parent.parent)

        sidebar=QWidget()
        sidebarLayout=QVBoxLayout(sidebar)
        sidebar.setFixedWidth(60)
        sidebar.setContentsMargins(0,0,0,0)

        self.addNav=QPushButton("+")
        self.viewNav=QPushButton("View")
        self.doneNav=QPushButton("Done")
        self.delNav=QPushButton("Del")

        sidebarLayout.addWidget(self.addNav)
        sidebarLayout.addWidget(self.viewNav)
        sidebarLayout.addWidget(self.doneNav)
        sidebarLayout.addStretch()
        self.pages=QStackedWidget()

        self.createPage()
        self.viewPage()
        self.donePage()
        
        self.addNav.clicked.connect(lambda: self.pages.setCurrentIndex(0))
        self.viewNav.clicked.connect(lambda: self.pages.setCurrentIndex(1))
        self.doneNav.clicked.connect(lambda: self.pages.setCurrentIndex(2))


        mainLayout.addWidget(sidebar)
        mainLayout.addWidget(self.pages)

        self.setCentralWidget(mainWidget)

        self.counter=1

    def createPage(self):
        createWidget=QWidget()
        layout=QVBoxLayout(createWidget)

        self.input=QLineEdit()
        self.input.setPlaceholderText("Add Task")
        button=QPushButton("Add")
        button.clicked.connect(self.addTask)
        self.input.returnPressed.connect(self.addTask)

        layout.addWidget(self.input)
        layout.addWidget(button)
        layout.addStretch()

        self.pages.addWidget(createWidget)

    def viewPage(self):
        viewWidget=QWidget()
        viewLayout=QVBoxLayout(viewWidget)
        viewLayout.addWidget(QLabel("All Tasks"))

        self.tasks=QTableWidget(0,4)
        self.tasks.setHorizontalHeaderLabels(["Tasks","Status","Done","Del"])

        header=self.tasks.horizontalHeader()
        header.setSectionResizeMode(0,QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1,QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2,QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3,QHeaderView.ResizeMode.ResizeToContents)
        self.tasks.setWordWrap(True)

        viewLayout.addWidget(self.tasks)


        self.pages.addWidget(viewWidget)

    def donePage(self):
        doneWidget=QWidget()
        doneLayout=QVBoxLayout(doneWidget)
        doneLayout.addWidget(QLabel("Completed Tasks"))

        self.completedTask=QTableWidget(0,3)
        self.completedTask.setHorizontalHeaderLabels(['Tasks','Status',"Undo"])
        headers=self.completedTask.horizontalHeader()

        headers.setSectionResizeMode(1,QHeaderView.ResizeMode.ResizeToContents)
        headers.setSectionResizeMode(0,QHeaderView.ResizeMode.Stretch)
        headers.setSectionResizeMode(2,QHeaderView.ResizeMode.ResizeToContents)

        self.completedTask.setWordWrap(True)

        doneLayout.addWidget(self.completedTask)

        self.pages.addWidget(doneWidget)


    def addTask(self):
        row=self.tasks.rowCount()
        task=self.input.text().strip()
        status="incomplete"
        completeButton=QPushButton()
        icon=str(self.iconPath+"/markAsDone.svg")
        completeButton.setIcon(QIcon(icon))
        completeButton.setIconSize(QSize(25,15))
        completeButton.clicked.connect(lambda _,b=completeButton: self.taskCompleted(b))

        delButton=QPushButton()
        delIcon=str(self.iconPath+"/del.svg")
        delButton.setIcon(QIcon(delIcon))
        delButton.setIconSize(QSize(25,15))
        delButton.clicked.connect(lambda _,b=delButton: self.delTask(b))

        if task:
            self.tasks.insertRow(row)
            self.tasks.setItem(row,0,QTableWidgetItem(self.counter))
            self.tasks.setItem(
                row,0,QTableWidgetItem(task)
            )
            self.tasks.setItem(
                row,1,QTableWidgetItem(status)
            )
            self.tasks.setCellWidget(
                row,2,completeButton
            )
            self.tasks.setCellWidget(
                row,3,delButton)
            self.input.clear()
            self.tasks.resizeRowsToContents()


        self.counter+=1

    def delTask(self,button):
        row=self.tasks.indexAt(button.pos()).row()
        if row!=-1:
            self.tasks.removeRow(row)

    def taskCompleted(self,button):        #change to move content to table
        row=self.tasks.indexAt(button.pos()).row()
        newRow=self.completedTask.rowCount()
        self.completedTask.insertRow(newRow)

        undoButton=QPushButton()
        undoIcon=str(self.iconPath+"/undo.svg")
        undoButton.setIcon(QIcon(undoIcon))
        undoButton.setIconSize(QSize(25,15))
        undoButton.clicked.connect(lambda _,b=undoButton: self.undoCompletion(b))

        item=self.tasks.takeItem(row,0)
        if item:
            self.completedTask.setItem(newRow,1,QTableWidgetItem("Completed"))  
            self.completedTask.setItem(newRow,0,item)
            self.completedTask.setCellWidget(newRow,2,undoButton)    

        self.tasks.removeRow(row)

    def undoCompletion(self,button):

        row=self.completedTask.indexAt(button.pos()).row()
        newRow=self.tasks.rowCount()

        completeButton=QPushButton()
        icon=str(self.iconPath+"/markAsDone.svg")
        completeButton.setIcon(QIcon(icon))
        completeButton.setIconSize(QSize(25,15))
        completeButton.clicked.connect(lambda _,r=newRow: self.taskCompleted(r))

        delButton=QPushButton()
        delIcon=str(self.iconPath+"/del.svg")
        delButton.setIcon(QIcon(delIcon))
        delButton.setIconSize(QSize(25,15))
        delButton.clicked.connect(lambda _,r=newRow: self.tasks.removeRow(r))
        self.tasks.insertRow(newRow)

        task=self.completedTask.takeItem(row,0)

        self.tasks.setItem(newRow,0,task)
        self.tasks.setItem(newRow,1,QTableWidgetItem("incomplete"))
        self.tasks.setCellWidget(newRow,2,completeButton)
        self.tasks.setCellWidget(newRow,3,delButton)

        self.completedTask.removeRow(row)

            


app=QApplication(sys.argv)

window=MainWindow()
window.show()

app.exec()