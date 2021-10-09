import sys
from PyQt5 import QtGui,uic,QtCore
from PyQt5.QtWidgets import *

import mysql.connector 

import datetime


import math
import csv

import matplotlib.pyplot as plt                                #!----ดึง ข้อมูลจาก ตาราง มาใน รูปแบบ  ** กราฟ  **
import numpy as np
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Window(QWidget):     

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    __sum_income = []                                           #!----ประกาศตัวเเปร เเบบ private เพื่อเก็บค่า ผลรวมไว้ สามารถ ** นำไปใช้งานในส่วนการทำงาน ตำเเหน่งอื่นๆได้ **
    __sum_expenses = []
    __sum_total = []

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    #* Main Window หลัก

    def __init__(self):
        super().__init__()

        self = uic.loadUi('test.ui',self)
        self.setWindowTitle('โปรเเกรมคำนวณของร้าน MonkeyMade Screen V 1.0.0')

        self.btn_cal.clicked.connect(self.cal_)                 #!----กดปุ่มไปทำงาน ** def cal_ **  คำนวณราคาสกรีนเสื้อ page 1 | เเละ เเสดงข้อมูล ใน page 2

        self.btn_save.clicked.connect(self.save_)               #!----กดปุ่มไปทำงาน ** def SAVE_ **  บันทึกข้อมูล รายรับขรายจ่าย page 3

        self.btn_g.clicked.connect(self.show_)                  #!----กดปุ่มไปทำงาน ** def show_ **  เเสดง กราฟข้อมูล รูปเเบบเเท่ง page 4

        self.rdg_shirt = QButtonGroup()                         #!----Radio Button
        self.rdg_shirt.addButton(self.rad_1)
        self.rdg_shirt.addButton(self.rad_2)

        #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        stamp_date = datetime.datetime.now()
        dt = stamp_date.strftime('%d/%m/%Y %H:%M:%S')           #!----ตั้งวัน เดือน ปี เวลา
        self.te_time.setText(dt)

        #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        #*----conect DB เพื่อ ให้เเสดง ข้อมูล เมื่อ run program ครั้งเเรก

        list_tbheader = ['วัน-เวลา',                              #!----ตั้งหัว  Header 
                        'รายการสินค้า',
                        'รายรับ',
                        'ค่าใช้จ่ายหลัก',
                        'ค่าใช้จ่ายอื่นๆ',
                        'ยอดรวมคงเหลือ'
                    ]

        self.tbw_.setRowCount(0)
        self.tbw_.setColumnCount(len(list_tbheader))
        self.tbw_.setHorizontalHeaderLabels(list_tbheader)

        account_mydb = mysql.connector.connect(                #!----connect DB
                       host = 'localhost',
                       user = '',
                       password = '',
                       database = 'ledger'

        )

        account_mycursor = account_mydb.cursor()              #!----ตั้ง Cursor เพื่อจัดการหรือเลือก ข้อมูลต่างๆ ใน DATABASE ได้

        account_mycursor.execute("SELECT date_time_ac,name_ac,income_ac,expenses_main_ac,other_expenses_ac,total_ac FROM accountmonkeymadetbw")

        dt_data = account_mycursor.fetchall()


        #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
        #* หาผลรวม ค่ารายรับ-รายจ่าย เเละ เก็บค่าลงตัวเเปร Private __...... 
        
        #!---- 1.หาผลรวม ** ยอดคงเหลือทั้งหมด ** บาท (เเสดง เมื่อ run program ครั้งเเรก)

        sum_total = 0
        for x in dt_data:
            #print(x[-1])                              ## ทดสอบ ปริ้นตัวสุดท้าย ยอดรวม
            sum_total += x[-1]

        self.__sum_total = sum_total                   #?----เก็บค่าไว้ในตัวเเปรเเบบ Privat(__sum_total) เพื่อนำไปกดเรียกเเสดงข้อมูลเเบบ ** กราฟ ** ออกมา

        self.re_total.setText(str(sum_total))          #!----ยัดค่าใส่ไว้ในช่อง ยอดคงเหลือ page 4 GUI

        #*------------------------------------------------------------------------------------------------------------------------------------------

        #!---- 2.หาผลรวม ** รายรับทั้งหมด ** บาท (เเสดง เมื่อ run program ครั้งเเรก)

        sum_income = 0
        for x in dt_data:
            #print(x[2])                               ## ทดสอบ ปริ้นตัวตำเเหน่งที่ 2 คือ ** รายรับ **
            sum_income += x[2]

        self.__sum_income = sum_income                 #?----เก็บค่าไว้ในตัวเเปรเเบบ Privat(__sum_income) เพื่อนำไปกดเรียกเเสดงข้อมูลเเบบ ** กราฟ ** ออกมา

        self.re_income.setText(str(sum_income))         #!----ยัดค่าใส่ไว้ในช่อง ยอดคงเหลือ page 4 GUI

        #*------------------------------------------------------------------------------------------------------------------------------------------

        #!---- 3.หาผลรวม ** รายจ่าย เเละ  ค่าใช้จ่ายอื่นๆ ** บาท (เเสดง เมื่อ run program ครั้งเเรก)

        sum_expenses = 0
        for x in dt_data:
            #print(x[3:5])                               ## ทดสอบ ปริ้นตัวตำเเหน่งที่ 3 เเละ 4 คือ ** รายจ่ายหลัก เเละ ค่าใช้จ่ายอื่น **
            sum_expenses += x[3] + x[4]                  #*----หาผลรวมค่าใช้จ่ายทั้งหมด *** ค่าใช้จ่ายหลัก(x[3]) + ค่าใช้จ่ายอื่นๆ(x[4]) ***

        self.__sum_expenses = sum_expenses               #?----เก็บค่าไว้ในตัวเเปรเเบบ Privat(__sum_income) เพื่อนำไปกดเรียกเเสดงข้อมูลเเบบ ** กราฟ ** ออกมา

        self.re_expenses.setText(str(sum_expenses))         #!----ยัดค่าใส่ไว้ในช่อง ยอดคงเหลือ page 4 GUI

        #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        #*โหลดตารางข้อมูลเก่าเมื่อ run program ครั้งเเรก

        self.__loaddatatotable(self.tbw_,dt_data)

        #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        self.show()
    
    #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    #*  ฟังชั่น กดปุ่ม คำนวณราคาสกรีนเสื้อ

    def cal_(self):
        white_ink = float(self.le_white.text())       
        color_ink = float(self.le_color.text())
        total_ink = white_ink + color_ink

        self.le_total.setText(str(total_ink))

        #*-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        #!!! ส่งเสื้อมาสกรีน  ** คิดค่าสกรีนอย่างเดียว **

        if self.rad_1.isChecked():
            total_price = math.ceil(50 + ((white_ink + color_ink))*25)
            self.line_result.setText(str(total_price) + ' บาท')

            self.textEdit.setText(f'***ใช้น้ำหมึกไป {total_ink} cc***\n**กรณีส่งเสื้อมาสกรีน **\n   -ค่าสกรีนราคา {total_price} บาท\n   -ค่าส่งกลับทาง Flash Express ฟรี')

            if total_ink > 5 :
                result_discount = math.ceil(total_price - ((total_price * 5)/100))
                self.la_result1.setText('5%')
                self.la_result2.setText(str(result_discount) + ' บาท')

                self.textEdit.setText(f'***ใช้น้ำหมึกไป {total_ink} cc***\n**กรณีส่งเสื้อมาสกรีน **\n   -ค่าสกรีนราคา {total_price} บาท\n   -น้ำหมึกเกิน 5 cc ได้ส่วนลด 5% เหลือ {result_discount} บาท\n   -ค่าส่งกลับทาง Flash Express ฟรี')

            if total_ink > 10 :
                result_discount = math.ceil(total_price - ((total_price * 10)/100))
                self.la_result1.setText('10%')
                self.la_result2.setText(str(result_discount) + ' บาท')

                self.textEdit.setText(f'***ใช้น้ำหมึกไป {total_ink} cc***\n**กรณีส่งเสื้อมาสกรีน **\n   -ค่าสกรีนราคา {total_price} บาท\n   -น้ำหมึกเกิน 10 cc ได้ส่วนลด 10% เหลือ {result_discount} บาท\n   -ค่าส่งกลับทาง Flash Express ฟรี')

            if total_ink > 15 :
                result_discount = math.ceil(total_price - ((total_price * 15)/100))
                self.la_result1.setText('15%')
                self.la_result2.setText(str(result_discount) + ' บาท')

                self.textEdit.setText(f'***ใช้น้ำหมึกไป {total_ink} cc***\n**กรณีส่งเสื้อมาสกรีน **\n   -ค่าสกรีนราคา {total_price} บาท\n   -น้ำหมึกเกิน 15 cc ได้ส่วนลด 15% เหลือ {result_discount} บาท\n   -ค่าส่งกลับทาง Flash Express ฟรี')

            if total_ink > 20 :
                result_discount = math.ceil(total_price - ((total_price * 20)/100))
                self.la_result1.setText('5%')
                self.la_result2.setText(str(result_discount) + ' บาท')

                self.textEdit.setText(f'***ใช้น้ำหมึกไป {total_ink} cc***\n**กรณีส่งเสื้อมาสกรีน **\n   -ค่าสกรีนราคา {total_price} บาท\n   -น้ำหมึกเกิน 20 cc ได้ส่วนลด 20% เหลือ {result_discount} บาท\n   -ค่าส่งกลับทาง Flash Express ฟรี')

            if total_ink > 25 :
                result_discount = math.ceil(total_price - ((total_price *25)/100))
                self.la_result1.setText('25%')
                self.la_result2.setText(str(result_discount) + ' บาท')

                self.textEdit.setText(f'***ใช้น้ำหมึกไป {total_ink} cc***\n**กรณีส่งเสื้อมาสกรีน **\n   -ค่าสกรีนราคา {total_price} บาท\n   -น้ำหมึกเกิน 25 cc ได้ส่วนลด 25% เหลือ {result_discount} บาท\n   -ค่าส่งกลับทาง Flash Express ฟรี')

        

        #*-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


        #!!! สกรีน ** รวมเสื้อร้าน **


        if self.rad_2.isChecked():
            total_price = math.ceil(285 + ((white_ink + color_ink))*25)
            self.line_result.setText(str(total_price) + ' บาท')

            self.textEdit.setText(f'***ใช้น้ำหมึกไป {total_ink} cc***\n**กรณีสกรีนรวมเสื้อที่ร้าน **\n   -ค่าสกรีนราคา {total_price} บาท\n   -ค่าส่งกลับทาง Flash Express ฟรี')

            if total_ink > 5 :
                result_discount = math.ceil(total_price - ((total_price *5)/100))
                self.la_result1.setText('5%')
                self.la_result2.setText(str(result_discount) + ' บาท')

                self.textEdit.setText(f'***ใช้น้ำหมึกไป {total_ink} cc***\n**กรณีสกรีนรวมเสื้อที่ร้าน **\n\n   -ค่าสกรีนรวมเสื้อราคา {total_price} บาท\n   -น้ำหมึกเกิน 5 cc ได้ส่วนลด 5% เหลือ {result_discount} บาท\n   -ค่าส่งทาง Flash Express ฟรี')

            if total_ink > 10 :
                result_discount = math.ceil(total_price - ((total_price *10)/100))
                self.la_result1.setText('10%')
                self.la_result2.setText(str(result_discount) + ' บาท')

                self.textEdit.setText(f'***ใช้น้ำหมึกไป {total_ink} cc***\n**กรณีสกรีนรวมเสื้อที่ร้าน **\n   -ค่าสกรีนรวมเสื้อราคา {total_price} บาท\n   -น้ำหมึกเกิน 10 cc ได้ส่วนลด 10% เหลือ {result_discount} บาท\n   -ค่าส่งทาง Flash Express ฟรี')

            if total_ink > 15 :
                result_discount = math.ceil(total_price - ((total_price *15)/100))
                self.la_result1.setText('15%')
                self.la_result2.setText(str(result_discount) + ' บาท')

                self.textEdit.setText(f'***ใช้น้ำหมึกไป {total_ink} cc***\n**กรณีสกรีนรวมเสื้อที่ร้าน **\n   -ค่าสกรีนรวมเสื้อราคา {total_price} บาท\n   -น้ำหมึกเกิน 15 cc ได้ส่วนลด 15% เหลือ {result_discount} บาท\n   -ค่าส่งทาง Flash Express ฟรี')

            if total_ink > 20 :
                result_discount = math.ceil(total_price - ((total_price *20)/100))
                self.la_result1.setText('20%')
                self.la_result2.setText(str(result_discount) + ' บาท')

                self.textEdit.setText(f'***ใช้น้ำหมึกไป {total_ink} cc***\n**กรณีสกรีนรวมเสื้อที่ร้าน **\n   -ค่าสกรีนรวมเสื้อราคา {total_price} บาท\n   -น้ำหมึกเกิน 20 cc ได้ส่วนลด 20% เหลือ {result_discount} บาท\n   -ค่าส่งทาง Flash Express ฟรี')

            if total_ink > 25 :
                result_discount = math.ceil(total_price - ((total_price *25)/100))
                self.la_result1.setText('25%')
                self.la_result2.setText(str(result_discount) + ' บาท')

                self.textEdit.setText(f'***ใช้น้ำหมึกไป {total_ink} cc***\n**กรณีสกรีนรวมเสื้อที่ร้าน **\n   -ค่าสกรีนรวมเสื้อราคา {total_price} บาท\n   -น้ำหมึกเกิน 25 cc ได้ส่วนลด 25% เหลือ {result_discount} บาท\n   -ค่าส่งทาง Flash Express ฟรี')

        # self.__clearform()
        #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def __checkformdata(self):

        str_msg = ''

        if(len(self.le_name.text().strip()) == 0):
            
            str_msg += 'กรุณากรอกรายชื้อรายการสินค้า <br/>'

        return str_msg

    #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    #*---Messagebox เเจ้งเตือน เมื่อกด save ***

    def save_(self):

        str_msg_error = self.__checkformdata()

        if(len(str_msg_error) > 0):
            QMessageBox.warning(self,'คำเเนะนำ','กรุณากรอกรายชื่อสินค้า',QMessageBox.OK)

        else:

            stamp_date = datetime.datetime.now()
            dt = stamp_date.strftime('%d/%m/%Y %H:%M:%S')           #!----ตั้งวัน เดือน ปี เวลา
            self.te_time.setText(dt)


            #*----ในส่วนการกรอกข้อมูล รายรับ-รายจ่าย | ลงในตารางเเละ DATABASE  |เเละ โชว์ กราฟ

            list_ = self.le_name.text()
            income_ = float(self.le_income.text())
            expenses_ = float(self.le_expenses.text())
            other_expenses = float(self.le_other.text())

            total_income = income_ - expenses_ - other_expenses

            total_income_result = float(self.re_income.text())          #!----ตั้งตัวเเปรของช่อง **รายรับทั้งหมด GUI** เพิ่ม  เพื่อนำไปคำนวณ เมื่อ add ค่าใหม่ๆลงมา

            total_expenses_result = float(self.re_expenses.text())      #!----ตั้งตัวเเปรของช่อง **รายจ่ายทั้งหมด GUI** เพิ่ม  เพื่อนำไปคำนวณ เมื่อ add ค่าใหม่ๆลงมา

            total_result = float(self.re_total.text())                  #!----ตั้งตัวเเปรของช่อง **ยอดคงเหลือ GUI** เพิ่ม  เพื่อนำไปคำนวณ เมื่อ add ค่าใหม่ๆลงมา

            #*-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

            #!----การทำงานในการ *** ใส่ข้อมูลลงตาราง ***

            int_newrowindex = self.tbw_.rowCount()
            self.tbw_.setRowCount(int_newrowindex + 1)

            tbwi_cell_1 = QTableWidgetItem(str(dt))
            tbwi_cell_2 = QTableWidgetItem(str(list_))
            tbwi_cell_3 = QTableWidgetItem(str(income_))
            tbwi_cell_4 = QTableWidgetItem(str(expenses_))
            tbwi_cell_5 = QTableWidgetItem(str(other_expenses))
            tbwi_cell_6 = QTableWidgetItem(str(total_income))

            self.tbw_.setItem(int_newrowindex,0,tbwi_cell_1)
            self.tbw_.setItem(int_newrowindex,1,tbwi_cell_2)
            self.tbw_.setItem(int_newrowindex,2,tbwi_cell_3)
            self.tbw_.setItem(int_newrowindex,3,tbwi_cell_4)
            self.tbw_.setItem(int_newrowindex,4,tbwi_cell_5)
            self.tbw_.setItem(int_newrowindex,5,tbwi_cell_6)

            #*-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

            #!----การทำงานในการ *** นำค่าใหม่ที่กรอกมาคำนวณ เเละเเสดงผลในช่อง GUI page 4 ***

            self.re_income.setText(str(income_ + total_income_result))                                   #คำนวณใส่ใน  **ช่องรายรับทั้งหมด**
            self.re_expenses.setText(str(expenses_ + other_expenses + total_expenses_result))           #คำนวณใส่ใน  **ช่องรายจ่ายทั้งหมด**
            self.re_total.setText(str(total_income + total_result))                                     #คำนวณใส่ใน  **ยอดรวมคงเหลือ**

            #!----การทำงานในการ *** นำค่าใหม่ที่กรอกมาคำนวณ เเละเเสดงออกมาเป็น  *** กราฟ *** GUI page 4 ***

            self.__sum_income = income_ + total_income_result                                            #คำนวณเเละเเสดง   *** กราฟ รายรับทั้งหมด ***
            self.__sum_expenses = expenses_ + other_expenses +total_expenses_result                        #คำนวณเเละเเสดง   *** กราฟ รายจ่ายทั้งหมด ***
            self.__sum_total = total_income + total_result                                               #คำนวณเเละเเสดง   *** กราฟ ยอดรวมคงเหลือ ***

            #*-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

            #!----การทำงานในการ *** connect DATABASE ***

            account_mydb = mysql.connector.connect(                #!----connect DB
                       host = 'localhost',
                       user = '',
                       password = '',
                       database = 'ledger'

            )

            account_mycursor = account_mydb.cursor()              #!----ตั้ง Cursor เพื่อจัดการหรือเลือก ข้อมูลต่างๆ ใน DATABASE ได้

            #*-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

            #!----การทำงานในการ *** SAVE ค่าใหม่ลง DATABASE ***

            str_sql = """INSERT INTO accountmonkeymadetbw (date_time_ac,
                                                        name_ac,
                                                        income_ac,
                                                        expenses_main_ac,
                                                        other_expenses_ac,
                                                        total_ac) VALUES (%s,%s,%s,%s,%s,%s)"""

            str_val = (str(dt),str(list_),str(income_),str(expenses_),str(other_expenses),str(total_income))

            account_mycursor.execute(str_sql,str_val)

            account_mydb.commit()

            #*-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

            QMessageBox.information(self,'บันทึกข้อมูล รายรับ-รายจ่าย','บันทึกข้อมูล รายรับ-รายจ่ายเรียบร้อย',QMessageBox.Ok)

            self.__clearform()           #!----เมื่อใส่ข้อมูลเสร็จ ไปทำงานที่ def __clearform(self) จะคืนค่าเป็นช่องว่างให้กรอก

             #*-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            
            #!----การทำงานในการ *** SAVE CSV FILE ***

            with open('save_1.csv','a',newline = '')as f:
                fw = csv.writer(f)
                data = [dt,list_,income_,expenses_,other_expenses,total_income]
                fw.writerow(data)

    #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
   
    #*---ฟังชั่น กดปุ่ม เเสดง *** กราฟข้อมูล รูปเเบบเเท่ง ***
    
    def show_(self):

        subject_ = ['Total-Income','Total-Expenses','Cash Flow']                 #!----สร้างชื่อ เเท่งกราฟ เเต่ละเเท่ง
        money_ =  self.__sum_income,self.__sum_expenses,self.__sum_total         #!----นำข้อมูลจาก Private ___.... ที่เก็บไว้ มาเเสดงเป็น กราฟ
        color_ = ['green','red','blue']                                          #!----ใส่สี ตามลำดับ ของ ** subject_ **

        plt.bar(subject_,money_,color = color_)                                  #!----สร้าง Bar

        plt.xlabel('status',color = 'blue')                                     #!----สร้างชื่อ เเละ ใส่สี  เเนวตั้ง X
        plt.ylabel('Money (Thai Bath)',color = 'red')                            #!----สร้างชื่อ เเละ ใส่สี  เเนวตั้ง Y
        plt.title('Financial Status',color = 'green')                            #!----สร้าง Header ของกราฟ

        plt.show()       #!----ปิดท้าย เพื่อให้เเสดง GUI ออกมา

    #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    #*---ฟังชั่นในส่วนเเสดงข้อมูลรูปแบบตาราง ***

    def __loaddatatotable(self,tbw,dt):

        for row_data in dt:
            self.__addrowtotable(tbw,row_data)

    def __addrowtotable(self,tbw,list_data):

        int_max = len(list_data)
        int_i = 0

        int_newrowindex = tbw.rowCount()
        tbw.setRowCount(int_newrowindex + 1)

        while int_i < int_max:
            tbwi_cell = QTableWidgetItem(str(list_data[int_i]))
            tbw.setItem(int_newrowindex,int_i,tbwi_cell)
            int_i = int_i + 1

    #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ฃ

    #*---เมื่อใส่ข้อมูลเสร็จ ให้คืนค่ากลับเป็น 0 ***

    def __clearform(self):

        self.le_name.clear();
        self.le_income.setText(str(0))
        self.le_expenses.setText(str(0))
        self.le_other.setText(str(0))

        # self.le_white.setText(str(0.0))     
        # self.le_color.setText(str(0.0))

    #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())


