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
style = '''

QWidget {
    background-color: rgb(250, 250, 200);
}
QPushButton {
    background-color: rgb(60, 0, 0);
    color: rgb(250, 250, 200);
    border-radius: 5px;
    height: 30px;
}
QListWidget {
    background-color: rgb(60, 0, 0);
    color: rgb(250, 250, 200);
    border-radius: 5px;
    border: 3px solid rgb(250, 250, 200)
}
'''

#створення вікна додатку
app = QApplication([])
app.setStyleSheet(style)
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
btn_detail = QPushButton('Деталізація')
btn_find_edges = QPushButton('Знайти межі')

#створення ліній 
row = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()
#додаємо віджети на лінії
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
row_tools.addWidget(btn_detail)
row_tools.addWidget(btn_find_edges)
#додаємо лінію з фільтрами на основну лінію
col2.addLayout(row_tools)
#додаємо лінії на головну лінію
row.addLayout(col1, 20)
row.addLayout(col2, 80)
win.setLayout(row)
#показуємо вікно
win.show()
'''ФУНКЦІОНАЛ ДОДАТКУ'''
workdir = ''#шлях до робочої папки
#фільтрує картинки
def filter(files, extentions):
    result = list()
    for filename in files:
        for ext in extentions:
            if filename.endswith(ext):
                result.append(filename)

    return result
#показує назви файлів в віджеті
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
    #конструктор класу
    def __init__(self):
        self.image = None
        self.filename = None
        self.dir = None
        self.save_dir = 'Modified/'
    #завантажити картинку
    def load_image(self, dir: str, filename: str):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)
    #показати картинку
    def show_image(self, path: str):
        lb_image.hide()
        qpixmap = QPixmap(path)
        w, h = lb_image.width(), lb_image.height()
        qpixmap = qpixmap.scaled(w, h, Qt.KeepAspectRatio)
        lb_image.setPixmap(qpixmap)
        lb_image.show()
    #зберегти картинку
    def save_image(self):
        path = os.path.join(workdir, self.save_dir)#шлях до папки Modified
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        full_path = os.path.join(path, self.filename)
        self.image.save(full_path)
    #чорно-біла
    def do_bw(self):
        self.image = self.image.convert('L')
        self.save_image()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.show_image(image_path)
    #повернути вліво
    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.save_image()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.show_image(image_path)
    #повернути вправо
    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.save_image()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.show_image(image_path)
    #відзеркалити картинку
    def do_mirror(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.save_image()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.show_image(image_path)
    #заблюрити картинку
    def do_blur(self):
        self.image = self.image.filter(ImageFilter.BLUR)
        self.save_image()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.show_image(image_path)

    def detail(self):
        """Функція, яка пікселізує зображення"""
        self.image = self.image.filter(ImageFilter.DETAIL)
        self.save_image()
        fullpath = os.path.join(workdir, self.save_dir, self.filename)
        self.show_image(fullpath)

    def find_edges(self):
        """Функція, яка показує межі зображення"""
        self.image = self.image.filter(ImageFilter.FIND_EDGES)
        self.save_image()
        fullpath = os.path.join(workdir, self.save_dir, self.filename)
        self.show_image(fullpath)

work_image = ImageProcessor()
#показати вибрану картинку
def show_chosen_image():
    if lw_files.currentRow() >=0:
        filename = lw_files.currentItem().text()
        work_image.load_image(workdir, filename)
        image_path = os.path.join(workdir, filename)
        work_image.show_image(image_path)
#підключаємо кнопки
lw_files.currentRowChanged.connect(show_chosen_image)
btn_bw.clicked.connect(work_image.do_bw)
btn_dir.clicked.connect(show_filenames_list)
btn_left.clicked.connect(work_image.do_left)
btn_right.clicked.connect(work_image.do_right)
btn_flip.clicked.connect(work_image.do_mirror)
btn_find_edges.clicked.connect(work_image.find_edges)
btn_detail.clicked.connect(work_image.detail)
#залишає вікно відкритим
app.exec()

