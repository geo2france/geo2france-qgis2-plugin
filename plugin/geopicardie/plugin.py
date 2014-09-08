# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import os
import json

from geopicardie.utils.plugin_globals import GpicGlobals
from geopicardie.gui.gpic_dock import GpicDockWidget
from geopicardie.gui.about_box import AboutBox
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

    GpicGlobals.Instance().updateGlobals(os.path.dirname(os.path.abspath(__file__)), self.iface)

    # Read the config file
    config_struct = None
    with open(GpicGlobals.Instance().config_file_path) as f:
      config_string = "".join(f.readlines())
      config_struct = json.loads(config_string)

    self.ressources_tree = FavoriteTreeNodeFactory().build_tree(config_struct)


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


  def unload(self):
    """
    Removes the plugin menu
    """
    
    self.iface.pluginMenu().removeAction(self.gpic_menu.menuAction())