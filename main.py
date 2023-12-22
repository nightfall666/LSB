from PIL import Image
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QGraphicsScene, QGraphicsPixmapItem, QSizePolicy
from PyQt5.QtGui import QPixmap
from GUI import Ui_MainWindow


class LSBSteganography:
    @staticmethod
    def encode_lsb(image_path, message, output_path):
        try:
            img = Image.open(image_path)
            pixels = img.load()
            width, height = img.size

            r, g, b = pixels[0, 0]

            def split(s):
                return [char for char in s]

            t = split(message)
            size = len(t)

            if size < 255:
                pixels[0, 0] = (size, g, b)
            else:
                print("Too big message. Over 255 characters.")

            for y in range(len(t)):
                char = t[y]
                binary = format(ord(char), '08b')
                for x in range(len(binary)):
                    r, g, b = pixels[x + 1, y]
                    bit = int(binary[x])
                    r = ((r & ~1) | bit)
                    pixels[x + 1, y] = (r, g, b)

            img.save(output_path, 'PNG')
            return output_path

        except Exception as e:
            print(e)

    @staticmethod
    def decode_lsb(image_path):
        try:
            img = Image.open(image_path)
            pixels = img.load()
            size, g, b = pixels[0, 0]
            binary_string = ""
            for y in range(size):
                char_binary = ""
                for x in range(8):
                    r, _, _ = pixels[x + 1, y]
                    char_binary += str(r & 1)
                binary_string += chr(int(char_binary, 2))

            return binary_string

        except Exception as e:
            print(e)


class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.encrypt)
        self.ui.pushButton_2.clicked.connect(self.decrypt)


        self.encoded_scene = QGraphicsScene()
        self.decoded_scene = QGraphicsScene()


        self.ui.graphicsView.setScene(self.encoded_scene)
        self.ui.graphicsView_2.setScene(self.decoded_scene)

    def encrypt(self):
        try:
            img_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл", '.', 'Изображение (*.png)')
            hide_text = self.ui.lineEdit.text()
            output_path = "encrypted.png"

            # Perform image encryption using LSBSteganography class
            encrypted_path = LSBSteganography.encode_lsb(img_path, hide_text, output_path)

            # Display the encrypted image in the encoded QGraphicsView
            pixmap = QPixmap(encrypted_path)
            pixmap_item = QGraphicsPixmapItem(pixmap)
            self.encoded_scene.clear()
            self.encoded_scene.addItem(pixmap_item)


        except Exception as e:
            print(e)

    def decrypt(self):
        try:
            img_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл", '.', 'Изображение (*.png)')

            binary_string = LSBSteganography.decode_lsb(img_path)


            pixmap = QPixmap(img_path)
            pixmap_item = QGraphicsPixmapItem(pixmap)
            self.decoded_scene.clear()
            self.decoded_scene.addItem(pixmap_item)

            self.ui.label_3.setText('Зашифрование сообщение: ' + binary_string)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mw = MyApp()
    mw.show()
    sys.exit(app.exec_())
