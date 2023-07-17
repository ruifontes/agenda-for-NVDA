#Agenda


## Informations
* Auteurs : Abel Passos, Ângelo Abrantes et Rui Fontes
* Mis à jour : 17.07.2023
* Télécharger[version stable][1]
* Compatibilité : NVDA Version 2019.3 et au-delà


## Présentation
Cette extension vous permet de noter des rendez-vous et des activités avec ou sans alarmes et avec ou sans répétitions périodiques.
Vous pouvez utiliser deux agendas différentes.
Pour basculer entre elles, accédez au menu NVDA, Préférences, Paramètres, dans la section agenda et choisissez, dans la zone de liste déroulante, l'agenda que vous souhaitez utiliser.
Si la deuxième ligne est vide, utilisez le bouton \"Sélectionner ou ajoutez un répertoire\" pour créer une deuxième agenda.
Si vous utilisez ce bouton avec un chemin sélectionné, l'agenda sera déplacé vers le nouveau chemin, s'il n'y a pas d'agenda. Si c'est le cas, seul le chemin sera modifié, et les deux agendas seront conservés, avec le nouveau chemin utilisé.
Au démarrage de NVDA, elle nous rappellera les rendez-vous pour les prochains jours, ce pense-bête peut être une fenêtre avec une liste de tous les rendez-vous ou un pense-bête avec un dialogue et une alarme audible pour les rendez-vous avec une alarme définie.
Cette option peut être configurée dans les paramètres de l'extension.


## Commande
La commande pour invoquer l'extension est NVDA+F4.
Vous pouvez le modifier dans le dialogue Gestes de commandes, dans la section agenda.


## Comment ça fonctionne :
* Lorsque vous ouvrez le programme, les rendez-vous de la journée seront affichés.
* Dans la fenêtre principale, il y a les champs pour modifier la date, les rendez-vous pour la date sélectionnée et certains boutons de contrôle du programme qui seront décrits plus loin.
Les champs de la date peuvent être modifiés à l'aide des flèches verticales ou en tapant la valeur souhaitée. Lors de la modification de la date, les rendez-vous de la journée seront automatiquement affichés.


### Touches de raccourci pour la fenêtre principale :


* Alt + 1-9 : Avance le nombre de jours correspondant à la valeur pressée ;
* Alt+0 : Revient à la date en cours ;
* Alt + flèche gauche : Recule un jour dans la date ;
* Alt + flèche droite : Avance un jour dans la date ;
* Alt + flèche haut : Avance une semaine ;
* Alt + flèche bas : Recule une semaine ;
* Alt + page précédente : Avance un mois ;
* Alt + page suivante : Recule un mois ;
* Entrée : Si un rendez-vous est sélectionné, il ouvre la fenêtre d'édition. Sinon, il ouvre la fenêtre pour créer un nouveau rendez-vous ;
* Supprimer : Supprime le registre sélectionné. Même fonction que le bouton Supprimer ;
* Contrôle+F : Ouvre la fenêtre "Recherche". Égal à activer le bouton "Rechercher".


### Fonctions des boutons de la fenêtre principale et de leurs touches d'accès rapides :
* Ajouter (Alt+A) : Ouvre une fenêtre pour enregistrer des rendez-vous à la date sélectionnée ;
* Éditer (Alt+É) : Ouvre une fenêtre pour éditer le rendez-vous sélectionné ;
* Supprimer (Alt+R) : Supprime le rendez-vous sélectionné ;
* Rechercher (Alt+E) : Ouvre une fenêtre pour rechercher des informations dans l'agenda ;
* Sortir (Alt+T) : Ferme la fenêtre.


### Les fonctions Ajouter et Éditer sont assez similaires et, pour cette raison, la fenêtre qui sera décrite sert pour les deux fonctions.
La principale différence est que pour éditer, vous devez avoir précédemment sélectionné un rendez-vous pour l'éditer.
De plus, dans la fonction Éditer, les données du rendez-vous sélectionné s'affichent dans la fenêtre pour l'éditer. Dans l'option Ajouter, la fenêtre s'ouvre avec la date sélectionnée et les autres champs vides.


### Ajouter et Éditer les champs de fenêtre
* jour / mois / année : Champs de date qui peuvent être modifiés avec les flèches verticales ou en tapant la valeur souhaitée
* heure / minutes : Champs de la durée de temps qui peuvent être modifiés avec les flèches verticales ou en tapant la valeur souhaitée
* Description : Champ pour remplir les informations sur le rendez-vous ;
* Bouton Répéter : Permet l'accès à la fenêtre "Définir les répétitions" où il est possible de définir la période de répétition et la fin de sa durée.
* Alarmes : Permet l'accès à la fenêtre "Réglage des alarmes" où vous trouverez diverses cases à cocher pour choisir quand déclencher une alarme. Par défaut, lorsque une alarme est sélectionnée avant la date et l'heure du rendez-vous, l'alarme exact est automatiquement activée.
* Bouton Ok (Alt+O) : Enregistre les informations du rendez-vous dans le calendrier.
* Bouton Annuler (Alt+N): N'enregistre pas les informations remplies dans cette fenêtre.
* La fenêtre Ajouter / Éditer a la touche de raccourci Ctrl+Entrée pour enregistrer les informations remplies. Cela équivaut à la fonction du bouton Ok


### Champs de la fenêtre Recherche
* Type de recherche : Vous devez sélectionner parmi les options suivantes :

	* Recherche de texte : Un champ d'édition s'ouvrira pour taper ce que vous souhaitez rechercher. Il n'est pas nécessaire de taper toute la phrase, la recherche peut être effectuée avec des parties des mots ;
	* Prochains 7 jours : Affiche les rendez-vous pour les 7 prochains jours, sans compter le jour en cours ;
	* Prochains 30 jours : Affiche les rendez-vous pour les 30 prochains jours, sans compter le jour en cours ;
	* Plage de dates : Affiche les champs de date de début et de fin de recherche ;

* Bouton Rechercher (Alt+E) : Exécute la recherche sélectionnée et renvoie les informations trouvées ;
* Bouton Ajouter (Alt+A) : La même fonction Ajouter que dans la fenêtre principale. La différence est que si vous avez sélectionné un rendez-vous, la fenêtre Ajouter sera à la date du rendez-vous sélectionné. Si aucun rendez-vous n'est sélectionné, il affiche la fenêtre à la date actuelle ;
* Bouton Éditer (Alt+É) : La même fonction de que dans la fenêtre principale. A besoin d'un rendez-vous pour être sélectionné ;
* Bouton Supprimer (Alt+R) : Supprime le rendez-vous sélectionné ;
* Bouton Supprimer tout (Alt+T) : Supprime tous les rendez-vous affichés ;
* Bouton Annuler (Alt+N) : Ferme la fenêtre de recherche et revient à la fenêtre principale.

[1]: https://github.com/ruifontes/agenda-for-NVDA/releases/download/2023.07.18/agenda-2023.07.18.nvda-addon
