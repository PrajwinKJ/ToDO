from PySide6.QtWidgets import (QApplication,QMainWindow,QPushButton,QLineEdit,QWidget,QStackedWidget,QVBoxLayout,QHBoxLayout,QLabel,QTableWidget,QTableWidgetItem,QHeaderView,QCheckBox)
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        mainWidget=QWidget()
        mainLayout=QHBoxLayout(mainWidget)
        self.resize(600,800)

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

        self.tasks=QTableWidget(0,4)
        self.tasks.setHorizontalHeaderLabels(["ID","Tasks","Status","Done"])

        header=self.tasks.horizontalHeader()
        header.setSectionResizeMode(1,QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(0,QHeaderView.ResizeMode.ResizeToContents)
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
        self.completedTask.setHorizontalHeaderLabels(['ID','Tasks','Status'])
        headers=self.completedTask.horizontalHeader()

        headers.setSectionResizeMode(0,QHeaderView.ResizeMode.ResizeToContents)
        headers.setSectionResizeMode(1,QHeaderView.ResizeMode.Stretch)
        headers.setSectionResizeMode(2,QHeaderView.ResizeMode.ResizeToContents)

        self.completedTask.setWordWrap(True)

        doneLayout.addWidget(self.completedTask)

        self.pages.addWidget(doneWidget)

    def delPage(self):
        delwidget=QWidget()
        delLayout=QVBoxLayout(delwidget)
        delLayout.addWidget(QLabel("Deleted Task"))

        self.deletedTask=QTableWidget(0,3)
        self.deletedTask.setHorizontalHeaderLabels(['ID','Task','Status'])

        headers=self.deletedTask.horizontalHeader()

        headers.setSectionResizeMode(0,QHeaderView.ResizeMode.ResizeToContents)
        headers.setSectionResizeMode(1,QHeaderView.ResizeMode.Stretch)
        headers.setSectionResizeMode(2,QHeaderView.ResizeMode.ResizeToContents)

        delLayout.addWidget(self.deletedTask)

        self.pages.addWidget(delwidget)

    def addTask(self):
        row=self.tasks.rowCount()
        task=self.input.text().strip()
        status="incomplete"
        checkbox=QCheckBox()
        checkbox.toggled.connect(lambda check,r=row: self.taskCompleted(r,check))
        if task:
            self.tasks.insertRow(row)
            self.tasks.setItem(row,0,QTableWidgetItem(self.counter))
            self.tasks.setItem(
                row,1,QTableWidgetItem(task)
            )
            self.tasks.setItem(
                row,2,QTableWidgetItem(status)
            )
            self.tasks.setCellWidget(
                row,3,checkbox
            )
            self.input.clear()
            self.tasks.resizeRowsToContents()


        self.counter+=1

    def taskCompleted(self,row,check):        #change to move content to table
        print(f"row: {row} {check}")


app=QApplication(sys.argv)

window=MainWindow()
window.show()

app.exec()