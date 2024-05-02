from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon,QKeySequence
from PyQt5.QtCore import QThread, pyqtSignal,Qt
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
                text=content_generate.conversation_ollama(prompt)  #ollama调用调试


        self.content_generate_signal.emit(text)


class Main(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
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



        self.button_sub=self.main_ui.button_submit
        self.button_sub_icon=QIcon('./img/send-2.svg')
        self.button_sub.setIcon(self.button_sub_icon)
        self.button_sub.clicked.connect(self.set_prompt)
        self.button_sub.clicked.connect(self.generate)
        self.button_exp=self.main_ui.button_export
        self.button_exp_icon=QIcon('./img/device-floppy.svg')
        self.button_exp.setIcon(self.button_exp_icon)
        self.button_exp.clicked.connect(self.save_obsidian)
        self.button_clear=self.main_ui.button_clear
        self.button_clear_icon=QIcon('./img/trash.svg')
        self.button_clear.setIcon(self.button_clear_icon)
        self.button_clear.clicked.connect(self.input_clear)
        self.input=self.main_ui.input_text
        self.input.clear()
        self.output=self.main_ui.output_content
        self.notes=self.main_ui.lineEdit_notes 
        self.clipboard_content=self.main_ui.button_clipboard
        self.clipboard_content_icon=QIcon('./img/clipboard-data.svg')
        self.clipboard_content.setIcon(self.clipboard_content_icon)
        self.clipboard_content.clicked.connect(self.clipboard)
        self.generate_thread=GeneratecontentThred()
        self.generate_thread.content_generate_signal.connect(self.on_content_generated)
        self.menu_set_xinghuo=self.main_ui.action_xinghuo
        self.menu_set_xinghuo.triggered.connect(self.open_menu_set_xinghuo)
        self.menu_set_obsidian=self.main_ui.action_obsidian
        self.menu_set_obsidian.triggered.connect(self.open_menu_set_obsidian)
        self.select_function=self.main_ui.comboBox_function
        self.import_note=self.main_ui.button_Import_Notes
        self.import_note_icon=QIcon('./img/file-import.svg')
        self.import_note.setIcon(self.import_note_icon)
        self.import_note.clicked.connect(self.improt_now_note)
        self.menu_about=self.main_ui.action_info
        self.menu_about.triggered.connect(self.product_info)
        self.menu_help=self.main_ui.action_help
        self.menu_help.triggered.connect(self.help_info)
        self.menu_feedback=self.main_ui.action_feedblack
        self.menu_feedback.triggered.connect(self.feedback)
        self.button_favorites=self.main_ui.button_Favorites
        self.favorites_icon=QIcon('./img/file-star.svg')
        self.button_favorites.setIcon(self.favorites_icon)
        self.button_favorites.clicked.connect(self.favorites)

    def toggle_visibility(self):
        if self.isMinimized():
            self.showNormal()  # 如果窗口已经是最小化状态，则恢复到正常大小
        else:
            self.showMinimized()  # 否则，最小化窗口



    def clipboard(self):
        self.output.selectAll()
        self.output.copy()
        message=QMessageBox()
        message.about(self, '提示', '复制成功')


    def input_clear(self):
        self.input.clear()
        #self.output.clear()

    def set_prompt(self):
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

    def generate(self):
        if self.input.toPlainText()=="":
            #self.output.setText('请输入内容')
            return # 如果输入框为空，则不执行后续操作
        
        else:
            self.output.setText('生成中，请稍后')
            self.generate_thread.start()
            if self.select_function.currentText()=="对话：":
                self.input.clear()

    def on_content_generated(self,text):
        self.output.setText(text)

    def save_obsidian(self):
        tree=ET.parse('configuration.xml')
        root=tree.getroot()
        obsidian_api=root.find('obsidian_api').text
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


    def favorites(self):
        tree=ET.parse('configuration.xml')
        root=tree.getroot()
        obsidian_api=root.find('obsidian_api').text
        date_time_now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        input_text = self.input.toPlainText()
        # 移除所有空行
        processed_text = re.sub(r'^\s*$\n', '', input_text, flags=re.MULTILINE)

        content = "\n >[!Abstract] 收藏  {} \n >{}".format(date_time_now,processed_text)
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


    def improt_now_note(self):
        tree=ET.parse('configuration.xml')
        root=tree.getroot()
        obsidian_api=root.find('obsidian_api').text
        url = 'http://127.0.0.1:27123/active/'
        headers = {
                'accept': '*/*',
                'Content-Type': 'text/markdown',
                'Authorization': 'Bearer {}'.format(obsidian_api)
                }
        #data = content.encode('utf-8')

        response = requests.get(url, headers=headers,verify=False)
        print(response.text)        

        self.input.setPlainText(response.text)


    def open_menu_set_xinghuo(self):
        llm_w.show()

    def open_menu_set_obsidian(self):
        set_obsidian_apiw.show()

    def product_info(self):
        text='"Kiko AI助手"是一款集成了先进的生成式人工智能技术的Obsidian辅助工具。它能够为您的Obsidian添加一颗强大的AI大脑，成为你的私人秘书，帮助你更高效的管理由Obsidian构建的笔记和知识库。\n当前版本：v1.3 \n官网：www.moaono.com'
        self.output.setText(text)

    def help_info(self):
        text='首次使用本软件需先配置大模型API相关信息。\n目前支持讯飞星火、通义千问及Ollama本地大模型，你需要在大模型配置窗口配置好相关API信息后再使用。'
        self.output.setText(text)

    def feedback(self):
        text='如果使用中遇到问题欢迎反馈：\nhttps://support.qq.com/products/118721/'
        self.output.setText(text)



class Set_obsidian_api(QWidget):
    tree=ET.parse('configuration.xml')
    root=tree.getroot()
    now_api_key=root.find('obsidian_api').text
    def __init__(self):
        super().__init__()
        self.setWindowTitle("设置Obsidian API")
        self.resize(500,200)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon('img/logo.png'))
        self.setFixedSize(self.width(),self.height())
        self.about_text=QTextBrowser()
        self.about_text.setText("在此处输入你的API KEY，你需要安装Local REST API插件，然后开启无需验证模式")
        self.about_text.setFixedSize(480,50)
        self.about_text.setStyleSheet("background-color: transparent;")
        self.set_api=QLineEdit()
        if self.now_api_key=="":
            #self.set_api.clear()
            self.set_api.setPlaceholderText("在此处输入你的API KEY")
        else:
            self.set_api.setText(self.now_api_key)
        
        self.set_api.setFixedHeight(35)
        self.submit_button=QPushButton("提交")
        self.submit_button.setFixedSize(250,45)
        self.button_layout=QHBoxLayout()
        self.button_layout.addWidget(self.submit_button)
        self.froms_layout=QVBoxLayout()
        self.froms_layout.addWidget(self.about_text)
        self.froms_layout.addWidget(self.set_api)
        self.froms_layout.addLayout(self.button_layout)
        self.setLayout(self.froms_layout)
        self.submit_button.clicked.connect(self.updata_api)

    def updata_api(self):
        self.root.find('obsidian_api').text=self.set_api.text()
        self.tree.write('configuration.xml')
        QMessageBox.about(self,'提醒','保存成功,需重启软件使设置生效')
       # 关闭整个程序
        QApplication.quit()



class Llm_set(QWidget):
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

    def save_setting(self):
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
        self.tree.write('configuration.xml')
        QMessageBox.about(self,'提醒','保存成功,需重启软件使设置生效')
        QApplication.quit()


class Initialization(QWidget):
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
    mainw=Main()
    llm_w=Llm_set()
    set_obsidian_apiw=Set_obsidian_api()
    initialization=Initialization()
    tree=ET.parse('configuration.xml')
    root=tree.getroot()

    now_obsidian_api=root.find('obsidian_api').text  # 修改变量名以避免混淆

    # 检查每个配置项是否为空，并根据需要显示设置窗口
    if not now_obsidian_api:
        
        set_obsidian_apiw.show()
        initialization.show()

    else:
        mainw.show()
        

    sys.exit(app.exec_())