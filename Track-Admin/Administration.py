#Project Header

# Python Libraries
# Graphic Interface
from tkinter import * #Graphical Interface Library
from tkinter import Tk, ttk, messagebox #Graphical Interface Library
import tkinter as tk
from tkinter.filedialog import askopenfilename #Library to Select Machine files
from ttkthemes import ThemedStyle
import customtkinter
import awesometkinter as atk
from PIL import Image, ImageTk #Library for Images with TkInter
# Utilities
from winotify import Notification, audio # Notifications Windows Library
import random as r # Randomize Number Library
import openpyxl # Excel Integration Library
import os # Windows Path Library
import requests # Library for API
import sys # System Library
# Data Base
import psycopg2

class Functions():

    #Function Database
    def TWBD(self):
        # Establish the connection to the database
        self.conn = psycopg2.connect(
            dbname="Track_RPA",
            user="postgres",
            password="senha21890",
            host="localhost",
            port="5432"
        )

        # Create a cursor to run queries
        self.sql = self.conn.cursor()

        # # Run a query
        # self.sql.execute("SELECT * FROM tb_webportal")
        #
        # # Get the results
        # record = self.sql.fetchall()
        # print("Records:", len(record))
        # for row in record:
        #     print(row)

    # Functions Utilities
    def check_login(self):
        # Receives the Value of the User Field
        if self.en_user.get():
            self.Login = self.en_user.get()

        # Receive the Value of the Pass Field
        if self.en_pass.get():
            self.Pass = self.en_pass.get()

        # Verify Administration User
        if self.Login == "admin":
            if self.Pass == "admin":
                for self.Widgets in self.FR1.winfo_children():  # Selects the Child Elements of Frame_01, that is, Labels, Inputs and Buttons.
                    self.Widgets.destroy()  # Destroy all Selected.
                self.FR1.destroy()
                self.Screen_Grid_Portals()  # Calls the Next Screen Function.
            else:
                messagebox.showwarning("Login!", "Incorrect password!")
                return
        else:
            messagebox.showwarning("Login!", "User is not Registered in Administration Track RPA!")
            return

    def call_back(self):
        # Checks the page the user is on to return to the previous one.
        if self.LO == "Screen_GridPortals":
            self.LO = None
            self.FR3.destroy()
            self.FR1.destroy()
            self.Screen_Login()
        elif self.LO == "Screen_Admin":
            self.LO = None
            self.FR3.destroy()
            self.Update = None
            self.Screen_Grid_Portals()
        elif self.LO == "Screen_Help":
            self.LO = None
            self.FR1.destroy()
            self.Screen_Login()
        elif self.LO == "Screen_GridUsers":
            self.LO = None
            self.FR3.destroy()
            self.Screen_Grid_Portals()
        elif self.LO == "Screen_Users":
            self.LO = None
            self.FR1.destroy()
            self.Screen_Grid_Users()

    def call_help(self):

        # Deletes all Elements from Frame 01 and recalls other Elements from Screen 02
        for self.Widgets in self.FR1.winfo_children():  # Selects the Child Elements of Frame_01, that is, Labels, Inputs and Buttons.
            self.Widgets.destroy()  # Destroy all Selected.
        self.Screen_Help()  # Calls the Help Screen Function.

    def save_portal(self):

        # Checks if the fields have been filled in
        if self.en_AT.get():
            self.API_Tk = self.en_AT.get()  # Receive the Value of the API Key
        else:
            messagebox.showwarning("Portal Registration", "API not defined. Please Fill in the Field.")
            return

        if self.en_portal.get():
            self.Portal_Link = self.en_portal.get()  # Receive the Value of the Link Portal
        else:
            messagebox.showwarning("Portal Registration", "Portal Link is not defined. Please Fill in the Field.")
            return

        if self.en_portaln.get():
            self.Portal_Name = self.en_portaln.get()  # Receives the Value of the Name Portal
        else:
            messagebox.showwarning("Portal Registration", "Portal Name is not defined, Please Fill in the Field.")
            return

        if self.en_uuidp.get():
            self.UUID_Client = self.en_uuidp.get()  # Receives the Value of the Name Portal
        else:
            messagebox.showwarning("Portal Registration", "Client is not defined, Please Fill in the Field.")
            return

        # Check if the Portal is already Registered
        self.sql.execute("SELECT * FROM tb_webportal WHERE Link = '" + self.Portal_Link + "' and environment = '" + self.Environment + "'")
        found = self.sql.fetchone()

        #If Registered
        if not found:
            self.sql.execute("SELECT COUNT(*) FROM tb_webportal")
            num_records = self.sql.fetchone()[0]
            if num_records == 0:
                id_webportal = 1
                # Insert in tb_webportal
                self.sql.execute("INSERT INTO tb_webportal (id_client, Portal, Link, API_Token, client_uuid, environment) VALUES ('" + str(id_webportal) + "', '" + self.Portal_Name + "', '" + self.Portal_Link + "', '" + self.API_Tk + "', '" + self.UUID_Client + "', '" + self.Environment + "')")
                self.sql.execute("SELECT COUNT(*) FROM tb_module")
                num_records = self.sql.fetchone()[0]
                if num_records == 0:
                    id_module = 1
                    self.sql.execute("INSERT INTO tb_module (id_module, Link) VALUES ('" + str(id_module) + "', '" + self.Portal_Link + "')")
                else:
                    id_module = num_records + 1
                    self.sql.execute("INSERT INTO tb_module (id_module, Link) VALUES ('" + str(id_module) + "', '" + self.Portal_Link + "')")
            else:
                id_webportal = num_records + 1
                # Insert in tb_webportal
                self.sql.execute("INSERT INTO tb_webportal (id_client, Portal, Link, API_Token, client_uuid, environment) VALUES ('" + str(id_webportal) + "', '" + self.Portal_Name + "', '" + self.Portal_Link + "', '" + self.API_Tk + "', '" + self.UUID_Client + "', '" + self.Environment + "')")
                self.sql.execute("SELECT COUNT(*) FROM tb_module")
                num_records = self.sql.fetchone()[0]
                if num_records == 0:
                    id_module = 1
                    self.sql.execute("INSERT INTO tb_module (id_module, Link) VALUES ('" + str(id_module) + "', '" + self.Portal_Link + "')")
                else:
                    id_module = num_records + 1
                    self.sql.execute("INSERT INTO tb_module (id_module, Link) VALUES ('" + str(id_module) + "', '" + self.Portal_Link + "')")
            messagebox.showwarning("Portal Registration", "Portal Added Successfully!")
        else:
            messagebox.showwarning("Portal Registration", "This Portal, in this Environment, is already registered!")
            return

        # Check CheckBox
        if self.check_partner.get():
            self.sql.execute("UPDATE tb_module SET Mod_Partner='" + "T" + "' WHERE Link='" + self.Portal_Link + "'")
        else:
            self.sql.execute("UPDATE tb_module SET Mod_Partner='" + "F" + "' WHERE Link='" + self.Portal_Link + "'")

        if self.check_product.get():
            self.sql.execute("UPDATE tb_module SET Mod_Product='" + "T" + "' WHERE Link='" + self.Portal_Link + "'")
        else:
            self.sql.execute("UPDATE tb_module SET Mod_Product='" + "F" + "' WHERE Link='" + self.Portal_Link + "'")

        if self.check_receiving.get():
            self.sql.execute("UPDATE tb_module SET Mod_Receiving='" + "T" + "' WHERE Link='" + self.Portal_Link + "'")
        else:
            self.sql.execute("UPDATE tb_module SET Mod_Receiving='" + "F" + "' WHERE Link='" + self.Portal_Link + "'")

        if self.check_out.get():
            self.sql.execute("UPDATE tb_module SET Mod_Outbound='" + "T" + "' WHERE Link='" + self.Portal_Link + "'")
        else:
            self.sql.execute("UPDATE tb_module SET Mod_Outbound='" + "F" + "' WHERE Link='" + self.Portal_Link + "'")

        if self.check_bypicking.get():
            self.sql.execute("UPDATE tb_module SET Mod_ByPicking='" + "T" + "' WHERE Link='" + self.Portal_Link + "'")
            self.sql.execute("UPDATE tb_module SET Mod_RMA='" + "T" + "' WHERE Link='" + self.Portal_Link + "'")
        else:
            self.sql.execute("UPDATE tb_module SET Mod_RMA='" + "F" + "' WHERE Link='" + self.Portal_Link + "'")
            self.sql.execute("UPDATE tb_module SET Mod_ByPicking='" + "F" + "' WHERE Link='" + self.Portal_Link + "'")

        if self.check_container.get():
            self.sql.execute("UPDATE tb_module SET Mod_Containers='" + "T" + "' WHERE Link='" + self.Portal_Link + "'")
        else:
            self.sql.execute("UPDATE tb_module SET Mod_Containers='" + "F" + "' WHERE Link='" + self.Portal_Link + "'")

        if self.check_quarantine.get():
            self.sql.execute("UPDATE tb_module SET Mod_Quarantine='" + "T" + "' WHERE Link='" + self.Portal_Link + "'")
        else:
            self.sql.execute("UPDATE tb_module SET Mod_Quarantine='" + "F" + "' WHERE Link='" + self.Portal_Link + "'")

        if self.check_compack.get():
            self.sql.execute("UPDATE tb_module SET Mod_Com_Pack='" + "T" + "' WHERE Link='" + self.Portal_Link + "'")
        else:
            self.sql.execute("UPDATE tb_module SET Mod_Com_Pack='" + "F" + "' WHERE Link='" + self.Portal_Link + "'")

        if self.check_disporsal.get():
            self.sql.execute("UPDATE tb_module SET Mod_Disporsal='" + "T" + "' WHERE Link='" + self.Portal_Link + "'")
        else:
            self.sql.execute("UPDATE tb_module SET Mod_Disporsal='" + "F" + "' WHERE Link='" + self.Portal_Link + "'")

        if self.check_transformation.get():
            self.sql.execute("UPDATE tb_module SET Mod_Transformation='" + "T" + "' WHERE Link='" + self.Portal_Link + "'")
        else:
            self.sql.execute("UPDATE tb_module SET Mod_Transformation='" + "F" + "' WHERE Link='" + self.Portal_Link + "'")

        if self.check_mgt.get():
            self.sql.execute("UPDATE tb_module SET Mod_Company='" + "T" + "' WHERE Link='" + self.Portal_Link + "'")
        else:
            self.sql.execute("UPDATE tb_module SET Mod_Company='" + "F" + "' WHERE Link='" + self.Portal_Link + "'")

        # We process the Query
        self.conn.commit()

        self.FR3.destroy()

        self.Screen_Grid_Portals()

    def update_portal(self):

        def save_changes():
            # Checks if the fields have been filled in
            if self.en_AT.get():
                self.API_Tk = self.en_AT.get()  # Receive the Value of the API Key
            else:
                messagebox.showwarning("Portal Registration", "API not defined. Please Fill in the Field.")
                return

            if self.en_portal.get():
                self.Portal_Link = self.en_portal.get()  # Receive the Value of the Link Portal
            else:
                messagebox.showwarning("Portal Registration", "Portal Link is not defined. Please Fill in the Field.")
                return

            if self.en_portaln.get():
                self.Portal_Name = self.en_portaln.get()  # Receives the Value of the Name Portal
            else:
                messagebox.showwarning("Portal Registration", "Portal Name is not defined, Please Fill in the Field.")
                return

            if self.en_uuidp.get():
                self.UUID_Client = self.en_uuidp.get()  # Receives the Value of the Name Portal
            else:
                messagebox.showwarning("Portal Registration", "Client is not defined, Please Fill in the Field.")
                return

            self.sql.execute("UPDATE tb_webportal SET Portal = '" + self.Portal_Name + "', Link = '" + self.Portal_Link + "', API_Token = '" + self.API_Tk + "', client_uuid = '" + self.UUID_Client + "', environment = '" + self.Environment + "' WHERE id_client='" + str(self.id) + "'")

            # Check CheckBox
            if self.check_partner.get():
                self.sql.execute("UPDATE tb_module SET Mod_Partner='" + "T" + "' WHERE Link='" + self.Portal_Link + "'")
            else:
                self.sql.execute("UPDATE tb_module SET Mod_Partner='" + "F" + "' WHERE Link='" + self.Portal_Link + "'")

            if self.check_product.get():
                self.sql.execute("UPDATE tb_module SET Mod_Product='" + "T" + "' WHERE Link='" + self.Portal_Link + "'")
            else:
                self.sql.execute("UPDATE tb_module SET Mod_Product='" + "F" + "' WHERE Link='" + self.Portal_Link + "'")

            if self.check_receiving.get():
                self.sql.execute(
                    "UPDATE tb_module SET Mod_Receiving='" + "T" + "' WHERE Link='" + self.Portal_Link + "'")
            else:
                self.sql.execute(
                    "UPDATE tb_module SET Mod_Receiving='" + "F" + "' WHERE Link='" + self.Portal_Link + "'")

            if self.check_out.get():
                self.sql.execute(
                    "UPDATE tb_module SET Mod_Outbound='" + "T" + "' WHERE Link='" + self.Portal_Link + "'")
            else:
                self.sql.execute(
                    "UPDATE tb_module SET Mod_Outbound='" + "F" + "' WHERE Link='" + self.Portal_Link + "'")

            if self.check_bypicking.get():
                self.sql.execute(
                    "UPDATE tb_module SET Mod_ByPicking='" + "T" + "' WHERE Link='" + self.Portal_Link + "'")
                self.sql.execute("UPDATE tb_module SET Mod_RMA='" + "T" + "' WHERE Link='" + self.Portal_Link + "'")
            else:
                self.sql.execute("UPDATE tb_module SET Mod_RMA='" + "F" + "' WHERE Link='" + self.Portal_Link + "'")
                self.sql.execute(
                    "UPDATE tb_module SET Mod_ByPicking='" + "F" + "' WHERE Link='" + self.Portal_Link + "'")

            if self.check_container.get():
                self.sql.execute(
                    "UPDATE tb_module SET Mod_Containers='" + "T" + "' WHERE Link='" + self.Portal_Link + "'")
            else:
                self.sql.execute(
                    "UPDATE tb_module SET Mod_Containers='" + "F" + "' WHERE Link='" + self.Portal_Link + "'")

            if self.check_quarantine.get():
                self.sql.execute(
                    "UPDATE tb_module SET Mod_Quarantine='" + "T" + "' WHERE Link='" + self.Portal_Link + "'")
            else:
                self.sql.execute(
                    "UPDATE tb_module SET Mod_Quarantine='" + "F" + "' WHERE Link='" + self.Portal_Link + "'")

            if self.check_compack.get():
                self.sql.execute(
                    "UPDATE tb_module SET Mod_Com_Pack='" + "T" + "' WHERE Link='" + self.Portal_Link + "'")
            else:
                self.sql.execute(
                    "UPDATE tb_module SET Mod_Com_Pack='" + "F" + "' WHERE Link='" + self.Portal_Link + "'")

            if self.check_disporsal.get():
                self.sql.execute(
                    "UPDATE tb_module SET Mod_Disporsal='" + "T" + "' WHERE Link='" + self.Portal_Link + "'")
            else:
                self.sql.execute(
                    "UPDATE tb_module SET Mod_Disporsal='" + "F" + "' WHERE Link='" + self.Portal_Link + "'")

            if self.check_transformation.get():
                self.sql.execute(
                    "UPDATE tb_module SET Mod_Transformation='" + "T" + "' WHERE Link='" + self.Portal_Link + "'")
            else:
                self.sql.execute(
                    "UPDATE tb_module SET Mod_Transformation='" + "F" + "' WHERE Link='" + self.Portal_Link + "'")

            if self.check_mgt.get():
                self.sql.execute("UPDATE tb_module SET Mod_Company='" + "T" + "' WHERE Link='" + self.Portal_Link + "'")
            else:
                self.sql.execute("UPDATE tb_module SET Mod_Company='" + "F" + "' WHERE Link='" + self.Portal_Link + "'")

            # We process the Query
            self.conn.commit()

            messagebox.showwarning("Portal Registration", "Portal Update Successfully!.")
            self.en_portal.config(state="normal")
            self.bt_change.destroy()

            self.FR3.destroy()

            self.Screen_Grid_Portals()

        if self.Update == "Yes":
            self.jan_popup.destroy()
            # Check if the Portal is already Registered
            self.sql.execute("SELECT * FROM tb_webportal WHERE id_client = '" + str(self.id) + "'")
            record = self.sql.fetchone()
            self.en_portaln.insert(0, record[1])
            self.en_portal.insert(0, record[2])
            self.Portal_Link = record[2]
            self.en_AT.insert(0, record[3])
            self.en_uuidp.insert(0, record[4])
            self.en_portal.config(state="readonly")
            sel = record[5]
            if sel == "Test":
                self.opc.set(1)
                self.Environment = "Test"
            elif sel == "Production":
                self.opc.set(2)
                self.Environment = "Production"

            self.sql.execute("SELECT * FROM tb_module WHERE Link = '" + record[2] + "'")
            record = self.sql.fetchone()
            vr = record[2]
            if vr == "T":
                self.check_partner.set(True)  # Inverts the value of the variable
            vr = record[3]
            if vr == "T":
                self.check_product.set(True)  # Inverts the value of the variable
            vr = record[4]
            if vr == "T":
                self.check_receiving.set(True)  # Inverts the value of the variable
            vr = record[5]
            if vr == "T":
                self.check_out.set(True)  # Inverts the value of the variable
            vr = record[6]
            if vr == "T":
                self.check_bypicking.set(True)  # Inverts the value of the variable
            vr = record[7]
            if vr == "T":
                self.check_container.set(True)  # Inverts the value of the variable
            vr = record[8]
            if vr == "T":
                self.check_quarantine.set(True)  # Inverts the value of the variable
            vr = record[10]
            if vr == "T":
                self.check_compack.set(True)  # Inverts the value of the variable
            vr = record[11]
            if vr == "T":
                self.check_disporsal.set(True)  # Inverts the value of the variable
            vr = record[12]
            if vr == "T":
                self.check_transformation.set(True)  # Inverts the value of the variable
            vr = record[13]
            if vr == "T":
                self.check_mgt.set(True)  # Inverts the value of the variable

            # Button Cad_User Style
            estilo = ttk.Style()
            estilo.configure("TButton", foreground='#729898', font=('Sans-serif', 8))
            # Button Back
            self.bt_users = ttk.Button(self.FR3, style="bt_login.TButton", text="Users Admin", command=self.Screen_Grid_Users)
            self.bt_users.place(relx=0.65, rely=0.87, relwidth=0.20)

            # Button Save Style
            estilo = ttk.Style()
            estilo.configure("TButton", foreground='#729898', font=('Sans-serif', 8))
            # Button Save
            self.bt_change = ttk.Button(self.FR3, style="bt_login.TButton", text="Save Changes", command=save_changes)
            self.bt_change.place(relx=0.15, rely=0.87, relwidth=0.20)

            self.Update = None

    def save_user(self):

        # Checks if the fields have been filled in
        if self.en_user_cad.get():
            self.Username = self.en_user_cad.get()  # Receive the Value of the API Key
        else:
            messagebox.showwarning("Users Registration", "Username is not defined. Please Fill in the Field.")
            return

        # Check if the Users is already Registered for the Portal
        self.Username
        self.sql.execute("SELECT * FROM tb_users WHERE email = '" + self.Username + "' and Link = '" + self.Portal_Link + "'")
        found = self.sql.fetchone()
        # If Registered
        if not found:
            self.sql.execute("SELECT id_user FROM tb_users ORDER BY id_user DESC LIMIT 1")
            X = self.sql.fetchone()
            if X:
                Y = X[0]
                id_users = Y + 1
                print(id_users)
                # Run the SQL query to get the data
                self.sql.execute("SELECT * FROM tb_webportal WHERE id_client = '" + str(self.id) + "'")
                record = self.sql.fetchone()
                Link = record[2]

                self.sql.execute("INSERT INTO tb_users (id_user, Link, Email) VALUES ('" + str(id_users) + "', '" + Link + "', '" + self.Username + "')")
                self.conn.commit()
            else:
                id_users = 1
                # Run the SQL query to get the data
                self.sql.execute("SELECT * FROM tb_webportal WHERE id_client = '" + str(self.id) + "'")
                record = self.sql.fetchone()
                Link = record[2]

                self.sql.execute("INSERT INTO tb_users (id_user, Link, Email) VALUES ('" + str(id_users) + "', '" + Link + "', '" + self.Username + "')")
                self.conn.commit()
                messagebox.showwarning("User Registration", "User Added Successfully!.")
        else:
            self.Update_User = "Yes"

        self.FR1.destroy()

        self.update_users_grid()

    def update_user(self):

        if self.Update_User == "Yes":
            self.jan_popup.destroy()
            # Check if the Portal is already Registered
            self.sql.execute("SELECT * FROM tb_users WHERE id_user= '" + str(self.id) + "'")
            record = self.sql.fetchone()
            self.en_portaln.insert(0, record[1])
            self.en_portal.insert(0, record[2])
            self.en_AT.insert(0, record[3])
            self.en_portal.config(state="readonly")

    def update_portals_grid(self):
        # Clear existing DataGrid data
        if tree:
            for row in tree.get_children():
                tree.delete(row)

            # Run the SQL query to get the data
            self.sql.execute("SELECT * FROM tb_webportal")
            record = self.sql.fetchall()

            # Insert data into the DataGrid
            for row in record:
                tree.insert("", "end", text=row[0], values=(row[1], row[2]))

    def update_users_grid(self):
        # Clear existing DataGrid data
        if tree:
            for row in tree.get_children():
                tree.delete(row)

            # Run the SQL query to get the data
            self.sql.execute("SELECT * FROM tb_webportal WHERE id_client = '" + str(self.id) + "'")
            record = self.sql.fetchone()
            Link = record[2]

            # Run the SQL query to get the data
            self.sql.execute("SELECT * FROM tb_users WHERE Link = '" + Link + "'")
            record = self.sql.fetchall()

            # Insert data into the DataGrid
            for row in record:
                tree.insert("", "end", text=row[0], values=(row[1], row[2]))

        self.LO = "Screen_GridUsers"

    def select_radiobutton(self):
        select = self.opc.get()
        if select == 1:
            self.Environment = "Test"
        elif select == 2:
            self.Environment = "Production"

    # Functions of Screen Builds

    def Screen_Help(self):
        # Frames in Screen
        estilo = ttk.Style()
        estilo.configure("TFrame", bd=0, background="#f8f8f8", relief="groove", padding=(10, 10))
        self.FR1 = ttk.Frame(self.Screen, style="TFrame")
        self.FR1.place(relx=0.3, rely=0.35, relwidth=0.4, relheight=0.4)

        self.LO = "Screen_Help"

        self.lb_instruction1 = Label(self.FR1, background='#f8f8f8', bd=4, fg='#729898', font=('Sans-serif', 8, 'bold'), text="This Product was designed to Manage \n  Track-RPA, with all its modules \n and configurations.").place(relx=0.1, rely=0.3)

        image_path = os.path.join(self.Path + "\\Archives\\images\\", "back_icon.png")
        imagem = Image.open(image_path)
        imagem = imagem.resize((13, 13))
        imagem_tk = ImageTk.PhotoImage(imagem)

        self.bt_back = Button(self.FR1, background='#f8f8f8', bd=0, image=imagem_tk, command=self.call_back, compound=CENTER)
        self.bt_back.image = imagem_tk
        self.bt_back.place(relx=0.01, rely=0.85, relwidth=0.13, relheight=0.13)

    def Screen_Login(self):
        self.LO = "Login"

        #Frames in Screen
        estilo = ttk.Style()
        estilo.configure("TFrame", bd=0, background="#f8f8f8", relief="groove", padding=(10, 10))
        self.FR1 = ttk.Frame(self.Screen, style="TFrame")
        self.FR1.place(relx=0.3, rely=0.35, relwidth=0.4, relheight=0.4)

        # Label User
        self.lb_user = Label(self.FR1, background='#f8f8f8', foreground='#729898', text="Username", font=('Sans-serif', 8, 'bold')).place(relx=0.38, rely=0.15)

        # Label Pass
        self.lb_pass = Label(self.FR1, background='#f8f8f8', foreground='#729898', text="Password", font=('Sans-serif', 8, 'bold')).place(relx=0.38, rely=0.40)

        # Input User
        self.en_user = ttk.Entry(self.FR1)
        self.en_user.place(relx=0.15, rely=0.25, relwidth=0.70)

        # Input Pass
        self.en_pass = ttk.Entry(self.FR1, show="*")
        self.en_pass.place(relx=0.15, rely=0.50, relwidth=0.70)

        # Button Style
        estilo = ttk.Style()
        estilo.configure("bt_login.TButton", foreground='#729898', font=('Sans-serif', 8))
        # Button Login
        self.bt_login = ttk.Button(self.FR1, style="bt_login.TButton", text="Next", command=self.check_login)
        self.bt_login.pack(pady=20, padx=50)
        self.bt_login.place(relx=0.27, rely=0.68, relwidth=0.45)

        # Link Help
        link_help = ttk.Label(self.FR1, text="Help", cursor="hand2", background='#f8f8f8', foreground='#729898', font=('Sans-serif', 8))
        link_help.place(relx=0.45, rely=0.85)
        # Adicionar um evento de clique ao rótulo
        link_help.bind("<Button-1>", lambda event: self.call_help())

    def Screen_Grid_Portals(self):
        self.FR1.destroy()
        self.LO = "Screen_GridPortals"
        self.Update = None

        def update_or_delete(event):

            def option(option):
                if option == "Delete Portal":
                    # Get the text of the selected item (in this case, the name)
                    self.id = tree.item(line, "text")

                    # Run the SQL query to get the data
                    self.sql.execute("SELECT * FROM tb_webportal WHERE id_client = '" + str(self.id) + "'")
                    record = self.sql.fetchone()

                    # Delete the record from the database
                    self.sql.execute("DELETE FROM tb_webportal WHERE id_client='" + str(record[0]) + "'")
                    self.sql.execute("DELETE FROM tb_module WHERE Link='" + str(record[2]) + "'")
                    self.conn.commit()
                    messagebox.showwarning("Aviso", "Registro Deletado")

                    # Update the DataGrid
                    self.update_portals_grid()
                    # Close the Popup Window
                    self.jan_popup.destroy()

                elif option == "Update Portal":
                    # Get the text of the selected item (in this case, the name)
                    self.id = tree.item(line, "text")

                    # Run the SQL query to get the data
                    self.sql.execute("SELECT * FROM tb_webportal WHERE id_client = '" + str(self.id) + "'")
                    record = self.sql.fetchone()

                    self.Update = "Yes"

                    self.Screen_Admin()


            line = tree.identify_row(event.y) # Get the Registration ID
            # Checks if it is not an Empty Data Grid Field
            if line:

                # Get the text of the selected item (in this case, the name)
                self.id = tree.item(line, "text")

                # Run the SQL query to get the data
                self.sql.execute("SELECT * FROM tb_webportal WHERE id_client = '" + str(self.id) + "'")
                record = self.sql.fetchone()

                # Create a custom popup window
                self.jan_popup = tk.Toplevel()
                self.jan_popup.resizable(False, False)  # Impede a janela de ser redimensionada

                # Determine the dimensions of the main window
                window_width = 300
                window_height = 160

                # Get screen dimensions
                screen_width = self.jan_popup.winfo_screenwidth()
                screen_height = self.jan_popup.winfo_screenheight()

                # Calculate window position in the center of the screen
                pos_x = (screen_width - window_width) // 2
                pos_y = (screen_height - window_height) // 2

                # Set the window geometry to open in the center of the screen
                self.jan_popup.geometry(f"{window_width}x{window_height}+{pos_x}+{pos_y}")

                # Add a message label
                msg = tk.Label(self.jan_popup, text="What do you want to do with the Portal Registry").place(relx=0.07, rely=0.15)
                msg = tk.Label(self.jan_popup, text=record[1]).place(relx=0.07, rely=0.25)

                # Add custom buttons
                Delete = tk.Button(self.jan_popup, text="Delete Portal", command=lambda: option("Delete Portal")).place(relx=0.35, rely=0.45)

                Update = tk.Button(self.jan_popup, text="Change Customer Information", command=lambda: option("Update Portal")).place(relx=0.20, rely=0.72)


        def create_datagrid():
            global tree

            # Create DataGrid
            tree = ttk.Treeview(self.FR3)
            tree["columns"] = ("Customers", "Link") # Create Columns

            # Sets the column width and aligns to the center
            tree.column("#0", width=30)
            tree.column("Customers", width=200, anchor="center")
            tree.column("Link", width=200, anchor="center")

            # Populate the DataGrid with data from the database
            self.update_portals_grid()

            # Sets column header text
            tree.heading("#0", text="Id")
            tree.heading("Customers", text="Customers")
            tree.heading("Link", text="Link")

            # Align header text to center
            for col in tree["columns"]:
                tree.heading(col, anchor="center")

            # Bind column click event to delete record
            tree.bind("<Button-1>", update_or_delete)

            # DataGrid Size and Dimension Settings
            tree.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.80)

        # Create New Frame
        estilo = ttk.Style()
        estilo.configure("TFrame", bd=0, background="#f8f8f8", relief="groove", padding=(10, 10))
        self.FR3 = ttk.Frame(self.Screen, style="TFrame")
        self.FR3.place(relx=0.15, rely=0.30, relwidth=0.7, relheight=0.60)

        # Back Button Style
        estilo = ttk.Style()
        estilo.configure("bt_back.TButton", foreground='#729898', font=('Sans-serif', 8))
        # Button Login
        self.bt_back = ttk.Button(self.FR3, style="bt_cad.TButton", text="Back To Login", command=self.call_back)
        self.bt_back.place(relx=0.12, rely=0.87, relwidth=0.35)

        # Portal Registration Button Style
        estilo = ttk.Style()
        estilo.configure("bt_cad_portal.TButton", foreground='#729898', font=('Sans-serif', 8))
        # Button Login
        self.bt_cad_portal = ttk.Button(self.FR3, style="bt_cad.TButton", text="Register Portal", command=self.Screen_Admin)
        self.bt_cad_portal.place(relx=0.52, rely=0.87, relwidth=0.35)

        create_datagrid()

    def Screen_Admin(self):

        self.FR3.destroy()
        self.LO = "Screen_Admin"

        self.FR3.destroy()

        estilo = ttk.Style()
        estilo.configure("TFrame", bd=0, background="#f8f8f8", relief="groove", padding=(10, 10))
        self.FR3 = ttk.Frame(self.Screen, style="TFrame")
        self.FR3.place(relx=0.15, rely=0.26, relwidth=0.7, relheight=0.68)

        # # Label Main
        # self.lb_main1 = Label(self.FR3, text="Welcome to TTRX - RPA Administrator", background='#f8f8f8', bd=4, fg='#729898', font=('Sans-serif', 10, 'bold')).place(relx=0.24, rely=0.05)

        # Label API Token
        self.lb_AT = Label(self.FR3, background='#f8f8f8', foreground='#729898', text="API Token:", font=('Sans-serif', 8, 'bold')).place(relx=0.10, rely=0.05)

        # Input API Token
        self.en_AT = ttk.Entry(self.FR3)
        self.en_AT.place(relx=0.28, rely=0.05, relwidth=0.63)

        # Label Portal Link
        self.lb_portal = Label(self.FR3, background='#f8f8f8', foreground='#729898', text="Portal Link:", font=('Sans-serif', 8, 'bold')).place(relx=0.10, rely=0.15)

        # Input Portal Link
        self.en_portal = ttk.Entry(self.FR3)
        self.en_portal.place(relx=0.28, rely=0.15, relwidth=0.63)

        # Label Portal Name
        self.lb_portaln = Label(self.FR3, background='#f8f8f8', foreground='#729898', text="Portal Name:", font=('Sans-serif', 8, 'bold')).place(relx=0.10, rely=0.25)

        # Input Portal Name
        self.en_portaln = ttk.Entry(self.FR3)
        self.en_portaln.place(relx=0.28, rely=0.25, relwidth=0.63)

        # Label UUID_Portal
        self.lb_uuidp = Label(self.FR3, background='#f8f8f8', foreground='#729898', text="UUID Client:", font=('Sans-serif', 8, 'bold')).place(relx=0.10, rely=0.35)

        # Input UUID_Portal
        self.en_uuidp = ttk.Entry(self.FR3)
        self.en_uuidp.place(relx=0.28, rely=0.35, relwidth=0.63)

        # Label RadioButton Environment
        self.lb_uuidp = Label(self.FR3, background='#f8f8f8', foreground='#729898', text="Environment:", font=('Sans-serif', 8, 'bold')).place(relx=0.10, rely=0.45)

        # Input RadioButton Environment
        self.opc = tk.IntVar()

        # Create RadioButton
        self.Test = tk.Radiobutton(self.FR3, text="Test", variable=self.opc, value=1, background='#f8f8f8', foreground='#729898', command=self.select_radiobutton)
        self.Test.place(relx=0.28, rely=0.45)
        self.Production = tk.Radiobutton(self.FR3, text="Production", variable=self.opc, value=2, background='#f8f8f8', foreground='#729898', command=self.select_radiobutton)
        self.Production.place(relx=0.48, rely=0.45)

        # Control variable for the checkbox
        self.check_partner = BooleanVar()
        self.check_product = BooleanVar()
        self.check_receiving = BooleanVar()
        self.check_out = BooleanVar()
        self.check_bypicking = BooleanVar()
        self.check_container = BooleanVar()
        self.check_quarantine = BooleanVar()
        self.check_compack = BooleanVar()
        self.check_disporsal = BooleanVar()
        self.check_transformation = BooleanVar()
        self.check_mgt = BooleanVar()

        # First Column

        # CheckBox Partner
        self.checkbox_tp = Checkbutton(self.FR3, background='#f8f8f8', foreground='#729898', variable=self.check_partner, text="Mod.Partner").place(relx=0.03, rely=0.55)

        # CheckBox Product
        self.checkbox_pd = Checkbutton(self.FR3, background='#f8f8f8', foreground='#729898', variable=self.check_product, text="Mod.Product").place(relx=0.03, rely=0.62)

        # CheckBox Receiving
        self.checkbox_rv = Checkbutton(self.FR3, background='#f8f8f8', foreground='#729898', variable=self.check_receiving, text="Mod.Receiving").place(relx=0.03, rely=0.69)

        # CheckBox Outbound
        self.checkbox_out = Checkbutton(self.FR3, background='#f8f8f8', foreground='#729898', variable=self.check_out, text="Mod.Outbound").place(relx=0.03, rely=0.76)

        # Second Column

        # CheckBox By Picking and RMA
        self.checkbox_bp = Checkbutton(self.FR3, background='#f8f8f8', foreground='#729898', variable=self.check_bypicking, text="Mod.By Picking and RMA").place(relx=0.30, rely=0.55)

        # CheckBox Container
        self.checkbox_ct = Checkbutton(self.FR3, background='#f8f8f8', foreground='#729898', variable=self.check_container, text="Mod.Container").place(relx=0.30, rely=0.62)

        # CheckBox Quarantine
        self.checkbox_qr = Checkbutton(self.FR3, background='#f8f8f8', foreground='#729898', variable=self.check_quarantine, text="Mod.Quarantine").place(relx=0.30, rely=0.69)

        # CheckBox Commission and Packaging
        self.checkbox_cp = Checkbutton(self.FR3, background='#f8f8f8', foreground='#729898', variable=self.check_compack, text="Mod.Commission and Pack").place(relx=0.30, rely=0.76)

        # Third Column

        # CheckBox Disporsal
        self.checkbox_dp = Checkbutton(self.FR3, background='#f8f8f8', foreground='#729898', variable=self.check_disporsal, text="Mod.Disporsal").place(relx=0.70, rely=0.55)

        # CheckBox Transformation
        self.checkbox_trans = Checkbutton(self.FR3, background='#f8f8f8', foreground='#729898', variable=self.check_transformation, text="Mod.Transformation").place(relx=0.70, rely=0.62)

        # CheckBox Company_Mgt
        self.checkbox_cm = Checkbutton(self.FR3, background='#f8f8f8', foreground='#729898', variable=self.check_mgt, text="Mod.Company Mgt").place(relx=0.70, rely=0.69)

        # Button Save Style
        estilo = ttk.Style()
        estilo.configure("TButton", foreground='#729898', font=('Sans-serif', 8))
        # Button Save
        self.bt_save = ttk.Button(self.FR3, style="bt_login.TButton", text="Save Portal", command=self.save_portal)
        self.bt_save.place(relx=0.15, rely=0.87, relwidth=0.20)

        # Button Back Style
        estilo = ttk.Style()
        estilo.configure("TButton", foreground='#729898', font=('Sans-serif', 8))
        # Button Back
        self.bt_back = ttk.Button(self.FR3, style="bt_login.TButton", text="Back", command=self.call_back)
        self.bt_back.place(relx=0.40, rely=0.87, relwidth=0.20)

        self.update_portal()

    def Screen_Users(self):
        self.LO = "Screen_Users"

        #Frames in Screen
        estilo = ttk.Style()
        estilo.configure("TFrame", bd=0, background="#f8f8f8", relief="groove", padding=(10, 10))
        self.FR1 = ttk.Frame(self.Screen, style="TFrame")
        self.FR1.place(relx=0.3, rely=0.35, relwidth=0.4, relheight=0.4)

        self.lb_main1 = Label(self.FR1, text="Registers Users", background='#f8f8f8', bd=4, fg='#729898', font=('Sans-serif', 8, 'bold')).place(relx=0.34, rely=0.09)

        # Label User
        self.lb_user = Label(self.FR1, background='#f8f8f8', foreground='#729898', text="User:", font=('Sans-serif', 8, 'bold')).place(relx=0.12, rely=0.40)

        # Input User
        self.en_user_cad = ttk.Entry(self.FR1)
        self.en_user_cad.place(relx=0.26, rely=0.40, relwidth=0.60)

        # Button Register Style
        estilo = ttk.Style()
        estilo.configure("bt_cad.TButton", foreground='#729898', font=('Sans-serif', 8))
        # Button Login
        self.bt_cad_user = ttk.Button(self.FR1, style="bt_cad.TButton", text="Register User", command=self.save_user).place(relx=0.12, rely=0.73, relwidth=0.35)

        # Button Back Style
        estilo = ttk.Style()
        estilo.configure("bt_cad.TButton", foreground='#729898', font=('Sans-serif', 8))
        # Button Login
        self.bt_back = ttk.Button(self.FR1, style="bt_cad.TButton", text="Back", command=self.call_back).place(relx=0.52, rely=0.73, relwidth=0.35)

    def Screen_Grid_Users(self):
        self.FR3.destroy()
        self.LO = "Screen_GridUsers"

        def delete(event):
            line = tree.identify_row(event.y)  # Get the Registration ID
            # Checks if it is not an Empty Data Grid Field
            if line:
                # Get the text of the selected item (in this case, the name)
                self.id_user_grid = tree.item(line, "text")

                # Run the SQL query to get the data
                self.sql.execute("SELECT * FROM tb_users WHERE id_user = '" + str(self.id_user_grid) + "'")
                record = self.sql.fetchone()

                # Delete the record from the database
                self.sql.execute("DELETE FROM tb_users WHERE id_user ='" + str(record[0]) + "'")
                self.conn.commit()
                messagebox.showwarning("Aviso", "Registro Deletado")

                # Update the DataGrid
                self.update_users_grid()

        def create_datagrid():
            global tree

            # Create DataGrid
            tree = ttk.Treeview(self.FR3)
            tree["columns"] = ("Name", "Username")  # Create Columns

            # Sets the column width and aligns to the center
            tree.column("#0", width=30)
            tree.column("Name", width=200, anchor="center")
            tree.column("Username", width=200, anchor="center")

            # Populate the DataGrid with data from the database
            self.update_users_grid()

            # Sets column header text
            tree.heading("#0", text="Id")
            tree.heading("Name", text="Name")
            tree.heading("Username", text="Username")

            # Align header text to center
            for col in tree["columns"]:
                tree.heading(col, anchor="center")

            # Bind column click event to delete record
            tree.bind("<Button-1>", delete)

            # DataGrid Size and Dimension Settings
            tree.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.80)

        # Create New Frame
        estilo = ttk.Style()
        estilo.configure("TFrame", bd=0, background="#f8f8f8", relief="groove", padding=(10, 10))
        self.FR3 = ttk.Frame(self.Screen, style="TFrame")
        self.FR3.place(relx=0.15, rely=0.30, relwidth=0.7, relheight=0.60)

        # Back Button Style
        estilo = ttk.Style()
        estilo.configure("bt_back.TButton", foreground='#729898', font=('Sans-serif', 8))
        # Button Login
        self.bt_back = ttk.Button(self.FR3, style="bt_cad.TButton", text="Back To Grid Portals", command=self.call_back)
        self.bt_back.place(relx=0.12, rely=0.87, relwidth=0.35)

        # Portal Registration Button Style
        estilo = ttk.Style()
        estilo.configure("bt_cad_portal.TButton", foreground='#729898', font=('Sans-serif', 8))
        # Button Login
        self.bt_cad_user = ttk.Button(self.FR3, style="bt_cad.TButton", text="Register User",command=self.Screen_Users)
        self.bt_cad_user.place(relx=0.52, rely=0.87, relwidth=0.35)

        create_datagrid()

class App(Functions):

    #Method Initialized When Calling the Class App

    def __init__(self):
        self.TWBD()
        self.Path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
        self.Screen() #Calls the TKInter Function that Generates the First Screen
        self.Frames() #Function that Generates Frames within Screen 01
        self.Widgets() #Screen that Generates Widgets
        self.Screen_Login() #Texts and Buttons
        self.Screen.mainloop() #Keep Screen 01 in the Loop

    #Definition of Screen 01 Attributes
    def Screen(self):
        self.Screen = Tk()
        self.Screen.title("Administration Track RPA")  # Create Text in the Top Bar of the Window
        self.Screen.configure(background="#f8f8f8")  # Color in Background
        self.Screen.resizable(False, False)  # Screen Responsiveness. If the First Argument is False, it does not allow the Width to be changed. If the Second Argument is False, it does not allow the Height to be changed.

        # Determine the dimensions of the main window
        window_width = 700
        window_height = 600

        # Get screen dimensions
        screen_width = self.Screen.winfo_screenwidth()
        screen_height = self.Screen.winfo_screenheight()

        # Calculate window position in the center of the screen
        pos_x = (screen_width - window_width) // 2
        pos_y = (screen_height - window_height) // 2

        # Set the window geometry to open in the center of the screen
        self.Screen.geometry(f"{window_width}x{window_height}+{pos_x}+{pos_y}")

    #Frame Definition
    def Frames(self):
        #Frame that Contains the Footer
        self.Footer = Frame(self.Screen, bd=0, highlightbackground="#000000", background='#072144', highlightthickness=2)
        self.Footer.place(relx=0, rely=0.95, relwidth=1.0, relheight=0.1)

    #Widgets Definition in Screen 01
    def Widgets(self):
        # Logo
        image_path = os.path.join(self.Path + "\\Archives\\images\\", "Logo_TrackTraceRX.png")
        self.Img = PhotoImage(file=image_path)
        self.Log = Label(self.Screen, image=self.Img, bg="#f8f8f8").place(relx=0.05, rely=0.09, relwidth=0.9, relheight=0.2)

        # Baseboard
        self.lb_base = Label(self.Footer, background='#072144', text="Powered By TrackTraceRX", fg='white', font=('Sans-serif', 8, 'bold')).place(relx=0.38, rely=0.01)

App()