import wx
import mysql.connector

class EcommerceDBApp(wx.Frame):
    def __init__(self, parent, title):
        super(EcommerceDBApp, self).__init__(parent, title=title, size=(500, 300))
        
        # Set up database connection
        #self.conn = sqlite3.connect('ecommerce.db')
        #self.cursor = self.conn.cursor()
        cnx = mysql.connector.connect(user='myuser', password='mypassword', host='localhost', database='ecommercedb')
        self.cursor=cnx.cursor();

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
            {"label": "View administrator table", "handler": self.view_administrators},
            {"label": "View customer table", "handler": self.view_customers},
            {"label": "View payment table", "handler": self.view_payments},
            {"label": "View orders table", "handler": self.view_orders},
            {"label": "View products table", "handler": self.view_products},
            {"label": "View category table", "handler": self.view_categories},
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
        self.cursor.execute("SELECT * FROM Administrator")
        data = self.cursor.fetchall()
        self.display_data(data)
    
    def view_customers(self, event):
        self.cursor.execute("SELECT * FROM Customer")
        data = self.cursor.fetchall()
        self.display_data(data)
    
    def view_payments(self, event):
        self.cursor.execute("SELECT * FROM Payment")
        data = self.cursor.fetchall()
        self.display_data(data)
    
    def view_orders(self, event):
        self.cursor.execute("SELECT * FROM Orders")
        data = self.cursor.fetchall()
        self.display_data(data)
    
    def view_products(self, event):
        self.cursor.execute("SELECT * FROM Products")
        data = self.cursor.fetchall()
        self.display_data(data)
    
    def view_categories(self, event):
        self.cursor.execute("SELECT * FROM Category")
        data = self.cursor.fetchall()
        self.display_data(data)
    
    def display_data(self, data):
        dlg = wx.MessageDialog(self, str(data), "Table Data", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
    
    def on_quit(self, event):
        self.Close()
    
if __name__ == "__main__":
    app = wx.App()
    EcommerceDBApp(None, title="Ecommerce Database")
    app.MainLoop()

