#!/usr/bin/python
# -*- coding: utf-8 -*-
# Version="0.3.1"

# comicslate-editor.py - Comicslate Editor
# Copyright (C) 2020 Ihor Buhaievskyi

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# You can also redistribute and/or modify this program under the
# terms of the Psi License, specified in the accompanied COPYING
# file, as published by the Psi Project; either dated January 1st,
# 2005, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA


import re
import sys
from PyQt5 import QtGui, Qt
from PyQt5.QtWidgets import (QMainWindow, QAction, qApp, QFileDialog, QGraphicsItem,
                             QWidget, QGridLayout, QTextEdit, QPushButton, QGraphicsRectItem,
                             QGraphicsTextItem, QGraphicsScene, QHBoxLayout, QVBoxLayout,
                             QLabel, QLineEdit, QGraphicsView, QApplication)
from PyQt5.QtCore import (QSettings, QFileInfo, QSize, QRectF, QPoint, QDir, QPointF)


class main_window(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle(u'Редактор comicslate.org')
        self.readSettings()

        self.createActions()
        # self.createMenus()
        self.createToolbar()
        self.statusBar().showMessage('Ready')
        self.mw = MainWidget()
        # self.mw.setParent(self)
        self.ow = OptionWindow()
        # self.ow.setParent(self)
        self.setCentralWidget(self.mw)

    def closeEvent(self, event):
        self.writeSettings()
        event.accept()
        self.close()

    def load(self):
        self.mw.open(self.filename)

    def writeSettings(self):
        self.settings = QSettings(u'Comicslate', u'Comicslate Viewer')
        self.settings.beginGroup('MainWindow')
        self.settings.setValue("size", self.size())
        self.settings.setValue("position", self.pos())
        self.settings.setValue("lastOpenedFile", self.filename)
        self.settings.setValue("lastDir", QFileInfo(self.filename).absolutePath())
        self.settings.endGroup()

    def readSettings(self):
        self.settings = QSettings(u'Comicslate', u'Comicslate Viewer')
        self.settings.beginGroup('MainWindow')
        #self.resize(self.settings.value('size', QSize(500, 500)).toQSize())
        self.resize(self.settings.value('size', QSize(500, 500)))
        self.move(self.settings.value('position', QPoint(100, 100)))
        self.filename = self.settings.value('lastOpenedFile', '')
        self.dirName = self.settings.value('lastDir', '')
        self.settings.endGroup()

    def createActions(self):
        self.saveAct = QAction(QtGui.QIcon('icons/save.png'), 'Save', self)
        self.saveAct.setShortcut("Ctrl+S")
        self.saveAct.setToolTip(u"Сохранить")
        self.nextAct = QAction(QtGui.QIcon('icons/next.png'), 'Next File', self)
        self.nextAct.setToolTip(u"Следующий стрип")
        self.nextAct.setShortcut("Qt.Qt.RightArrow")
        self.prevAct = QAction(QtGui.QIcon('icons/prev.png'), 'Previos File', self)
        self.prevAct.setToolTip(u"Предыдущий стрип")
        self.prevAct.setShortcut("Qt.Qt.LeftArrow")
        self.openAct = QAction(QtGui.QIcon('icons/open.png'), 'Open', self)
        self.openAct.setShortcut("Ctrl+O")
        self.openAct.setToolTip(u"Открыть")
        self.hideAct = QAction(QtGui.QIcon('icons/hide.png'), 'Hide', self)
        self.hideAct.setShortcut("Ctrl+H")
        self.hideAct.setToolTip(u"Скрыть/Показать все балуны")
        self.zoomInAct = QAction(QtGui.QIcon('icons/zoom-in.png'), 'ZoomIn', self)
        self.zoomInAct.setShortcut("Ctrl+-")
        self.zoomInAct.setToolTip(u"Увеличить все")
        self.zoomOutAct = QAction(QtGui.QIcon('icons/zoom-out.png'), 'ZoomOut', self)
        self.zoomOutAct.setShortcut("Ctrl+=")
        self.zoomOutAct.setToolTip(u"Уменьшить все")
        self.optionAct = QAction(QtGui.QIcon('icons/option.png'), 'Option', self)
        # self.open_file.setShortcut("Ctrl+O")
        self.optionAct.setToolTip(u"Опции")
        self.exitAct = QAction(QtGui.QIcon('icons/exit.png'), 'Exit', self)
        self.exitAct.setShortcut("Ctrl+Q")
        self.exitAct.setToolTip(u"Выход")
        self.openAct.triggered.connect(self.openFile)
        self.exitAct.triggered.connect(self.exitProgramm)
        self.nextAct.triggered.connect(self.nextFile)
        self.prevAct.triggered.connect(self.prevFile)
        self.optionAct.triggered.connect(self.optionShow)
        self.hideAct.triggered.connect(self.hideAll)
        self.zoomInAct.triggered.connect(self.zoomIn)
        self.zoomOutAct.triggered.connect(self.zoomOut)
        self.saveAct.triggered.connect(self.save)

    def save(self):
        self.mw.saveTextFile()

    def zoomIn(self):
        self.mw.zoomIn()

    def zoomOut(self):
        self.mw.zoomOut()

    def hideAll(self):
        self.mw.hideAllBaloons()

    def optionShow(self):
        self.ow.show()

    def exitProgramm(self):
        self.writeSettings()
        self.close()
        qApp.closeAllWindows()

    def createMenus(self):
        menubar = self.menuBar()
        file = menubar.addMenu('&File')
        file.addAction(self.openAct)
        # file.addMenu('ff')

        menu_bar = self.menuBar()
        files = menu_bar.addMenu('&Exit')
        files.addAction(self.exitAct)

    def createToolbar(self):
        self.toolbar = self.addToolBar('toolbar')
        self.toolbar.addAction(self.openAct)
        self.toolbar.addAction(self.saveAct)
        self.toolbar.addAction(self.prevAct)
        self.toolbar.addAction(self.nextAct)
        self.toolbar.addAction(self.hideAct)
        # self.toolbar.addAction(self.zoomInAct)
        # self.toolbar.addAction(self.zoomOutAct)
        # self.toolbar.addAction(self.optionAct)
        self.toolbar.addAction(self.exitAct)

    def openFile(self):
        fileWidget = QFileDialog()
        filename = fileWidget.getOpenFileName(self, 'Open file', self.dirName, "Image Files (*.png *.jpg *.bmp *.gif)")
        # print filename
        if filename != '':
            self.filename = filename
            fileInf = QFileInfo(self.filename)
            self.dirName = fileInf.canonicalPath()
            self.setWindowTitle(self.filename)
            self.mw.open(self.filename)

    def nextFile(self):
        lst, filename = self.dirList()
        if lst != None:
            indexFile = lst.lastIndexOf(filename.fileName())
            if indexFile + 1 < len(lst):
                self.filename = self.directory.filePath(lst[indexFile + 1])
                self.setWindowTitle(self.filename)
                self.mw.open(self.filename)

    def prevFile(self):
        lst, filename = self.dirList()
        if lst != None:
            indexFile = lst.lastIndexOf(filename.fileName())
            if indexFile - 1 >= 0:
                self.filename = self.directory.filePath(lst[indexFile - 1])
                self.setWindowTitle(self.filename)
                self.mw.open(self.filename)

    def dirList(self):
        if self.filename != '':
            fileInf = QFileInfo(self.filename)
            self.directory = QDir(fileInf.canonicalPath())
            listOfFiles = self.directory.entryList(Qt.QStringList("*.png *.jpg *.bmp *.gif".split(" ")))
            return listOfFiles, fileInf
        else:
            return None, None


class node(QGraphicsItem):
    def __init__(self, parent=None, scene=None):
        QGraphicsItem.__init__(self, parent=None, scene=None)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setZValue(-1)

    def boundingRect(self):
        return QRectF(-5, -5, 10, 10)

    def shape(self):
        path = QtGui.QPainterPath()
        path.addEllipse(-5, -5, 10, 10)
        return path

    def paint(self, painter, option, widget=None):
        painter.setPen(Qt.Qt.NoPen)
        painter.setBrush(Qt.Qt.darkGreen)
        painter.drawEllipse(-5, -5, 10, 10)

    def type(self):
        return 65540

    def mousePressEvent(self, event):
        self.parentItem().textItem.show()
        self.parentItem().color = QtGui.QColor(255, 255, 255, 160)
        self.update()
        QGraphicsItem.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        self.parentItem().retMoved(self.pos(), self)

        self.update()
        QGraphicsItem.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event):
        self.parentItem().textItem.hide()
        self.parentItem().color = QtGui.QColor(255, 255, 255, 40)
        self.update()
        QGraphicsItem.mouseReleaseEvent(self, event)


class nodeDel(QGraphicsItem):
    def __init__(self, parent=None, scene=None):
        QGraphicsItem.__init__(self, parent=None, scene=None)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setZValue(-1)

    def boundingRect(self):
        return QRectF(-5, -5, 10, 10)

    def shape(self):
        path = QtGui.QPainterPath()
        path.addEllipse(-5, -5, 10, 10)
        return path

    def paint(self, painter, option, widget=None):
        painter.setPen(Qt.Qt.NoPen)
        painter.setBrush(Qt.Qt.red)
        painter.drawEllipse(-5, -5, 10, 10)

    def type(self):
        return 65540

    def mousePressEvent(self, event):
        self.parentItem().textEdit.Cancel()
        self.parentItem().scene().removeItem(self.parentItem())
        self.update()
        QGraphicsItem.mousePressEvent(self, event)


class myTextEdit(QWidget):
    def __init__(self, text, parent=None):
        QWidget.__init__(self, parent=None)
        self.grid = QGridLayout()
        # self.setWindowFlags(Qt.Qt.FramelessWindowHint | Qt.Qt.WindowStaysOnBottomHint)
        self.readSettings()
        self.text = text
        self.parent = parent

        self.textEdit = QTextEdit()
        self.textEdit.setPlainText(self.text)

        self.buttonOk = QPushButton(u"Применить", self)
        self.buttonCancel = QPushButton(u"Отменить", self)

        self.grid.addWidget(self.textEdit, 0, 0, 1, 2)
        self.grid.addWidget(self.buttonOk, 1, 0)
        self.grid.addWidget(self.buttonCancel, 1, 1)
        self.setLayout(self.grid)

        self.okAct = QAction('Ok', self)
        self.cancelAct = QAction('Cancel', self)

        #self.connect(self.buttonOk, SIGNAL('clicked()'), self.Ok)
        self.buttonOk.connect(self.Ok)
        #self.connect(self.buttonCancel, SIGNAL('clicked()'), self.Cancel)
        self.buttonCancel.connect(self.Cancel)

    def Ok(self):
        # print unicode(self.textEdit.toPlainText())
        self.parent.retOk(self.textEdit.toPlainText())
        self.writeSettings()
        self.close()

    def Cancel(self):
        # print unicode(self.text)
        self.parent.retClose()
        self.writeSettings()
        self.close()

    def closeEvent(self, event):
        self.parent.retClose()
        self.writeSettings()
        event.accept()

    def writeSettings(self):
        self.settings = QSettings(u'Comicslate', u'Comicslate Viewer')
        self.settings.beginGroup('EditWindow')
        self.settings.setValue("size", self.size())
        self.settings.setValue("position", self.pos())
        self.settings.endGroup()

    def readSettings(self):
        self.settings = QSettings(u'Comicslate', u'Comicslate Viewer')
        self.settings.beginGroup('EditWindow')
        self.resize(self.settings.value('size', QSize(100, 100)).toSize())
        self.move(self.settings.value('position', QPoint(100, 100)).toPoint())
        self.settings.endGroup()


class myBaloon(QGraphicsRectItem):
    def __init__(self, text, x, y, w, h, niks, parent=None, scene=None):
        QGraphicsRectItem.__init__(self, QRectF(x - 5, y - 5, w + 10, h + 10), parent=None)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.niks = niks
        self.text = Qt.QString(text.decode("utf-8"))
        font = QtGui.QFont("Comic Sans MS", 8)
        self.color = QtGui.QColor(255, 255, 255, 255)
        self.pen = QtGui.QPen(Qt.Qt.black, 0)

        self.textItem = QGraphicsTextItem(self)
        self.textItem.setHtml("<div align=\"center\">" + self.text + "</div>")
        self.textItem.setTextWidth(self.w)
        self.textItem.setPos(self.x - 1, self.y - 1)
        self.textItem.setFont(font)

        point = QPointF(self.x, self.y)
        self.baloonNode1 = node()
        self.baloonNode1.setParentItem(self)
        self.baloonNode1.setPos(point)
        point = QPointF(self.x + self.w, self.y + self.h)
        self.baloonNode2 = node()
        self.baloonNode2.setParentItem(self)
        self.baloonNode2.setPos(point)
        self.baloonNode1.hide()
        self.baloonNode2.hide()
        point = QPointF(self.x + self.w, self.y)
        self.delNode = nodeDel()
        self.delNode.setParentItem(self)
        self.delNode.setPos(point)
        self.delNode.hide()

        self.setZValue(0)
        self.setEnabled(True)
        self.setAcceptHoverEvents(True)

        self.itemsColided = []

    def boundingRect(self):
        return QRectF(self.x - 5, self.y - 5, self.w + 10, self.h + 10)

    def shape(self):
        path = QtGui.QPainterPath()
        path.addRoundedRect(self.x - 5, self.y - 5, self.w + 10, self.h + 10, 5, 5)
        self.textItem.setTextWidth(self.w)
        self.textItem.setPos(self.x - 1, self.y - 1)
        return path

    def type(self):
        return 65550

    def paint(self, painter, option, widget=None):
        painter.save()
        painter.setBrush(self.color)
        painter.setPen(self.pen)
        painter.drawRoundedRect(self.x - 5, self.y - 5, self.w + 10, self.h + 10, 5, 5)
        painter.restore()

    def mousePressEvent(self, event):
        if event.button() == Qt.Qt.LeftButton:
            self.textItem.hide()
            self.textItem.setTextInteractionFlags(Qt.Qt.TextEditorInteraction)
            self.setFlag(QGraphicsItem.ItemIsMovable)
            self.baloonNode1.show()
            self.baloonNode2.show()
            self.delNode.show()
            for i in self.itemsColided:
                i.show()
            for i in self.scene().items():
                if self.collidesWithItem(i):
                    if i.type() not in [7, 65540]:
                        if i != self:
                            i.hide()
                            # print i.type(), i
                            self.itemsColided.append(i)
            self.color = QtGui.QColor(255, 255, 255, 40)
            self.pen = QtGui.QPen(Qt.Qt.blue, 2)
            self.textEdit = myTextEdit(self.fullText(), self)
            self.textEdit.setParent(self.parentWidget())
            self.textEdit.show()
            self.update()

    def fullText(self):
        string = ''
        for i in self.niks:
            string = string + i
        string = string + self.text
        return string

    def onlyText(self, text):
        self.niks = re.compile(u'\(.*?\)|\[.*?\]', re.S).findall(text)
        text = re.compile(u'\(.*?\)|\[.*?\]').sub('', text)
        return text

    def retText(self):
        string = "@" + str(int(self.y)) + "," + str(int(self.x)) + "," + str(int(self.w)) + "," + str(
            int(self.h)) + "\n"
        string = string + self.fullText() + "\n~"
        # print string
        return string

    def retOk(self, text):
        self.textItem.show()
        self.text = self.onlyText(text)
        # print unicode(text)
        self.textItem.setHtml("<div align=\"center\">" + self.text + "</div>")
        self.setFlag(QGraphicsItem.ItemIsMovable, enabled=False)
        self.textItem.setTextInteractionFlags(Qt.Qt.NoTextInteraction)
        self.color = QtGui.QColor(255, 255, 255, 255)
        self.pen = QtGui.QPen(Qt.Qt.black, 0)

        for i in self.itemsColided:
            i.show()
        self.baloonNode1.hide()
        self.baloonNode2.hide()
        self.delNode.hide()
        self.update()

    def retClose(self):
        self.textItem.show()
        self.textItem.setTextInteractionFlags(Qt.Qt.NoTextInteraction)
        self.setFlag(QGraphicsItem.ItemIsMovable, enabled=False)
        self.color = QtGui.QColor(255, 255, 255, 255)
        self.pen = QtGui.QPen(Qt.Qt.black, 0)
        self.baloonNode1.hide()
        self.baloonNode2.hide()
        self.delNode.hide()
        for i in self.itemsColided:
            i.show()
        self.update()

    def retMoved(self, pos, node):
        if node == self.baloonNode1:
            self.w = self.w + self.x - pos.x()
            self.h = self.h + self.y - pos.y()
            self.x = pos.x()
            self.y = pos.y()
        if node == self.baloonNode2:
            sceneW = self.w + self.x
            sceneH = self.h + self.y
            self.w = self.w - sceneW + pos.x()
            self.h = self.h - sceneH + pos.y()
        self.textItem.setTextWidth(self.w)
        self.textItem.setPos(self.x - 1, self.y - 1)
        point = QPointF(self.x + self.w, self.y)
        self.delNode.setPos(point)
        self.update()

    def hoverEnterEvent(self, event):
        # print 'focus in'
        self.setZValue(1)
        self.update()

    def hoverLeaveEvent(self, event):
        self.setZValue(0)
        self.update()


class OptionWindow(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)
        self.grid = QGridLayout()
        self.setLayout(self.grid)


class SceneWidget(QGraphicsScene):
    def __init__(self, *args):
        QGraphicsScene.__init__(self, *args)

    def mouseDoubleClickEvent(self, event):
        # print "click ok"
        if event.button() == Qt.Qt.LeftButton:
            p = event.buttonDownScenePos(Qt.Qt.LeftButton)
            baloon = myBaloon("", p.x(), p.y(), 40.0, 40.0, [])
            self.addItem(baloon)


class MainWidget(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)
        self.grid = QGridLayout()
        self.hbox = QHBoxLayout()
        self.vbox = QVBoxLayout()
        self.hbox.addStretch(1)
        self.imageName = ""
        self.scene = SceneWidget()

        self.view = QGraphicsView(self.scene)
        self.view.setAlignment(Qt.Qt.AlignTop | Qt.Qt.AlignLeft)
        self.view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        # self.view.setViewportUpdateMode(QtGui.QGraphicsView.BoundingRectViewportUpdate)

        labelTitle = QLabel(u"Заглавие стрипа")
        labelPath = QLabel(u"Путь хранения стрипа в вики")
        self.titleImg = QLineEdit(self)
        self.lineEdit = QLineEdit(self)
        self.grid.addWidget(labelTitle, 0, 0)
        self.grid.addWidget(self.titleImg, 0, 1)
        self.grid.addWidget(labelPath, 1, 0)
        self.grid.addWidget(self.lineEdit, 1, 1)
        self.grid.addWidget(self.view, 2, 0, 2, 2)
        self.setLayout(self.grid)

        self.hideItems = []
        self.hided = False

    def zoomIn(self):
        self.view.scale(1.25, 1.25)
        self.scene.update()

    def zoomOut(self):
        self.view.scale(0.75, 0.75)
        self.scene.update()

    def openTxt(self, filename):
        def str2int(string):
            result = []
            for i in string.split(","):
                # print string
                result.append(int(i))
            return result

        fileInf = QFileInfo(filename)
        self.txtname = fileInf.absolutePath() + '/' + fileInf.baseName() + ".txt"
        coordinates = []
        texts = []
        niks = []
        if QFileInfo(self.txtname).isFile():
            f = open(self.txtname, "r")
            data = f.read()
            f.close()
            self.body = re.compile(u'<aimg}}(.*)', re.S).findall(data)[0]
            # print self.body
            s = re.compile(u'@(.*?)~', re.S).findall(data)
            titleImg = re.compile(u'{cnav}[^*]\*\*([^*]*?)\*').findall(data)[0].decode('utf8')
            self.titleImg.setText(titleImg)
            pathImg = re.compile(u'{aimg>([^]]*?)}').findall(data)
            self.lineEdit.setText(":".join(pathImg[0].split(":")[:-1]))
            # print ":".join(pathImg[0].split(":")[:-1])
            # print pathImg[0].split(":")
            for i in s:
                ss = i.split("\n")

                coordinates.append(str2int(ss[0]))
                rr = re.compile(u'\(.*?\)|\[.*?\]', re.S).findall(ss[1])
                # print rr
                niks.append(rr)
                ss[1] = re.compile(u'\(.*?\)|\[.*?\]').sub('', ss[1])
                # ss[1]=re.compile(u'\[.*?\]').sub('',ss[1])
                texts.append(ss[1])
            return coordinates, texts, niks
        else:
            main.statusBar().showMessage(u'Файл ' + filename + u' не имеет текстового подстрочника')
            return None, None, None

    def open(self, fileName):
        if fileName != '':
            self.imageName = fileName
            image = QtGui.QImage(fileName)
            self.scene.clear()
            self.scene.setSceneRect(0.0, 0.0, float(image.width()), float(image.height()))
            self.scene.addPixmap(QtGui.QPixmap.fromImage(image))
            coord, texts, niks = self.openTxt(fileName)
            if coord != None:
                for i in range(0, len(coord)):
                    balun = myBaloon(texts[i], coord[i][1], coord[i][0], coord[i][2], coord[i][3], niks[i])
                    self.scene.addItem(balun)
                # break
                main.statusBar().showMessage(u'Загружен ' + fileName)
            self.scene.update()

    def saveTextFile(self):
        fileInf = QFileInfo(self.txtname)
        fileInf2 = QFileInfo(self.imageName)
        pathImg = self.lineEdit.text()
        titleImg = self.titleImg.text()
        # print titleImg.toUtf8()
        body1 = u"""{cnav} **""" + titleImg.toUtf8() + """**\\\n{{aimg>""" + pathImg + ":" + fileInf2.fileName() + """}}\n"""
        sss = ''
        for i in self.scene.items():
            if i.type() == 65550:
                sss = i.retText() + "\n" + sss + "\n"
        sss = sss.strip().encode('utf-8')

        if QFileInfo(self.txtname).isFile():
            f = open(self.txtname, "w")
            body2 = u"""{{<aimg}}"""
            ff = re.compile(u"}}([^{]*?){{", re.S).sub('}}' + "\n" + sss + '{{', self.body)
            # f.write(ff)
            f.write(body1 + sss + body2 + self.body)
            f.close()
        else:
            f = open(self.txtname, "w")

            body2 = u"""{{<aimg}}
{cnav}"""
            f.write(body1 + sss + body2)
            f.close()
        main.statusBar().showMessage(u'Сохранен ' + fileInf.fileName() + u" к стрипу" + fileInf2.fileName())

    def hideAllBaloons(self):
        if not self.hided:
            for i in self.scene.items():
                if i.type() not in [7, 65540]:
                    if i != self:
                        i.hide()
                        # print i.type(), i
                        self.hideItems.append(i)
            self.hided = True
        else:
            for i in self.hideItems:
                i.show()
            self.hided = False


app = QApplication(sys.argv)
main = main_window()
main.load()
main.show()

sys.exit(app.exec_())
