from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import datetime
import time
import random
import requests
from sms_report import SMSReport
from Customer_Details import CustomerDetails
import csv
from babel.numbers import *
from babel.dates import *


class SMSEngineWindow:
    def __init__(self, root):
        self.SMS = root
        self.SMS.title("SMS Engine")
        self.SMS.geometry("1600x700+0+0")
        self.SMS.maxsize(1300, 700)
        self.SMS.minsize(1300, 700)

        mydb = sqlite3.connect("SMS_Engine_and_Data.db")
        my_cursor = mydb.cursor()

        ####    Customer Details Table


        my_cursor.execute("""CREATE TABLE if not exists customer_details (
                                        cst_ID integer unique,
                                        cst_name text,
                                        cst_contact integer,
                                        cst_address text,
                                        primary key ('cst_ID'))""")

        mydb.commit()

        ####     Customer SMS Report Table

        my_cursor.execute("""CREATE TABLE if not exists SMS_details_cst (
                                sms_ID integer unique,
                                cst_ID integer,
                                cst_name text,
                                cst_address text,
                                cst_contact integer,
                                sms_context text,
                                sms_date text,
                                sms_time text,
                                primary key ('sms_ID'))""")

        mydb.commit()

        ####      Message prototype Table for Customer

        my_cursor.execute("""CREATE TABLE if not exists message_details_cst (
                                message_ID integer unique,
                                message text,
                                message_creation_date text,
                                message_update_date text,
                                message_update_time text,
                                primary key ('message_ID'))""")

        mydb.commit()
        mydb.close()

        def sms_report_data_Window():
            self.SMS_Report_Window = Toplevel(self.SMS)
            self.app = SMSReport(self.SMS_Report_Window)

        def Customer_Details_Window():
            self.customer_details_window = Toplevel(self.SMS)
            self.app = CustomerDetails(self.customer_details_window)

        def fetch_msg_data_cst():
            try:
                mydb = sqlite3.connect("SMS_Engine_and_Data.db")
                my_cursor = mydb.cursor()

                my_cursor.execute("SELECT * FROM message_details_cst")
                data = my_cursor.fetchall()
                if len(data) >= 1:
                    self.Message_details_table.delete(*self.Message_details_table.get_children())
                    for i in data:
                        self.Message_details_table.insert("", END, values=i)
                    mydb.commit()
                    mydb.close()

                else:
                    self.Message_details_table.delete(*self.Message_details_table.get_children())

            except Exception as e:
                messagebox.showerror("Customer Message Error", f"Something went Wrong in Message Data {str(e)}", parent=self.SMS)

        def get_cst_data(event):
            try:
                cursor_row = self.Employee_and_Customer_details_table.focus()
                content = self.Employee_and_Customer_details_table.item(cursor_row)
                content_value = content["values"]

                self.cst_id_var.set(int(content_value[0]))
                self.Receiver_Name_var.set(content_value[1])
                self.Receiver_Contact_var.set(int(content_value[2]))
                self.cst_contact_var.set(self.Receiver_Contact_var.get())
                self.CST_Address_var.set(content_value[3])

            except Exception as e:
                pass

        def get_msg_data_emp(event):
            try:
                cursor_row = self.Message_details_table.focus()
                content = self.Message_details_table.item(cursor_row)
                content_value = content["values"]

                Message_Composition_label_entry.delete(1.0, END)
                Message_Composition_label_entry.insert(1.0, content_value[1])

            except Exception as e:
                pass

        def send_button_cst():
            try:
                url = "Your SMS API Providers Link"

                querystring = {"authorization": "Your API Key", "message": f"{Message_Composition_label_entry.get(1.0, END)}",
                               "language": "english", "route": "q", "numbers": f"{self.Receiver_Contact_var.get()}"}

                headers = {
                    'cache-control': "no-cache"
                }

                response = requests.request("GET", url, headers=headers, params=querystring)
                messagebox.showinfo("Successful", "SMS has been sent Successfully", parent=self.SMS)

                sms_report_cst()
                reset_button()

            except Exception as e:
                messagebox.showerror("Error", f"Something Went Wrong...! {str(e)}", parent=self.SMS)

        def sms_report_cst():
            try:
                mydb = sqlite3.connect("SMS_Engine_and_Data.db")
                my_cursor = mydb.cursor()

                my_cursor.execute("INSERT INTO SMS_details_cst VALUES (:sms_id, :cst_id, :cst_name, :cst_address, :cst_contact, :sms_context, :sms_date, :sms_time)",
                    {
                        "sms_id": self.SMS_ID_var.get(),
                        "cst_id": self.cst_id_var.get(),
                        "cst_name": self.Receiver_Name_var.get(),
                        "cst_address": self.CST_Address_var.get(),
                        "cst_contact": self.cst_contact_var.get(),
                        "sms_context": Message_Composition_label_entry.get(1.0, END),
                        "sms_date": str(datetime.date.today()),
                        "sms_time": time.strftime("%H:%M:%S", time.localtime())
                    })

                mydb.commit()
                mydb.close()
                messagebox.showinfo("Successful", "SMS data has been saved", parent=self.SMS)

            except Exception as e:
                messagebox.showerror("Error", f"Something went Wrong!{str(e)}", parent=self.SMS)

        def refresh_balance():
            messagebox.showinfo("Balance", f"Your SMS Balance has been Updated. Your Balance is {self.Balance_data}/-", parent=self.SMS)

        def search_cst():
            mydb = sqlite3.connect("SMS_Engine_and_Data.db")
            my_cursor = mydb.cursor()

            try:
                if self.Search_by_table_var.get() == "Customer ID":
                    my_cursor.execute(F"SELECT * FROM customer_details WHERE cst_ID = {self.Search_by_attribute_var.get()}")
                    data = my_cursor.fetchall()
                    if len(data) >= 1:
                        self.Employee_and_Customer_details_table.delete(
                            *self.Employee_and_Customer_details_table.get_children())
                        for i in data:
                            self.Employee_and_Customer_details_table.insert("", END, values=i)
                        mydb.commit()
                    mydb.close()

                elif self.Search_by_table_var.get() == "Name":
                    my_cursor.execute(f"SELECT * FROM customer_details WHERE cst_name = '{self.Search_by_attribute_var.get()}'")
                    data = my_cursor.fetchall()
                    if len(data) >= 1:
                        self.Employee_and_Customer_details_table.delete(
                            *self.Employee_and_Customer_details_table.get_children())
                        for i in data:
                            self.Employee_and_Customer_details_table.insert("", END, values=i)
                        mydb.commit()
                    mydb.close()

                elif self.Search_by_table_var.get() == "Contact":
                    my_cursor.execute(f"SELECT * FROM customer_details WHERE cst_contact = {self.Search_by_attribute_var.get()}")
                    data = my_cursor.fetchall()
                    if len(data) >= 1:
                        self.Employee_and_Customer_details_table.delete(
                            *self.Employee_and_Customer_details_table.get_children())
                        for i in data:
                            self.Employee_and_Customer_details_table.insert("", END, values=i)
                        mydb.commit()
                    mydb.close()

                elif self.Search_by_table_var.get() == "Address":
                    my_cursor.execute(f"SELECT * FROM customer_details WHERE cst_address = '{self.Search_by_attribute_var.get()}'")
                    data = my_cursor.fetchall()
                    if len(data) >= 1:
                        self.Employee_and_Customer_details_table.delete(
                            *self.Employee_and_Customer_details_table.get_children())
                        for i in data:
                            self.Employee_and_Customer_details_table.insert("", END, values=i)
                        mydb.commit()
                    mydb.close()

            except Exception as e:
                messagebox.showerror("Error", f"Something went Wrong {e}", parent=self.SMS)

        def show_all_cst():
            customer_data_fetch()

        def refresh_button():
            check_customer()
            x = random.randint(1000000, 9999999)
            self.SMS_ID_var.set(int(x))
            self.Receiver_Name_var.set("")
            self.Receiver_Contact_var.set(0)
            self.Message_Composition_var.set("")
            self.CST_Address_var.set("")
            self.Assigned_customer_id_var.set("")
            self.Service_date_var.set("YYYY-MM-DD")
            self.Customer_Name_Data_var.set("")
            self.Customer_Contact_Data_var.set("")
            self.Customer_address_data_var.set("")
            self.Search_by_table_var.set("")
            self.Search_by_attribute_var.set("")
            fetch_msg_data_cst()

        def customer_data_fetch():
            mydb = sqlite3.connect("SMS_Engine_and_Data.db")
            my_cursor = mydb.cursor()

            my_cursor.execute("""SELECT * FROM customer_details""")
            data = my_cursor.fetchall()

            if len(data) != 0:
                self.Employee_and_Customer_details_table.delete(
                    *self.Employee_and_Customer_details_table.get_children())
                for i in data:
                    self.Employee_and_Customer_details_table.insert("", END, values=i)
                mydb.commit()
            mydb.close()

        def export_to_exel():
            try:
                path = "customer.csv"
                lst = []
                column_list = ("CST_ID", "Name", "Contact_No", "eMail", "Address", "GSTIN_No", "product_name", "unit_no")
                with open(path, "w", newline='') as myfile:
                    csvwriter = csv.writer(myfile, delimiter=',')
                    for row_id in self.Employee_and_Customer_details_table.get_children():
                        row = self.Employee_and_Customer_details_table.item(row_id, 'values')
                        lst.append(row)
                    lst = list(map(list, lst))
                    lst.insert(0, column_list)
                    for row in lst:
                        csvwriter.writerow(row)

                messagebox.showinfo("Successful", "Data has been Exported Successfully", parent=self.SMS)

            except Exception as e:
                messagebox.showerror("Error", f"Something went Wrong in Exporting Data {str(e)}", parent=self.SMS)

        def check_customer():
            self.Employee_ID_List = []
            mydb = sqlite3.connect("SMS_Engine_and_Data.db")
            my_cursor = mydb.cursor()

            my_cursor.execute("SELECT cst_ID FROM customer_details")
            data = my_cursor.fetchall()

            for i in data:
                for j in i:
                    self.Employee_ID_List.append(j)

            mydb.commit()
            mydb.close()

        def reset_button():
            x = random.randint(1000000, 9999999)
            self.SMS_ID_var.set(x)
            self.Receiver_Name_var.set("")
            self.Receiver_Contact_var.set(0)
            self.CST_Address_var.set("")
            Message_Composition_label_entry.delete(1.0, END)
            self.Assigned_customer_id_var.set("")
            self.Service_date_var.set("YYYY-MM-DD")
            self.Customer_Name_Data_var.set("")
            self.Customer_Contact_Data_var.set("")
            self.Customer_address_data_var.set("")

        def refresh_SMS_ID_button():
            x = random.randint(1000000, 9999999)
            self.SMS_ID_var.set(int(x))

        ##################=================================================== Title Section ============================================================

        self.Employee_ID_List = []
        self.Balance_data = ""

        title_label = Label(self.SMS, text="SMS Engine by APPARKY", font=("Calibre", 20, "bold"), background="gold", foreground="black", border=1, relief=RIDGE)
        title_label.place(x=0, y=0, width=1300, height=50)

        ####============================== Variables ============================================

        self.SMS_ID_var = IntVar()
        x = random.randint(1000000, 9999999)
        self.SMS_ID_var.set(int(x))
        self.Receiver_Name_var = StringVar()
        self.Sender_name_var = StringVar()
        self.Receiver_Contact_var = IntVar()
        self.Message_Composition_var = StringVar()

        self.emp_id_var = IntVar()

        self.Assigned_customer_id_var = IntVar()
        self.Service_date_var = StringVar()
        self.Service_date_var.set("YYYY-MM-DD")

        self.Customer_Name_Data_var = StringVar()
        self.Customer_Contact_Data_var = IntVar()
        self.Customer_address_data_var = StringVar()

        self.cst_id_var = IntVar()
        self.CST_Address_var = StringVar()
        self.cst_contact_var = IntVar()

        self.Search_by_table_var = StringVar()
        self.Search_by_attribute_var = StringVar()

        self.updated_date_var = StringVar()
        self.updated_time_var = StringVar()
        _date = datetime.date.today()
        _time = time.strftime("%H:%M:%S", time.localtime())
        self.updated_date_var.set(str(_date))
        self.updated_time_var.set(_time)

        ###################=============================================== Label Frame =============================================================

        SMS_Engine_label_frame = LabelFrame(self.SMS, text="Receiver & Message Info", border=2, relief=RIDGE, padx=2, font=("Calibre", 9))
        SMS_Engine_label_frame.place(x=5, y=50, width=410, height=645)

        SMS_ID_label = Label(SMS_Engine_label_frame, text="SMS ID", font=("Calibre", 10, "bold"), padx=4, pady=8)
        SMS_ID_label.grid(row=0, column=0, sticky=W)
        SMS_ID_label_entry = ttk.Entry(SMS_Engine_label_frame, textvariable=self.SMS_ID_var, width=13, font=("arial", 10), state="readonly")
        SMS_ID_label_entry.place(x=174, y=5)

        SMS_ID_Refresh_Button = Button(SMS_Engine_label_frame, text="Refresh", font=("Calibre", 10, "bold"), background="gold", foreground="black", width=11, cursor="hand2", command=refresh_SMS_ID_button)
        SMS_ID_Refresh_Button.place(x=293, y=3)

        Receiver_Name_label = Label(SMS_Engine_label_frame, text="Receiver Name", font=("Calibre", 10, "bold"), padx=4, pady=8)
        Receiver_Name_label.grid(row=1, column=0, sticky=W)
        Receiver_Name_label_entry = ttk.Entry(SMS_Engine_label_frame, textvariable=self.Receiver_Name_var, width=30, font=("arial", 10))
        Receiver_Name_label_entry.grid(row=1, column=1, sticky=E, padx=4)

        Receiver_Contact_label = Label(SMS_Engine_label_frame, text="Receiver Contact No.", font=("Calibre", 10, "bold"), padx=4, pady=8)
        Receiver_Contact_label.grid(row=3, column=0, sticky=W)
        Receiver_Contact_label_entry = ttk.Entry(SMS_Engine_label_frame, textvariable=self.Receiver_Contact_var, width=30, font=("arial", 10))
        Receiver_Contact_label_entry.grid(row=3, column=1, sticky=E, padx=4)

        Address_label = Label(SMS_Engine_label_frame, text="Address", font=("Calibre", 10, "bold"), padx=4, pady=8)
        Address_label.grid(row=6, column=0, sticky=W)
        Address_label_entry = ttk.Entry(SMS_Engine_label_frame, textvariable=self.CST_Address_var, width=30, font=("arial", 10))
        Address_label_entry.grid(row=6, column=1, sticky=E, padx=4)

        Message_Composition_label = Label(SMS_Engine_label_frame, text="Message", font=("Calibre", 10, "bold"), padx=4, pady=8)
        Message_Composition_label.grid(row=7, column=0, sticky=W)
        Message_Composition_label_entry = Text(SMS_Engine_label_frame, width=34, height=8, font=("arial", 10))
        Message_Composition_label_entry.grid(row=7, column=1, sticky=E, padx=4)

        check_customer()
        self.Assigned_customer_id_var.set("")


        #######################  ========================================= Customer Details, Employee Details & Employee Service worksheet Details ============================

        Customer_Employee_worksheet_Button_Frame = Frame(SMS_Engine_label_frame, border=2, relief=RIDGE)
        Customer_Employee_worksheet_Button_Frame.place(x=2, y=555, width=400, height=35)

        Reset_Button = Button(Customer_Employee_worksheet_Button_Frame, text="Reset", font=("Calibre", 10, "bold"), background="gold", foreground="black", width=14, cursor="hand2", command=reset_button)
        Reset_Button.place(x=2, y=2)

        Customer_details_Window_Button = Button(Customer_Employee_worksheet_Button_Frame, font=("Calibre", 10, "bold"), width=14, text="Customer Details", background="gold", foreground="black", cursor="hand2", command=Customer_Details_Window)
        Customer_details_Window_Button.place(x=136, y=2)

        Send_Button = Button(Customer_Employee_worksheet_Button_Frame, text="Send", font=("Calibre", 10, "bold"), background="gold", foreground="black", width=14, cursor="hand2", command=send_button_cst)
        Send_Button.place(x=272, y=2)

        ###################==================================================  Some Functional Buttons ===============================================================

        Button_Frame = Frame(SMS_Engine_label_frame, border=2, relief=RIDGE)
        Button_Frame.place(x=2, y=590, width=400, height=35)

        Refresh_Balance_Button = Button(Button_Frame, text="Refresh Balance", font=("Calibre", 10, "bold"), width=14, background="gold", foreground="black", cursor="hand2", command=refresh_balance)
        Refresh_Balance_Button.place(x=2, y=2)

        Export_to_Exel_Button = Button(Button_Frame, text="Export", font=("Calibre", 10, "bold"), width=14, background="gold", foreground="black", cursor="hand2", command=export_to_exel)
        Export_to_Exel_Button.place(x=136, y=2)

        SMS_Report_Button = Button(Button_Frame, text="SMS Report", font=("Calibre", 10, "bold"), width=14, background="gold", foreground="black", cursor="hand2", command=sms_report_data_Window)
        SMS_Report_Button.place(x=272, y=2)

        ############============================================================ Right Frame ===================================================================

        Details_and_search_system_frame = LabelFrame(self.SMS, border=2, relief=RIDGE, text="Customer Details and Search System", font=("Calibre", 9))
        Details_and_search_system_frame.place(x=420, y=50, width=875, height=645)

        Search_by_label = Label(Details_and_search_system_frame, font=("Calibre", 11, "bold"), text="Search By", background="gold", foreground="green")
        Search_by_label.grid(row=0, column=0, sticky=W, padx=8, pady=4)

        Search_by_table_name_combobox = ttk.Combobox(Details_and_search_system_frame, font=("Calibre", 10), width=20, state="readonly", textvariable=self.Search_by_table_var)
        Search_by_table_name_combobox["values"] = ("Customer ID", "Name", "Contact", "Address")
        Search_by_table_name_combobox.set("")
        Search_by_table_name_combobox.grid(row=0, column=1, padx=8, pady=4)

        Search_by_attribute_combobox = ttk.Combobox(Details_and_search_system_frame, font=("Calibre", 10), width=20, textvariable=self.Search_by_attribute_var)
        Search_by_attribute_combobox["values"] = ("")
        Search_by_attribute_combobox.set("")
        Search_by_attribute_combobox.grid(row=0, column=2, padx=8, pady=4)

        Search_button = Button(Details_and_search_system_frame, text="Search", font=("Calibre", 10, "bold"), background="gold", foreground="black", width=10, cursor="hand2", command=search_cst)
        Search_button.place(x=480, y=0)

        ShowAll_button = Button(Details_and_search_system_frame, text="Show All", font=("Calibre", 10, "bold"), background="gold", foreground="black", width=10, cursor="hand2", command=show_all_cst)
        ShowAll_button.place(x=590, y=0)

        refresh_button = Button(Details_and_search_system_frame, text="Refresh", font=("Calibre", 10, "bold"), background="gold", foreground="black", width=10, cursor="hand2", command=refresh_button)
        refresh_button.place(x=700, y=0)

        ######========================================================== Show Data Table for Employee ========================================================================

        Employee_and_Customer_Date_table_frame = Frame(Details_and_search_system_frame, border=2, relief=RIDGE)
        Employee_and_Customer_Date_table_frame.place(x=0, y=40, width=870, height=340)

        self.scroll_bar_X_for_employee_and_customer_table = Scrollbar(Employee_and_Customer_Date_table_frame, orient=HORIZONTAL)
        self.scroll_bar_Y_for_employee_and_customer_table = Scrollbar(Employee_and_Customer_Date_table_frame, orient=VERTICAL)

        self.Employee_and_Customer_details_table = ttk.Treeview(Employee_and_Customer_Date_table_frame, columns=("CST_ID", "Name", "Contact_No", "Address"), xscrollcommand=self.scroll_bar_X_for_employee_and_customer_table.set, yscrollcommand=self.scroll_bar_Y_for_employee_and_customer_table.set)

        self.scroll_bar_X_for_employee_and_customer_table.config(command=self.Employee_and_Customer_details_table.xview)
        self.scroll_bar_Y_for_employee_and_customer_table.config(command=self.Employee_and_Customer_details_table.yview)

        self.Employee_and_Customer_details_table.heading("CST_ID", text="ID", anchor=CENTER)
        self.Employee_and_Customer_details_table.heading("Name", text="Name", anchor=CENTER)
        self.Employee_and_Customer_details_table.heading("Contact_No", text="Contact No", anchor=CENTER)
        self.Employee_and_Customer_details_table.heading("Address", text="Address", anchor=CENTER)

        self.Employee_and_Customer_details_table["show"] = "headings"

        self.Employee_and_Customer_details_table.column("CST_ID", width=80, anchor=CENTER)
        self.Employee_and_Customer_details_table.column("Name", width=150, anchor=CENTER)
        self.Employee_and_Customer_details_table.column("Contact_No", width=110, anchor=CENTER)
        self.Employee_and_Customer_details_table.column("Address", width=180, anchor=CENTER)

        self.Employee_and_Customer_details_table.pack(fill=BOTH, expand=1)
        self.Employee_and_Customer_details_table.bind("<ButtonRelease-1>", get_cst_data)
        customer_data_fetch()

        #### =================================== Message Details Table ==============================================================

        Message_Date_table_frame = Frame(Details_and_search_system_frame, border=2, relief=RIDGE)
        Message_Date_table_frame.place(x=330, y=400, width=520, height=220)

        scroll_bar_x_for_message_table = ttk.Scrollbar(Message_Date_table_frame, orient=HORIZONTAL)
        scroll_bar_y_for_message_table = ttk.Scrollbar(Message_Date_table_frame, orient=VERTICAL)

        self.Message_details_table = ttk.Treeview(Message_Date_table_frame, columns=("MSG_ID", "Message", "Date_Created"), xscrollcommand=scroll_bar_x_for_message_table.set, yscrollcommand=scroll_bar_y_for_message_table.set)
        scroll_bar_x_for_message_table.pack(side=BOTTOM, fill=X)
        scroll_bar_y_for_message_table.pack(side=RIGHT, fill=Y)

        self.Message_details_table.heading("MSG_ID", text="Message ID", anchor=CENTER)
        self.Message_details_table.heading("Message", text="Message", anchor=CENTER)
        self.Message_details_table.heading("Date_Created", text="Date Created", anchor=CENTER)

        self.Message_details_table["show"] = "headings"

        self.Message_details_table.column("MSG_ID", width=80, anchor=CENTER)
        self.Message_details_table.column("Message", width=300, anchor=CENTER)
        self.Message_details_table.column("Date_Created", width=100, anchor=CENTER)

        self.Message_details_table.pack(fill=BOTH, expand=1)
        self.Message_details_table.bind("<ButtonRelease-1>", get_msg_data_emp)
        fetch_msg_data_cst()


if __name__ == '__main__':
    pharmacy = Tk()
    obj = SMSEngineWindow(pharmacy)
    pharmacy.mainloop()
