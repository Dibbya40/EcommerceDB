import wx
import mysql.connector
import wx.grid

class EcommerceDBApp(wx.Frame):
    def __init__(self, parent, title):
        super(EcommerceDBApp, self).__init__(parent, title=title, size=(500, 500))
        
        # Set up database connection
        self.cnx = mysql.connector.connect(user='myuser', password='mypassword', host='localhost', database='ecommerce')
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
            {"label": "Tables In This Database", "handler": self.view_table_names},
            {"label": "View Any Table", "handler": self.on_view_table},
            {"label": "Retrieve Orders With Corresponding Customer Information", "handler": self.retrieve_orders},
            {"label": "Insert Into Any Table", "handler": self.insert},
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
    
    def view_table_names(self, event):
        self.cursor.execute("SHOW TABLES")
        tables = self.cursor.fetchall()
        table_names = [table[0] for table in tables]
        table_names_str = "\n".join(table_names)
        wx.MessageBox(table_names_str, "Table Names", wx.OK | wx.ICON_INFORMATION)

    def on_view_table(self, event):
        table_name = wx.GetTextFromUser("Enter table name:")
        self.cursor.execute(f"SELECT * FROM {table_name}")
        data = self.cursor.fetchall()
        column_names = [i[0] for i in self.cursor.description]
        self.display_data(data, column_names)    
      
    def retrieve_orders(self, event):
        self.cursor.execute("SELECT o.Order_ID, o.OrderDate, o.Price, c.Name AS Customer_Name, c.Address FROM ORDERS o INNER JOIN CUSTOMER c ON o.Cust_ID = c.Cust_ID;")
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
        #table.HideRowLabels() //to hide row labels
     
     
    def insert(self, event):
        # Prompt user to enter table name
        dlg = wx.TextEntryDialog(self.panel, "Enter table name:")
        if dlg.ShowModal() == wx.ID_OK:
            table_name = dlg.GetValue()

        # Retrieve column names for specified table
        self.cursor.execute(f"SELECT * FROM {table_name}")
        columns = [column[0] for column in self.cursor.description]
        self.cursor.fetchall()  # consume the result set
        # Prompt user to enter values for each column
        values = []
        for column in columns:
            dlg = wx.TextEntryDialog(self.panel, f"Enter {column}:")
            if dlg.ShowModal() == wx.ID_OK:
                value = dlg.GetValue()
                values.append(value)

        # Build and execute INSERT query
        query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s' for _ in columns])})"
        self.cursor.execute(query, tuple(values))
        self.cnx.commit()

        wx.MessageBox("Data inserted successfully!", "Success", wx.OK | wx.ICON_INFORMATION)
 
      
    def on_quit(self, event):
        self.Close()
    
if __name__ == "__main__":
    app = wx.App()
    EcommerceDBApp(None, title="Ecommerce Database")
    app.MainLoop()
