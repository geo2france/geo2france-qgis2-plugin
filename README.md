geopicardie-qgis-plugin
=======================

Plugin pour QGIS fournissant un accès simple aux données de GéoPicardie et d'autres ressources géographiques utiles en Picardie.


Installation
------------

Pré-requis :
* Installation opérationnelle de QGIS 2.0 ou plus récent sur votre ordinateur

Installation manuelle :
* Installation :
  * Télécharger le répertoire ./plugin/geopicardie
  * Copier ce répertoire dans le répertoire des plugin de votre répertoire personnel (typiquement ~/.qgis2/python/plugins)
* Activation de l'extension :
  * Lancer QGIS
  * Ouvrir le gestionnaire d'extensions
  * Activer le plugin "GeoPicardie" dans le gestionnaire d'extensions
  * Fermer le gestionnaire d'extensions

Installation automatique (via le gestionnaire d'extensions de QGIS) :
* Déclarer et activer le dépôt suivant : http://www.geopicardie.fr/files/qgis/plugins.xml
* Autoriser le chargement des extensions expérimentales
* Rechercher et charger l'extension intitulée "GéoPicardie"



Utilisation
-----------

Affichage des ressources mises à disposition des utilisateurs via l'extension :
* Dans le menu de QGIS : Extension > GéoPicardie > Afficher le panneau GéoPicardie

Un nouveau panneau latéral apparaît alors. Il contient une vue arbosrescente des ressources utiles aux partenaires de GéoPicardie.
Cet arbre contient pour l'instant (version 0.4.1 du plugin) :
* des couches et des styles issues de services internet WMS
* des feature types (classes d'entités) de services internet WFS (avec la possibilité de définir un filtre sur certaines entités)
* des couches TMS préconfigurées (MapQuest, OpenStreetMap, Stamen) via des fichiers de configuration GDAL
* des répertoires facilitant l'organisation et la présentation des ressources décrites ci-dessus

Pour ajouter une couche WMS ou une classe d'entités WFS sur la carte courante de QGIS vous pouvez utiliser l'une des opérations suivantes :
* double-clic sur le nœud en question
* clic-droit sur le nœud en question et menu contextuel "Ajouter à la carte"
* glisser-déposer du nœud sur la carte de QGIS

L'arbre des ressources n'est pas entièrement renseigné, par conséquent, le double-clic sur certains nœuds peut ne rien ajouter à la carte courante. Les ressources non correctement paramétrées dans le plugin sont marquées d'une icône avec un point d'exclamation.



Notes
-----

Version 0.4.4 :
* correction des conditions de téléchargement du fichier de configuration

Version 0.4.3 :
* téléchargement du fichier de configuration sans utiliser de cache (utilisation de l'en-tête HTTP Cache-Control: no-cache). Permet d'avoir le fichier de configuration le plus à jour

Version 0.4.2 :
* correction du ticket #25 (cf. https://github.com/bchartier/geopicardie-qgis-plugin/issues/25) : support des caractères spéciaux dans le nom du répertoire de l'utilisateur sous Windows

Version 0.4.1 :
* support de filtres pour les couches WFS
* support de raster GDAL_WMS préconfigurés (stockés dans le répertoire config pour l'instant)
* récupération des fichiers de configuration JSON sur le web
* ajout d'une fenêtre de paramétrage
* ajout du glisser-déposer vers la carte

Version 0.3 :
* ajout d'une info-bulle sur chaque nœud. Elle reprend le champ "description" du nœud
* ajout d'un champ "icon" pour chaque nœud. Il permet d'afficher une icône différente de celle associée à la valeur du champ "node_type". Avec la valeur "warn", ce champ permet d'afficher une icône d'avertissement pour les nœuds qui sont en attente d'un paramétrage correct par exemple
* ajout d'un menu contextuel avec les fonctions suivantes :
** ajouter la ressource à la carte
** afficher la fiche de métadonnées (si elle est renseignée dans le champ "metadata_url" du fichier de configuration)
** afficher ou masquer un ensemble de nœuds de l'arbre
** signaler une anomalie (masqué des utilisateurs pour l'instant)
* compléments apportés à l'arbre des ressources

Version 0.2 :
* Présentation des ressources dans un arbre affiché dans un panneau latéral ancrable
* Ajout du support de styles WMS
* Ajout du support de WFS
* Ajout de support de WMTS (non testé faute de disposer d'un service WMTS opérationnel)



Auteurs
-------

Auteurs :
* Benjamin Chartier

Source d'inspiration :
* Nicolas Damiens

Autres remerciements :
* Auteurs des icônes de QGIS, reprises dans l'arbre des ressources
* Pour le fichier plugin/geopicardie/images/Icon_Simple_Warn.png cf. http://commons.wikimedia.org/wiki/File:Icon_Simple_Warn.png


Licence
-------

Licence : New BSD

cf. fichier LICENSE.txt

cf. http://choosealicense.com/licenses/bsd-3-clause/
