import requests
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtGui import QPixmap
from io import BytesIO

toponym_longitude = 0
toponym_lattitude = 0
delta = 0.0005

# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    "ll": ",".join(map(str, [toponym_longitude, toponym_lattitude])),
    "spn": ",".join(map(str, [delta, delta])),
    "l": "map",
    "pt": f"{(','.join(map(str, [toponym_longitude, toponym_lattitude])))},pm2dgl",
    "size": "650,450"
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params, proxies={"http": "10.0.58.52:3128",
                                                                    "https": "10.0.58.52:3128"})


class MainWindow(QMainWindow):
    def __init__(self, image_bytes):
        super().__init__()

        # Create a QLabel to display the image
        self.image_label = QLabel(self)
        self.image_label.setGeometry(0, 0, 650, 450)

        # Load the image from the BytesIO object
        image = QPixmap()
        image.loadFromData(image_bytes.getvalue())

        # Set the image as the pixmap of the QLabel
        self.image_label.setPixmap(image)

        # Set the window size to 650x450
        self.setGeometry(100, 100, 650, 450)

        # Show the window
        self.show()


if __name__ == '__main__':
    # Create a QApplication instance
    app = QApplication(sys.argv)

    # Create a BytesIO object with the image data
    image_data = BytesIO(response.content)

    # Create the main window with the image data
    window = MainWindow(image_data)

    # Run the application's event loop
    sys.exit(app.exec_())
