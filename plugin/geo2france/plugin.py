# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import os

from geo2france.utils.plugin_globals import GpicGlobals
from geo2france.gui.gpic_dock import GpicDockWidget
from geo2france.gui.about_box import AboutBox
from geo2france.gui.param_box import ParamBox
from geo2france.nodes.treenodefactory import FavoriteTreeNodeFactory
from geo2france.nodes.treenodefactory import downloadResourcesTreeFile


class PluginGeo2France:
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

    # Download the config if needed
    if self.needDownloadResourcesTreeFile():
      downloadResourcesTreeFile(GpicGlobals.Instance().CONFIG_FILE_URLS[0])

    # Read the resources tree file and update the GUI
    self.ressources_tree = FavoriteTreeNodeFactory(GpicGlobals.Instance().config_file_path).root_node


  def needDownloadResourcesTreeFile(self):
    """
    Do we need to download a new version of the resources tree file?
    2 possible reasons:
    - the user wants it to be downloading at plugin start up
    - the file is currently missing
    """

    return (GpicGlobals.Instance().CONFIG_FILES_DOWNLOAD_AT_STARTUP > 0 or
      not os.path.isfile(GpicGlobals.Instance().config_file_path))


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
    self.gpic_menu = QMenu(u"Géo2France", plugin_menu)
    plugin_menu.addMenu(self.gpic_menu)

    show_gpic_panel_action = QAction(u'Afficher le panneau Géo2France', self.iface.mainWindow())
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

    dialog = ParamBox(self.iface.mainWindow(), self.dock)
    dialog.exec_()


  def unload(self):
    """
    Removes the plugin menu
    """
    
    self.iface.pluginMenu().removeAction(self.gpic_menu.menuAction())