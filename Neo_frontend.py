'''
Created on Dec 21, 2018

@author: afukxs8
'''
from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QLabel,QFormLayout,QTableView,QLCDNumber,QLineEdit,QInputDialog
from PyQt5.QtSql import QSqlDatabase,QSqlQuery,QSqlTableModel
from PyQt5.QtCore import Qt,QTime,QTimer,QDate
import sys
from PyQt5.Qt import QCalendarWidget,QMessageBox


class CRUD(QWidget):
    def __init__(self):
        super().__init__()
        self.iniUI()
    def iniUI(self):
        
        createDBConnection()
        

        time = QTime.currentTime()
        text = time.toString('hh:mm:ss')
        self.lCD_time = QLCDNumber(self)
        self.lCD_time.setDigitCount(25)     # change the number of digits displayed from 5 to 8
        self.lCD_time.setSegmentStyle(QLCDNumber.Flat)
        self.lCD_time.setStyleSheet("QLCDNumber {color: Teal;}") 
        self.lCD_time.setMinimumHeight(40) # change the font size to bigger        
        self.lCD_time.display(text)        
               
        # refresh timer to reset time in lCD_time
        self.refreshTimer = QTimer(self)
        self.refreshTimer.start(1000) # Starts or restarts the timer with a timeout of duration msec milliseconds.
        self.refreshTimer.timeout.connect(self.show_Time) # This signal is emitted when the timer times out.       
       
        bt_add = QPushButton("Add")
        bt_del = QPushButton("Delete")
        bt_clr = QPushButton("Clear Screen")
        bt_sho = QPushButton("Show_Current")
        bt_sho_all = QPushButton("Show_All")
        lb_ID = QLabel("Associate ID #")
        self.ln_ID = QLineEdit()
        self.ln_ID.setMaxLength(6)
        lb_Name = QLabel("Full Name")
        self.ln_Name = QLineEdit()
        self.ln_Name.setMaxLength(30)        
        lb_Desig = QLabel("Designation")
        self.ln_Desig = QLineEdit()
        self.ln_Desig.setMaxLength(15)
        lb_Dob = QLabel("Date of Birth")
        self.lbl = QLineEdit(self)
        self.cal_Dob = QCalendarWidget(self)
        self.cal_Dob.setGridVisible(True)             
        self.cal_Dob.clicked[QDate].connect(self.showDate)
#         self.lb_msg = QMessageBox(self)
#         self.lb_msg.setReadOnly(True)
              
        layout = QFormLayout()
        layout.addWidget(self.lCD_time)
        layout.addWidget(lb_ID)
        layout.addWidget(self.ln_ID)        
        layout.addWidget(lb_Name)
        layout.addWidget(self.ln_Name)
        layout.addWidget(lb_Desig)
        layout.addWidget(self.ln_Desig)
        layout.addWidget(lb_Dob)
        layout.addWidget(self.lbl)
        layout.addWidget(self.cal_Dob)        
        layout.addWidget(bt_add)
        layout.addWidget(bt_del)
        layout.addWidget(bt_clr)
        layout.addWidget(bt_sho)        
        layout.addWidget(bt_sho_all)
        self.ln_ID.setFocus() 
#         layout.addWidget(self.lb_msg)       
        
        bt_add.clicked.connect(self.add_records)
        bt_del.clicked.connect(self.del_records)
        bt_clr.clicked.connect(self.clr_records)
        bt_sho.clicked.connect(self.show_records)
        bt_sho_all.clicked.connect(self.show_all_records)            

        self.tableView = QTableView(self)
        self.tableView.setObjectName("tableView")
        
        layout.addWidget(self.tableView)
        
        self.setLayout(layout)
        self.setWindowTitle("Employee Details form")
        self.setGeometry(100,300,250,450) # x,y, width, height
        self.show()
        
    def showDate(self, date): 
        self.lbl.setText(date.toString("dd-MMM-yyyy"))

    def add_records(self):
        
        emp_id = self.ln_ID.text()
        name = self.ln_Name.text()        
        designation = self.ln_Desig.text()
        dob = self.lbl.text()
        
#             createDBConnection()
        query=QSqlQuery()
        query.prepare("INSERT INTO employee1 (emp_id, name, designation, dob) "
                      "VALUES (:emp_id, :name, :designation, :dob)")

        query.bindValue(":emp_id", emp_id)
        query.bindValue(":name", name)
        query.bindValue(":designation", designation)
        query.bindValue(":dob", dob)
                    
        try:
            if query.exec_():
#                 add_msg = "Row Added"
#                 self.lb_msg.setText(add_msg)
                print("add_records Successful")
                QMessageBox.information(self,'Info','Row Added',QMessageBox.Ok)
#                 self.show_records()
                self.clr_records()
                 
            else:
                err_text = query.lastError().text()
                print("add_records Error: ", err_text)
                QMessageBox.critical(self,'Error',err_text,QMessageBox.Retry)
#                 fail_msg = "Insert Failed !! "
#                 self.lb_msg.SetText(fail_msg)    
        except:
            pass
                
    def show_records(self):  
#         createDBConnection()
        query=QSqlQuery()
        try:
            emp_id_txt = self.ln_ID.text()
        except:
            pass
            
        if emp_id_txt:
            emp_id = int(emp_id_txt)
            query.prepare("SELECT emp_id, name, Designation, dob from employee1 where emp_id = (:emp_id) ")
            query.bindValue(":emp_id", emp_id)
            
            if query.exec_():
                print("show_records Successful")
    #             self.lb_msg.SetText("showing current record !! ")
            else:
                print("show_records Error: ", query.lastError().text())
                model = QSqlTableModel()
                self.show_records_View("Title",model)
            while query.next():
                print ("query show_records " , query.value(0),query.value(1),query.value(2),query.value(3) )
        else:
            QMessageBox.critical(self,'Error','Please Enter Associate ID',QMessageBox.Retry)
            self.ln_ID.setFocus()
        
    def show_all_records(self):  
#         createDBConnection()
        query=QSqlQuery()
        query.exec_("SELECT emp_id, name, Designation, dob from employee1")
        
        if query.exec_():
            print("show_records Successful")
#             all_msg = "Showing ALL records !!"
#             self.lb_msg.SetText(all_msg)            
        else:
            print("show_records Error: ", query.lastError().text())
            
        while query.next():
            print ("query show_records " , query.value(0),query.value(1),query.value(2),query.value(3) )
        model = QSqlTableModel() 
        self.show_records_View("Title",model)
 
                  
    def clr_records(self):  
#         createDBConnection()
      
        print("inside Clear records")
        self.ln_ID.setText("")
        self.ln_Name.setText("")
        self.ln_Desig.setText("")
        print(toString(QDate.currentDate(),"dd-MMM-yyyy"))
#         self.cal_Dob.setText(QDate.currentDate())
#         self.lbl.setText(toString(QDate.currentDate(),"dd-MMM-yyyy")

    def del_records(self):  
#         createDBConnection()
        
        query=QSqlQuery()
        emp_id_txt = self.ln_ID.text()
        emp_id = int(emp_id_txt)
        query.prepare("DELETE from employee1 where emp_id = (:emp_id)  ")
        query.bindValue(":emp_id", emp_id)
        
        if query.exec_():
            print("del_records Successful")
            QMessageBox.information(self,'Info','Row Deleted',QMessageBox.Ok)
            self.show_records() 
        else:
            print("del_records Error: ", query.lastError().text())
            
    def del_records1(self):  
#         createDBConnection()
        query=QSqlQuery()
        query.exec_("DELETE from employee1")
        if query.exec_():
            print("del_records Successful")
            self.show_records() 
        else:
            print("del_records Error: ", query.lastError().text())

    def show_records_View(self,title, model):
        
        model.setTable('employee1')
        model.setEditStrategy(QSqlTableModel.OnFieldChange)
        model.select()
        model.setHeaderData(0, Qt.Horizontal,"emp_id")
        model.setHeaderData(1, Qt.Horizontal,"name")
        model.setHeaderData(2, Qt.Horizontal,"designation")
        model.setHeaderData(3, Qt.Horizontal,"dob")
                    
        self.tableView.setModel(model)
        self.tableView.setWindowTitle(title)
        return self.tableView
    
    def show_Time(self):
        time = QTime.currentTime()
#         print(time)
        text = time.toString('hh:mm:ss')
        self.lCD_time.display(text)
        

def createDBConnection():
    db = QSqlDatabase.addDatabase("QSQLITE") 
    db.setDatabaseName('test1.db')
    if db.open():
        print('created db file!')
        query = QSqlQuery()
        query.exec_("create table IF NOT EXISTS employee1 (emp_id int primary key, "
                "name varchar(30), designation varchar(20), dob date )")
        print('created table employee')
        
        query.exec_("SELECT row_id,emp_id,name from employee1")
#         query.exec_("Delete from employee1")
        print('initial data in employee')
    else:
        print('Unable to create db file!')
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = CRUD()
    sys.exit(app.exec_())
    