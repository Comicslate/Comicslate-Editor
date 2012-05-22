#!/usr/bin/python
# -*- coding: utf-8 -*-
#Version="0.3"

import sys, os, re
from PyQt4 import QtGui, QtCore,Qt

class main_window(QtGui.QMainWindow):
	def __init__ (self, parent=None):
		QtGui.QMainWindow.__init__ (self, parent)
		self.setWindowTitle(u'Редактор comicslate.org')
		self.readSettings()
		
		
		
		self.createActions()
		#self.createMenus()
		self.createToolbar()
		self.statusBar().showMessage('Ready')
		self.mw=MainWidget()
		#self.mw.setParent(self)
		self.ow=OptionWindow()
		#self.ow.setParent(self)
		self.setCentralWidget(self.mw)
	
	def closeEvent(self, event):
		self.writeSettings()
		event.accept()
		self.close()
	
	def load(self):
		self.mw.open(self.filename)
		
	def writeSettings(self):
		self.settings = QtCore.QSettings(u'Comicslate',u'Comicslate Viewer')
		self.settings.beginGroup('MainWindow')
		self.settings.setValue("size",self.size())
		self.settings.setValue("position",self.pos())
		self.settings.setValue("lastOpenedFile",self.filename)
		self.settings.setValue("lastDir",QtCore.QFileInfo(self.filename).absolutePath())
		self.settings.endGroup()
		
	def readSettings(self):
		self.settings = QtCore.QSettings(u'Comicslate',u'Comicslate Viewer')
		self.settings.beginGroup('MainWindow')
		self.resize(self.settings.value('size',QtCore.QSize(500,500)).toSize())
		self.move(self.settings.value('position',QtCore.QPoint(100,100)).toPoint())
		self.filename=self.settings.value('lastOpenedFile','').toString()
		self.dirName=self.settings.value('lastDir','').toString()
		self.settings.endGroup()
		
	def createActions(self):
		self.saveAct = QtGui.QAction(QtGui.QIcon('icons/save.png'), 'Save', self)
		self.saveAct.setShortcut("Ctrl+S")
		self.saveAct.setToolTip(u"Сохранить")
		self.nextAct=QtGui.QAction(QtGui.QIcon('icons/next.png'), 'Next File', self)
		self.nextAct.setToolTip(u"Следующий стрип")
		self.nextAct.setShortcut("Qt.Qt.RightArrow")
		self.prevAct=QtGui.QAction(QtGui.QIcon('icons/prev.png'), 'Previos File', self)
		self.prevAct.setToolTip(u"Предыдущий стрип")
		self.prevAct.setShortcut("Qt.Qt.LeftArrow")
		self.openAct = QtGui.QAction(QtGui.QIcon('icons/open.png'), 'Open', self)
		self.openAct.setShortcut("Ctrl+O")
		self.openAct.setToolTip(u"Открыть")
		self.hideAct = QtGui.QAction(QtGui.QIcon('icons/hide.png'), 'Hide', self)
		self.hideAct.setShortcut("Ctrl+H")
		self.hideAct.setToolTip(u"Скрыть/Показать все балуны")
		self.zoomInAct = QtGui.QAction(QtGui.QIcon('icons/zoom-in.png'), 'ZoomIn', self)
		self.zoomInAct.setShortcut("Ctrl+-")
		self.zoomInAct.setToolTip(u"Увеличить все")
		self.zoomOutAct = QtGui.QAction(QtGui.QIcon('icons/zoom-out.png'), 'ZoomOut', self)
		self.zoomOutAct.setShortcut("Ctrl+=")
		self.zoomOutAct.setToolTip(u"Уменьшить все")
		self.optionAct = QtGui.QAction(QtGui.QIcon('icons/option.png'), 'Option', self)
		#self.open_file.setShortcut("Ctrl+O")
		self.optionAct.setToolTip(u"Опции")
		self.exitAct = QtGui.QAction(QtGui.QIcon('icons/exit.png'), 'Exit', self)
		self.exitAct.setShortcut("Ctrl+Q")
		self.exitAct.setToolTip(u"Выход")
		self.connect(self.openAct, QtCore.SIGNAL('triggered()'), self.openFile)
		self.connect(self.exitAct, QtCore.SIGNAL('triggered()'), self.exitProgramm)
		self.connect(self.nextAct, QtCore.SIGNAL('triggered()'), self.nextFile)
		self.connect(self.prevAct, QtCore.SIGNAL('triggered()'), self.prevFile)
		self.connect(self.optionAct, QtCore.SIGNAL('triggered()'), self.optionShow)
		self.connect(self.hideAct, QtCore.SIGNAL('triggered()'), self.hideAll)
		self.connect(self.zoomInAct, QtCore.SIGNAL('triggered()'), self.zoomIn)
		self.connect(self.zoomOutAct, QtCore.SIGNAL('triggered()'), self.zoomOut)
		self.connect(self.saveAct, QtCore.SIGNAL('triggered()'), self.save)
	
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
		QtGui.qApp.closeAllWindows()
	
	def createMenus(self):
		menubar = self.menuBar()
		file = menubar.addMenu('&File')
		file.addAction(self.openAct)
		#file.addMenu('ff')

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
		#self.toolbar.addAction(self.zoomInAct)
		#self.toolbar.addAction(self.zoomOutAct)
		#self.toolbar.addAction(self.optionAct)
		self.toolbar.addAction(self.exitAct)
	
	def openFile(self):
		fileWidget=QtGui.QFileDialog()
		filename = fileWidget.getOpenFileName(self, 'Open file', self.dirName,"Image Files (*.png *.jpg *.bmp *.gif)")
		#print filename
		if filename != '':
			self.filename = filename
			fileInf=QtCore.QFileInfo(self.filename)
			self.dirName = fileInf.canonicalPath()
			self.setWindowTitle(self.filename)
			self.mw.open(self.filename)

		
	def nextFile(self):
		lst, filename=self.dirList()
		if lst != None:
			indexFile=lst.lastIndexOf(filename.fileName())
			if indexFile+1 < len(lst):
				self.filename=self.directory.filePath(lst[indexFile+1])
				self.setWindowTitle(self.filename)
				self.mw.open(self.filename)
			
	def prevFile(self):
		lst, filename=self.dirList()
		if lst != None:
			indexFile=lst.lastIndexOf(filename.fileName())
			if indexFile-1 >= 0:
				self.filename=self.directory.filePath(lst[indexFile-1])
				self.setWindowTitle(self.filename)
				self.mw.open(self.filename)
			
	def dirList(self):
		if self.filename != '':
			fileInf=QtCore.QFileInfo(self.filename)
			self.directory=QtCore.QDir(fileInf.canonicalPath())
			listOfFiles=self.directory.entryList(QtCore.QStringList("*.png *.jpg *.bmp *.gif".split(" ")))
			return listOfFiles, fileInf
		else:
			return None, None

class node(QtGui.QGraphicsItem):
	def __init__(self, parent = None, scene = None):
		QtGui.QGraphicsItem.__init__(self, parent = None, scene = None)
		self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
		self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)
		self.setZValue(-1)
		
	def boundingRect(self):
		return QtCore.QRectF(-5, -5, 10, 10)
		
	def shape(self):
		path=QtGui.QPainterPath()
		path.addEllipse(-5, -5, 10, 10)
		return path
		
	def paint(self, painter, option, widget = None):
		painter.setPen(Qt.Qt.NoPen)
		painter.setBrush(Qt.Qt.darkGreen)
		painter.drawEllipse(-5, -5, 10, 10)
		
	def type(self):
		return 65540
		
	def mousePressEvent(self, event):
		self.parentItem().textItem.show()
		self.parentItem().color = QtGui.QColor(255,255,255,160)
		self.update()
		QtGui.QGraphicsItem.mousePressEvent(self, event)
		
	def mouseMoveEvent(self, event):
		self.parentItem().retMoved(self.pos(),self)
		
		self.update()
		QtGui.QGraphicsItem.mouseMoveEvent(self, event)
		
	def mouseReleaseEvent(self, event):
		self.parentItem().textItem.hide()
		self.parentItem().color = QtGui.QColor(255,255,255,40)
		self.update()
		QtGui.QGraphicsItem.mouseReleaseEvent(self, event)
		
class nodeDel(QtGui.QGraphicsItem):
	def __init__(self, parent = None, scene = None):
		QtGui.QGraphicsItem.__init__(self, parent = None, scene = None)
		self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
		self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)
		self.setZValue(-1)
		
	def boundingRect(self):
		return QtCore.QRectF(-5, -5, 10, 10)
		
	def shape(self):
		path=QtGui.QPainterPath()
		path.addEllipse(-5, -5, 10, 10)
		return path
		
	def paint(self, painter, option, widget = None):
		painter.setPen(Qt.Qt.NoPen)
		painter.setBrush(Qt.Qt.red)
		painter.drawEllipse(-5, -5, 10, 10)
		
	def type(self):
		return 65540
		
	def mousePressEvent(self, event):
		self.parentItem().textEdit.Cancel()
		self.parentItem().scene().removeItem(self.parentItem())
		self.update()
		QtGui.QGraphicsItem.mousePressEvent(self, event)

class myTextEdit(QtGui.QWidget):
	def __init__(self, text, parent = None):
		QtGui.QWidget.__init__(self, parent = None)
		self.grid = QtGui.QGridLayout()
		#self.setWindowFlags(Qt.Qt.FramelessWindowHint | Qt.Qt.WindowStaysOnBottomHint)
		self.readSettings()
		self.text=text
		self.parent=parent
		
		self.textEdit=QtGui.QTextEdit()
		self.textEdit.setPlainText(self.text)
		
		self.buttonOk=QtGui.QPushButton(u"Применить",self)
		self.buttonCancel=QtGui.QPushButton(u"Отменить",self)
		
		self.grid.addWidget(self.textEdit,0,0,1,2)
		self.grid.addWidget(self.buttonOk,1,0)
		self.grid.addWidget(self.buttonCancel,1,1)
		self.setLayout(self.grid)
		
		self.okAct=QtGui.QAction('Ok', self)
		self.cancelAct=QtGui.QAction('Cancel', self)
		
		self.connect(self.buttonOk, QtCore.SIGNAL('clicked()'), self.Ok)
		self.connect(self.buttonCancel, QtCore.SIGNAL('clicked()'), self.Cancel)

	def Ok(self):
		#print unicode(self.textEdit.toPlainText())
		self.parent.retOk(self.textEdit.toPlainText())
		self.writeSettings()
		self.close()
	
	def Cancel(self):
		#print unicode(self.text)
		self.parent.retClose()
		self.writeSettings()
		self.close()
		
	def closeEvent(self, event):
		self.parent.retClose()
		self.writeSettings()
		event.accept()
		
	def writeSettings(self):
		self.settings = QtCore.QSettings(u'Comicslate',u'Comicslate Viewer')
		self.settings.beginGroup('EditWindow')
		self.settings.setValue("size",self.size())
		self.settings.setValue("position",self.pos())
		self.settings.endGroup()
		
	def readSettings(self):
		self.settings = QtCore.QSettings(u'Comicslate',u'Comicslate Viewer')
		self.settings.beginGroup('EditWindow')
		self.resize(self.settings.value('size',QtCore.QSize(100,100)).toSize())
		self.move(self.settings.value('position',QtCore.QPoint(100,100)).toPoint())
		self.settings.endGroup()


class myBaloon(QtGui.QGraphicsRectItem):
	def __init__(self, text, x, y, w, h, niks, parent = None, scene = None):
		QtGui.QGraphicsRectItem.__init__(self, QtCore.QRectF(x-5, y-5, w+10, h+10),parent = None)
		self.x=x
		self.y=y
		self.w=w
		self.h=h
		self.niks=niks
		self.text=QtCore.QString(text.decode("utf-8"))
		font= QtGui.QFont("Comic Sans MS", 8)
		self.color=QtGui.QColor(255,255,255,255)
		self.pen=QtGui.QPen(Qt.Qt.black,0)
		
		self.textItem=QtGui.QGraphicsTextItem(self)
		self.textItem.setHtml("<div align=\"center\">"+self.text+"</div>")
		self.textItem.setTextWidth(self.w)
		self.textItem.setPos(self.x-1,self.y-1)
		self.textItem.setFont(font)
		
		point=QtCore.QPointF(self.x, self.y)
		self.baloonNode1 = node()
		self.baloonNode1.setParentItem(self)
		self.baloonNode1.setPos(point)
		point=QtCore.QPointF(self.x+self.w, self.y+self.h)
		self.baloonNode2 = node()
		self.baloonNode2.setParentItem(self)
		self.baloonNode2.setPos(point)
		self.baloonNode1.hide()
		self.baloonNode2.hide()
		point=QtCore.QPointF(self.x+self.w, self.y)
		self.delNode = nodeDel()
		self.delNode.setParentItem(self)
		self.delNode.setPos(point)
		self.delNode.hide()
		
		self.setZValue(0)
		self.setEnabled(True)
		self.setAcceptHoverEvents(True)
		
		self.itemsColided=[]
		
	def boundingRect(self):
		return QtCore.QRectF(self.x-5, self.y-5, self.w+10, self.h+10)
		
	def shape(self):
		path=QtGui.QPainterPath()
		path.addRoundedRect(self.x-5, self.y-5, self.w+10, self.h+10,5,5)
		self.textItem.setTextWidth(self.w)
		self.textItem.setPos(self.x-1,self.y-1)
		return path
	
	def type(self):
		return 65550
	
	def paint(self, painter, option, widget = None):
		painter.save()
		painter.setBrush(self.color)
		painter.setPen(self.pen)
		painter.drawRoundedRect(self.x-5, self.y-5, self.w+10, self.h+10, 5, 5)
		painter.restore()
		
	def mousePressEvent(self, event):
		if event.button() == Qt.Qt.LeftButton:
			self.textItem.hide()
			self.textItem.setTextInteractionFlags(Qt.Qt.TextEditorInteraction)
			self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
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
							#print i.type(), i
							self.itemsColided.append(i)
			self.color=QtGui.QColor(255,255,255,40)
			self.pen=QtGui.QPen(Qt.Qt.blue,2)
			self.textEdit=myTextEdit(self.fullText(),self)
			self.textEdit.setParent(self.parentWidget())
			self.textEdit.show()
			self.update()
	
	def fullText(self):
		string=''
		for i in self.niks:
			string=string+i
		string=string+self.text
		return string
	
	def onlyText(self, text):
		self.niks=re.compile(u'\(.*?\)|\[.*?\]',re.S).findall(text)
		text=re.compile(u'\(.*?\)|\[.*?\]').sub('', unicode(text))
		return text
		
	def retText(self):
		string="@"+str(int(self.y))+","+str(int(self.x))+","+str(int(self.w))+","+str(int(self.h))+"\n"
		string=string+self.fullText()+"\n~"
		#print string
		return string
	
	def retOk(self, text):
		self.textItem.show()
		self.text=self.onlyText(text)
		#print unicode(text)
		self.textItem.setHtml("<div align=\"center\">"+self.text+"</div>")
		self.setFlag(QtGui.QGraphicsItem.ItemIsMovable,enabled = False)
		self.textItem.setTextInteractionFlags(Qt.Qt.NoTextInteraction)
		self.color=QtGui.QColor(255,255,255,255)
		self.pen=QtGui.QPen(Qt.Qt.black,0)
		
		for i in self.itemsColided:
			i.show()
		self.baloonNode1.hide()
		self.baloonNode2.hide()
		self.delNode.hide()
		self.update()
		
	def retClose(self):
		self.textItem.show()
		self.textItem.setTextInteractionFlags(Qt.Qt.NoTextInteraction)
		self.setFlag(QtGui.QGraphicsItem.ItemIsMovable,enabled = False)
		self.color=QtGui.QColor(255,255,255,255)
		self.pen=QtGui.QPen(Qt.Qt.black,0)
		self.baloonNode1.hide()
		self.baloonNode2.hide()
		self.delNode.hide()
		for i in self.itemsColided:
			i.show()
		self.update()
		
	def retMoved(self,pos,node):
		if node == self.baloonNode1:
			self.w = self.w + self.x - pos.x()
			self.h = self.h + self.y - pos.y()
			self.x=pos.x()
			self.y=pos.y()
		if node == self.baloonNode2:
			sceneW = self.w + self.x
			sceneH = self.h + self.y
			self.w=self.w - sceneW  + pos.x()
			self.h=self.h - sceneH  + pos.y()
		self.textItem.setTextWidth(self.w)
		self.textItem.setPos(self.x-1,self.y-1)
		point=QtCore.QPointF(self.x+self.w, self.y)
		self.delNode.setPos(point)
		self.update()
	
	def hoverEnterEvent(self, event):
		#print 'focus in'
		self.setZValue(1)
		self.update()
	
	def hoverLeaveEvent(self, event):
		self.setZValue(0)
		self.update()

class OptionWindow(QtGui.QWidget):
	def __init__(self, *args):
		QtGui.QWidget.__init__(self, *args)
		self.grid = QtGui.QGridLayout()
		
		
		
		self.setLayout(self.grid)
		

class SceneWidget(QtGui.QGraphicsScene):
	def __init__(self, *args):
		QtGui.QGraphicsScene.__init__(self, *args)
	
	def mouseDoubleClickEvent(self, event):
		#print "click ok"
		if event.button() == Qt.Qt.LeftButton:
			p=event.buttonDownScenePos(Qt.Qt.LeftButton)
			baloon=myBaloon("",p.x(),p.y(),40.0,40.0,[])
			self.addItem(baloon)

class MainWidget(QtGui.QWidget):
	def __init__(self, *args):
		QtGui.QWidget.__init__(self, *args)
		self.grid = QtGui.QGridLayout()
		self.hbox = QtGui.QHBoxLayout()
		self.vbox = QtGui.QVBoxLayout()
		self.hbox.addStretch(1)
		self.imageName=""
		self.scene=SceneWidget()

		self.view=QtGui.QGraphicsView(self.scene)
		self.view.setAlignment(Qt.Qt.AlignTop|Qt.Qt.AlignLeft)
		self.view.setViewportUpdateMode(QtGui.QGraphicsView.FullViewportUpdate)
		#self.view.setViewportUpdateMode(QtGui.QGraphicsView.BoundingRectViewportUpdate)
		
		labelTitle = QtGui.QLabel(u"Заглавие стрипа")
		labelPath = QtGui.QLabel(u"Путь хранения стрипа в вики")
		self.titleImg = QtGui.QLineEdit(self)
		self.lineEdit = QtGui.QLineEdit(self)
		self.grid.addWidget(labelTitle,0,0)
		self.grid.addWidget(self.titleImg,0,1)
		self.grid.addWidget(labelPath,1,0)
		self.grid.addWidget(self.lineEdit,1,1)
		self.grid.addWidget(self.view,2,0,2,2)
		self.setLayout(self.grid)
		
		self.hideItems = []
		self.hided = False
	
	def zoomIn(self):
		self.view.scale(1.25,1.25)
		self.scene.update()
	
	def zoomOut(self):
		self.view.scale(0.75,0.75)
		self.scene.update()
	
	def openTxt(self,filename):
		def str2int(string):
			result=[]
			for i in string.split(","):
				#print string
				result.append(int(i))
			return result
		fileInf=QtCore.QFileInfo(filename)
		self.txtname=unicode(fileInf.absolutePath())+'/'+unicode(fileInf.baseName())+".txt"
		coordinates=[]
		texts=[]
		niks=[]
		if QtCore.QFileInfo(self.txtname).isFile():
			f=open(self.txtname,"r")
			data=f.read()
			f.close()
			self.body=re.compile(u'<aimg}}(.*)',re.S).findall(data)[0]
			#print self.body
			s=re.compile(u'@(.*?)~',re.S).findall(data)
			titleImg = re.compile(u'{cnav}[^*]\*\*([^*]*?)\*').findall(data)[0].decode('utf8')
			self.titleImg.setText(titleImg)
			pathImg = re.compile(u'{aimg>([^]]*?)}').findall(data)
			self.lineEdit.setText(":".join(pathImg[0].split(":")[:-1]))
			#print ":".join(pathImg[0].split(":")[:-1])
			#print pathImg[0].split(":")
			for i in s:
				ss=i.split("\n")
				
				coordinates.append(str2int(ss[0]))
				rr=re.compile(u'\(.*?\)|\[.*?\]',re.S).findall(ss[1])
				#print rr
				niks.append(rr)
				ss[1]=re.compile(u'\(.*?\)|\[.*?\]').sub('',ss[1])
				#ss[1]=re.compile(u'\[.*?\]').sub('',ss[1])
				texts.append(ss[1])
			return coordinates, texts, niks
		else:
			main.statusBar().showMessage(u'Файл '+filename+u' не имеет текстового подстрочника')
			return None, None, None
	
	def open(self, fileName):
		if fileName != '':			
			self.imageName=fileName
			image=QtGui.QImage(fileName)
			self.scene.clear()
			self.scene.setSceneRect(0.0,0.0,float(image.width()),float(image.height()))
			self.scene.addPixmap(QtGui.QPixmap.fromImage(image))
			coord, texts, niks = self.openTxt(fileName)
			if coord != None:
				for i in range(0,len(coord)):
					balun=myBaloon(texts[i],coord[i][1],coord[i][0],coord[i][2],coord[i][3],niks[i])
					self.scene.addItem(balun)
					#break
				main.statusBar().showMessage(u'Загружен '+fileName)
			self.scene.update()
	
	def saveTextFile(self):
		fileInf=QtCore.QFileInfo(self.txtname)
		fileInf2=QtCore.QFileInfo(self.imageName)
		pathImg = self.lineEdit.text()
		titleImg = self.titleImg.text()
		#print titleImg.toUtf8()
		body1=u"""{cnav} **"""+titleImg.toUtf8()+"""**\\\n{{aimg>"""+pathImg+":"+fileInf2.fileName()+"""}}\n"""
		sss=''
		for i in self.scene.items():
				if i.type() == 65550:
					sss = unicode(i.retText()) +"\n"+ sss +"\n"
		sss=sss.strip().encode('utf-8')
		
		if QtCore.QFileInfo(self.txtname).isFile():
			f=open(self.txtname,"w")
			body2=u"""{{<aimg}}"""
			ff = re.compile(u"}}([^{]*?){{",re.S).sub('}}'+"\n"+sss+'{{',self.body)
			#f.write(ff)
			f.write(body1+sss+body2+self.body)
			f.close()
		else:
			f=open(self.txtname,"w")
			
			
			body2=u"""{{<aimg}}
{cnav}"""
			f.write(body1+sss+body2)
			f.close()
		main.statusBar().showMessage(u'Сохранен '+fileInf.fileName()+ u" к стрипу" +fileInf2.fileName())
	
	def hideAllBaloons(self):
		if not self.hided:
			for i in self.scene.items():
					if i.type() not in [7, 65540]:
						if i != self:
							i.hide()
							#print i.type(), i
							self.hideItems.append(i)
			self.hided = True
		else:
			for i in self.hideItems:
				i.show()
			self.hided = False


app=QtGui.QApplication(sys.argv)
main=main_window()
main.load()
main.show()

sys.exit(app.exec_())
