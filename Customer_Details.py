from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import random
import csv
import datetime
import time
from babel.numbers import *
from babel.dates import *


class CustomerDetails:
    def __init__(self, root):
        self.customer_window = root
        self.customer_window.title("Customer Window")
        self.customer_window.geometry("1300x700+0+0")
        self.customer_window.minsize(1300, 700)
        self.customer_window.maxsize(1300, 700)

        ####   Employee Details Table #1

        mydb = sqlite3.connect("SMS_Engine_and_Data.db")
        my_cursor = mydb.cursor()

        def add_button():
            try:
                mydb = sqlite3.connect("SMS_Engine_and_Data.db")
                my_cursor = mydb.cursor()

                if self.Customer_Name_var.get() == "":
                    messagebox.showerror("Name Error", "Name is Missing...! Please fill the Name Section", parent=self.customer_window)

                elif self.Customer_Contact_No_var.get() == "":
                    messagebox.showerror("Contact Error", "Contact is Missing...! Please fill the Contact Section", parent=self.customer_window)

                elif self.Customer_Address_var.get() == "":
                    messagebox.showerror("Address Error", "Address is Missing...! Please fill the Address Section", parent=self.customer_window)
                else:
                    my_cursor.execute(
                        """INSERT INTO customer_details VALUES (:cst_ID, :cst_name, :cst_contact, :cst_address)""",
                        {
                            "cst_ID": self.Customer_ID_var.get(),
                            "cst_name": self.Customer_Name_var.get(),
                            "cst_contact": self.Customer_Contact_No_var.get(),
                            "cst_address": self.Customer_Address_var.get(),
                        })

                    mydb.commit()
                    mydb.close()
                    messagebox.showinfo("Successful", "Data has been Added Successfully", parent=self.customer_window)
                    fetch_customer_data()
                    reset_button()

            except Exception as e:
                messagebox.showerror("Error", f"Something went Wrong {str(e)}", parent=self.customer_window)

        def update_button():
            try:
                mydb = sqlite3.connect("SMS_Engine_and_Data.db")
                my_cursor = mydb.cursor()

                if self.Customer_Name_var.get() == "":
                    messagebox.showerror("Name Error", "Name Section can not be Empty...! Please fill the Name", parent=self.customer_window)

                elif self.Customer_Contact_No_var.get() == "":
                    messagebox.showerror("Contact Error",
                                         "Contact Section can not be Empty...! Please fill the Contact", parent=self.customer_window)

                elif self.Customer_Address_var.get() == "":
                    messagebox.showerror("Address Error",
                                         "Address Section can not be Empty...! Please fill the Address", parent=self.customer_window)

                else:
                    my_cursor.execute("""UPDATE customer_details SET 
                                            cst_name = :Name,
                                            cst_contact = :Contact,
                                            cst_address = :Address
                                            
                                            WHERE cst_ID = :ID""",
                                      {
                                          "Name": self.Customer_Name_var.get(),
                                          "Contact": self.Customer_Contact_No_var.get(),
                                          "Address": self.Customer_Address_var.get(),
                                          "ID": self.Customer_ID_var.get()
                                      })

                    mydb.commit()
                    mydb.close()
                    messagebox.showinfo("Updated", "Your data has been Updated", parent=self.customer_window)
                    fetch_customer_data()
                    reset_button()

            except Exception as e:
                messagebox.showerror("Error", f"Something went Wrong {str(e)}", parent=self.customer_window)

        def delete_button():
            try:
                delete = messagebox.askyesno("Delete?", "Are You Sure, You want to Delete that Data?", parent=self.customer_window)
                if delete == 1:
                    mydb = sqlite3.connect("SMS_Engine_and_Data.db")
                    my_cursor = mydb.cursor()

                    my_cursor.execute(f"DELETE FROM customer_details WHERE cst_ID = {self.Customer_ID_var.get()}")

                    mydb.commit()
                    mydb.close()
                    fetch_customer_data()
                    reset_button()
                    messagebox.showinfo("Deleted", "Your data has been Deleted Successfully", parent=self.customer_window)

                else:
                    messagebox.showinfo("Info", "You have Select No..! Your Data is Secure now.", parent=self.customer_window)
                    reset_button()
                    fetch_customer_data()

            except Exception as e:
                messagebox.showerror("Error", f"Something went Wrong {str(e)}", parent=self.customer_window)

        def reset_button():
            x = random.randint(100000, 999999)
            self.Customer_ID_var.set(int(x))
            self.Customer_Name_var.set("")
            self.Customer_Contact_No_var.set(0)
            self.Customer_Address_var.set("")

        def fetch_customer_data():
            try:
                mydb = sqlite3.connect("SMS_Engine_and_Data.db")
                my_cursor = mydb.cursor()

                my_cursor.execute("""SELECT * FROM customer_details""")
                data = my_cursor.fetchall()
                if len(data) >= 1:
                    self.Customer_details_table.delete(*self.Customer_details_table.get_children())
                    for i in data:
                        self.Customer_details_table.insert("", END, values=i)
                    mydb.commit()
                mydb.close()

            except Exception as e:
                pass

        def get_customer_data(event):
            try:
                cursor_row = self.Customer_details_table.focus()
                content = self.Customer_details_table.item(cursor_row)
                content_value = content["values"]

                self.Customer_ID_var.set(int(content_value[0]))
                self.Customer_Name_var.set(content_value[1])
                self.Customer_Contact_No_var.set(int(content_value[2]))
                self.Customer_Address_var.set(content_value[3])

            except Exception as e:
                pass

        def search_button():
            mydb = sqlite3.connect("SMS_Engine_and_Data.db")
            my_cursor = mydb.cursor()
            '''("ID", "Name", "Contact", "Address")'''

            if self.Search_by_table_var.get() == "ID":
                my_cursor.execute(f"SELECT * FROM customer_details WHERE cst_ID = {self.Search_by_attribute_var.get()}")
                data = my_cursor.fetchall()
                if len(data) >= 1:
                    self.Customer_details_table.delete(*self.Customer_details_table.get_children())
                    for i in data:
                        self.Customer_details_table.insert("", END, values=i)
                    mydb.commit()
                    mydb.close()

                else:
                    messagebox.showerror("Error", "Sorry, No Data Found...!", parent=self.customer_window)

            elif self.Search_by_table_var.get() == "Name":
                my_cursor.execute(
                    f"SELECT * FROM customer_details WHERE cst_name = '{self.Search_by_attribute_var.get()}'")
                data = my_cursor.fetchall()
                if len(data) >= 1:
                    self.Customer_details_table.delete(*self.Customer_details_table.get_children())
                    for i in data:
                        self.Customer_details_table.insert("", END, values=i)
                    mydb.commit()
                    mydb.close()

                else:
                    messagebox.showerror("Error", "Sorry, No Data Found...!", parent=self.customer_window)

            elif self.Search_by_table_var.get() == "Contact":
                my_cursor.execute(
                    f"SELECT * FROM customer_details WHERE cst_contact = {self.Search_by_attribute_var.get()}")
                data = my_cursor.fetchall()
                if len(data) >= 1:
                    self.Customer_details_table.delete(*self.Customer_details_table.get_children())
                    for i in data:
                        self.Customer_details_table.insert("", END, values=i)
                    mydb.commit()
                    mydb.close()

                else:
                    messagebox.showerror("Error", "Sorry, No Data Found...!", parent=self.customer_window)

            elif self.Search_by_table_var.get() == "Address":
                my_cursor.execute(
                    f"SELECT * FROM customer_details WHERE cst_address = '{self.Search_by_attribute_var.get()}'")
                data = my_cursor.fetchall()
                if len(data) >= 1:
                    self.Customer_details_table.delete(*self.Customer_details_table.get_children())
                    for i in data:
                        self.Customer_details_table.insert("", END, values=i)
                    mydb.commit()
                    mydb.close()

                else:
                    messagebox.showerror("Error", "Sorry, No Data Found...!", parent=self.customer_window)

        def show_all_button():
            fetch_customer_data()

        def refresh_button():
            reset_button()
            fetch_customer_data()
            self.Search_by_table_var.set("")
            self.Search_by_attribute_var.set("")

        def search_attribute(event):
            if self.Search_by_table_var.get() == "ID":
                Search_by_attribute_combobox["values"] = ("")
                Search_by_attribute_combobox.set("")

            elif self.Search_by_table_var.get() == "Name":
                Search_by_attribute_combobox["values"] = ("")
                Search_by_attribute_combobox.set("")

            elif self.Search_by_table_var.get() == "Contact":
                Search_by_attribute_combobox["values"] = ("")
                Search_by_attribute_combobox.set("")

            elif self.Search_by_table_var.get() == "Address":
                Search_by_attribute_combobox["values"] = ("")
                Search_by_attribute_combobox.set("")

        def refresh_Customer_ID_button():
            x = random.randint(100000, 999999)
            self.Customer_ID_var.set(int(x))

        def export_data():
            try:
                path = "customer.csv"
                lst = []
                with open(path, "w", newline='') as myfile:
                    csvwriter = csv.writer(myfile, delimiter=',')
                    for row_id in self.Customer_details_table.get_children():
                        row = self.Customer_details_table.item(row_id, 'values')
                        lst.append(row)
                    lst = list(map(list, lst))
                    lst.insert(0, self.customer_column_list)
                    for row in lst:
                        csvwriter.writerow(row)

                messagebox.showinfo("Successful", "Data has been Exported Successfully",
                                    parent=self.customer_window)

            except Exception as e:
                messagebox.showerror("Error", f"Something went Wrong in Exporting Data {str(e)}",
                                     parent=self.customer_window)

        ##################=================================================== Title Section ============================================================

        Employee_Data_title_label = Label(self.customer_window, text="Customer Details", font=("Calibre", 20, "bold"), background="gold", foreground="black", border=1, relief=RIDGE)
        Employee_Data_title_label.place(x=0, y=0, width=1300, height=50)

        Export_to_exel_button = Button(self.customer_window, text="Export", font=("Calibre", 15, "bold"), background="gold", foreground="black", border=0, relief=RIDGE, cursor="hand2", command=export_data)
        Export_to_exel_button.place(x=10, y=5, height=40)

        ####============================== Variables ============================================

        self.Customer_ID_var = IntVar()
        x = random.randint(100000, 999999)
        self.Customer_ID_var.set(int(x))
        self.Customer_Name_var = StringVar()
        self.Customer_Contact_No_var = IntVar()
        self.Customer_Address_var = StringVar()

        self.Search_by_table_var = StringVar()
        self.Search_by_attribute_var = StringVar()

        ###################=============================================== Label Frame =============================================================

        Customer_Details_label_frame = LabelFrame(self.customer_window, text="Customer Details", border=2, relief=RIDGE, padx=2, font=("Calibre", 9))
        Customer_Details_label_frame.place(x=5, y=50, width=333, height=645)

        Customer_ID_label = Label(Customer_Details_label_frame, text="Customer ID", font=("Calibre", 10, "bold"), padx=4, pady=8)
        Customer_ID_label.grid(row=0, column=0, sticky=W)
        Customer_ID_label_entry = ttk.Entry(Customer_Details_label_frame, textvariable=self.Customer_ID_var, width=13, font=("arial", 10), state="readonly")
        Customer_ID_label_entry.grid(row=0, column=1, sticky=W, padx=4)

        Customer_ID_Refresh_Button = Button(Customer_Details_label_frame, text="Refresh", font=("Calibre", 10, "bold"), background="gold", foreground="black", width=11, cursor="hand2", command=refresh_Customer_ID_button)
        Customer_ID_Refresh_Button.place(x=220, y=3)

        Customer_Name_label = Label(Customer_Details_label_frame, text="Customer Name", font=("Calibre", 10, "bold"), padx=4, pady=8)
        Customer_Name_label.grid(row=1, column=0, sticky=W)
        Customer_Name_label_entry = ttk.Entry(Customer_Details_label_frame, textvariable=self.Customer_Name_var, width=25, font=("arial", 10))
        Customer_Name_label_entry.grid(row=1, column=1, sticky=E, padx=4)

        Customer_Contact_No_label = Label(Customer_Details_label_frame, text="Contact No.", font=("Calibre", 10, "bold"), padx=4, pady=8)
        Customer_Contact_No_label.grid(row=2, column=0, sticky=W)
        Customer_Contact_No_label_entry = ttk.Entry(Customer_Details_label_frame, textvariable=self.Customer_Contact_No_var, width=25, font=("arial", 10))
        Customer_Contact_No_label_entry.grid(row=2, column=1, sticky=E, padx=4)

        Customer_address_label = Label(Customer_Details_label_frame, text="Address", font=("Calibre", 10, "bold"), padx=4, pady=8)
        Customer_address_label.grid(row=3, column=0, sticky=W)
        Customer_address_label_entry = ttk.Entry(Customer_Details_label_frame, textvariable=self.Customer_Address_var, width=25, font=("arial", 10))
        Customer_address_label_entry.grid(row=3, column=1, sticky=E, padx=4)

        ############======================================================= Buttons =========================================================================

        Button_Frame = Frame(Customer_Details_label_frame, border=2, relief=RIDGE)
        Button_Frame.place(x=3, y=590, width=313, height=35)

        Add_Button = Button(Button_Frame, text="Add", font=("Calibre", 10, "bold"), background="gold", foreground="black", width=7, cursor="hand2", command=add_button)
        Add_Button.grid(row=0, column=0, padx=1, pady=2)

        Update_Button = Button(Button_Frame, text="Update", font=("Calibre", 10, "bold"), background="gold", foreground="black", width=9, cursor="hand2", command=update_button)
        Update_Button.grid(row=0, column=1, padx=1, pady=2)

        Delete_Button = Button(Button_Frame, text="Delete", font=("Calibre", 10, "bold"), background="gold", foreground="black", width=8, cursor="hand2", command=delete_button)
        Delete_Button.grid(row=0, column=2, padx=1, pady=2)

        Reset_button = Button(Button_Frame, text="Reset", font=("Calibre", 10, "bold"), background="gold", foreground="black", width=8, cursor="hand2", command=reset_button)
        Reset_button.grid(row=0, column=3, padx=1, pady=2)

        ############============================================================ Right Frame ===================================================================

        Details_and_search_system_frame = LabelFrame(self.customer_window, border=2, relief=RIDGE, text="Details and Search System", font=("Calibre", 9))
        Details_and_search_system_frame.place(x=344, y=50, width=950, height=645)

        Search_by_label = Label(Details_and_search_system_frame, font=("Calibre", 11, "bold"), text="Search By", background="gold", foreground="green")
        Search_by_label.grid(row=0, column=0, sticky=W, padx=10, pady=4)

        Search_by_table_name_combobox = ttk.Combobox(Details_and_search_system_frame, font=("Calibre", 10), width=23, state="readonly", textvariable=self.Search_by_table_var)
        Search_by_table_name_combobox["values"] = ("ID", "Name", "Contact", "Address")
        Search_by_table_name_combobox.set("")
        Search_by_table_name_combobox.grid(row=0, column=1, padx=10, pady=4)
        Search_by_table_name_combobox.bind("<<ComboboxSelected>>", search_attribute)

        Search_by_attribute_combobox = ttk.Combobox(Details_and_search_system_frame, font=("Calibre", 10), width=23, textvariable=self.Search_by_attribute_var)
        Search_by_attribute_combobox["values"] = ("")
        Search_by_attribute_combobox.set("")
        Search_by_attribute_combobox.grid(row=0, column=2, padx=10, pady=4)

        Search_button = Button(Details_and_search_system_frame, text="Search", font=("Calibre", 10, "bold"), background="gold", foreground="black", width=10, cursor="hand2", command=search_button)
        Search_button.place(x=510, y=0)

        ShowAll_button = Button(Details_and_search_system_frame, text="Show All", font=("Calibre", 10, "bold"), background="gold", foreground="black", width=10, cursor="hand2", command=show_all_button)
        ShowAll_button.place(x=620, y=0)

        refresh_button = Button(Details_and_search_system_frame, text="Refresh", font=("Calibre", 10, "bold"), background="gold", foreground="black", width=10, cursor="hand2", command=refresh_button)
        refresh_button.place(x=730, y=0)

        ######========================================================== Show Data Table for Employee and Customer ========================================================================

        Customer_Date_table_frame = Frame(Details_and_search_system_frame, border=2, relief=RIDGE)
        Customer_Date_table_frame.place(x=0, y=40, width=945, height=580)

        self.customer_column_list = ("CST_ID", "CST_Name", "Contact", "CST_address")

        self.scroll_bar_x_for_Customer_table = ttk.Scrollbar(Customer_Date_table_frame, orient=HORIZONTAL)
        self.scroll_bar_y_for_Customer_table = ttk.Scrollbar(Customer_Date_table_frame, orient=VERTICAL)

        self.Customer_details_table = ttk.Treeview(Customer_Date_table_frame, columns=self.customer_column_list, xscrollcommand=self.scroll_bar_x_for_Customer_table.set, yscrollcommand=self.scroll_bar_y_for_Customer_table.set)
        self.scroll_bar_x_for_Customer_table.pack(side=BOTTOM, fill=X)
        self.scroll_bar_y_for_Customer_table.pack(side=RIGHT, fill=Y)

        self.scroll_bar_x_for_Customer_table.config(command=self.Customer_details_table.xview)
        self.scroll_bar_y_for_Customer_table.config(command=self.Customer_details_table.yview)

        self.Customer_details_table.heading("CST_ID", text="ID", anchor=CENTER)
        self.Customer_details_table.heading("CST_Name", text="Name", anchor=CENTER)
        self.Customer_details_table.heading("Contact", text="Contact No.", anchor=CENTER)
        self.Customer_details_table.heading("CST_address", text="Address", anchor=CENTER)

        self.Customer_details_table["show"] = "headings"

        self.Customer_details_table.column("CST_ID", width=50, anchor=CENTER)
        self.Customer_details_table.column("CST_Name", width=120, anchor=CENTER)
        self.Customer_details_table.column("Contact", width=100, anchor=CENTER)
        self.Customer_details_table.column("CST_address", width=250, anchor=CENTER)

        self.Customer_details_table.pack(fill=BOTH, expand=1)
        self.Customer_details_table.bind("<ButtonRelease-1>", get_customer_data)
        fetch_customer_data()


if __name__ == '__main__':
    Customer_Window = Tk()
    obj = CustomerDetails(Customer_Window)
    Customer_Window.mainloop()
