# _*_ coding: utf8 _*_

import sys
import time
import datetime
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from getprice import date_interconvert
from PyQt4 import QtGui, QtCore, Qt

class Window(QtGui.QMainWindow):
    
    
    def __init__(self):
        self.conn = sqlite3.connect('stock.sqlite3')
        self.cur = self.conn.cursor()
        
        super(Window, self).__init__()
        
        self.result_thread = Worker()
        
        
        self.main_widget = QtGui.QWidget(self)
        self.setCentralWidget(self.main_widget)
        
        self.setGeometry(50, 50, 1280, 800)
        self.setWindowTitle(u'Snail')
        self.setWindowIcon(QtGui.QIcon('snail_120.png'))
        self.setWindowOpacity(0.95)
        
        #=======================================================================
        # self.window_rect = self.frameSize()
        # self.window_width = self.window_rect.width()
        # self.window_height = self.window_rect.height()     
        #    
        # # position and size of search_widget
        # self.widget_search_rect = QtCore.QRect(0, 0, self.window_width, 100)
        # # position and size of result_widget
        # self.widget_result_rect = QtCore.QRect(0, 100, self.window_width, 500)
        # # size of search widgets
        # self.search_combo_size = QtCore.QSize(120, 30)
        # self.search_input_size = QtCore.QSize(200, 30)
        # self.search_button_size = QtCore.QSize(100, 30)
        # # position of search widgets
        # self.search_combo_move = QtCore.QPoint((self.widget_search_rect.width()-(self.search_combo_size.width()+self.search_input_size.width()+self.search_button_size.width()))/2, 
        #                                   50
        #                                   )
        # self.search_input_move = QtCore.QPoint((self.widget_search_rect.width()+self.search_combo_size.width()-self.search_input_size.width()-self.search_button_size.width())/2, 
        #                                   50
        #                                   )
        # self.search_button_move = QtCore.QPoint((self.widget_search_rect.width()+self.search_combo_size.width()+self.search_input_size.width()-self.search_button_size.width())/2, 
        #                                    50
        #                                    )
        # # result editor position
        # self.result_browser_size = QtCore.QSize(self.widget_result_rect.width(), 
        #                                 self.widget_result_rect.height()*0.8
        #                                 )
        # self.result_browser_move = QtCore.QPoint(0, 0)       
        #=======================================================================
        
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
          
        # self.statusBar()
          
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
        search_combo = QtGui.QComboBox()
        search_combo.addItem('Profile')
        search_combo.addItem('Number of Holders')
        
        # search input
        search_input = QtGui.QLineEdit()
        search_input.returnPressed.connect(lambda: self.search(search_input.text()))
        
        # search button
        search_button = QtGui.QPushButton('Search')
        search_button.clicked.connect(lambda: self.search(search_input.text()))
        
        # search area layout
        search_layout = QtGui.QHBoxLayout()
        search_layout.addWidget(search_combo, stretch = 10, alignment = QtCore.Qt.AlignRight)
        search_layout.addWidget(search_input, stretch = 5)
        search_layout.addWidget(search_button, stretch = 10, alignment = QtCore.Qt.AlignLeft)
        
        # result area layout
        result_holderid_lable = QtGui.QLabel('<b>HOLDER</b>')
        result_stockid_lable =  QtGui.QLabel('<b>STOCK</b>')
        result_holderid = QtGui.QListView()
        result_stockid = QtGui.QListView()
        self.result_main = QtGui.QWidget()
        
        result_holderid_layout = QtGui.QVBoxLayout()
        result_stockid_layout = QtGui.QVBoxLayout()
        result_holderid_layout.addWidget(result_holderid_lable, stretch = 1, alignment = QtCore.Qt.AlignCenter)
        result_holderid_layout.addWidget(result_holderid, stretch = 30)
        result_stockid_layout.addWidget(result_stockid_lable, stretch = 1, alignment = QtCore.Qt.AlignCenter)
        result_stockid_layout.addWidget(result_stockid, stretch = 30)
        
        result_layout = QtGui.QHBoxLayout()
        result_layout.addLayout(result_holderid_layout, stretch = 1)
        result_layout.addLayout(result_stockid_layout, stretch = 1)
        result_layout.addWidget(self.result_main, stretch = 20)
        
        # global layout
        global_layout = QtGui.QVBoxLayout()
        global_layout.setSpacing(10)
        global_layout.addSpacing(50)
        global_layout.addLayout(search_layout)
        global_layout.addLayout(result_layout)
        
        self.main_widget.setLayout(global_layout)
        
        # prepare the canvas    
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        
        # set the layout of result_main
        result_main_layout = QtGui.QVBoxLayout()
        result_main_layout.addWidget(self.canvas)
        self.result_main.setLayout(result_main_layout)        
        # self.show()
        
    def search(self, search_text):
        #=======================================================================
        # # prepare the browser
        # self.result_browser = QtGui.QTextBrowser(self.result_main)
        # self.result_browser.show()
        #=======================================================================
        
        # connect the loop signal to update_browser or plot
        # self.result_thread.result_item_emitted[str].connect(self.update_browser)
        self.result_thread.result_item_emitted[list, list].connect(self.plot_preprocessing)
        
        # query database
        self.cur.execute("SELECT DISTINCT reportdate, holdersnumber FROM Majorholderinfo WHERE stockid = ? AND reportdate <> '-1' AND holdersnumber <> '-1'", ('%s' % search_text, ))
        results = self.cur.fetchall()

        #update the browser
        self.result_thread.show(results)
        
        # print dates, holders
          
        # plt.plot(dates, holders)
        # plt.show()
        
    #===========================================================================
    # def update_browser(self, item, *args):
    #     
    #     self.result_browser.append(item)
    #     
    #     print item, 'aha', args
    #===========================================================================
        
    def plot_preprocessing(self, data):
        self.plot(data, self.figure, self.canvas)
        
    def plot(self, data, figure, canvas):
        plots = figure.add_subplot(111)
        plots.hold(False)
        plots.plot(data)
        canvas.draw()
        
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
    
#===============================================================================
#     def object_appending(self, object_single, objects):
#         if object_single not in objects:
#             objects.append(object_single)
#         return objects
# 
#     def toggle_widget(self, show_widget, widgets):
#         for widget in widgets:
#             if widget == show_widget:
#                 widget.show()
#             else:
#                 widget.hide()
#===============================================================================
                
    def style_set(self, action_triggered):
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(action_triggered.text()))
           
    def about(self):
        pass

    def close_application(self):
        self.cur.close()
        self.conn.close
        sys.exit()
        

class Worker(QtCore.QThread):
    result_item_emitted = QtCore.pyqtSignal([str], [list, list])
    
    def __init__(self, parent = None):
        super(Worker, self).__init__(parent = None)
    
    #===========================================================================
    # def __del__(self):
    #     self.wait()
    #===========================================================================
        
    def show(self, results):
        self.results = results
        self.start()
    
    def run(self):
        dates = []
        holders = []
        for item in self.results:
            dates.append(date_interconvert(item[0]))
            holders.append(item[1])
            item_str = str(item).decode('unicode-escape')
            self.result_item_emitted[str].emit(item_str)
            # time.sleep(0.1)
        self.result_item_emitted[list, list].emit(holders, dates)
    
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    GUI.show()
    sys.exit(app.exec_())    