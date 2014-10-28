# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4 import QtCore
from qgis.core import *

import os

from geopicardie.utils.plugin_globals import GpicGlobals


class ParamBox(QtGui.QDialog):
  """
  Param box of the plugin
  """

  def __init__(self, parent=None):

    QtGui.QWidget.__init__(self, parent)
    mainLayout = QtGui.QVBoxLayout()


    # Tabs
    self.tabWidget = QtGui.QTabWidget(self)
    self.configFilesTab = QtGui.QWidget()
    self.resourceTreeTab = QtGui.QWidget()


    # Config files tab

    configFileTabLayout = QtGui.QFormLayout(self.tabWidget)

    self.download_cb = QtGui.QCheckBox(u"Télécharger le fichier de configuration au démarrage", self)
    self.download_cb.setChecked(GpicGlobals.Instance().CONFIG_FILES_DOWNLOAD_AT_STARTUP == 1)
    self.download_cb.stateChanged.connect(self.downloadCbChanged)
    configFileTabLayout.addRow(self.download_cb)

    self.config_file_url_label = QtGui.QLabel(u"URL du fichier de configuration", self)
    self.config_file_url_edit = QtGui.QLineEdit(self)
    self.config_file_url_edit.setText(GpicGlobals.Instance().CONFIG_FILE_URLS[0])
    self.config_file_url_edit.setCursorPosition(0)
    self.config_file_url_edit.editingFinished.connect(self.configFileUrlChanged)
    configFileTabLayout.addRow(self.config_file_url_label, self.config_file_url_edit)

    self.configFilesTab.setLayout(configFileTabLayout)

    # Button to update a given config file


    # Resource tree tab
    resourceTreeTabLayout = QtGui.QFormLayout(self.tabWidget)

    self.mask_resources_with_warn_status_cb = QtGui.QCheckBox(u"Masquer les ressources en cours d'intégration", self)
    self.mask_resources_with_warn_status_cb.setChecked(GpicGlobals.Instance().MASK_RESOURCES_WITH_WARN_STATUS == 1)
    self.mask_resources_with_warn_status_cb.stateChanged.connect(self.maskResourcesCbChanged)
    resourceTreeTabLayout.addRow(self.mask_resources_with_warn_status_cb)

    self.resourceTreeTab.setLayout(resourceTreeTabLayout)


    self.tabWidget.addTab(self.configFilesTab, u"Fichiers de ressources");
    self.tabWidget.addTab(self.resourceTreeTab, u"Arbre des ressources");

    mainLayout.addWidget(self.tabWidget)

    # Add a button to reset params to default values

    
    self.setLayout(mainLayout)

    self.setModal(True)
    self.setSizeGripEnabled(False)


    self.setFixedSize(600, 400)
    title = u"Paramétrage de l'extension GéoPicardie…"
    self.setWindowTitle(title)
        
        
  def downloadCbChanged(self, state):
    """
    Event sent when the state of the checkbox change
    """
    new_value = 1 if state == QtCore.Qt.Checked else 0
    GpicGlobals.Instance().setQgisSettingsValue("config_files_download_at_startup", new_value)
        
        
  def configFileUrlChanged(self):
    """
    Event sent when the text of the line edit has been edited
    """
    new_value = [self.config_file_url_edit.text()]
    GpicGlobals.Instance().setQgisSettingsValue("config_file_urls", new_value)

        
  def maskResourcesCbChanged(self, state):
    """
    Event sent when the state of the checkbox change
    """
    new_value = 1 if state == QtCore.Qt.Checked else 0
    GpicGlobals.Instance().setQgisSettingsValue("mask_resources_with_warn_status", new_value)
