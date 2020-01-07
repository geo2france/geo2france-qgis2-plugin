# -*- coding: utf-8 -*-

def classFactory(iface):
	from plugin import PluginGeo2France
	return PluginGeo2France(iface)
