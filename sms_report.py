from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import random
import sqlite3
import datetime
import time
from babel.numbers import *
from babel.dates import *


class SMSReport:
    def __init__(self, root):
        self.sms_report = root
        self.sms_report.title("SMS Report")
        self.sms_report.geometry("1300x700+0+0")
        self.sms_report.maxsize(1300, 700)
        self.sms_report.minsize(1300, 700)

        ####   Employee Details Table #1

        mydb = sqlite3.connect("SMS_Engine_and_Data.db")
        my_cursor = mydb.cursor()

        def add_message_cst():
            mydb = sqlite3.connect("SMS_Engine_and_Data.db")
            my_cursor = mydb.cursor()

            try:
                my_cursor.execute(
                    """INSERT INTO message_details_cst VALUES (:msg_id, :msg, :msg_date, :msg_update_date, :msg_update_time)""",
                    {
                        "msg_id": self.MSG_ID_var.get(),
                        "msg": Message_Composition_label_entry.get(1.0, END),
                        "msg_date": datetime.date.today(),
                        "msg_update_date": "YYYY-MM-DD",
                        "msg_update_time": "HH:MM:SS"
                    })

                mydb.commit()
                mydb.close()

                messagebox.showinfo("Successful", "Message has been saved Successfully", parent=self.sms_report)
                fetch_message_data_cst()
                x = random.randint(1000, 9999)
                self.MSG_ID_var.set(int(x))
                Message_Composition_label_entry.delete(1.0, END)

            except Exception as e:
                messagebox.showerror("Error", f"Something went Wrong {str(e)}", parent=self.sms_report)

        def update_message_cst():
            try:
                mydb = sqlite3.connect("SMS_Engine_and_Data.db")
                my_cursor = mydb.cursor()

                my_cursor.execute("""UPDATE message_details_cst SET
                                        message = :msg,
                                        message_update_date = :msg_update,
                                        message_update_time = :msg_uptime

                                        WHERE message_ID = :msg_id""",
                                  {
                                      "msg": Message_Composition_label_entry.get(1.0, END),
                                      "msg_update": str(datetime.date.today()),
                                      "msg_uptime": str(time.strftime("%H:%M:%S", time.localtime())),
                                      "msg_id": self.MSG_ID_var.get()
                                  })

                mydb.commit()
                mydb.close()

                messagebox.showinfo("Update", "Message has been Updated Successfully", parent=self.sms_report)
                fetch_message_data_cst()
                reset_button_cst()

            except Exception as e:
                messagebox.showerror("Error", f"Something went Wrong {str(e)}", parent=self.sms_report)

        def delete_message_cst():
            delete = messagebox.askyesno("Delete?", "Are you sure you want to Delete this Message?",
                                         parent=self.sms_report)
            if delete == 1:
                try:
                    mydb = sqlite3.connect("SMS_Engine_and_Data.db")
                    my_cursor = mydb.cursor()

                    my_cursor.execute(f"DELETE FROM message_details_cst WHERE message_ID = {self.MSG_ID_var.get()}")
                    mydb.commit()
                    mydb.close()
                    messagebox.showinfo("Deleted", "Message has been Deleted Successfully", parent=self.sms_report)

                except Exception as e:
                    messagebox.showerror("Error", f"something went Wrong {str(e)}", parent=self.sms_report)

            else:
                messagebox.showinfo("Info", "You have select No! Your Message is not been Deleted!",
                                    parent=self.sms_report)

            fetch_message_data_cst()
            reset_button_cst()

        def reset_button_cst():
            x = random.randint(1000, 9999)
            self.MSG_ID_var.set(int(x))
            Message_Composition_label_entry.delete(1.0, END)
            fetch_message_data_cst()

        def reset_button_emp():
            x = random.randint(1000, 9999)
            self.MSG_ID_var.set(int(x))
            Message_Composition_label_entry.delete(1.0, END)
            fetch_message_data_emp()

        def fetch_sms_report_data_for_cst():
            mydb = sqlite3.connect("SMS_Engine_and_Data.db")
            my_cursor = mydb.cursor()

            my_cursor.execute("SELECT * FROM SMS_details_cst")
            data = my_cursor.fetchall()
            if len(data) != 0:
                self.SMS_details_table.delete(*self.SMS_details_table.get_children())
                for i in data:
                    self.SMS_details_table.insert("", END, values=i)
                mydb.commit()
            mydb.close()

        def fetch_message_data_emp():
            mydb = sqlite3.connect("SMS_Engine_and_Data.db")
            my_cursor = mydb.cursor()

            my_cursor.execute("SELECT * from message_details_emp")
            data = my_cursor.fetchall()

            if len(data) >= 1:
                self.message_details_table.delete(*self.message_details_table.get_children())
                for i in data:
                    self.message_details_table.insert("", END, values=i)
                    mydb.commit()
                    mydb.close()
            else:
                self.message_details_table.delete(*self.message_details_table.get_children())

        def fetch_message_data_cst():
            mydb = sqlite3.connect("SMS_Engine_and_Data.db")
            my_cursor = mydb.cursor()

            my_cursor.execute("SELECT * from message_details_cst")
            data = my_cursor.fetchall()

            if len(data) >= 1:
                self.message_details_table.delete(*self.message_details_table.get_children())
                for i in data:
                    self.message_details_table.insert("", END, values=i)
                    mydb.commit()
                    mydb.close()
            else:
                self.message_details_table.delete(*self.message_details_table.get_children())

        def get_message_data_cst(event):
            try:
                cursor_row = self.message_details_table.focus()
                content = self.message_details_table.item(cursor_row)
                content_value = content["values"]

                self.MSG_ID_var.set(int(content_value[0]))
                Message_Composition_label_entry.delete(1.0, END)
                Message_Composition_label_entry.insert(1.0, content_value[1])

            except Exception as e:
                pass

        def export_button():
            messagebox.showinfo("Update", "Coming Soon, We are Working on it!", parent=self.sms_report)

        def search_button_cst():
            mydb = sqlite3.connect("SMS_Engine_and_Data.db")
            my_cursor = mydb.cursor()

            try:
                if self.Search_by_table_var.get() == "SMS ID":
                    my_cursor.execute(
                        f"SELECT * FROM SMS_details_cst WHERE sms_ID = {self.Search_by_attribute_var.get()}")
                    data = my_cursor.fetchall()
                    if len(data) >= 1:
                        self.SMS_details_table.delete(*self.SMS_details_table.get_children())
                        for i in data:
                            self.SMS_details_table.insert("", END, values=i)
                        mydb.commit()
                        mydb.close()

                    else:
                        self.SMS_details_table.delete(*self.SMS_details_table.get_children())

                elif self.Search_by_table_var.get() == "Customer ID":
                    my_cursor.execute(
                        f"SELECT * FROM SMS_details_cst WHERE cst_ID = {self.Search_by_attribute_var.get()}")
                    data = my_cursor.fetchall()
                    if len(data) >= 1:
                        self.SMS_details_table.delete(*self.SMS_details_table.get_children())
                        for i in data:
                            self.SMS_details_table.insert("", END, values=i)
                        mydb.commit()
                        mydb.close()

                    else:
                        self.SMS_details_table.delete(*self.SMS_details_table.get_children())

                elif self.Search_by_table_var.get() == "Customer Name":
                    my_cursor.execute(
                        f"SELECT * FROM SMS_details_cst WHERE cst_name = '{self.Search_by_attribute_var.get()}'")
                    data = my_cursor.fetchall()
                    if len(data) >= 1:
                        self.SMS_details_table.delete(*self.SMS_details_table.get_children())
                        for i in data:
                            self.SMS_details_table.insert("", END, values=i)
                        mydb.commit()
                        mydb.close()

                    else:
                        self.SMS_details_table.delete(*self.SMS_details_table.get_children())

                elif self.Search_by_table_var.get() == "Contact No":
                    my_cursor.execute(
                        f"SELECT * FROM SMS_details_cst WHERE cst_contact = {self.Search_by_attribute_var.get()}")
                    data = my_cursor.fetchall()
                    if len(data) >= 1:
                        self.SMS_details_table.delete(*self.SMS_details_table.get_children())
                        for i in data:
                            self.SMS_details_table.insert("", END, values=i)
                        mydb.commit()
                        mydb.close()

                    else:
                        self.SMS_details_table.delete(*self.SMS_details_table.get_children())

            except Exception as e:
                messagebox.showerror("Error", f"Something went Wrong {str(e)}", parent=self.sms_report)

        def show_all_button_cst():
            self.SMS_details_table.delete(*self.SMS_details_table.get_children())
            fetch_sms_report_data_for_cst()

        def refresh_button():
            x = random.randint(1000, 9999)
            self.MSG_ID_var.set(int(x))
            self.Search_by_table_var.set("")
            self.Search_by_attribute_var.set("")
            Message_Composition_label_entry.delete(1.0, END)
            fetch_sms_report_data_for_cst()

        def refresh_SMS_ID_Button():
            x = random.randint(1000, 9999)
            self.MSG_ID_var.set(int(x))

        ##################=================================================== Title Section ============================================================

        sms_report_title_label = Label(self.sms_report, text="SMS Report & Message Details", font=("Calibre", 20, "bold"), background="gold", foreground="black", border=1, relief=RIDGE)
        sms_report_title_label.place(x=0, y=0, width=1300, height=50)

        Export_to_exel_button = Button(self.sms_report, text="Export", font=("Calibre", 15, "bold"), background="gold", foreground="black", border=0, relief=RIDGE, cursor="hand2", command=export_button)
        Export_to_exel_button.place(x=10, y=5, height=40)

        ####============================== Variables ============================================

        self.MSG_ID_var = IntVar()
        x = random.randint(1000, 9999)
        self.MSG_ID_var.set(int(x))
        self.Search_by_table_var = StringVar()
        self.Search_by_attribute_var = StringVar()

        ###################=============================================== Label Frame =============================================================

        SMS_Engine_label_frame = LabelFrame(self.sms_report, text="Customer Message Info", border=2, relief=RIDGE, padx=2, font=("Calibre", 9))
        SMS_Engine_label_frame.place(x=5, y=50, width=330, height=645)

        SMS_ID_label = Label(SMS_Engine_label_frame, text="SMS ID", font=("Calibre", 10, "bold"), padx=4, pady=8)
        SMS_ID_label.grid(row=0, column=0, sticky=W)
        SMS_ID_label_entry = ttk.Entry(SMS_Engine_label_frame, textvariable=self.MSG_ID_var, width=13, font=("arial", 10), state="readonly")
        SMS_ID_label_entry.grid(row=0, column=1, sticky=W, padx=4)

        SMS_ID_Refresh_Button = Button(SMS_Engine_label_frame, text="Refresh", font=("Calibre", 10, "bold"), width=9, background="gold", foreground="black", cursor="hand2", command=refresh_SMS_ID_Button)
        SMS_ID_Refresh_Button.place(x=200, y=3)

        Message_Composition_label = Label(SMS_Engine_label_frame, text="Message", font=("Calibre", 10, "bold"), padx=4, pady=8)
        Message_Composition_label.grid(row=3, column=0, sticky=W)
        Message_Composition_label_entry = Text(SMS_Engine_label_frame, width=30, height=7, font=("arial", 9))
        Message_Composition_label_entry.grid(row=3, column=1, sticky=E, padx=4)

        ##############################======================================================== Message Data Frame ================================================================

        Message_Date_table_frame = Frame(SMS_Engine_label_frame, border=2, relief=RIDGE)
        Message_Date_table_frame.place(x=0, y=227, width=320, height=358)

        scroll_bar_x_for_message_table = ttk.Scrollbar(Message_Date_table_frame, orient=HORIZONTAL)
        scroll_bar_y_for_message_table = ttk.Scrollbar(Message_Date_table_frame, orient=VERTICAL)

        self.message_details_table = ttk.Treeview(Message_Date_table_frame, columns=("ID", "Message"), xscrollcommand=scroll_bar_x_for_message_table.set, yscrollcommand=scroll_bar_y_for_message_table.set)
        scroll_bar_x_for_message_table.pack(side=BOTTOM, fill=X)
        scroll_bar_y_for_message_table.pack(side=RIGHT, fill=Y)

        scroll_bar_x_for_message_table.config(command=self.message_details_table.xview)
        scroll_bar_y_for_message_table.config(command=self.message_details_table.yview)

        self.message_details_table.heading("ID", text="ID", anchor=CENTER)
        self.message_details_table.heading("Message", text="Message", anchor=CENTER)

        self.message_details_table["show"] = "headings"

        self.message_details_table.column("ID", width=30, anchor=CENTER)
        self.message_details_table.column("Message", width=250, anchor=CENTER)

        self.message_details_table.pack(fill=BOTH, expand=1)
        fetch_message_data_cst()
        self.message_details_table.bind("<ButtonRelease-1>", get_message_data_cst)

        ############======================================================= Buttons =========================================================================

        Button_Frame = Frame(SMS_Engine_label_frame, border=2, relief=RIDGE)
        Button_Frame.place(x=3, y=590, width=313, height=35)

        Add_Button = Button(Button_Frame, text="Add", font=("Calibre", 9, "bold"), background="gold", foreground="black", width=8, cursor="hand2", command=add_message_cst)
        Add_Button.grid(row=0, column=0, padx=1, pady=2)

        Update_Button = Button(Button_Frame, text="Update", font=("Calibre", 9, "bold"), background="gold", foreground="black", width=10, cursor="hand2", command=update_message_cst)
        Update_Button.grid(row=0, column=1, padx=1, pady=2)

        Delete_Button = Button(Button_Frame, text="Delete", font=("Calibre", 9, "bold"), background="gold", foreground="black", width=10, cursor="hand2", command=delete_message_cst)
        Delete_Button.grid(row=0, column=2, padx=1, pady=2)

        Reset_button = Button(Button_Frame, text="Reset", font=("Calibre", 9, "bold"), background="gold", foreground="black", width=9, cursor="hand2", command=reset_button_cst)
        Reset_button.grid(row=0, column=3, padx=1, pady=2)

        ############============================================================ Right Frame ===================================================================

        Details_and_search_system_frame = LabelFrame(self.sms_report, border=2, relief=RIDGE, text="Customer SMS Report and Search System", font=("Calibre", 9))
        Details_and_search_system_frame.place(x=340, y=50, width=950, height=645)

        Search_by_label = Label(Details_and_search_system_frame, font=("Calibre", 11, "bold"), text="Search By", background="gold", foreground="green")
        Search_by_label.grid(row=0, column=0, sticky=W, padx=10, pady=4)

        Search_by_table_name_combobox = ttk.Combobox(Details_and_search_system_frame, font=("Calibre", 10), width=20, state="readonly", textvariable=self.Search_by_table_var)
        Search_by_table_name_combobox["values"] = ("SMS ID", "Customer ID", "Customer Name", "Contact No")
        Search_by_table_name_combobox.set("")
        Search_by_table_name_combobox.grid(row=0, column=1, padx=10, pady=4)

        Search_by_attribute_combobox = ttk.Combobox(Details_and_search_system_frame, font=("Calibre", 10), width=20, textvariable=self.Search_by_attribute_var)
        Search_by_attribute_combobox["values"] = ("")
        Search_by_attribute_combobox.set("")
        Search_by_attribute_combobox.grid(row=0, column=2, padx=10, pady=4)

        Search_button = Button(Details_and_search_system_frame, text="Search", font=("Calibre", 10, "bold"), background="gold", foreground="black", width=10, cursor="hand2", command=search_button_cst)
        Search_button.place(x=510, y=0)

        ShowAll_button = Button(Details_and_search_system_frame, text="Show All", font=("Calibre", 10, "bold"), background="gold", foreground="black", width=10, cursor="hand2", command=show_all_button_cst)
        ShowAll_button.place(x=620, y=0)

        refresh_button = Button(Details_and_search_system_frame, text="Refresh", font=("Calibre", 10, "bold"), background="gold", foreground="black", width=10, cursor="hand2", command=refresh_button)
        refresh_button.place(x=730, y=0)

        ######========================================================== Show Data Table for Employee and Customer ========================================================================

        SMS_Date_table_frame = Frame(Details_and_search_system_frame, border=2, relief=RIDGE)
        SMS_Date_table_frame.place(x=0, y=40, width=945, height=580)

        self.scroll_bar_x_for_SMS_table = ttk.Scrollbar(SMS_Date_table_frame, orient=HORIZONTAL)
        self.scroll_bar_y_for_SMS_table = ttk.Scrollbar(SMS_Date_table_frame, orient=VERTICAL)

        self.SMS_details_table = ttk.Treeview(SMS_Date_table_frame, columns=("SMS_ID", "Cst_ID", "Cst_Name", "Cst_Address", "Cst_Contact", "SMS_Context", "SMS_Date", "SMS_Time"), xscrollcommand=self.scroll_bar_x_for_SMS_table.set, yscrollcommand=self.scroll_bar_y_for_SMS_table.set)
        self.scroll_bar_x_for_SMS_table.pack(side=BOTTOM, fill=X)
        self.scroll_bar_y_for_SMS_table.pack(side=RIGHT, fill=Y)

        self.scroll_bar_x_for_SMS_table.config(command=self.SMS_details_table.xview)
        self.scroll_bar_y_for_SMS_table.config(command=self.SMS_details_table.yview)

        self.SMS_details_table.heading("SMS_ID", text="SMS ID", anchor=CENTER)
        self.SMS_details_table.heading("Cst_ID", text="Customer ID", anchor=CENTER)
        self.SMS_details_table.heading("Cst_Name", text="Name", anchor=CENTER)
        self.SMS_details_table.heading("Cst_Address", text="Address", anchor=CENTER)
        self.SMS_details_table.heading("Cst_Contact", text="Contact No.", anchor=CENTER)
        self.SMS_details_table.heading("SMS_Context", text="SMS Context", anchor=CENTER)
        self.SMS_details_table.heading("SMS_Date", text="Date", anchor=CENTER)
        self.SMS_details_table.heading("SMS_Time", text="Time", anchor=CENTER)

        self.SMS_details_table["show"] = "headings"

        self.SMS_details_table.column("SMS_ID", width=60, anchor=CENTER)
        self.SMS_details_table.column("Cst_ID", width=100, anchor=CENTER)
        self.SMS_details_table.column("Cst_Name", width=120, anchor=CENTER)
        self.SMS_details_table.column("Cst_Address", width=200, anchor=CENTER)
        self.SMS_details_table.column("Cst_Contact", width=100, anchor=CENTER)
        self.SMS_details_table.column("SMS_Context", width=300, anchor=CENTER)
        self.SMS_details_table.column("SMS_Date", width=80, anchor=CENTER)
        self.SMS_details_table.column("SMS_Time", width=80, anchor=CENTER)

        self.SMS_details_table.pack(fill=BOTH, expand=1)
        fetch_sms_report_data_for_cst()


if __name__ == '__main__':
    SmsReport = Tk()
    obj = SMSReport(SmsReport)
    SmsReport.mainloop()
