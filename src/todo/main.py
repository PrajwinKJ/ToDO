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
        sidebarLayout.addWidget(self.delNav)
        sidebarLayout.addStretch()
        self.pages=QStackedWidget()

        self.createPage()
        self.viewPage()
        self.donePage()
        self.delPage()
        
        self.addNav.clicked.connect(lambda: self.pages.setCurrentIndex(0))
        self.viewNav.clicked.connect(lambda: self.pages.setCurrentIndex(1))
        self.doneNav.clicked.connect(lambda: self.pages.setCurrentIndex(2))
        self.delNav.clicked.connect(lambda: self.pages.setCurrentIndex(3))


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

        self.tasks=QTableWidget(0,3)
        self.tasks.setHorizontalHeaderLabels(["Tasks","Status","Done"])

        header=self.tasks.horizontalHeader()
        header.setSectionResizeMode(0,QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1,QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2,QHeaderView.ResizeMode.ResizeToContents)

        self.tasks.setWordWrap(True)

        viewLayout.addWidget(self.tasks)


        self.pages.addWidget(viewWidget)

    def donePage(self):
        doneWidget=QWidget()
        doneLayout=QVBoxLayout(doneWidget)
        doneLayout.addWidget(QLabel("Completed Tasks"))

        self.completedTask=QTableWidget(0,2)
        self.completedTask.setHorizontalHeaderLabels(['Tasks','Status'])
        headers=self.completedTask.horizontalHeader()

        headers.setSectionResizeMode(1,QHeaderView.ResizeMode.ResizeToContents)
        headers.setSectionResizeMode(0,QHeaderView.ResizeMode.Stretch)

        self.completedTask.setWordWrap(True)

        doneLayout.addWidget(self.completedTask)

        self.pages.addWidget(doneWidget)

    def delPage(self):
        delwidget=QWidget()
        delLayout=QVBoxLayout(delwidget)
        delLayout.addWidget(QLabel("Deleted Task"))

        self.deletedTask=QTableWidget(0,2)
        self.deletedTask.setHorizontalHeaderLabels(['Task','Status'])

        headers=self.deletedTask.horizontalHeader()

        headers.setSectionResizeMode(1,QHeaderView.ResizeMode.ResizeToContents)
        headers.setSectionResizeMode(0,QHeaderView.ResizeMode.Stretch)

        delLayout.addWidget(self.deletedTask)

        self.pages.addWidget(delwidget)

    def addTask(self):
        row=self.tasks.rowCount()
        task=self.input.text().strip()
        status="incomplete"
        completeButton=QPushButton()
        icon=str(self.iconPath+"/markAsDone.svg")
        completeButton.setIcon(QIcon(icon))
        completeButton.setIconSize(QSize(25,15))
        completeButton.clicked.connect(lambda _,r=row: self.taskCompleted(r))
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
            self.input.clear()
            self.tasks.resizeRowsToContents()


        self.counter+=1

    def taskCompleted(self,row):        #change to move content to table
        newRow=self.completedTask.rowCount()
        self.completedTask.insertRow(newRow)

        for col in range(self.tasks.columnCount()-1):
            item=self.tasks.takeItem(row,col)
            header=self.completedTask.horizontalHeaderItem(col).text().strip().lower()
            if item:
                if header=='status':
                    self.completedTask.setItem(newRow,1,QTableWidgetItem("Completed"))  
                    print("HEader Status found")                 
                else:
                    self.completedTask.setItem(newRow,col,item)
            

        self.tasks.removeRow(row)
            


app=QApplication(sys.argv)

window=MainWindow()
window.show()

app.exec()