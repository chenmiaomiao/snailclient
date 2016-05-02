# _*_ coding: utf8 _*_

import sys
import time
import datetime
import sqlite3
import matplotlib.pyplot as plt
from getprice import date_interconvert
from PyQt4 import QtGui, QtCore

class Window(QtGui.QMainWindow):
    
    
    def __init__(self):
        self.conn = sqlite3.connect('stock.sqlite3')
        self.cur = self.conn.cursor()
        
        super(Window, self).__init__()
        # self.setGeometry(50, 50, 1280, 800)
        self.setWindowTitle(u'Snail')
        self.setWindowIcon(QtGui.QIcon('snail_120.png'))
        
        self.window_rect = self.frameSize()
        self.window_width = self.window_rect.width()
        self.window_height = self.window_rect.height()     
           
        # position and size of search_widget
        self.widget_search_rect = QtCore.QRect(0, 0, self.window_width, 100)
        # position and size of result_widget
        self.widget_result_rect = QtCore.QRect(0, 100, self.window_width, 500)
        # size of search widgets
        self.search_combo_size = QtCore.QSize(120, 30)
        self.search_input_size = QtCore.QSize(200, 30)
        self.search_button_size = QtCore.QSize(100, 30)
        # position of search widgets
        self.search_combo_move = QtCore.QPoint((self.widget_search_rect.width()-(self.search_combo_size.width()+self.search_input_size.width()+self.search_button_size.width()))/2, 
                                          50
                                          )
        self.search_input_move = QtCore.QPoint((self.widget_search_rect.width()+self.search_combo_size.width()-self.search_input_size.width()-self.search_button_size.width())/2, 
                                          50
                                          )
        self.search_button_move = QtCore.QPoint((self.widget_search_rect.width()+self.search_combo_size.width()+self.search_input_size.width()-self.search_button_size.width())/2, 
                                           50
                                           )
        # result editor position
        self.result_browser_size = QtCore.QSize(self.widget_result_rect.width(), 
                                        self.widget_result_rect.height()*0.8
                                        )
        self.result_browser_move = QtCore.QPoint(0, 0)       
        
        # self.main_widgets = []
        
        # global layout
        self.global_layout = QtGui.QVBoxLayout(self)
        
        # search widget
        self.widget_search = QtGui.QWidget(self)
        # self.widget_search.resize(500, 100)
        # self.widget_search.setGeometry(self.widget_search_rect)
        # mother board of reslut
        self.widget_result = QtGui.QWidget(self)
        # self.widget_result.resize(500, 500)
        # self.widget_result.setGeometry(self.widget_result_rect)
        # global method widget
        # self.widget_result_g_promisholder = QtGui.QWidget(self.widget_result)
        # self.main_widgets = self.object_appending(self.widget_result_g_promisholder, self.main_widgets)
        # self.widget_result_g_npo = QtGui.QWidget(self.widget_result)
        # self.main_widgets = self.object_appending(self.widget_result_g_npo, self.main_widgets)
        
        # put widget in layout
        self.global_layout.addWidget(self.widget_search)
        self.global_layout.addWidget(self.widget_result)
        
        # action of file
        self.act_file_exit = QtGui.QAction('&Exit', self)
        self.act_file_exit.setShortcut('Ctrl+Q')
        self.act_file_exit.setStatusTip('Leave The App')
        self.act_file_exit.triggered.connect(self.close_application)
        # action of global method
        self.act_global_promise = QtGui.QAction('&Promising Holder', self)
        self.act_global_promise.triggered.connect(self.promise_holder)
        self.act_global_npo = QtGui.QAction('&Non-public Offering', self)
        self.act_global_npo.triggered.connect(self.non_public_offering)
        # action of help>style
        self.act_style_all = QtGui.QActionGroup(self)
        self.act_style_plastique= QtGui.QAction('Plastique', self.act_style_all)# , checkable = True)
        self.act_style_cleanlooks = QtGui.QAction('Cleanlooks', self.act_style_all)# , checkable = True)
        self.act_style_all.triggered.connect(self.style_set)
        self.style_actions = (self.act_style_plastique, self.act_style_cleanlooks)
        self.act_style_plastique.trigger()
        # action of help
        self.act_help_about = QtGui.QAction('&About', self)
        self.act_help_about.setStatusTip('About The App')
        self.act_help_about.triggered.connect(self.about)
        
        self.statusBar()
        
        # sub menu of help
        self.sub_help_style = QtGui.QMenu('Style', self)
        self.sub_help_style.addActions(self.style_actions)
        
        # main menu
        self.menu_main = self.menuBar()
        # file menu
        self.menu_file = self.menu_main.addMenu('&File')
        self.menu_file.addAction(self.act_file_exit)
        # global menu
        self.menu_global = self.menu_main.addMenu('&Global')
        self.menu_global.addAction(self.act_global_promise)
        self.menu_global.addAction(self.act_global_npo)
        # help menu
        self.menu_help = self.menu_main.addMenu('&Help')
        self.menu_help.addMenu(self.sub_help_style)
        self.menu_help.addAction(self.act_help_about)

        self.home()
        
    def home(self):
        # method
        self.search_combo = QtGui.QComboBox(self)
        self.search_combo.resize(self.search_combo_size)
        # self.search_combo.move(self.search_combo_move)
        self.search_combo.addItem('Profile')
        self.search_combo.addItem('Number of Holders')
        
        # search input
        self.search_input = QtGui.QLineEdit(self.widget_search)
        self.search_input.resize(self.search_input_size)
        # self.search_input.move(self.search_input_move)
        self.search_input.returnPressed.connect(self.search)
        
        # search button
        self.search_button = QtGui.QPushButton('Search', self.widget_search)
        self.search_button.clicked.connect(self.search)
        self.search_button.resize(self.search_button_size)
        # self.search_button.move(self.search_button_move)
        
        # search area layout
        self.search_layout = QtGui.QHBoxLayout()
        self.search_layout.addWidget(self.search_combo)
        self.search_layout.addWidget(self.search_input)
        self.search_layout.addWidget(self.search_button)
        self.global_layout.addChildLayout(self.search_layout)
        
        self.setLayout(self.global_layout)
                
        # self.show()
        
    def search(self):        
        search_code = self.search_input.text()

        # result widget
        self.widget_result_common = QtGui.QWidget(self.widget_result)
        self.widget_result_common.resize(self.widget_result.width(), self.widget_result.height())
        # self.widget_result_layout = QtGui.QHBoxLayout(self.widget_result)
        # self.widget_result_layout.addWidget(self.widget_result_common)
        # self.main_widgets = self.object_appending(self.widget_result_common, self.main_widgets)
        # self.widget_result_common_layout = QtGui.QHBoxLayout(self.widget_result_common)

        self.cur.execute("SELECT DISTINCT reportdate, holdersnumber FROM Majorholderinfo WHERE stockid = ? AND reportdate <> '-1' AND holdersnumber <> '-1'", ('%s' % search_code, ))
        search_stocks = self.cur.fetchall()
        
        self.result_browse()
        
        dates = []
        holders = []
        for search_stock in search_stocks:
            dates.append(date_interconvert(search_stock[0]))
            holders.append(search_stock[1])
            print str(search_stock).decode('unicode-escape')
            search_stock_str = str(search_stock).decode('unicode-escape')
            self.result_browser.append(search_stock_str)
            self.result_browser.show()
            
            QtGui.QApplication.processEvents()
        
        print dates, holders
        
        plt.plot(dates, holders)
        plt.show()

    def result_browse(self):
        self.result_browser = QtGui.QTextBrowser(self.widget_result_common)
        # self.result_browser.setGeometry(0, 0, 800, 500)
        # self.widget_result_common.setCentralWidget(self.result_browser)
        self.result_browser.resize(self.result_browser_size)
        self.result_browser.move(self.result_browser_move)
        # self.widget_result_common_layout.addWidget(self.result_browser)
        # self.toggle_widget(self.widget_result_common, self.main_widgets)
        # self.result_browser.show()
    
    def promise_holder(self):
        print "I'm promising holder"
        
        self.cur.execute("CREATE TABLE IF NOT EXISTS Holderprofile (shareholder TEXT PRIMARY KEY, holderid TEXT) WITHOUT ROWID")
        self.cur.execute("INSERT OR REPLACE INTO Holderprofile (shareholder, holderid) SELECT DISTINCT shareholder, holderid FROM Majorholderinfo")
        self.cur.execute("SELECT DISTINCT Holderprofit.holderid, shareholder, avg(holderprofit), count(DISTINCT Holderprofit.stockid) FROM Holderprofit INNER JOIN Holderprofile ON Holderprofit.holderid = Holderprofile.holderid GROUP BY Holderprofit.holderid ORDER BY avg(holderprofit) DESC, count(DISTINCT Holderprofit.stockid) DESC LIMIT 100")
        promising_holders = self.cur.fetchall()
        
        for holder in promising_holders:
            print str(holder).decode('unicode-escape')
        
        
    def non_public_offering(self):
        print "I'm private placement"
    
    def object_appending(self, object_single, objects):
        if object_single not in objects:
            objects.append(object_single)
        return objects

    def toggle_widget(self, show_widget, widgets):
        for widget in widgets:
            if widget == show_widget:
                widget.show()
            else:
                widget.hide()
                
    def style_set(self, action_triggered):
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(action_triggered.text()))
           
    def about(self):
        pass

    def close_application(self):
        self.cur.close()
        self.conn.close
        sys.exit() 


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    GUI.show()
    sys.exit(app.exec_())    