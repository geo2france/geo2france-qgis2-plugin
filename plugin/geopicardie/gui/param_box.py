# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4 import QtCore
from qgis.core import *
from qgis.gui import *

import os

from geopicardie.utils.plugin_globals import GpicGlobals
from geopicardie.nodes.treenodefactory import FavoriteTreeNodeFactory
from geopicardie.nodes.treenodefactory import downloadResourcesTreeFile


class ParamBox(QtGui.QDialog):
  """
  Param box of the plugin
  """

  def __init__(self, parent=None, tree_dock=None):

    QtGui.QWidget.__init__(self, parent)
    self.tree_dock = tree_dock

    # Init GUI
    self.initGui()

    # Evaluate flags and tupdate the state of the Save button
    self.evaluateFlags()


  def initGui(self):
    """
    """

    dialogLayout = QtGui.QVBoxLayout()
    paramsLayout = QtGui.QVBoxLayout()
    paramsLayout.setAlignment(QtCore.Qt.AlignTop)


    # Config files groupbox
    self.configFilesGB = QgsCollapsibleGroupBox(u"Fichier de configuration de l'arbre des ressources")
    configFileGBLayout = QtGui.QFormLayout(self.configFilesGB)


    # URL of the file
    self.config_file_url_label = QtGui.QLabel(u"URL du fichier", self)
    self.config_file_url_edit = QtGui.QLineEdit(self)
    self.config_file_url_edit.editingFinished.connect(self.configFileUrlChanged)
    configFileGBLayout.addRow(self.config_file_url_label, self.config_file_url_edit)

    # Download the file at startup
    self.download_cb = QtGui.QCheckBox(u"Télécharger le fichier à chaque lancement de QGIS", self)
    self.download_cb.stateChanged.connect(self.downloadCbChanged)
    configFileGBLayout.addRow(self.download_cb)

    paramsLayout.addWidget(self.configFilesGB)

    # Download the file now
    self.download_now_label = QtGui.QLabel(u"Télécharger le fichier maintenant", self)
    self.download_now_btnbox = QtGui.QDialogButtonBox()
    self.download_now_btnbox.setOrientation(QtCore.Qt.Horizontal)
    self.download_now_btnbox.setStandardButtons(QtGui.QDialogButtonBox.Yes)
    self.download_now_btnbox.button(QtGui.QDialogButtonBox.Yes).clicked.connect(self.downloadFileNow)
    configFileGBLayout.addRow(self.download_now_label, self.download_now_btnbox)


    # Content of the resource tree groupbox
    self.resourceTreeGB = QgsCollapsibleGroupBox(u"Contenu de l'arbre des ressources")
    resourceTreeGBLayout = QtGui.QFormLayout(self.resourceTreeGB)

    # Hide resources with a warn flag
    self.hide_resources_with_warn_status_cb = QtGui.QCheckBox(u"Masquer les ressources en cours d'intégration", self)
    self.hide_resources_with_warn_status_cb.stateChanged.connect(self.hideResourcesWithWarnCbChanged)
    resourceTreeGBLayout.addRow(self.hide_resources_with_warn_status_cb)

    # Hide empty groups in the resources tree
    self.hide_empty_groups_cb = QtGui.QCheckBox(u"Masquer les groupes de ressources vides", self)
    self.hide_empty_groups_cb.stateChanged.connect(self.hideEmptyGroupsCbChanged)
    resourceTreeGBLayout.addRow(self.hide_empty_groups_cb)

    paramsLayout.addWidget(self.resourceTreeGB)
    dialogLayout.addLayout(paramsLayout)

    # Set values
    self.setValuesFromQSettings()

    # Bottom dialog buttons
    self.buttonBox = QtGui.QDialogButtonBox()
    self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
    self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.RestoreDefaults|QtGui.QDialogButtonBox.Save|QtGui.QDialogButtonBox.Discard)
    self.buttonBox.button(QtGui.QDialogButtonBox.RestoreDefaults).clicked.connect(self.restoreDefaults)
    self.buttonBox.button(QtGui.QDialogButtonBox.Discard).clicked.connect(self.discard)
    self.buttonBox.button(QtGui.QDialogButtonBox.Save).clicked.connect(self.save)

    # Dialog box title, layout, size and display
    title = u"Paramétrage de l'extension GéoPicardie…"
    self.setWindowTitle(title)
    dialogLayout.addWidget(self.buttonBox)
    self.setLayout(dialogLayout)
    self.setMinimumWidth(500)
    self.resize(self.sizeHint())
    self.setSizeGripEnabled(False)
    self.setFixedSize(self.size())
    self.show()
    self.setSizeGripEnabled(False)


  def setValuesFromQSettings(self):
    """
    """

    # URL of the file
    self.config_file_url_edit.blockSignals(True)
    self.config_file_url_edit.setText(GpicGlobals.Instance().CONFIG_FILE_URLS[0])
    self.config_file_url_edit.setCursorPosition(0)
    self.config_file_url_edit.blockSignals(False)

    # Download the file at startup
    self.download_cb.blockSignals(True)
    self.download_cb.setChecked(GpicGlobals.Instance().CONFIG_FILES_DOWNLOAD_AT_STARTUP in (u"1", "1", 1, True))
    self.download_cb.blockSignals(False)

    # Hide resources with a warn flag
    self.hide_resources_with_warn_status_cb.blockSignals(True)
    self.hide_resources_with_warn_status_cb.setChecked(GpicGlobals.Instance().HIDE_RESOURCES_WITH_WARN_STATUS in (u"1", "1", 1))
    self.hide_resources_with_warn_status_cb.blockSignals(False)

    # Hide empty groups in the resources tree
    self.hide_empty_groups_cb.blockSignals(True)
    self.hide_empty_groups_cb.setChecked(GpicGlobals.Instance().HIDE_EMPTY_GROUPS in (u"1", "1", 1, True))
    self.hide_empty_groups_cb.blockSignals(False)


  def evaluateFlags(self):
    """
    """

    # Detect modifications
    fileUrlChanged = (self.config_file_url_edit.text() != GpicGlobals.Instance().CONFIG_FILE_URLS[0])

    downloadAtStartupChanged = (self.download_cb.isChecked() != (GpicGlobals.Instance().CONFIG_FILES_DOWNLOAD_AT_STARTUP in (u"1", "1", 1, True)))

    hideResourcesWithWarnStatusChanged = (self.hide_resources_with_warn_status_cb.isChecked() != (GpicGlobals.Instance().HIDE_RESOURCES_WITH_WARN_STATUS in (u"1", "1", 1, True)))

    hideEmptyGroupsChanged = (self.hide_empty_groups_cb.isChecked() != (GpicGlobals.Instance().HIDE_EMPTY_GROUPS in (u"1", "1", 1, True)))


    # Init flags
    self.needUpdateVisibilityOfEmptyGroups = hideEmptyGroupsChanged
    self.needUpdateOfTreeContents = hideResourcesWithWarnStatusChanged or fileUrlChanged
    self.needSave = fileUrlChanged or downloadAtStartupChanged or hideResourcesWithWarnStatusChanged or hideEmptyGroupsChanged

    # Update state of the Save Button
    self.buttonBox.button(QtGui.QDialogButtonBox.Save).setEnabled(self.needSave)


  def downloadCbChanged(self, state):
    """
    Event sent when the state of the checkbox change
    """

    self.evaluateFlags()


  def configFileUrlChanged(self):
    """
    Event sent when the text of the line edit has been edited
    """

    self.evaluateFlags()


  def hideResourcesWithWarnCbChanged(self, state):
    """
    Event sent when the state of the checkbox change
    """

    self.evaluateFlags()


  def hideEmptyGroupsCbChanged(self, state):
    """
    Event sent when the state of the checkbox change
    """

    self.evaluateFlags()


  def downloadFileNow(self):
    """
    """

    # Download, read the resources tree file and update the GUI
    downloadResourcesTreeFile(self.config_file_url_edit.text())
    self.ressources_tree = FavoriteTreeNodeFactory(GpicGlobals.Instance().config_file_path).root_node
    self.tree_dock.setTreeContents(self.ressources_tree)


  def save(self):
    """
    """

    # URL of the file
    new_value = [self.config_file_url_edit.text()]
    GpicGlobals.Instance().setQgisSettingsValue("config_file_urls", new_value)

    # Download the file at startup
    new_value = u"1" if self.download_cb.isChecked() else u"0"
    GpicGlobals.Instance().setQgisSettingsValue("config_files_download_at_startup", new_value)

    # Hide resources with a warn flag
    new_value = u"1" if self.hide_resources_with_warn_status_cb.isChecked() else u"0"
    GpicGlobals.Instance().setQgisSettingsValue("hide_resources_with_warn_status", new_value)
    
    # Hide empty groups in the resources tree
    new_value = u"1" if self.hide_empty_groups_cb.isChecked() else u"0"
    GpicGlobals.Instance().setQgisSettingsValue("hide_empty_groups", new_value)

    # Download, read the resources tree file and update the GUI
    if self.needUpdateOfTreeContents:
      downloadResourcesTreeFile(GpicGlobals.Instance().CONFIG_FILE_URLS[0])
      self.ressources_tree = FavoriteTreeNodeFactory(GpicGlobals.Instance().config_file_path).root_node
      self.tree_dock.setTreeContents(self.ressources_tree)

    self.evaluateFlags()


  def discard(self):
    """
    """

    self.close()


  def restoreDefaults(self):
    """
    """

    GpicGlobals.Instance().resetToDefaults()
    self.setValuesFromQSettings()


  def closeEvent(self, evnt):
    """
    """

    super(ParamBox, self).closeEvent(evnt)