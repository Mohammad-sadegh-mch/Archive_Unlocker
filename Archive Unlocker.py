import sys
import string
import os
import json
import itertools
from pyzipper import AESZipFile
import rarfile
from PyQt6.QtWidgets import QDialog, QFrame, QProgressBar, QApplication, QRadioButton, QLineEdit
from PyQt6.QtWidgets import QCheckBox, QLabel, QPushButton, QFileDialog, QButtonGroup, QMessageBox
from PyQt6.QtCore import QRect, QMetaObject, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QIcon, QClipboard

ICONBOX = {"Warning": QMessageBox.Icon.Warning,
    "Info": QMessageBox.Icon.Information,
    "Error": QMessageBox.Icon.Critical,
    None: QMessageBox.Icon.NoIcon}

errorstyle = "color:red;"
defaultWinRAR = r"C:\Program Files\WinRAR\UnRAR.exe"
PROGRAMNAME = "Archive Unlocker"


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# pyinstaller --onefile --windowed --icon=pic.ico --add-data "pic.png;." main.py

def centering_text_html(text:str) -> str:
    start = '<html><body align="center" style="font-size:10pt;"><p>'
    end = '</p></body></html>'
    return start + text + end

class ArchiveTools():
    def __init__(self):
        self.DocumentsPath = os.path.join(os.environ["USERPROFILE"], "Documents")
        self.ProgramPath = os.path.join(self.DocumentsPath, "ArchiveUnlocker")
        
    def GetJsonPath(self) -> str:
        os.makedirs(self.ProgramPath, exist_ok=True)
        return os.path.join(self.ProgramPath, "data.json")

    def LoadJson(self) -> dict[str, list[str]]:
        JsonPath = self.GetJsonPath()

        if os.path.exists(JsonPath):
            with open(JsonPath, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {"ArchiveTools": []}
            data["ArchiveTools"].append(defaultWinRAR)

            with open(JsonPath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        return data

    def AddDataJson(self, addr:str):
        data = self.LoadJson()
        if addr not in data['ArchiveTools']:
            data["ArchiveTools"].append(addr)
            with open(self.GetJsonPath(), "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)


class Ui_Dialog(object):
    def __init__(self):
        self.Hline = QFrame.Shape.HLine
        self.Vline = QFrame.Shape.VLine
        self.Shadow = QFrame.Shadow.Sunken
        icon_path = resource_path("pic.png")
        self.ICON = QIcon(icon_path)

    def font_self(self, size:int=None, family:str=None):
        Font = QFont()
        if size: Font.setPointSize(size)
        if family: Font.setFamily(family)
        return Font

    def _set_label(self, Dialog):
        self.label_ragham = QLabel(parent=Dialog)
        self.label_ragham.setGeometry(QRect(270, 140, 270, 50))
        self.label_ragham.setFont(self.font_self(size=10))
        text_ragham = centering_text_html("تعداد رقم‌‌های پسورد را انتخاب کنید")
        self.label_ragham.setText(text_ragham)

        self.label_password = QLabel(parent=Dialog)
        self.label_password.setGeometry(QRect(10, 130, 210, 61))
        self.label_password.setFont(self.font_self(size=10))
        text_password = centering_text_html("دسته حروف پسورد را انتخاب کنید</p><p>یا در کادر وارد کنید")
        self.label_password.setText(text_password)

        self.label_browse = QLabel(parent=Dialog)
        self.label_browse.setGeometry(QRect(0, 70, 100, 50))
        self.label_browse.setFont(self.font_self(size=10))
        self.label_browse.setText("محل ذخیره فایل")

        self.label_title = QLabel(parent=Dialog)
        self.label_title.setGeometry(QRect(10, 16, 210, 40))
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.label_title.setFont(font)
        self.label_title.setText(PROGRAMNAME)

        self.label_icon = QLabel(parent=Dialog)
        self.label_icon.setGeometry(QRect(210, 10, 220, 30))
        self.label_icon.setFont(self.font_self(size=10))
        self.label_icon.setText('<html><body><p><span style="color:#ff0000;">Programmer: </span>Mohammad Sadegh</p></body></html>')

        self.label_info = QLabel(parent=Dialog)
        self.label_info.setGeometry(QRect(245, 30, 190, 30))
        self.label_info.setFont(self.font_self(size=10))
        self.label_info.setText('<html><body><p><span style="color:#ff0000;">telegram: </span>@Computer_MCH</p></body></html>')

    def _set_line(self, Dialog):
        self.line_1 = QFrame(parent=Dialog)
        self.line_1.setGeometry(QRect(260, 130, 20, 240))
        self.line_1.setFrameShape(self.Vline)
        self.line_1.setFrameShadow(self.Shadow)
        self.line_2 = QFrame(parent=Dialog)
        self.line_2.setGeometry(QRect(-10, 360, 570, 20))
        self.line_2.setFrameShape(self.Hline)
        self.line_2.setFrameShadow(self.Shadow)
        self.line_3 = QFrame(parent=Dialog)
        self.line_3.setGeometry(QRect(-3, 120, 540, 20))
        self.line_3.setFrameShape(self.Hline)
        self.line_3.setFrameShadow(self.Shadow)
        self.line_4 = QFrame(parent=Dialog)
        self.line_4.setGeometry(QRect(0, 60, 540, 20))
        self.line_4.setFrameShape(self.Hline)
        self.line_4.setFrameShadow(self.Shadow)

    def _set_radiobutton(self, Dialog):

        self.radio1 = QRadioButton(text="1", parent=Dialog)
        self.radio2 = QRadioButton(text="2", parent=Dialog)
        self.radio3 = QRadioButton(text="3", parent=Dialog)
        self.radio4 = QRadioButton(text="4", parent=Dialog)
        self.radio5 = QRadioButton(text="5", parent=Dialog)
        self.radio6 = QRadioButton(text="6", parent=Dialog)
        self.radio7 = QRadioButton(text="7", parent=Dialog)
        self.radio8 = QRadioButton(text="8", parent=Dialog)
        self.radio9 = QRadioButton(text="9", parent=Dialog)

        self.radio1.setGeometry(QRect(290, 190, 80, 17))
        self.radio2.setGeometry(QRect(290, 220, 80, 17))
        self.radio3.setGeometry(QRect(290, 250, 80, 17))
        self.radio4.setGeometry(QRect(380, 190, 80, 17))
        self.radio5.setGeometry(QRect(380, 220, 82, 17))
        self.radio6.setGeometry(QRect(380, 250, 80, 17))
        self.radio7.setGeometry(QRect(460, 190, 80, 17))
        self.radio8.setGeometry(QRect(460, 220, 80, 17))
        self.radio9.setGeometry(QRect(460, 250, 80, 17))

        self.RadioBtn = QButtonGroup(parent=Dialog)
        self.RadioBtn.addButton(self.radio1, 1)
        self.RadioBtn.addButton(self.radio2, 2)
        self.RadioBtn.addButton(self.radio3, 3)
        self.RadioBtn.addButton(self.radio4, 4)
        self.RadioBtn.addButton(self.radio5, 5)
        self.RadioBtn.addButton(self.radio6, 6)
        self.RadioBtn.addButton(self.radio7, 7)
        self.RadioBtn.addButton(self.radio8, 8)
        self.RadioBtn.addButton(self.radio9, 9)
        
    def _set_checkbox(self, Dialog):

        self.uper_check = QCheckBox(text=string.ascii_uppercase, parent=Dialog)
        self.uper_check.setGeometry(QRect(20, 240, 240, 17))
        
        self.lower_check = QCheckBox(text=string.ascii_lowercase, parent=Dialog)
        self.lower_check.setGeometry(QRect(20, 270, 240, 17))

        self.number_check = QCheckBox(text=string.digits, parent=Dialog)
        self.number_check.setGeometry(QRect(20, 300, 240, 17))

        self.namad_check = QCheckBox(text=string.punctuation+"‌ ", parent=Dialog)
        self.namad_check.setGeometry(QRect(20, 330, 240, 17))

    def _set_button(self, Dialog):
        self.browse_button = QPushButton(parent=Dialog)
        self.browse_button.setGeometry(QRect(430, 80, 100, 30))
        self.browse_button.setFont(self.font_self(size=10))
        self.browse_button.setText("انتخاب فایل")

        self.start_button = QPushButton(parent=Dialog)
        self.start_button.setGeometry(QRect(280, 290, 120, 30))
        self.start_button.setText("Start")
        
        self.stop_button = QPushButton(parent=Dialog)
        self.stop_button.setGeometry(QRect(410, 290, 120, 30))
        self.stop_button.setText("Stop")

        self.cancel_button = QPushButton(parent=Dialog)
        self.cancel_button.setGeometry(QRect(280, 325, 250, 30))
        self.cancel_button.setText("Cancel")

        self.info_button = QPushButton(parent=Dialog)
        self.info_button.setGeometry(QRect(430, 20, 100, 40))
        self.info_button.setText("information")

    def _set_bar(self, Dialog):
        self.bar = QProgressBar(parent=Dialog)
        self.bar.setEnabled(True)
        self.bar.setGeometry(QRect(10, 380, 530, 23))
        self.bar.setProperty("value", 0)

    def setupUi(self, Dialog:QDialog):
        Dialog.setFixedSize(545, 420)
        Dialog.setWindowTitle(PROGRAMNAME)
        Dialog.setWindowIcon(self.ICON)

        self._set_label(Dialog)
        self._set_line(Dialog)
        self._set_radiobutton(Dialog)
        self._set_checkbox(Dialog)
        self._set_button(Dialog)
        self._set_bar(Dialog)

        self.notification = QMessageBox()
        self.notification.setFont(self.font_self(size=10))
        self.notification.setWindowIcon(self.ICON)

        self.browser_entry = QLineEdit(parent=Dialog)
        self.browser_entry.setGeometry(QRect(120, 80, 300, 30))
        self.passwordentry = QLineEdit(parent=Dialog)
        self.passwordentry.setGeometry(QRect(10, 200, 240, 20))

        QMetaObject.connectSlotsByName(Dialog)


class BruteForceThread(QThread):
    update_status = pyqtSignal(int)
    finished = pyqtSignal(str, str)

    def __init__(self, characters, length, archive_path, FormatArchive, start_index=0):
        super().__init__()
        self.characters = characters
        self.length = length
        self.archive_path = archive_path
        self._running = True
        self.self_start_index = start_index
        self.FormatArchive = FormatArchive
        self.total_combinations = len(characters) ** length

    def run(self):
        combos = itertools.product(self.characters, repeat=self.length)
        counter = 0

        OutputFolder = os.path.split(self.archive_path)[0]
        for i, combo in enumerate(combos):
            counter += 1
            if i < self.self_start_index: continue

            if not self._running:
                self.update_status.emit(i)
                self.self_start_index = i
                return

            self.password = "".join(combo)
            
            try:
                if self.FormatArchive == ".rar":
                    rf = rarfile.RarFile(self.archive_path)
                    rf.extractall(path=OutputFolder, pwd=self.password)

                elif self.FormatArchive == ".zip":
                    with AESZipFile(self.archive_path) as zf:
                        zf.pwd = self.password.encode()
                        zf.extractall(path=OutputFolder)
                self.finished.emit(f"پسورد فایل : {self.password}\nپسورد فایل در کلیپ بورد شما قابل دسترس است.", "Info")
                return

            except:
                self.update_status.emit(i)
        self.finished.emit("پسورد در موارد انتخابی شما نبود\nلطفا دوباره تلاش کنید.", "Error")
        return

    def stop(self):
        self._running = False


class ArchiveUnlockerMain(QDialog):
    def __init__(self):
        super().__init__()
        self.obj = Ui_Dialog()
        self.obj.setupUi(self)
        self.last_index = 0
        self.threa = False
        self.FormatFile = ""
        self.obj.browse_button.clicked.connect(self.Set_Browser_Text)
        self.obj.start_button.clicked.connect(self.Start_Progress)
        self.obj.stop_button.clicked.connect(self.stop_brute_force)
        self.obj.info_button.clicked.connect(self.information)
        self.obj.cancel_button.clicked.connect(self.Quit)

    def Set_Browser_Text(self):
        filename, _ = QFileDialog.getOpenFileName(
            parent=self, caption="Select Archive File",
            filter="Archive Files (*.zip *.rar);;ZIP Files (*.zip);;RAR Files (*.rar)")

        self.obj.browser_entry.setText(filename)


    def Create_Characters(self) -> str:
        characters = ""
        lowerchk = self.obj.lower_check
        uperchek = self.obj.uper_check
        number = self.obj.number_check
        namad = self.obj.namad_check
        entry = self.obj.passwordentry.text()

        if namad.isChecked(): characters += namad.text()
        if lowerchk.isChecked(): characters += lowerchk.text()
        if uperchek.isChecked(): characters += uperchek.text()
        if number.isChecked(): characters += number.text()

        if entry:
            for i in entry:
                if i in characters: continue
                else: characters += i

        return characters

    def Start_Progress(self):

        archive_path = self.obj.browser_entry.text()
        charlist = self.Create_Characters()
        self.ClearStyle()

        FormatArchive = os.path.splitext(archive_path)[1].lower()

        if FormatArchive == '.rar':
            if os.path.exists(defaultWinRAR):
                rarfile.UNRAR_TOOL = defaultWinRAR
            else:
                Foundation = False
                Archive = ArchiveTools()
                data = Archive.LoadJson()['ArchiveTools']
                for folder in data:
                    if os.path.exists(folder):
                        rarfile.UNRAR_TOOL = folder
                        Foundation = True
                if not Foundation:
                    self.showerror("نرم‌افزار WinRAR نصب نیست.\nلطفا نصب کنید یا در صورتیکه نصب دارید ، پوشه\nنرم‌افزار رو انتخاب کنید", mode="Warning")
                    foldername = QFileDialog.getExistingDirectory(
                    parent=self, caption="انتخاب پوشه", options=QFileDialog.Option.ShowDirsOnly)
                    if foldername:
                        foldername = foldername.replace("/", "\\")
                        Archive.AddDataJson(os.path.join(foldername, "UnRAR.exe"))
                    return

        if not archive_path:
            self.showerror("لطفا یک فایل انتخاب کنید", "Error")
            self.obj.browse_button.setStyleSheet(errorstyle)
            self.obj.label_browse.setStyleSheet(errorstyle)            
            return

        if not os.path.exists(archive_path):
            self.showerror("فایل وجود ندارد", "Error")
            self.obj.browser_entry.setStyleSheet(errorstyle)
            return

        if charlist == "":
            self.showerror("حداقل یک حرف باید انتخاب شود", "Warning")
            self.obj.label_password.setStyleSheet(errorstyle)
            self.obj.passwordentry.setStyleSheet(errorstyle)
            self.obj.uper_check.setStyleSheet(errorstyle)
            self.obj.lower_check.setStyleSheet(errorstyle)
            self.obj.namad_check.setStyleSheet(errorstyle)
            self.obj.number_check.setStyleSheet(errorstyle)
            return

        if self.obj.RadioBtn.checkedId() == -1:
            self.obj.label_ragham.setStyleSheet(errorstyle)
            self.obj.radio1.setStyleSheet(errorstyle)
            self.obj.radio2.setStyleSheet(errorstyle)
            self.obj.radio3.setStyleSheet(errorstyle)
            self.obj.radio4.setStyleSheet(errorstyle)
            self.obj.radio5.setStyleSheet(errorstyle)
            self.obj.radio6.setStyleSheet(errorstyle)
            self.obj.radio7.setStyleSheet(errorstyle)
            self.obj.radio8.setStyleSheet(errorstyle)
            self.obj.radio9.setStyleSheet(errorstyle)
            self.showerror("مقدار رقم نباید خالی باشد!", "Error")
            return

        length = self.obj.RadioBtn.checkedId()
        self.ClearStyle()
        self.obj.bar.setMaximum(len(charlist) ** length)
        self.threa = BruteForceThread(charlist, length, archive_path, FormatArchive, start_index=self.last_index)
        self.threa.update_status.connect(self.updatebar)
        self.threa.finished.connect(self.showerror)
        self.threa.start()


    def ClearStyle(self):
        self.obj.label_password.setStyleSheet("")
        self.obj.label_password.setStyleSheet("")
        self.obj.passwordentry.setStyleSheet("")
        self.obj.uper_check.setStyleSheet("")
        self.obj.lower_check.setStyleSheet("")
        self.obj.namad_check.setStyleSheet("")
        self.obj.number_check.setStyleSheet("")
        self.obj.browse_button.setStyleSheet("")
        self.obj.browser_entry.setStyleSheet("")
        self.obj.label_browse.setStyleSheet("")

    def updatebar(self, value):
        self.obj.bar.setValue(value)
        self.last_index = value

    def stop_brute_force(self):
        if self.threa: self.threa.stop()

    def information(self):
        text = """<html><body style="font-family:'MS Shell Dlg 2'; font-size:10pt; font-weight:400;" dir="rtl">
        <p align="right"><span>این برنامه برای بازیابی رمز فایل‌های فشرده طراحی شده </span></p>
        <p align="right"><span>با انتخاب حروف و انتخاب تعداد رقم های پسورد ، به برنامه کمک کنید که پسورد شما رو زودتر پیدا کنه</span></p>
        <p align="center"><span>کانال تلگرام : </span><a href="https://t.me/Computer_MCH"><span>Computer_MCH@</span></a></p>
        <p align="center"><span>آیدی برنامه‌نویس : </span><a href="https://t.me/mohammad_sadegh_mch"><span>mohammad_sadegh_mch@</span></a></p></body></html>"""
        self.showerror(text, mode=None)

    def showerror(self, message:str=None, mode:str=None):
        " mode: ('Warning', 'Info', 'Error') "

        icon = ICONBOX[mode]
        if mode == "Info":
            QApplication.clipboard().setText(self.threa.password, mode=QClipboard.Mode.Clipboard)

        if mode == None:
            self.obj.notification.setWindowTitle("About")
        else:
            self.obj.notification.setWindowTitle(mode)

        self.obj.notification.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.obj.notification.setIcon(icon)
        self.obj.notification.setText(message)
        self.obj.notification.exec()

    def Quit(self): QApplication.quit()


Application = QApplication(sys.argv)
Window = ArchiveUnlockerMain()
Window.show()
sys.exit(Application.exec())
