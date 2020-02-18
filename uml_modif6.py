# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 17:22:50 2019

@author: eloda
"""

from random import random
from random import randint
import matplotlib.pyplot as plt
from random import sample
import numpy as np
from mp_toolkits.mplot3d import Axes3D



class Entite(object):
    """
    Classe décrivant une entité du réseau.
    
    Attributs : 
        - id (str(int))
        - p_conn, p_trans, p_cons, p_app (float)
        - voisins (liste)
        - pas_max (int)
        - liste_instances_infos (liste)
        - infos_recues (dictionnaire)
        
    Méthodes :
        - __init__(self, ID, groupe, bp_seuil, mp_seuil) :
        Initialise tous les attributs, et notamment p_appr selon le groupe auquel
        appartient l'entité
        - envoie_info(self,info) :
        Envoie l'information en argument à tous les voisins de l'entité
        - recoie_info(self,info) :
        Stocke l'identifiant et l'instance de l'information en argument dans infos_recues
        et liste_instances_infos
        - manipule_info(self) :
        Pour chaque information encore consultable, diminue le temps (en pas) qui lui
        reste pour être consultée de 1 et teste si elle est consultée et/ou appréciée.
        Pour chaque information consultée et pas encore transférée, teste si elle est
        transférée aux voisins.
        - distance(self,entite2,pas_seuil) :
        Calcule la distance entre cette entité et celle en argument (i.e. le nombre 
        d'entités qui les sépare)
    """
    
    def __init__(self, ID, groupe, bp_seuil, mp_seuil):
        
        """
        Arguments : 
             - ID : l'identifiant de l'entité str(int)
             - groupe : groupe auquel appartient l'entité, définit sa proba d'appréciation (str)
             - bp_seuil et mp_seuil : seuils définissant la p_appr (float e [0,1])
            
        Objectifs : 
         - Initialise les attributs :
            
            - ID : ID de l'entité (str(int))
            - p_conn (probabilité de connexion), p_cons (probabilité de consulter), 
            p_trans 'probabilité de transférer) (float)
            - p_app (probabilité d'apprécier) selon les groupes renseignés en entrée (float)
            - self.voisins : liste des voisins de l'entité (liste)
            - pas_max : le temps maximum pour lequel une information est consultable
            par l'entité (int)
            -liste_instances_infos : la liste des instances des informations
            que l'entité a reçu, initialisé à la liste vide (liste)
            
            - info_recues : le dictionnaire dont les clés sont les identifiants
            des informations reçues et les valeurs le pas de temps qu'il reste
            à chaque information pour être consultée (dictionnaire). Si une information présente
            dans ce dictionnaire a comme valeur 0, elle n'est plus consultable
            ni recevable. Si l'information est consultée, elle prend comme valeur
            'consult'. Si elle est transférée, elle prend comme valeur 'transfere'.
        """
        
        self.id = ID
        self.p_conn = random()
        self.p_cons = random()
        self.p_trans = random()
        self.voisins = []
        self.pas_max = 0
        self.infos_recues = {}
        self.liste_instances_infos = []
        
        if groupe=="bp":
            seuil=bp_seuil
            self.p_app=random()*(1-seuil)+seuil
        elif groupe=="mp":
            seuil=mp_seuil
            self.p_app=random()*seuil
        
        
        
    def envoie_info(self,info):
        """
        Argument : 
        info : instance d'information
        
        Objectif :
        Envoie l'information en argument à tous les voisins. 
        """
        
        for i in self.voisins:
            i.recoie_info(info)


    def recoie_info(self,info):
        """
        Argument : 
        info : instance d'information
        
        Objectif :
        Ajoute l'identitifant de information en entrée dans le dictionnaire 
        info_recues avec comme valeur le nombre de pas qu'il reste à l'information 
        pour être encore consultable. Ajoute également l'instance de l'information
        dans le liste liste_instances_infos.
        """
        if info.id not in self.infos_recues :
            self.infos_recues[info.id]=self.pas_max
            self.liste_instances_infos.append(info)
        
        
        
    def manipule_info(self):
        """
        Objectifs :
         - Pour chaque information encore consultable, actualise le temps qui lui
         reste pour être consultée 
         
         - Pour chaque information encore consultable, teste si elle est consultée,
         et si oui, si elle est appréciée. Stocke ces informations dans des 
         attributs de l'instance de l'information en cours de manipulation.
         
         - Pour chaque information déjà consultée, teste si elle est transférée
         aux voisins de l'entité. 
        """
        
        for i in self.infos_recues.keys():
            
            #On récupère l'instance d'information qui correspond à l'identifiant
            #présent dans la clé du dictionnaire 
            for j in self.liste_instances_infos:
                if j.id == i:
                    info = j
            
            #On actualise le nombre de pas restant à l'info pour être consultable        
            if self.infos_recues[i] != 0 and self.infos_recues[i] != "consult" and self.infos_recues[i] != "transfere": #Si l'info est encore consultable
                self.infos_recues[i]=self.infos_recues[i]-1
                
            if self.infos_recues[i] != 0 and self.infos_recues[i] != "consult" and self.infos_recues[i] != "transfere": #Si l'info est encore consultable
                
                #On teste si elle est consultée ou non
                alea = random()
                if alea<self.p_cons: 
                    info.consult(self.id)
                    self.infos_recues[info.id] = "consult"
                    
                    #On teste, si elle est consultée, si elle est appréciée ou non
                    alea = random()
                    if alea<self.p_app:
                        info.apprecie(self.id)

        
        
        for i in self.infos_recues.keys():
            
            if self.infos_recues[i] == "consult": #Pour chaque info consultée
                for j in self.liste_instances_infos:
                    if j.id == i:
                        info = j
            
            #On teste si elle est transférée ou non
                alea = random()
                if alea<self.p_trans:
                
                    for j in self.voisins:
                        j.recoie_info(info)
                        self.infos_recues[info.id] = "transfere"

                    
        
    def distance(self,entite2,pas_seuil):
        """
        Arguments :
             - entite2 : instance de l'entité avec laquelle on veut calculer la distance
             - pas_seuil
            
        Objectif :
        Donne la plus courte distance entre l'entité et une autre entité du réseau
        grâce à un algorithme de parcours d'arbre en largeur.
        Renvoie d ayant pour valeur :
            - distance d entre l'entité et entité 2 si il existe un chemin entre elles (int)
            - 0 sinon (int)
        """
        pas=pas_seuil
        #print("entite"+self.id+"  voisins :")
        nod1=self.voisins
        nod2=[]
        d=1
        while entite2 not in nod1 and nod1!=[] and pas!=0:
            pas=pas-1
            for a in nod1:
                nod2.extend(a.voisins)
            d=d+1
            nod1=nod2
            nod2=[]
        if nod1==[] or pas==0:
            d=0
        return(d)
                   
        
        
        



class information(object):
    """
    Classe décrivant une information du réseau.
    
    Attributs :
        - id (int)
        - dico_consult_appr (dictionnaire)
        - temps_reseau (int)
    
    Méthodes :
        - __init__(self,ID) :
        Initialise les attributs
        - consult(self,entite_id) :
        Stocke l'identifiant de l'entité en argument dans le dico_consult_appr en tant
        que clé et assigne 0 en valeur par défaut
        - apprecie(self,entite_id) :
        Assigne 1 comme valeur dans dico_consult_appr à l'entité en argument
    """
    
    def __init__(self,ID):
        """
        Agument : 
        ID : l'identifiant de l'information (int)
        
        Objectif :
        Initialise les attributs:
            - id : l'identifiant de l'information (int)
            - dico_consult_appr : un dictionnaire qui contiendra en clés les id des
            entités qui ont consulté cette information et en valeur si elles l'ont 
            appréciées au non (1 si appréciée et 0 sinon) (dictionnaire)
            - temps_reseau : le temps que l'information a passé dans le réseau,
            initialisé à la valeur 0 et calculé dans reseau (int)
        """
        
        self.id = ID
        self.dico_consult_appr = {}
        self.temps_reseau = 0
        

    def consult(self,entite_id):
        """
        Argument : 
        entite_id : l'id de l'entite considérée (attribut de entité) (str(int))
            
        Objectif :
        Stocke dans un dico les entités qui l'ont consultée, en initialisant
        la valeur à 0 pour chacune d'elles.
        """
        
        self.dico_consult_appr[entite_id]=0

        #stocke dans un dico les entités qui l'ont apprécié ce qui donne 
        #par def pour les valeurs non nulles les entités qui l'ont consultées
        #met tout dans l'attribut self.dico_consult_appr -> standard 0 et si apprécié 1
        
    
    def apprecie(self,entite_id):
        """
        Argument : 
        Entite_id : l'id de l'entite considérée (str(int))
            
        Objectif : 
        Stocke dans le dico des entités qui ont consultée l'information des 1 pour celles qui
        l'ont appréciées.
        Si la fonction est invoquée on sait que l'information a été appréciée
        """
        
        self.dico_consult_appr[entite_id]+=1
        
             
      
      
      
            
        
class reseau(object):
    """
    Classe décrivant un réseau et faisant tourner des simulations dessus.
    
    Attributs : 
        - taille (int)
        - liste_entites (liste)
        - liste_infos (liste)
        - liste_infos_restantes (liste)
        - liste_infos_envoyees (liste)
        - liste_infos_consultables (liste)
        - dico_general (dictionnaire)
        - diametre (int)
        
    Méthodes : 
        - __init__(self,nb_entites, groupes, bp_seuil,mp_seuil) :
        Initialise les attributs et créé le réseau (les entités et les connexions
        entre elles)
        - calcule_diametre(self) :
        Calcul le diamètre du réseau (i.e. la distance maximale entre 2 entités)
        - dico_general(self,pas) :
        - graphe(self) :
        Créé et affiche un graphe permettant de visualiser le réseau
        - simulation(self, pas_max_simul, nbre_infos, pas_max_info) :
        Créé et fait tourner une simulation
        - graphe_immeuble(self) :
        Créé et affiche un graphe récapitulatif de la propagation des informations
        dans la dernière simulation lancée.
        - bilan(self) :
        Affiche un bilan de toutes les informations du réseau et de la dernière
        simulation lancée.
    """
    
    def __init__(self,nb_entites, groupes, bp_seuil,mp_seuil):
        """
        Arguments:
            - nb_entites : nombre d'entités que le réseau contient (int)
            - groupes : liste de str ayant pour valeur "bp" ou "mp"     (list of str)
            - bp_seuil : seuil de probabilité minimum tel que les proba d'appréciation des entités bon public soient
            comprises dans [mp_seuil:1]                                 (float)
            - mp_seuil : même définition que bp_seuil dans [0:bp_seuil]

        Objectifs :
         - Initialise les arguments :
            - taille : nombre d'entités (int)
            - liste_entites : dico des entités renseignées par leur identifiant en str(int) (liste)
            - liste_infos : liste contenant les informations (liste)
            - liste_infos_restantes : liste contenant les informations pas encore envoyées dans le réseau (liste)
            - liste_infos_envoyees : liste contenant les informations envoyées dans le réseau (liste)
            - liste_infos_consultables : liste des infos envoyées encore consultables par au moins une entité (liste)
            - dico_general
            - diametre : distance maximale entre 2 entités du réseau (int)
            
         - Créé les entités du réseau en créant des instances d'entités et les relie
        les unes avec les autres.
        """
        self.taille=nb_entites
        self.liste_entites={}
        self.liste_infos=[]
        self.liste_infos_restantes=[]
        self.liste_infos_envoyees=[]
        self.liste_infos_consultables=[]
        self.dict_general={}
        self.diametre = 0

        groupes=["bp"]*groupes[0]+["mp"]*groupes[1]
        #generer les entités
        for entite_id in range(self.taille) :
            self.liste_entites[str(entite_id)]=Entite(str(entite_id),groupes[entite_id],bp_seuil,mp_seuil)
        
        #generer les connexions entre entites
        for entite_id in self.liste_entites:
            for id_2 in self.liste_entites:
                if self.liste_entites[id_2] not in self.liste_entites[entite_id].voisins and random()<=self.liste_entites[entite_id].p_conn:
                    self.liste_entites[entite_id].voisins.append(self.liste_entites[id_2])
        
        
        
    def calcule_diametre(self):
        """
        Objectifs :
        Calcule la distance maximale entre deux entites dans le réseau et la stocje
        dans l'attribut diametre.
        """
        liste_distances=[]
        entite_left=list(self.liste_entites.keys())
        for entite1 in self.liste_entites:
            entite_left.remove(entite1)
            for entite2 in entite_left:
                liste_distances.append(self.liste_entites[entite1].distance(self.liste_entites[entite2], self.taille))
        self.diametre = max(liste_distances)    
                    
    
    def dico_general(self,pas):
        """
        Arguments :
            Pas, ie le pas de temps de la simulation au moment où on veut remplir le dico
        Objectif :
            Remplit un dictionnaire répertoriant les informations consultables ou consultées et à renvoyer présentes sur chaque entité au pas de temps "pas" 
            Dans info_consult (attribut de entité) les informations ont la valeur :
                int >0 si il reste du temps pour qu'elles soient consultées
                0 si elles ne sont plus consultables
                "consult" si elles ont été consultées mais pas encore renvoyées
                "transfer" si elles ont été envoyées
        """
        #initialiser le dictionnaire au pas considéré
        self.dict_general[pas]={}
        #On répertorie toutes les informations présentes au pas de temps considéré dans infos_reçue pour chaque entité
        for entite in self.liste_entites :
            truc=self.liste_entites[entite].infos_recues
            dico={}
            for info in truc:
                #essayer de tester sa valeur si l'info est un entier
                try :
                    if truc[info]>0:
                        dico[info]=1
                #sinon, tester sa valeur si c'est un str
                except :
                    if truc[info]=="consult":
                        dico[info]=1
            self.dict_general[pas][entite]=dico
        
          
    
    def graphe(self):
        """
        Objectif :
        Crée un graphe du réseau en 3D avec les entités et leurs connexions
        On relie une entite à ses voisins et on affecte aléatoirement des coordonnées 
        à chaque entité 
        
        """
        fig = plt.figure('Connexions entre entités du réseau')
        ax = fig.add_subplot(111,projection='3d')
        
        liste_x = []
        liste_y = []
        liste_z = []
        for k in self.liste_entites:
            liste_x.append(random()) ; liste_y.append(random()); liste_z.append(random())
        
        #print(liste_x)
        for ent in self.liste_entites.values():
            x=[] ; y=[] ; z=[]
            x.append(liste_x[int(ent.id)])
            y.append(liste_y[int(ent.id)])
            z.append(liste_z[int(ent.id)])
            for vois in ent.voisins :
                rang=int(vois.id)
                x.append(liste_x[rang])
                y.append(liste_y[rang])
                z.append(liste_z[rang])
            ax.plot(x,y,z,color='r', marker="o")
            #print(x)
       
            
            
            
    def simulation(self, pas_max_simul, nbre_infos, pas_max_info):
        """
        Arguments :
            - pas_max_simul : nombre de pas à partir duquel la simulation est arrêtée (entier)
            - nbre_infos : nombre d'informations que le réseau va contenir
            - pas_max_info : temps (en pas de temps) à partir duquel une information
            n'est plus consultable par une entité
        
        Objectifs : 
         - Créé les instances d'information qui font parties de la simulation
         - Envoie une information choisie aléatoirement parmis celles qui restent
         à une entité choisie aléatoirement 
         - Fait tourner la méthode manipule_info() de chaque entité
         - Calcule pour chaque information plus consultable le temps qu'elle a passé dans le réseau 
        """
        
        self.dict_general={}
        info_pas_debut = {}
        
        #On créé la liste des instances d'information
        for i in range(nbre_infos):
            nv_info = information(i)
            self.liste_infos.append(nv_info)
            self.liste_infos_restantes.append(nv_info)
            self.liste_infos_consultables.append(nv_info)
            info_pas_debut[nv_info.id]= ''
        
        #On attribue à l'attribut pas_max de chaque ientité temps maximal
        #pour lequel une info est consultable
        for j in self.liste_entites.values():
            j.pas_max = pas_max_info

        
        #La simulation à proprement parlé

        k=0
        #Temps qu'au moins une information est encore consultable ou que le temps de la simulation n'excède pas le temps maximal entré, on fait tourner la simulation
        while self.liste_infos_consultables != [] and k<pas_max_simul:

            #A chaque pas, on envoie une information choisie aléatoirement parmi celles qui
            #restent à une entité choisie aléatoirement
            if self.liste_infos_restantes != []:
                rang_entite_alea = randint(0,len(self.liste_entites)-1)
                rang_info_alea = randint(0,len(self.liste_infos_restantes)-1)
                
                info_pas_debut[self.liste_infos_restantes[rang_info_alea].id] = k
                
                self.liste_entites[str(rang_entite_alea)].recoie_info(self.liste_infos_restantes[rang_info_alea])
                self.liste_entites[str(rang_entite_alea)].envoie_info(self.liste_infos_restantes[rang_info_alea])
    
                self.liste_infos_envoyees.append(self.liste_infos_restantes[rang_info_alea])
                self.liste_infos_restantes.pop(rang_info_alea)
            
            
            #Pour chaque entité, on fait tourner la méthode manipule_info()
            for p in self.liste_entites.values():
                p.manipule_info()
            
            
            
            #Pour chaque info envoyée, on stocke son temps passé dans le réseau si elle n'est plus consultable par personne
            for i in self.liste_infos_envoyees :
                
                #Pour les informations qui n'ont pas encore été noté comme plus consultables, on teste si elles le sont ou non
                if i in self.liste_infos_consultables:
                #On récupère le pas auquel l'info i a été envoyée dans le reseau
                    for m in info_pas_debut.keys():
                        if m == i.id: 
                            debut = info_pas_debut[m]
                    
                    etat_info = []
                    for j in self.liste_entites.values() : 
                        if i.id in j.infos_recues.keys(): #Pour les entités qui ont reçu l'info i
                            #On stocke "l'état" de l'info dans cette entité (consultable,consultée ou transférée)
                            etat_info.append(j.infos_recues[i.id])
                            
                    #Si toutes les entités ont reçues cette information
                    if len(etat_info) == len(self.liste_entites):
                        compteur_consult = 0
                        for p in etat_info:
                            if p == "consult" or p == "transfere":
                                compteur_consult += 1
                    #Et si toutes ces entités l'ont consultée et/ou transférée, l'info n'est plus consultable par personne (elle est "morte")
                        if compteur_consult == len(etat_info):
                            i.temps_reseau = k-debut
                            self.liste_infos_consultables.remove(i)
                     
                        
                    compteur_zero = 0
                    for p in etat_info:
                        if p == 0:
                            compteur_zero += 1
                        #Si, pour toutes les entités qui ont reçues l'info, elle n'est plus consutable, elle est "morte"
                    if compteur_zero == len(etat_info):
                        i.temps_reseau = k-debut
                        self.liste_infos_consultables.remove(i)
                        
            self.dico_general(k)
            k +=1
            
        #Pour les infos encore consultables à la fin de la simulation, on stocke leur temps dans le réseau
        for i in self.liste_infos_consultables:
            for m in info_pas_debut.keys():
                if m == i.id: 
                    debut = info_pas_debut[m]
            i.temps_reseau = pas_max_simul-debut
        

    def graphe_immeuble(self):
        """
        Arguments :
            Pas d'argument, mais utilise self.dict_general donc il faut l'avoir rempli a priori dans une simulation
        Objectif :
            Crée un barplot groupé représentant pour chaque entité à un temps t les informations disponibles consultables ou consultées par cette entité
        """
        
        #définir les ticks. Pour être sûr d'avoir la place, on met autant d'espace entre chaque pas qu'il y a d'entités
        X=list(self.dict_general.keys())
        X=[int(i)*len(self.liste_entites) for i in X]
        #On définit barWidth en fonction du nombre d'entités
        barWidth = 1/len(self.liste_entites)
        
        #On définit une couleur aléatoire pour chaque information... On considère qu'il y a moins de 250 informations, sinon ça bug
        r=sample(range(0,255),len(self.liste_infos))
        g=sample(range(0,255),len(self.liste_infos))
        b=sample(range(0,255),len(self.liste_infos))
        rgb=[[(r[i]/255),(g[i]/255),(b[i]/255)] for i in range(len(self.liste_infos))]
        
        ######On trace ensuite les barplot pour chaque pas
        #intitialisation des variables
        fig=plt.figure("Propagation des informations dans la dernière simulation")
        ax=fig.add_subplot(111)
        entite_labels=[]
        entite_xticks=[]
        
        #On trace chaque barplot et on remplit la liste de labels et de ticks pour la légende
        for pas in self.dict_general:
            x_tics=[X[pas]]
            for entite in self.dict_general[pas]:
                nb_info=0
                x_tics.append(x_tics[-1]+3*barWidth)
                for info in self.dict_general[pas][str(entite)]:
                    #on trace des barplot superposés pour chaque info d'une entite
                    ax.bar(x_tics[-1],height=1, bottom=nb_info,color=rgb[int(info)], width=barWidth)
                    nb_info+=1
                if len(self.dict_general[pas][str(entite)])>0:
                    entite_labels.append(str(entite))
                    entite_xticks.append(x_tics[-1])
                    
        #ajouter les label box pour chaque info dans la légende:
        for info in self.liste_infos:
            info=info.id
            ax.bar(0,0,color=rgb[int(info)],label=str(info))

        #rajouter la légende
        ax.legend(title="informations")
        ax.set_xticks(entite_xticks)
        ax.set_xticklabels(entite_labels)
        fig.suptitle('propagation des informations durant la simulation', fontsize=13)
        plt.xlabel('entités groupées par pas de temps', fontsize=11)
        plt.ylabel('informations', fontsize=11)
             
        
    def bilan(self):
        """
        Objectif :
        Renvoie un bilan de toutes les informations d'une simulation donnée
        """
        #self.graphe()
        self.graphe_immeuble()
        self.calcule_diametre()
        print("Diamètre du graphe : ", self.diametre)
        #self.graphe_immeuble()
        print("Caractéristiques des informations de la dernière simulation : ")
        bilan_info = np.array([["Id","Temps passé dans le réseau","nbre d'entités qui l'ont consultées", "nbre d'entités qui l'ont apprécié"]])
        
        for i in self.liste_infos:
            compteur_appr = 0
            for j in i.dico_consult_appr.values() :
                if j ==1 :
                    compteur_appr += 1
                    
            a = np.array([[i.id,i.temps_reseau,len(i.dico_consult_appr),compteur_appr]])
            bilan_info = np.append(bilan_info,a,axis=0)
        
        print(bilan_info)
        
"""
CODE PRINCIPAL
"""        

#a = Entite("1","bp",0.3,0.7)
#info_1 = information(0)


groupe=[1,4]
R=reseau(5,groupe,0.2,0.8)
R.simulation(15,5,3)
R.bilan()
R.graphe()

            
            
            
        
        
            
            
            
            
            