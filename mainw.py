from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon,QKeySequence,QFont
from PyQt5.QtCore import QThread, pyqtSignal,Qt,QTimer
# 导入 QDesktopWidget
from PyQt5.QtWidgets import QDesktopWidget
import main
import content_generate,llm_config
import sys
import requests
import xml.etree.ElementTree as ET
import re
import datetime
#from img import img

def check_service_available(): #服务启动检测
        
        url = 'http://127.0.0.1:27123/active/'
        try:
            # 发送 HEAD 请求检查服务是否可用
            response = requests.head(url, timeout=2)  # 设置超时时间为2秒
            #print(response.status_code)
            if response.status_code == 401: #这里只检测到服务能响应即可
                return True
            else:
                return False
        except requests.ConnectionError:
            return False
        except requests.Timeout:
            return False

class GeneratecontentThred(QThread):
    content_generate_signal=pyqtSignal(str)

    def run(self):
        tree=ET.parse('configuration.xml')
        root=tree.getroot()
        llm=root.find('llm_setting/now_llm').text
        match llm:
            case '讯飞星火': #讯飞星火
                text=content_generate.conversation(prompt) 
            case '通义千问': #qwen

                text=content_generate.conversation_qwen(prompt)
 
                
            case 'Ollama本地大模型': #ollama
                text=content_generate.conversation_ollama(prompt)  
            
            case 'Kimi': #kimi
                text=content_generate.conversation_kimi(prompt)


        self.content_generate_signal.emit(text) #发送信号


class Main(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        # 设置全局字体样式
        font = QFont("微软雅黑",9)  # 选择字体和大小
        QApplication.setFont(font)
        self.main_ui=main.Ui_MainWindow()
        self.main_ui.setupUi(self)
        self.setWindowIcon(QIcon('img/logo.png'))
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)       
        screen = QDesktopWidget().screenGeometry() # 获取屏幕尺寸
        size = self.geometry()   # 获取窗口尺寸    
        self.move(screen.width() - size.width(), 10)  # 将窗口移动到屏幕右侧
        self.setFixedSize(self.width(),self.height())
         
        self.toggle_visibility_shortcut = QShortcut(QKeySequence('ctrl+H'), self)  # 设置快捷键隐藏
        self.toggle_visibility_shortcut.activated.connect(self.toggle_visibility)



        self.button_sub=self.main_ui.button_submit #提交按钮
        self.button_sub_icon=QIcon('./img/send-2.svg')
        self.button_sub.setIcon(self.button_sub_icon)
        self.button_sub.setToolTip("提交")
        self.button_sub.clicked.connect(self.set_prompt)
        self.button_sub.clicked.connect(self.generate)
        self.button_exp=self.main_ui.button_export #导出按钮
        self.button_exp_icon=QIcon('./img/device-floppy.svg')
        self.button_exp.setIcon(self.button_exp_icon)
        self.button_exp.setToolTip("存入当前笔记")
        self.button_exp.clicked.connect(self.save_obsidian)
        self.button_clear=self.main_ui.button_clear #清空按钮
        self.button_clear_icon=QIcon('./img/trash.svg')
        self.button_clear.setIcon(self.button_clear_icon)
        self.button_clear.setToolTip("清空输入内容")
        self.button_clear.clicked.connect(self.input_clear)
        self.input=self.main_ui.input_text
        self.input.clear()
        self.output=self.main_ui.output_content
        self.notes=self.main_ui.lineEdit_notes 
        self.clipboard_content=self.main_ui.button_clipboard #剪贴板
        self.clipboard_content_icon=QIcon('./img/clipboard-data.svg')
        self.clipboard_content.setIcon(self.clipboard_content_icon)
        self.clipboard_content.setToolTip("复制生成内容到剪贴板")
        self.clipboard_content.clicked.connect(self.clipboard)
        self.generate_thread=GeneratecontentThred() #生成内容线程
        self.generate_thread.content_generate_signal.connect(self.on_content_generated)
        self.menu_set_xinghuo=self.main_ui.action_xinghuo
        self.menu_set_xinghuo.triggered.connect(self.open_menu_set_xinghuo)
        self.menu_set_obsidian=self.main_ui.action_obsidian
        self.menu_set_obsidian.triggered.connect(self.open_menu_set_obsidian)
        self.select_function=self.main_ui.comboBox_function
        self.import_note=self.main_ui.button_Import_Notes #导入笔记
        self.import_note_icon=QIcon('./img/file-import.svg')
        self.import_note.setIcon(self.import_note_icon)
        self.import_note.setToolTip("导入当前笔记")
        self.import_note.clicked.connect(self.improt_now_note)
        self.menu_about=self.main_ui.action_info
        self.menu_about.triggered.connect(self.product_info)
        self.menu_help=self.main_ui.action_help
        self.menu_help.triggered.connect(self.help_info)
        self.menu_sponsor=self.main_ui.action_sponsor
        self.menu_sponsor.triggered.connect(self.sponsor)
        self.button_favorites=self.main_ui.button_Favorites #收藏
        self.favorites_icon=QIcon('./img/file-star.svg')
        self.button_favorites.setIcon(self.favorites_icon)
        self.button_favorites.setToolTip("收藏到笔记")
        self.button_favorites.clicked.connect(self.favorites)
        self.button_todo=self.main_ui.button_todo #待办
        self.todo_icon=QIcon('./img/list-check.svg')
        self.button_todo.setIcon(self.todo_icon)
        self.button_todo.setToolTip("查看待办")
        self.button_todo.clicked.connect(self.plugin_todolist_prompt)
        self.generate_todo_answer = None  # 初始化一个属性来持有线程对象

        #设置循环效果--开始
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_text)
        self.text_cycle = 0


        #系统托盘相关代码----开始
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon('img/logo.png'))  # 设置托盘图标
        self.tray_icon.setToolTip("Kiko AI助手")  # 设置鼠标悬停时显示的提示文本

        show_action = QAction("显示", self)
        quit_action = QAction("退出", self)
        show_action.triggered.connect(self.show)
        quit_action.triggered.connect(self.quit)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        # 添加点击图标恢复窗口的功能
        self.tray_icon.activated.connect(self.tray_icon_clicked)
        
    def tray_icon_clicked(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.showNormal()  # 恢复窗口到正常大小并激活

        

    def closeEvent(self, event): #关闭窗口
        if self.tray_icon.isVisible():
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setWindowTitle("系统托盘")
            msg_box.setText("程序将继续在系统托盘运行。")
            quit_button = msg_box.addButton("直接退出", QMessageBox.AcceptRole)
            continue_button = msg_box.addButton("继续运行", QMessageBox.RejectRole)
            msg_box.exec_()

            if msg_box.clickedButton() == quit_button:
                QApplication.quit()
            else:
                self.hide()
                event.ignore()

    def quit(self):
        QApplication.quit()
    #系统托盘相关代码----结束


    def toggle_visibility(self):
        if self.isMinimized():
            self.showNormal()  # 如果窗口已经是最小化状态，则恢复到正常大小
        else:
            self.showMinimized()  # 否则，最小化窗口


    def update_text(self):
        texts = ['🍉生成中，请稍后', '🍈生成中，请稍后.', '🍍生成中，请稍后..', '🍅生成中，请稍后...']
        self.output.setText(texts[self.text_cycle])
        self.text_cycle = (self.text_cycle + 1) % len(texts)


    def clipboard(self): #剪贴板
        self.output.selectAll()
        self.output.copy()
        message=QMessageBox()
        message.about(self, '提示', '复制成功')


    def input_clear(self): #清空输入窗口
        self.input.clear()
        #self.output.clear()

    def set_prompt(self): #设置prompt
        global prompt
        now_function=self.select_function.currentText()
        print(now_function)
        if now_function=="对话：":
            if self.input.toPlainText()=="":
                message=QMessageBox()
                message.about(self, '提示', '请输入内容')
                return
            else:
                prompt=self.input.toPlainText()
                #self.input.clear()
        else:
            if self.input.toPlainText()=="":
                message=QMessageBox()
                message.about(self, '提示', '请输入内容')
                return
            else:
                prompt="{}{}{}".format(self.notes.text(),now_function,self.input.toPlainText(),)
            #print(self.notes.text())

    def generate(self): #生成
        if self.input.toPlainText()=="":
            #self.output.setText('请输入内容')
            return # 如果输入框为空，则不执行后续操作
        
        else:
            #self.output.setText('生成中，请稍后')
            self.timer.start(500)  # 每500毫秒更新一次文本
            self.generate_thread.start() # 启动生成内容线程
            if self.select_function.currentText()=="对话：":
                self.input.clear()

    def on_content_generated(self,text): #生成完成
        self.timer.stop()  # 停止定时器
        self.output.setText(text)


    

    def save_obsidian(self): #保存到obsidian
        tree=ET.parse('configuration.xml')
        root=tree.getroot()
        obsidian_api=root.find('obsidian/obsidian_api').text
        content = self.output.toPlainText()
        url = 'http://127.0.0.1:27123/active/'
        headers = {
            'accept': '*/*',
            'Content-Type': 'text/markdown',
            'Authorization': 'Bearer {}'.format(obsidian_api)
        }
        data = content.encode('utf-8')

        response = requests.post(url, headers=headers, data=data, verify=False)
        message=QMessageBox()
        message.about(self,'提示','保存成功')


    def favorites(self): #收藏
        tree=ET.parse('configuration.xml')
        root=tree.getroot()
        obsidian_api=root.find('obsidian/obsidian_api').text
        obsidian_favorite_folder=root.find('obsidian/obsidian_favorite_folder').text
        obsidian_favorite_file=root.find('obsidian/obsidian_favorite_file').text
        print(obsidian_favorite_folder)
        if obsidian_favorite_folder ==None:
            
            message=QMessageBox()
            message.about(self,'提示','请先设置收藏夹')  
            return
        elif obsidian_favorite_file==None:
            message=QMessageBox()
            message.about(self,'提示','请先设置收藏文件')  
            return
        elif self.input.toPlainText()=="":
            message=QMessageBox()
            message.about(self,'提示','请输入待收藏内容')
        else:
            print('test')
                
            date_time_now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            input_text = self.input.toPlainText()
                # 移除所有空行
            processed_text = re.sub(r'^\s*$\n', '', input_text, flags=re.MULTILINE)

            content = "\n >[!Abstract] 收藏  {} \n >{}".format(date_time_now,processed_text)
            url = f'http://127.0.0.1:27123/vault/{obsidian_favorite_folder}/{obsidian_favorite_file}.md'
            headers = {
                        'accept': '*/*',
                        'Content-Type': 'text/markdown',
                        'Authorization': 'Bearer {}'.format(obsidian_api)
                    }
            data = content.encode('utf-8')
            requests.post(url, headers=headers, data=data, verify=False)
            message=QMessageBox()
            message.about(self,'提示','保存成功')        


    def improt_now_note(self): #导入当前笔记
        if check_service_available():
            # 如果服务可用，执行后续操作
            tree=ET.parse('configuration.xml')
            root=tree.getroot()
            obsidian_api=root.find('obsidian/obsidian_api').text
            url = 'http://127.0.0.1:27123/active/'
            headers = {
                    'accept': '*/*',
                    'Content-Type': 'text/markdown',
                    'Authorization': 'Bearer {}'.format(obsidian_api)
                    }
            #data = content.encode('utf-8')

            response = requests.get(url, headers=headers,verify=False)
            self.input.setPlainText(response.text)

            
        else:
            QMessageBox.about(self,'提示','获取失败,请检验你的obsidian api是否正确，或是否处于打开状态')        

        


    def open_menu_set_xinghuo(self): #设置讯飞星火
        llm_w.show()

    def open_menu_set_obsidian(self): #设置obsidian
        set_obsidian_apiw.show()

    def product_info(self): #产品介绍
        text='"Kiko AI助手"是一款集成了先进的生成式人工智能技术的Obsidian辅助工具。它能够为您的Obsidian添加一颗强大的AI大脑，成为你的私人秘书，帮助你更高效的管理由Obsidian构建的笔记和知识库。\n当前版本：v1.6 \n官网：www.moaono.com\nicon by icons8'
        self.output.setText(text)

    def help_info(self): #帮助
        text='如果你还不太会用，可以查看使用指南：\nhttps://moaono.notion.site/Kiko-AI-2cffebb6f07a4692951df2dd0f2178e2'
        self.output.setText(text)

    def sponsor(self): #赞助
        text='本链接仅用于对我设计制作产品支持，如果我设计或制作的产品真的帮助到了您，同时您有条件给予支持，那您可以根据自己的情况拍下此链接。\n如果您没考虑支持一下，那也没关系的，您依然可以安心的使用它，它本来就是免费的。赞助链接：\nhttps://item.taobao.com/item.htm?id=798448763386'
        self.output.setText(text)

    #TODOLIST 插件
    def plugin_todolist_prompt(self):
        tree=ET.parse('configuration.xml')
        root=tree.getroot()
        kiko_todo_state=root.find('obsidian/obsidian_kiko_todo_state').text
        if kiko_todo_state=="True":
            global prompt
            self.generate_todo_answer=GeneratecontentThred()
            self.generate_todo_answer.content_generate_signal.connect(self.get_answer)
            tree=ET.parse('configuration.xml')
            root=tree.getroot()
            obsidian_api=root.find('obsidian/obsidian_api').text
            url = 'http://127.0.0.1:27123/vault/kiko_todo.md'
            headers = {
                    'accept': '*/*',
                    'Content-Type': 'text/markdown',
                    'Authorization': 'Bearer {}'.format(obsidian_api)
                    }
            #data = content.encode('utf-8')

            response = requests.get(url, headers=headers,verify=False)
            print(response.text)        
            prompt_1='''
    下是我的任务清单样式，我用以下清单管理每天的任务：\n
    | 任务   | 内容     | 时间          | 完成状态   |
    |-|-|-|-|
    | {任务} | {任务内容} | {开始时间-结束时间} | {完成状态} |'''
            prompt_2="现在的时间是{}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
            prompt_3=response.text
            prompt="{}。{}。这是当前的待办任务列表：{}。请按以下方式总结：\n已完成:。\n未完成:.请跟据未完成任务的事项，为我做出必要的提示。".format(prompt_1,prompt_2,prompt_3)
            self.timer.start(500)
            self.generate_todo_answer.start()
        else:
            message=QMessageBox()
            message.about(self,'提示','请先开启TODOLIST插件')
    def get_answer(self, content):
            self.timer.stop()
            self.output.setText(content)
        
        


class Set_obsidian_api(QWidget): #设置obsidian api窗口
    tree=ET.parse('configuration.xml')
    root=tree.getroot()
    now_api_key=root.find('obsidian/obsidian_api').text
    now_favorite_folder=root.find('obsidian/obsidian_favorite_folder').text
    now_favorite_file=root.find('obsidian/obsidian_favorite_file').text
    now_kiko_todo_state=root.find('obsidian/obsidian_kiko_todo_state').text
    def __init__(self):
        super().__init__()
        self.setWindowTitle("配置Obsidian相关功能")
        self.resize(550,300)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon('img/logo.png'))
        self.setFixedSize(self.width(),self.height())
        self.about_text=QTextBrowser()
        self.about_text.setText("在此处输入你的API KEY，你需要安装Local REST API插件，然后开启无需验证模式")
        self.about_text.setFixedSize(530,50)
        self.about_text.setStyleSheet("background-color: transparent;")
        self.set_api_key=QLabel("API KEY")
        self.set_api=QLineEdit()
        if self.now_api_key=="":
            #self.set_api.clear()
            self.set_api.setPlaceholderText("在此处输入你的API KEY")
        else:
            self.set_api.setText(self.now_api_key)
        
        self.set_api.setFixedHeight(35)
        
        self.from_favorite=QFormLayout()
        self.from_favorite.setSpacing(10)
        self.from_favorite.addRow(self.set_api_key,self.set_api)
        self.folder=QLabel("收藏文件夹")
        self.folder_name=QLineEdit()
        self.folder_name.setText(self.now_favorite_folder)
        self.folder_name.setPlaceholderText("在此处输入文件夹名称")
        self.folder_name.setFixedHeight(35)
        self.from_favorite.addRow(self.folder,self.folder_name)
        self.favorite=QLabel("收藏文件名")
        self.favorite_name=QLineEdit()
        self.favorite_name.setText(self.now_favorite_file)
        self.favorite_name.setPlaceholderText("在此处输入文件名")
        self.favorite_name.setFixedHeight(35)
        self.from_favorite.addRow(self.favorite,self.favorite_name)
        self.kiko_todo=QLabel("Kiko-Todo")
        self.kiko_todo_state=QCheckBox()
        if self.now_kiko_todo_state=="True":
            self.kiko_todo_state.setChecked(True)
        else:
            self.kiko_todo_state.setChecked(False)
        self.from_favorite.addRow(self.kiko_todo,self.kiko_todo_state)

        self.submit_button=QPushButton("提交")
        self.submit_button.setFixedSize(250,45)
        self.button_layout=QHBoxLayout()
        self.button_layout.addWidget(self.submit_button)
        self.froms_layout=QVBoxLayout()
        self.froms_layout.addWidget(self.about_text)
        #self.froms_layout.addWidget(self.set_api)
        self.froms_layout.addLayout(self.from_favorite)
        self.froms_layout.addLayout(self.button_layout)
        
        self.setLayout(self.froms_layout)
        self.submit_button.clicked.connect(self.updata_api)
        self.submit_button.clicked.connect(self.kiko_todo_initialization)

    def updata_api(self): #保存api
        self.root.find('obsidian/obsidian_api').text=self.set_api.text()
        self.root.find('obsidian/obsidian_favorite_folder').text=self.folder_name.text()
        self.root.find('obsidian/obsidian_favorite_file').text=self.favorite_name.text()
        if self.kiko_todo_state.isChecked()==True:
            self.root.find('obsidian/obsidian_kiko_todo_state').text="True"
        else:
            self.root.find('obsidian/obsidian_kiko_todo_state').text="False"
        self.tree.write('configuration.xml')
        QMessageBox.about(self,'提醒','保存成功,需重启软件使设置生效')
       # 关闭整个程序
        QApplication.quit()

    def kiko_todo_initialization(self): #初始化kiko-todo
        tree=ET.parse('configuration.xml')
        root=tree.getroot()
        obsidian_api=root.find('obsidian/obsidian_api').text
        url = 'http://127.0.0.1:27123/vault/kiko_todo.md'
        headers = {
                'accept': '*/*',
                'Content-Type': 'text/markdown',
                'Authorization': 'Bearer {}'.format(obsidian_api)
                }
        response=requests.get(url, headers=headers,verify=False)
        todolist='''
| 任务           | 内容      | 时间                                | 完成状态 |
| ------------ | ------- | --------------------------------- | ---- |
| obsidian使用学习 | 学习工具的使用 | 2024-5-26 13:00 - 2024-5-26 15:00 | 完成   |
'''
        
        if self.kiko_todo_state.isChecked()==True and response.status_code==200:
            return print("Kiko-Todo已存在")
        elif self.kiko_todo_state.isChecked()==True and response.status_code!=200:
            requests.post(url, headers=headers, data=todolist.encode('utf-8'),verify=False)
            print("Kiko-Todo初始化成功")

        else:
            return print("未启动")


class Llm_set(QWidget): #llm设置窗口
    tree=ET.parse('configuration.xml')
    root=tree.getroot()

    now_llm_info=root.find('llm_setting/now_llm').text
    system_promp_info=root.find('llm_setting/system_prompt').text
    temperature_info=root.find('llm_setting/temperature').text

    spark_appid_info= root.find('xinghuo_api/appid').text
    spark_api_secret_info=root.find('xinghuo_api/api_secret').text
    spark_api_key_info =root.find('xinghuo_api/api_key').text
    spark_version_info=root.find('xinghuo_api/version').text

    ollama_url_info=root.find('ollama_api/api_url').text
    ollama_model_info=root.find('ollama_api/model').text

    qwen_api_key_info=root.find('qwen_api/api_key').text
    qwen_model_info=root.find('qwen_api/model').text

    kimi_api_key_info=root.find('kimi_api/api_key').text
    kimi_model_info=root.find('kimi_api/model').text

    def __init__(self):
        super().__init__()
        self.llm_ui=llm_config.Ui_Form_llm_config()
        self.llm_ui.setupUi(self)
        self.setWindowIcon(QIcon('img/logo.png'))
        self.setFixedSize(self.width(),self.height())
        self.save_button=self.llm_ui.pushButton_save
        self.now_llm=self.llm_ui.comboBox_select_model
        self.now_llm.setCurrentText(self.now_llm_info)
        self.system_prompt=self.llm_ui.plainTextEdit_prompt
        self.system_prompt.setPlainText(self.system_promp_info)
        self.spark_appid=self.llm_ui.lineEdit_xinghuo_appid
        self.spark_appid.setText(self.spark_appid_info)
        self.spark_api_secret=self.llm_ui.lineEdit_xinghuo_APISecre
        self.spark_api_secret.setText(self.spark_api_secret_info)
        self._api_key=self.llm_ui.lineEdit_xinghuo_apikey
        self._api_key.setText(self.spark_api_key_info)
        self.spark_version=self.llm_ui.comboBox_xinghuo_model
        self.spark_version.setCurrentText(self.spark_version_info)
        self.ollama_url=self.llm_ui.lineEdit_ollama_api
        self.ollama_url.setText(self.ollama_url_info)
        self.ollama_model=self.llm_ui.lineEdit_ollama_model
        self.ollama_model.setText(self.ollama_model_info)
        self.temperature=self.llm_ui.comboBox_temperature
        self.temperature.setCurrentText(self.temperature_info)
        self.qwen_api_key=self.llm_ui.lineEdit_qwen_apikey
        self.qwen_api_key.setText(self.qwen_api_key_info)
        self.qwen_model=self.llm_ui.lineEdit_qwen_model
        self.qwen_model.setText(self.qwen_model_info)
        self.save_button.clicked.connect(self.save_setting)
        self.kimi_api_key=self.llm_ui.lineEdit_kimi_api_key
        self.kimi_api_key.setText(self.kimi_api_key_info)
        self.kimi_model=self.llm_ui.comboBox_kimi_model
        self.kimi_model.setCurrentText(self.kimi_model_info)


    def save_setting(self): #保存llm设置
        self.root.find('llm_setting/now_llm').text=self.now_llm.currentText()
        self.root.find('llm_setting/system_prompt').text=self.system_prompt.toPlainText()
        self.root.find('llm_setting/temperature').text=self.temperature.currentText()
        self.root.find('xinghuo_api/appid').text=self.spark_appid.text()
        self.root.find('xinghuo_api/api_secret').text=self.spark_api_secret.text()
        self.root.find('xinghuo_api/api_key').text=self._api_key.text()
        self.root.find('xinghuo_api/version').text=self.spark_version.currentText()
        self.root.find('ollama_api/api_url').text=self.ollama_url.text()
        self.root.find('ollama_api/model').text=self.ollama_model.text()
        self.root.find('qwen_api/api_key').text=self.qwen_api_key.text()
        self.root.find('qwen_api/model').text=self.qwen_model.text()
        self.root.find('kimi_api/api_key').text=self.kimi_api_key.text()
        self.root.find('kimi_api/model').text=self.kimi_model.currentText()
        self.tree.write('configuration.xml')
        QMessageBox.about(self,'提醒','保存成功,需重启软件使设置生效')
        QApplication.quit()


class Initialization(QWidget): #初始化窗口
    def __init__(self):
        super().__init__()
        self.setWindowTitle("初始化说明")
        self.resize(500,300)
        self.setFixedSize(self.width(),self.height())
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon('img/logo.png'))
        self.content=QTextBrowser()
        self.content.setPlainText('欢迎使用Kiko AI助手。第一次使用本软件需要配置Obsidian的API ,你需要安装Obsidian的\"Local REST API\"插件，实现笔记的导入导出功能。')
        self.button=QPushButton("确定")
        self.layout=QVBoxLayout()
        self.layout.addWidget(self.content)
        self.layout.addWidget(self.button)
        #self.content.setFixedSize(480,50)
        self.content.setStyleSheet("background-color: transparent;")
        self.button=QPushButton("确定")
        self.layout=QVBoxLayout()
        self.layout.addWidget(self.content)
        self.layout.addWidget(self.button)
        self.button.clicked.connect(lambda: self.close())
        self.setLayout(self.layout)
        


if __name__=='__main__':
    app=QApplication(sys.argv)
    # 设置全局 QSS 样式
    #app.setStyleSheet("QMessageBox { background-color: #f4f9fa; color: #000; } QPushButton { background-color: #a6bbd0; color: #fff; border: 1px solid #a6bbd0; }")
    mainw=Main()
    llm_w=Llm_set()
    set_obsidian_apiw=Set_obsidian_api()
    initialization=Initialization()
    tree=ET.parse('configuration.xml')
    root=tree.getroot()

    now_obsidian_api=root.find('obsidian/obsidian_api').text  # 修改变量名以避免混淆

    # 检查每个配置项是否为空，并根据需要显示设置窗口
    if not now_obsidian_api:
        
        set_obsidian_apiw.show()
        initialization.show()

    else:
        mainw.show()
        

    sys.exit(app.exec_())