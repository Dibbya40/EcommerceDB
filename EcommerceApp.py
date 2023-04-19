import wx
import mysql.connector
import wx.grid

class EcommerceDBApp(wx.Frame):
    def __init__(self, parent, title):
        super(EcommerceDBApp, self).__init__(parent, title=title, size=(500, 500))
        
        # Set up database connection
        self.cnx = mysql.connector.connect(user='myuser', password='mypassword', host='localhost', database='ecommercedb')
        self.cursor = self.cnx.cursor()

        # Set up user interface
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(self.sizer)
        
        # Create menu bar
        menu_bar = wx.MenuBar()
        
        # Create options menu
        options_menu = wx.Menu()
        self.menu_quit = options_menu.Append(wx.ID_EXIT, "Quit")
        menu_bar.Append(options_menu, "Options")
        
        self.SetMenuBar(menu_bar)
        self.Bind(wx.EVT_MENU, self.on_quit, self.menu_quit)
        
        # Create list of options
        self.options = [
            {"label": "View Administrator Table", "handler": self.view_administrators},
            {"label": "View Customer Table", "handler": self.view_customers},
            {"label": "View Payment Table", "handler": self.view_payments},
            {"label": "View Orders Table", "handler": self.view_orders},
            {"label": "View Products Table", "handler": self.view_products},
            {"label": "View Category Table", "handler": self.view_categories},
            {"label": "Retrieve Orders With Corresponding Customer Information", "handler": self.retrieve_orders},
            {"label": "Quit", "handler": self.on_quit}
        ]
        
        # Create option buttons
        for option in self.options:
            #button = wx.Button(self, label=option["label"])
            button = wx.Button(self.panel, label=option["label"])
            self.sizer.Add(button, 0, wx.ALL, 5)
            button.Bind(wx.EVT_BUTTON, option["handler"])
        
        #self.SetSizer(self.sizer)
        self.Show()
      
    def view_administrators(self, event):
        self.cursor.execute("SELECT * FROM ADMINISTRATOR")
        data = self.cursor.fetchall()
        column_names = [i[0] for i in self.cursor.description]
        self.display_data(data, column_names)

    def view_customers(self, event):
        self.cursor.execute("SELECT * FROM CUSTOMER")
        data = self.cursor.fetchall()
        column_names = [i[0] for i in self.cursor.description]
        self.display_data(data, column_names)

    def view_payments(self, event):
        self.cursor.execute("SELECT * FROM PAYMENT")
        data = self.cursor.fetchall()
        column_names = [i[0] for i in self.cursor.description]
        self.display_data(data, column_names)
    
    def view_orders(self, event):
        self.cursor.execute("SELECT * FROM ORDERS")
        data = self.cursor.fetchall()
        column_names = [i[0] for i in self.cursor.description]
        self.display_data(data, column_names)
    
    def view_products(self, event):
        self.cursor.execute("SELECT * FROM PRODUCTS")
        data = self.cursor.fetchall()
        column_names = [i[0] for i in self.cursor.description]
        self.display_data(data, column_names)

    def view_categories(self, event):
        self.cursor.execute("SELECT * FROM CATEGORY")
        data = self.cursor.fetchall()
        column_names = [i[0] for i in self.cursor.description]
        self.display_data(data, column_names)
    def retrieve_orders(self, event):
        self.cursor.execute("SELECT o.O_ID, o.OrderDate, o.Price, c.Name AS Customer_Name, c.Address FROM ORDERS o INNER JOIN CUSTOMER c ON o.C_ID = c.C_ID;")
        data = self.cursor.fetchall()
        column_names = [i[0] for i in self.cursor.description]
        self.display_data(data, column_names)

    def display_data(self, data, column_names):
        # Clear sizer containing buttons and previous output
        self.sizer.Clear(True)

        # Create table to display data
        table = wx.grid.Grid(self.panel)

        # Set table data
        table.CreateGrid(len(data), len(column_names))
        for i, row in enumerate(data):
            for j, value in enumerate(row):
                table.SetCellValue(i, j, str(value))

        # Set table column names
        for i, name in enumerate(column_names):
            table.SetColLabelValue(i, name)

        # Add table to sizer
        self.sizer.Add(table, 0, wx.ALL, 5)

         # Add buttons back to sizer
        for option in self.options:
            button = wx.Button(self.panel, label=option["label"])
            self.sizer.Add(button, 0, wx.ALL, 5)
            button.Bind(wx.EVT_BUTTON, option["handler"])

        # Refresh sizer layout
        self.panel.Layout()

    def on_quit(self, event):
        self.Close()
    
if __name__ == "__main__":
    app = wx.App()
    EcommerceDBApp(None, title="Ecommerce Database")
    app.MainLoop()
