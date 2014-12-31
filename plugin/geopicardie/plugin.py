# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.gui import *
from qgis.core import *

import os
import json
import urllib2

from geopicardie.utils.plugin_globals import GpicGlobals
from geopicardie.gui.gpic_dock import GpicDockWidget
from geopicardie.gui.about_box import AboutBox
from geopicardie.gui.param_box import ParamBox
from geopicardie.nodes.nodes import FavoriteTreeNodeFactory
from geopicardie.nodes.nodes import FavoritesTreeNode


class PluginGeoPicardie:
  """
  Plugin class.
  """

  def __init__(self, iface):
    """
    Plugin initialisation.
    A json config file is read in order to configure the plugin GUI.
    """

    self.iface = iface

    GpicGlobals.Instance().setPluginPath(os.path.dirname(os.path.abspath(__file__)))
    GpicGlobals.Instance().setPluginIFace(self.iface)
    GpicGlobals.Instance().reloadGlobalsFromQgisSettings()

    config_struct = None
    config_string = ""
    if self.needDownloadResourcesTreeFile():
      self.downloadResourcesTreeFile()

    self.updateResourcesTree()


  def needDownloadResourcesTreeFile(self):
    """
    Do we need to download a new version of the resources tree file?
    2 possible reasons:
    - the user wants it to be downloading at plugin start up
    - the file is currently missing
    """

    return (GpicGlobals.Instance().CONFIG_FILES_DOWNLOAD_AT_STARTUP > 0 or
      not os.path.isfile(GpicGlobals.Instance().config_file_path))


  def downloadResourcesTreeFile(self):
    """
    Download the resources tree file
    """

    self.ressources_tree = None

    try:

      # Download the config file
      config_file_url = GpicGlobals.Instance().CONFIG_FILE_URLS[0]
      http_req = urllib2.Request(config_file_url)
      http_req.add_header("Cache-Control", "no-cache")
      config_file = urllib2.urlopen(http_req)
      with open(GpicGlobals.Instance().config_file_path, 'wb') as f:
        f.write(config_file.read())


    except Exception as e:
      short_message = u"Le téléchargement du fichier de configuration du plugin {0} a échoué.".format(GpicGlobals.Instance().PLUGIN_TAG)
      self.iface.messageBar().pushMessage("Erreur", short_message, level=QgsMessageBar.CRITICAL)

      long_message = u"{0}\n{1}\n{2}".format(short_message, e.__doc__, e.message)
      QgsMessageLog.logMessage(long_message, tag=GpicGlobals.Instance().PLUGIN_TAG, level=QgsMessageLog.CRITICAL)


  def updateResourcesTree(self):
    """
    Read the resources tree file and update the GUI
    """

    self.ressources_tree = None

    resourcesTreeFile = GpicGlobals.Instance().config_file_path
    if not os.path.isfile(resourcesTreeFile):
      message = u"Le fichier de configuration du plugin {0} n'a pas pu être trouvé.".format(GpicGlobals.Instance().PLUGIN_TAG)
      self.iface.messageBar().pushMessage("Erreur", message, level=QgsMessageBar.CRITICAL)
      QgsMessageLog.logMessage(message, tag=GpicGlobals.Instance().PLUGIN_TAG, level=QgsMessageLog.CRITICAL)
      return


    try:

      # Read the config file
      with open(resourcesTreeFile) as f:
        config_string = "".join(f.readlines())
        config_struct = json.loads(config_string)
        self.ressources_tree = FavoriteTreeNodeFactory().build_tree(config_struct)

    except Exception as e:
      short_message = u"La lecture du fichier de configuration du plugin {0} a produit des erreurs.".format(GpicGlobals.Instance().PLUGIN_TAG)
      self.iface.messageBar().pushMessage("Erreur", short_message, level=QgsMessageBar.CRITICAL)

      long_message = u"{0}\n{1}\n{2}".format(short_message, e.__doc__, e.message)
      QgsMessageLog.logMessage(long_message, tag=GpicGlobals.Instance().PLUGIN_TAG, level=QgsMessageLog.CRITICAL)


  def initGui(self):
    """
    Plugin GUI initialisation.
    Creates a menu item in the menu of QGIS
    Creates a DockWidget containing the tree of resources
    """

    # Create a menu
    self.createPluginMenu()

    # Create a dockable panel with a tree of resources
    self.dock = GpicDockWidget()
    self.dock.setTreeContents(self.ressources_tree)
    self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dock)


  def createPluginMenu(self):
    """
    Creates the plugin main menu
    """

    plugin_menu = self.iface.pluginMenu()
    self.gpic_menu = QMenu(u"GéoPicardie", plugin_menu)
    plugin_menu.addMenu(self.gpic_menu)

    show_gpic_panel_action = QAction(u'Afficher le panneau GéoPicardie', self.iface.mainWindow())        
    show_gpic_panel_action.triggered.connect(self.showGpicPanelMenuTriggered)
    self.gpic_menu.addAction(show_gpic_panel_action)

    param_action = QAction(u'Paramétrage…', self.iface.mainWindow())        
    param_action.triggered.connect(self.paramMenuTriggered)
    self.gpic_menu.addAction(param_action)

    about_action = QAction(u'À propos…', self.iface.mainWindow())        
    about_action.triggered.connect(self.aboutMenuTriggered)
    self.gpic_menu.addAction(about_action)


  def showGpicPanelMenuTriggered(self):
    """
    Shows the dock widget
    """
    self.dock.show()


  def aboutMenuTriggered(self):
    """
    Shows the About box
    """

    dialog = AboutBox(self.iface.mainWindow())
    dialog.exec_()


  def paramMenuTriggered(self):
    """
    Shows the Param box
    """

    dialog = ParamBox(self.iface.mainWindow())
    dialog.exec_()

    if GpicGlobals.Instance().RESOURCES_TREE_NEED_DOWNLOAD:
      self.downloadResourcesTreeFile()

    if GpicGlobals.Instance().RESOURCES_TREE_NEED_RELOAD:
      self.updateResourcesTree()

    GpicGlobals.Instance().resetFlags()


  def unload(self):
    """
    Removes the plugin menu
    """
    
    self.iface.pluginMenu().removeAction(self.gpic_menu.menuAction())