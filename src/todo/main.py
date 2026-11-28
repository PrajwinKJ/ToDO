from PySide6.QtWidgets import (QApplication,QMainWindow,QPushButton,QLineEdit,QWidget,QStackedWidget,QVBoxLayout,QHBoxLayout,QLabel,QTableWidget,QTableWidgetItem,QHeaderView,QCheckBox,QTableView)
import sys
from PySide6.QtGui import QIcon
from pathlib import Path
from PySide6.QtCore import QSize,Qt
import backend as sql

iconPath=str(Path(__file__).resolve().parent.parent)


def doneButton():
    button=QPushButton()
    icon=iconPath+"/markAsDone.svg"
    button.setIcon(QIcon(icon))
    button.setIconSize(QSize(25,15))
    return button

def undoButton():
    button=QPushButton()
    icon=iconPath+"/undo.svg"
    button.setIcon(QIcon(icon))
    button.setIconSize(QSize(25,15))
    return button

def delButton():
    button=QPushButton()
    icon=iconPath+"/del.svg"
    button.setIcon(QIcon(icon))
    button.setIconSize(QSize(25,15))
    return button

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

    def reloadViewPage(self):
        allTasks=sql.loadAllTasks()
        self.tasks.setRowCount(0)
        for row,objects in enumerate(allTasks):
            self.tasks.insertRow(row)
            doneBtn=doneButton()
            doneBtn.clicked.connect(lambda _,b=doneBtn: self.taskCompleted(b))
            delBtn=delButton()
            delBtn.clicked.connect(lambda _,b=delBtn: self.delTask(b))
            self.tasks.setItem(row,0,QTableWidgetItem(objects.title))
            self.tasks.setItem(row,1,QTableWidgetItem(objects.status))
            self.tasks.setCellWidget(row,2,doneBtn)
            self.tasks.setCellWidget(row,3,delBtn)

    def reloadDonePage(self):
        self.completedTask.setRowCount(0)
        completedTasks=sql.loadCompletedTasks()
        for row,results in enumerate(completedTasks):
            self.completedTask.insertRow(row)
            undoBtn=undoButton() 
            
            delBtn=delButton()
            delBtn.clicked.connect(lambda _,b=delBtn: self.delTask(b,self.completedTask))                            #implement undo method
            self.completedTask.setItem(row,0,QTableWidgetItem(results.task.title))
            self.completedTask.setCellWidget(row,1,undoBtn)
            self.completedTask.setCellWidget(row,2,delBtn)

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

        self.reloadViewPage()

    def donePage(self):
        doneWidget=QWidget()
        doneLayout=QVBoxLayout(doneWidget)
        doneLayout.addWidget(QLabel("Completed Tasks"))

        self.completedTask=QTableWidget(0,3)
        self.completedTask.setHorizontalHeaderLabels(['Tasks',"Undo",'Del'])
        headers=self.completedTask.horizontalHeader()

        headers.setSectionResizeMode(1,QHeaderView.ResizeMode.ResizeToContents)
        headers.setSectionResizeMode(0,QHeaderView.ResizeMode.Stretch)
        headers.setSectionResizeMode(2,QHeaderView.ResizeMode.ResizeToContents)

        self.completedTask.setWordWrap(True)

        doneLayout.addWidget(self.completedTask)

        self.pages.addWidget(doneWidget)

        self.reloadDonePage()

    def addTask(self):
        row=self.tasks.rowCount()
        task=self.input.text().strip()
        status="incomplete"
        completeBtn=doneButton()
        completeBtn.clicked.connect(lambda _,b=completeBtn: self.taskCompleted(b))

        delBtn=delButton()
        delBtn.clicked.connect(lambda _,b=delBtn: self.delTask(b))

        if task:
            sql.addTask(task,status)
            self.tasks.insertRow(row)
            self.tasks.setItem(row,0,QTableWidgetItem(self.counter))
            self.tasks.setItem(
                row,0,QTableWidgetItem(task)
            )
            self.tasks.setItem(
                row,1,QTableWidgetItem(status)
            )
            self.tasks.setCellWidget(
                row,2,completeBtn
            )
            self.tasks.setCellWidget(
                row,3,delBtn)
            self.input.clear()
            self.tasks.resizeRowsToContents()


        self.counter+=1

    def delTask(self,button,table=None):              #implement deletion in sql
        tbClass=table or self.tasks
        row=tbClass.indexAt(button.pos()).row()
        if row!=-1:
            title=tbClass.item(row,0).text().strip()
            sql.delTask(title)
            self.reloadDonePage()
            self.reloadViewPage()            

    def taskCompleted(self,button):        
        row=self.tasks.indexAt(button.pos()).row()
        newRow=self.completedTask.rowCount()
        self.completedTask.insertRow(newRow)

        self.tasks.setItem(row,1,QTableWidgetItem('completed'))

        undoBtn=undoButton()
        undoBtn.clicked.connect(lambda _,b=undoBtn: self.undoCompletion(b))

        delBtn=delButton()
        delBtn.clicked.connect(lambda _,b=delBtn: self.delTask(b,self.completedTask))

        item=self.tasks.item(row,0)
        if item:
            sql.markCompleted(item.text())
            self.completedTask.setItem(newRow,0,QTableWidgetItem(item.text()))
            self.completedTask.setCellWidget(newRow,1,undoBtn) 
            self.completedTask.setCellWidget(newRow,2,delBtn)   

 

    def undoCompletion(self,button):                               #implement undo mechanism in sql

        row=self.completedTask.indexAt(button.pos()).row()

        completeBtn=doneButton()
        completeBtn.clicked.connect(lambda _,b=completeBtn: self.taskCompleted(b))

        delBtn=delButton()
        delBtn.clicked.connect(lambda _,b=delBtn: self.delTask(b))

        self.tasks.setItem(row,1,QTableWidgetItem("incomplete"))

        title=self.completedTask.item(row,0)
        sql.undoTask(title.text())

        self.completedTask.removeRow(row)


app=QApplication(sys.argv)

window=MainWindow()
window.show()

app.exec()