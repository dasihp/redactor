import os
from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QFileDialog,
    QLabel, QPushButton, QListWidget,
    QHBoxLayout, QVBoxLayout
)
#імпортуємо бібліотеки
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from PIL import Image
from PIL import ImageFilter

#створення вікна додатку
app = QApplication([])
win = QWidget()
win.resize(700, 500)
win.setWindowTitle('Easy Editor')
'''ІНТЕРФЕЙС ДОДАТКУ'''
btn_dir = QPushButton('Папка')
lw_files = QListWidget()
lb_image = QLabel('Картинка')
#створення кнопок редагування
btn_left = QPushButton('Ліво')
btn_right = QPushButton('Право')
btn_flip = QPushButton('Дзеркало')
btn_sharp = QPushButton('Різкість')
btn_bw = QPushButton('Ч/Б')
#створення ліній 
row = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()

col1.addWidget(btn_dir)
col1.addWidget(lw_files)
col2.addWidget(lb_image, 95)
#створення рамок для кнопок релагуваняя
row_tools = QHBoxLayout()
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_flip)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_bw)
col2.addLayout(row_tools)

row.addLayout(col1, 20)
row.addLayout(col2, 80)
win.setLayout(row)

win.show()
'''ФУНКЦІОНАЛ ДОДАТКУ'''
workdir = ''

def filter(files, extentions):
    result = list()
    for filename in files:
        for ext in extentions:
            if filename.endswitch(ext):
                result.append(filename)

    return result

def show_filenames_list():
    global workdir
    extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    try:
        workdir = QFileDialog.getExistingDirectory()
        filenames = filter(os.listdir(workdir), extensions)
    except:
        workdir = ''
        filenames = []
    lw_files.clear()
    lw_files.addItems(filenames)

class ImageProcessor:
    def __init__(self):
        self.image = None
        self.filename = None
        self.dir = None
        self.save_dir = 'Modified/'
    def load_image(self, dir: str, filename: str):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)

    def show_image(self, path: str):
        lb_image.hide()
        qpixmap - QPixmap(path)
        w, h = lb_image.width(), lb_image.height()
        qpixmap = qpixmap.scaled(w, h, Qt.KeepAspectRatio)
        lb_image.setPixmap(qpixmap)
        lb_image.show()

    def save_image(self):
        path = os.path.join(workdir, self.save_dir)#шлях до папки Modified
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        full_path = os.path.join(path, self.filename)
        self.image.save(full_path)
    
    def do_bw(self):
        self.image = self.image.convert('L')
        self.save_image()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.show_image(image_path)

work_image = ImageProcessor()

def show_chosen_image():
    if lw_files.currentRow() >=0:
        filename = lw_files.currentItem().text()
        work_image.load_image(workdir, filename)
        image_path = os.path.join(workdir, filename)
        work_image.show_image(image_path)

lw_files.currentRowChanged.connect(show_chosen_image)
btn_bw.clicked.connect(work_image.do_bw)
btn_dir.clicked.connect(show_filenames_list)

app.exec()

