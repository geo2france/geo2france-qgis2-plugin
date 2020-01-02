# -*- coding: utf-8 -*-

from PyQt4 import QtGui

import os

from geo2france.utils.plugin_globals import GpicGlobals


class AboutBox(QtGui.QDialog):
  """
  About box of the plugin
  """

  def __init__(self, parent=None):

    QtGui.QWidget.__init__(self, parent)

    mainLayout = QtGui.QVBoxLayout()

    logo_file_path = GpicGlobals.Instance().geopic_logo_file_path
    self.logo = QtGui.QLabel()
    self.logo.setPixmap(QtGui.QPixmap(logo_file_path))
    mainLayout.addWidget(self.logo)


    title = u"À propos de l'extension Géo2France…"
    description = u"""Extension pour QGIS donnant un accès simplifié aux ressources géographiques utiles aux partenaires de GéoPicardie
Version {0}
Plus d'informations à l'adresse suivante : {1}
    """.format(GpicGlobals.Instance().PLUGIN_VERSION,
        GpicGlobals.Instance().PLUGIN_SOURCE_REPOSITORY)

    self.textArea = QtGui.QTextEdit()
    self.textArea.setReadOnly(True)
    self.textArea.setText(description)
    self.textArea.setFrameShape(QtGui.QFrame.NoFrame)
    mainLayout.addWidget(self.textArea)

    self.setModal(True)
    self.setSizeGripEnabled(False)

    self.setLayout(mainLayout)

    self.setFixedSize(400, 250)
    self.setWindowTitle(title)