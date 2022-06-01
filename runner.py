from dataclasses import dataclass
from enum import IntEnum, auto

from PySide6.QtCore import QRect, QSize, Qt
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QApplication
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QLabel,
    QLayout,
    QLayoutItem,
    QWidget,
    QWidgetItem,
    QMenuBar,
    QListWidget,
    QTextEdit 
)
import sys



import satellite_loader as run
import satellite_state
from orbit_plot import get_gp_value, build_plot
import satellite_loader

class Position(IntEnum):
    West = auto()
    North = auto()
    South = auto()
    East = auto()
    Center = auto()


class SizeType(IntEnum):
    MinimumSize = auto()
    SizeHint = auto()


@dataclass
class ItemWrapper:
    item: QLayoutItem
    position: Position


class BorderLayout(QLayout):
    def __init__(self, parent=None, spacing: int = -1):
        super().__init__(parent)

        self._list: list[ItemWrapper] = []

        self.setSpacing(spacing)

        if parent is not None:
            self.setParent(parent)

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item: QLayoutItem):
        self.add(item, Position.West)

    def addWidget(self, widget: QWidget, position: Position):
        self.add(QWidgetItem(widget), position)

    def expandingDirections(self) -> Qt.Orientations:
        return Qt.Horizontal | Qt.Vertical

    def hasHeightForWidth(self) -> bool:
        return False

    def count(self) -> int:
        return len(self._list)

    def itemAt(self, index: int) -> QLayoutItem:
        if index < len(self._list):
            wrapper: ItemWrapper = self._list[index]
            return wrapper.item
        return None

    def minimumSize(self) -> QSize:
        return self.calculate_size(SizeType.MinimumSize)

    def setGeometry(self, rect: QRect):
        center: ItemWrapper = None
        east_width = 0
        west_width = 0
        north_height = 0
        south_height = 0

        super().setGeometry(rect)

        for wrapper in self._list:
            item: QLayoutItem = wrapper.item
            position: Position = wrapper.position

            if position == Position.North:
                item.setGeometry(
                    QRect(
                        rect.x(), north_height, rect.width(), item.sizeHint().height()
                    )
                )

                north_height += item.geometry().height() + self.spacing()

            elif position == Position.South:
                item.setGeometry(
                    QRect(
                        item.geometry().x(),
                        item.geometry().y(),
                        rect.width(),
                        item.sizeHint().height(),
                    )
                )

                south_height += item.geometry().height() + self.spacing()

                item.setGeometry(
                    QRect(
                        rect.x(),
                        rect.y() + rect.height() - south_height + self.spacing(),
                        item.geometry().width(),
                        item.geometry().height(),
                    )
                )
            elif position == Position.Center:
                center = wrapper

        center_height = rect.height() - north_height - south_height

        for wrapper in self._list:
            item: QLayoutItem = wrapper.item
            position: Position = wrapper.position

            if position == Position.West:
                item.setGeometry(
                    QRect(
                        rect.x() + west_width,
                        north_height,
                        item.sizeHint().width(),
                        center_height,
                    )
                )

                west_width += item.geometry().width() + self.spacing()

            elif position == Position.East:
                item.setGeometry(
                    QRect(
                        item.geometry().x(),
                        item.geometry().y(),
                        item.sizeHint().width(),
                        center_height,
                    )
                )

                east_width += item.geometry().width() + self.spacing()

                item.setGeometry(
                    QRect(
                        rect.x() + rect.width() - east_width + self.spacing(),
                        north_height,
                        item.geometry().width(),
                        item.geometry().height(),
                    )
                )

        if center:
            center.item.setGeometry(
                QRect(
                    west_width,
                    north_height,
                    rect.width() - east_width - west_width,
                    center_height,
                )
            )

    def sizeHint(self) -> QSize:
        return self.calculate_size(SizeType.SizeHint)

    def takeAt(self, index: int):
        if 0 <= index < len(self._list):
            layout_struct: ItemWrapper = self._list.pop(index)
            return layout_struct.item
        return None

    def add(self, item: QLayoutItem, position: Position):
        self._list.append(ItemWrapper(item, position))

    def calculate_size(self, size_type: SizeType):
        total_size = QSize()

        for wrapper in self._list:
            position = wrapper.position

            item_size: QSize
            if size_type == SizeType.MinimumSize:
                item_size = wrapper.item.minimumSize()
            else:
                item_size = wrapper.item.sizeHint()

            if position in (Position.North, Position.South, Position.Center):
                total_size.setHeight(total_size.height() + item_size.height())

            if position in (Position.West, Position.East, Position.Center):
                total_size.setWidth(total_size.width() + item_size.width())

        return total_size

class Window2(QWidget):
    def __init__(self):
        super(Window2, self).__init__()
        self.setWindowTitle('Select satellite')
        self.sat_list = QListWidget(self)
        self.setMinimumWidth(250)
        self.setMinimumHeight(800)
        sat_nameList = [o.name for o in run.get_satellitesList()]
        self.sat_list.addItems(sat_nameList)
        self.sat_list.setMinimumWidth(200)
        self.sat_list.setMinimumHeight(800)
        self.sat_list.itemClicked.connect(self.selectionChanged)
    
    def selectionChanged(self, item):
       print("Вы кликнули: {}".format(item.text()))
       satellite_loader.set_selected_sat(item.text())

       self.close()

class Window3(QWidget):
     def __init__(self):
         super(Window3, self).__init__()
         self.setWindowTitle('Select satellite')
         self.sat_list = QTextEdit(self)
         self.sat_list.setText(satellite_state.get_sattelite_passes_above_location_string())
         self.sat_list.setMinimumWidth(600)
         self.sat_list.setMinimumHeight(800)       
        
       
class Window(QWidget, QQmlApplicationEngine):
    def __init__(self):
        super().__init__()
        self.border_layout = BorderLayout()

        self.plot_3d = self.get_3d_lpot()
        self.border_layout.addWidget(self.plot_3d, Position.Center)

        self.satellite_info = self.get_satellite_info()
        self.border_layout.addWidget(self.satellite_info, Position.South)
        
        self.setLayout(self.border_layout)
        self.init_toolbar()
        self.setWindowTitle("Satellite tracker")
       

    def init_toolbar(self):

       my_menu = QMenuBar(self)

       self.change_menu = my_menu.addMenu("Change")     
       self.change_menu.addAction("Change Satellite",self.show_window_2)         

       self.change_menu = my_menu.addMenu("passes")     
       self.change_menu.addAction("Satellite passes for 5 days",self.show_window_3)    
       
    def show_window_2(self):
        self.w2 = Window2()
        self.w2.show()

    def update_widg(self):
        self.border_layout.update()
    
    def show_window_3(self):
        self.w3 = Window3()
        self.w3.show()
    

    @staticmethod
    def create_label(text: str):
        label = QLabel(text)
        label.setFrameStyle(QFrame.Box | QFrame.Raised)
        return label
  
    @staticmethod
    def get_satellite_info():
        satellite_info = satellite_state.get_satellite_param_string()
        widget = QLabel(satellite_info)
        return widget

    @staticmethod
    def get_3d_lpot():
        fig = get_gp_value()
        html = build_plot(fig)
        view = QWebEngineView()
        view.setHtml(html)
        return view     


if __name__ == "__main__":
    run.main_default()
    app = QApplication(sys.argv)
    window = Window()
    window.showMaximized()
    sys.exit(app.exec())
