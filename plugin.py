#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
try:
	from PyQt4.QtCore import QString
except:
	QString = type("")

from PyQt4.QtGui import *
from qgis.core import *

class PluginGeoPicardie:

	def __init__(self,iface):
		self.iface = iface
		

	def initGui(self):

		menu = QMenu(u"GéoPicardie", self.iface.pluginMenu())

		menu_gpic = QMenu(u"Couches raster courantes", menu)

		action_composite = QAction(u"Vue aérienne 2008-2009", self.iface.mainWindow())
		QObject.connect(action_composite, SIGNAL("triggered()"), self.wmsGeopicardieComposite)

		action_scan25 = QAction(u"Scan 25 - IGN", self.iface.mainWindow())
		QObject.connect(action_scan25, SIGNAL("triggered()"), self.wmsGeopicardieSCAN25)

		action_ortho2002 = QAction(u"Vue aérienne 2002", self.iface.mainWindow())
		QObject.connect(action_ortho2002, SIGNAL("triggered()"), self.wmsGeopicardieOrtho2002)

		menu_gpic.addAction(action_ortho2002)
		menu_gpic.addAction(action_composite)
		menu_gpic.addAction(action_scan25)
		menu.addMenu(menu_gpic)
		self.iface.pluginMenu().addMenu(menu)
		self.iface.zoomToActiveLayer()
	
	def wmsGeopicardie(self,titre,url):
		self.iface.addRasterLayer(url,titre,"wms")

	def wmsGeopicardieSCAN25(self):
		self.wmsGeopicardie(u"Scan 25","crs=EPSG:2154&dpiMode=7&featureCount=10&format=image/png&layers=geopicardie:picardie_scan25&styles=&url=http://www.geopicardie.fr/geoserver/wms")

	def wmsGeopicardieComposite(self):
		self.wmsGeopicardie(u"Vue aérienne 2008-2009", "crs=EPSG:2154&dpiMode=7&featureCount=10&format=image/png&layers=geopicardie:picardie_ortho_composite_2008_2009_vis&styles=&url=http://www.geopicardie.fr/geoserver/wms")

	def wmsGeopicardieOrtho2002(self):
		self.wmsGeopicardie(u"Vue aérienne 2002", "crs=EPSG:2154&dpiMode=7&featureCount=10&format=image/png&layers=reg22:picardie_ortho_2002&styles=&url=http://www.geopicardie.fr/geoserver/wms")


	def unload(self):
		pass
