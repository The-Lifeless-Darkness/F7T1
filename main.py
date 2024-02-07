import requests
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from io import BytesIO

toponym_longitude = 0
toponym_lattitude = 0
delta = 1
delta_min = 0
delta_max = 21


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a QLabel to display the image
        self.image_label = QLabel(self)
        self.image_label.setGeometry(0, 0, 650, 450)

        self.redrawImage()

        # Set the window size to 650x450
        self.setGeometry(100, 100, 650, 450)

        # Show the window
        self.show()

    def keyPressEvent(self, event):
        global delta, toponym_longitude, toponym_lattitude

        # Handle PgUp key press
        if event.key() == Qt.Key_PageUp:
            if delta < delta_max:
                delta += 1

        # Handle PgDown key press
        elif event.key() == Qt.Key_PageDown:
            if delta > delta_min:
                delta -= 1

        elif event.key() == Qt.Key_Right:
            if toponym_longitude < 179:
                toponym_longitude += 1

        elif event.key() == Qt.Key_Left:
            if toponym_longitude > 1:
                toponym_longitude -= 1

        elif event.key() == Qt.Key_Up:
            if toponym_longitude < 89:
                toponym_lattitude += 1

        elif event.key() == Qt.Key_Down:
            if toponym_longitude > 1:
                toponym_lattitude -= 1
        else:
            return

        self.redrawImage()

    def redrawImage(self):
        # Собираем параметры для запроса к StaticMapsAPI:
        map_params = {
            "ll": ",".join(map(str, [toponym_longitude, toponym_lattitude])),
            "z": str(delta),
            "l": "map",
            "pt": f"{(','.join(map(str, [toponym_longitude, toponym_lattitude])))},pm2dgl",
            "size": "650,450"
        }

        map_api_server = "http://static-maps.yandex.ru/1.x/"
        # ... и выполняем запрос
        response = requests.get(map_api_server, params=map_params, proxies={"http": "10.0.58.52:3128",
                                                                            "https": "10.0.58.52:3128"})

        image_data = BytesIO(response.content)

        image = QPixmap()
        image.loadFromData(image_data.getvalue())

        self.image_label.setPixmap(image)


if __name__ == '__main__':
    # Create a QApplication instance
    app = QApplication(sys.argv)

    window = MainWindow()

    # Run the application's event loop
    sys.exit(app.exec_())
