geopicardie-qgis-plugin
=======================

Plugin pour QGIS donnant un accès simple aux données de GéoPicardie.


Installation
------------

Pré-requis :
* Installation opérationnelle de QGIS 2.0 ou plus récent sur votre ordinateur

Processus d'installation (manuelle pour l'instant) :
* Installation :
  * Télécharger le répertoire ./plugin/geopicardie
  * Copier ce répertoire dans le répertoire des plugin de votre répertoire personnel (typiquement ~/.qgis2/python/plugins)
* Activation de l'extension :
  * Lancer QGIS
  * Ouvrir le gestionnaire d'extensions
  * Activer le plugin "GeoPicardie" dans le gestionnaire d'extensions
  * Fermer le gestionnaire d'extensions


Utilisation
-----------

Affichage des ressources mises à disposition des utilisateurs via l'extension :
* Dans le menu de QGIS : Extension > GéoPicardie > Afficher le panneau GéoPicardie

Un nouveau panneau latéral apparaît alors. Il contient un vue arbosrescente des ressources utiles aux partenaires de GéoPicardie.
Cet arbre contient pour l'instant (version 0.2 du plugin) :
* des couches et des styles issues de services internet WMS
* des feature types (classes d'entités) de services internet WFS
* des répertoires facilitant l'organisation et la présentation des ressources décrites ci-dessus

Pour ajouter une couche WMS ou une classe d'entités WFS sur la carte courante de QGIS : double-clic sur le noeud en question.

L'arbre des ressources n'est pas entièrement renseigné, par conséquent, le double-clic sur certains nœuds peut ne rien ajouter à la carte courante. Les ressources non correctement paramétrées dans le plugin sont marquées d'une icône avec un point d'exclamation.



Notes
-----

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
* Présentation des ressources dans un arbre affiché dans un panneau latéral encrable
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
