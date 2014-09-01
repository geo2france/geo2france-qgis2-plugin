# -*- coding: utf-8 -*-

from PyQt4 import QtGui

import os

from geopicardie.utils.plugin_globals import GpicGlobals


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


    title = u"À propos de l'extension GéoPicardie…"
    description = u"""Extension pour GéoPicardie
Accès simplifié aux ressources géographiques utiles aux partenaires de GéoPicardie
Version 0.2
Réalisé par Benjamin Chartier
    """

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