#!/usr/bin/env python
# coding: utf-8

# DAUNAT Romain  
# PINON Mathias 

# # SAE S2 : LABYRINTHES

# In[8]:


from random import *


# ## Classe Maze

# In[123]:


class Maze:
    """
    Classe Labyrinthe
    Représentation sous forme de graphe non-orienté
    dont chaque sommet est une cellule (un tuple (l,c))
    et dont la structure est représentée par un dictionnaire
      - clés : sommets
      - valeurs : ensemble des sommets voisins accessibles
    """
    def __init__(self, height, width , empty=False) :
        """
        Constructeur d'un labyrinthe de height cellules de haut 
        et de width cellules de large 
        Les voisinages sont initialisés à des ensembles vides
        Remarque : dans le labyrinthe créé, chaque cellule est complètement emmurée
        """
        self.height    = height
        self.width     = width
        self.neighbors = {(i,j): set() for i in range(height) for j in range (width)}
        if empty ==  True   : 
            for i in range(self.height) :
                for j in range(self.width):
                    if (i == (self.height -1 ) and j == (self.width - 1 )) : 
                        a = 0 
                    elif i == (self.height -1 ) :
                        self.neighbors[(i,j)].add((i,j+1))
                    elif j == (self.width - 1 ) : 
                        self.neighbors[(i, j)].add((i+1, j))
                    else : 
                        self.neighbors[(i,j)].add((i,j+1))
                        self.neighbors[(i,j)].add((i+1,j))

    def info(self):
        """
        **NE PAS MODIFIER CETTE MÉTHODE**
        Affichage des attributs d'un objet 'Maze' (fonction utile pour deboguer)
        Retour:
            chaîne (string): description textuelle des attributs de l'objet
        """
        txt = "**Informations sur le labyrinthe**\n"
        txt += f"- Dimensions de la grille : {self.height} x {self.width}\n"
        txt += "- Voisinages :\n"
        txt += str(self.neighbors)+"\n"
        valid = True
        for c1 in {(i, j) for i in range(self.height) for j in range(self.width)}:
            for c2 in self.neighbors[c1]:
                if c1 not in self.neighbors[c2]:
                    valid = False
                    break
            else:
                continue
            break
        txt += "- Structure cohérente\n" if valid else f"- Structure incohérente : {c1} X {c2}\n"
        return txt

    def __str__(self):
        """
        **NE PAS MODIFIER CETTE MÉTHODE**
        Représentation textuelle d'un objet Maze (en utilisant des caractères ascii)
        Retour:
             chaîne (str) : chaîne de caractères représentant le labyrinthe
        """
        txt = ""
        # Première ligne
        txt += "┏"
        for j in range(self.width-1):
            txt += "━━━┳"
        txt += "━━━┓\n"
        txt += "┃"
        for j in range(self.width-1):
            txt += "   ┃" if (0,j+1) not in self.neighbors[(0,j)] else "    "
        txt += "   ┃\n"
        # Lignes normales
        for i in range(self.height-1):
            txt += "┣"
            for j in range(self.width-1):
                txt += "━━━╋" if (i+1,j) not in self.neighbors[(i,j)] else "   ╋"
            txt += "━━━┫\n" if (i+1,self.width-1) not in self.neighbors[(i,self.width-1)] else "   ┫\n"
            txt += "┃"
            for j in range(self.width):
                txt += "   ┃" if (i+1,j+1) not in self.neighbors[(i+1,j)] else "    "
            txt += "\n"
        # Bas du tableau
        txt += "┗"
        for i in range(self.width-1):
            txt += "━━━┻"
        txt += "━━━┛\n"

        return txt
    
    def add_wall(self , c1, c2):
        self.neighbors[c1].remove(c2)
    
    def remove_wall(self,c1, c2):
        self.neighbors[c1].add(c2)
        
    
    def get_walls(self) :
        lst  = []
        for i in range(self.height): 
            for t in range (self.width) : 
                cell = (i,t)
                valcell = self.neighbors[cell]
                if  i+1 != self.height and (i+1,t) not in valcell :
                    liste = [] 
                    liste.append(cell)
                    liste.append((i+1,t))
                    lst.append(liste)
                if t+1 != self.width and (i,t+1) not in valcell:
                    liste = [] 
                    liste.append(cell)
                    liste.append((i,t+1))
                    lst.append(liste)
        return lst 
                    
    
    def fill(self) : 
        for i in range(self.height) : 
            for t in range(self.width): 
                cell = (i,t)
                if t+1 != self.width :   
                    self.add_wall(cell , (i,t+1))
                if i+1 != self.height:
                    self.add_wall(cell , (i+1,t))
    def empty(self) : 
        for i in range(self.height) : 
            for t in range(self.width): 
                cell = (i,t)
                if t+1 != self.width :   
                    self.remove_wall(cell , (i,t+1))
                if i+1 != self.height:
                    self.remove_wall(cell , (i+1,t))
                    
    def get_contiguous_cells(self,cell):
        cord1 =  cell[0]
        cord2 = cell[1]
        lst = []
        # CONDITION --------------------------------------------------------------------------
        if (cord1 != 0 and cord1 != self.height-1) and (cord2 != 0 and cord2 != self.width-1) : 
            lst.append((cord1+1 ,cord2))
            lst.append((cord1-1 ,cord2))
            lst.append((cord1 ,cord2+1)) 
            lst.append((cord1 ,cord2-1))                                                      
        elif cord1 == 0 and (cord2 != 0 and cord2 != self.width-1) :
            lst.append((cord1+1 ,cord2)) 
            lst.append((cord1 ,cord2+1)) 
            lst.append((cord1 ,cord2-1))
        elif cord1 == self.height-1 and (cord2 != 0 and cord2 != self.width-1) :
            lst.append((cord1-1 ,cord2))
            lst.append((cord1 ,cord2+1))
            lst.append((cord1 ,cord2-1))
        elif cord2 == 0 and (cord1 != 0 and cord1 != self.height-1) : 
            lst.append((cord1+1 ,cord2))
            lst.append((cord1-1 ,cord2))
            lst.append((cord1 ,cord2+1)) 
                                                                                
        elif cord2 == self.width-1 and (cord1 != 0 and cord1 != self.height-1): 
            lst.append((cord1+1 ,cord2))
            lst.append((cord1-1 ,cord2)) 
            lst.append((cord1 ,cord2-1))
        elif cord1 == 0 and cord2 == 0 : 
            lst.append((cord1+1 ,cord2))
            lst.append((cord1 ,cord2+1)) 
        
        elif cord1 == 0 and cord2 == self.width-1 : 
            lst.append((cord1-1 ,cord2))
            lst.append((cord1 ,cord2+1)) 
             
        elif cord1 == self.height-1 and cord2 == 0 : 
            lst.append((cord1-1 ,cord2))
            lst.append((cord1 ,cord2+1)) 
        
        elif cord1 == self.height-1 and cord2 == self.width-1 : 
            lst.append((cord1-1 ,cord2))
            lst.append((cord1 ,cord2-1))
        # -------------------------------------------------------------------------------------- 
        return lst 
    
    def get_reachable_cells(self , cell) : 
        lst = []
        mur = self.get_walls()
        murvoisin = []
        voisin = self.get_contiguous_cells(cell)
        for t in range(len(voisin)) : 
            liste = []
            liste.append(cell)
            liste.append(voisin[t])
            murvoisin.append(liste)
        for i in range(len(murvoisin)):
            reverse = [murvoisin[i][1] , murvoisin[i][0]]
            if murvoisin[i] not in mur and reverse not in mur : 
                lst.append(murvoisin[i][1]) 
        return lst 
    
    def gen_btree(h:int,w:int) :
        laby = Maze(h,w)
        for i in range (laby.height):
            for j in range (laby.width) :
                if ((i+1,j) not in laby.get_reachable_cells((i,j)) and (i+1) < laby.height) and ((i,j+1) not in laby.get_reachable_cells((i,j)) and (j+1) < laby.width):
                    k = randint(1,2)
                    if k == 1 :
                        laby.remove_wall((i,j),(i+1,j))
                    else :
                        laby.remove_wall((i,j),(i,j+1))
                elif (i+1,j) not in laby.get_reachable_cells((i,j)) and i+1 < laby.height :
                    laby.remove_wall((i,j),(i+1,j))
                elif (i,j+1) not in laby.get_reachable_cells((i,j)) and j+1 < laby.width :
                    laby.remove_wall((i,j),(i,j+1))
        return laby
    
    def gen_sidewinder(h:int,w:int) :
        laby = Maze(h,w)
        for i in range (laby.height-1):
            seq = []
            for j in range (laby.width-1):
                seq += [(i,j)]
                k = randint(1,2)
                if k == 1 :
                    laby.remove_wall((i,j),(i,j+1))
                else :
                    m = randint(0,len(seq)-1)
                    a =(seq[m][0]+1,seq[m][1])
                    laby.remove_wall(seq[m],a)
                    seq = []
            seq += [(i,laby.width-1)]
            k = randint(0,len(seq)-1)
            a =(seq[k][0]+1,seq[k][1]) 
            laby.remove_wall(seq[k],a)
        for l in range (laby.width-1):
            laby.remove_wall((laby.height-1,l),(laby.height-1,l+1))
        return laby


# ### Test de la classe

# In[2]:


laby = Maze(4, 4)
print(laby.info())


# In[3]:


print(laby)


# In[4]:


laby = Maze(4, 4)
print(laby.info())


# Changement du labyrinthe

# In[5]:


laby.neighbors = {
    (0, 0): {(1, 0)},
    (0, 1): {(0, 2), (1, 1)},
    (0, 2): {(0, 1), (0, 3)},
    (0, 3): {(0, 2), (1, 3)},
    (1, 0): {(2, 0), (0, 0)},
    (1, 1): {(0, 1), (1, 2)},
    (1, 2): {(1, 1), (2, 2)},
    (1, 3): {(2, 3), (0, 3)},
    (2, 0): {(1, 0), (2, 1), (3, 0)},
    (2, 1): {(2, 0), (2, 2)},
    (2, 2): {(1, 2), (2, 1)},
    (2, 3): {(3, 3), (1, 3)},
    (3, 0): {(3, 1), (2, 0)},
    (3, 1): {(3, 2), (3, 0)},
    (3, 2): {(3, 1)},
    (3, 3): {(2, 3)}
}
print(laby.neighbors)


# In[6]:


laby.neighbors[(1,3)].remove((2,3))
print(laby)


# In[7]:


laby.neighbors[(1, 3)].add((2, 3))

print(laby)


# In[8]:


laby.neighbors[(1, 3)].remove((2, 3))
print(laby)
print(laby.info())


# In[9]:


laby.neighbors[(2, 3)].remove((1,3))


# In[10]:


c1 = (1, 3)
c2 = (2, 3)
if c1 in laby.neighbors[c2] and c2 in laby.neighbors[c1]:
    print(f"Il n'y a pas de mur entre {c1} et {c2} car elles sont mutuellement voisines")
elif c1 not in laby.neighbors[c2] and c2 not in laby.neighbors[c1]:
    print(f"Il y a un mur entre {c1} et {c2} car {c1} n'est pas dans le voisinage de {c2} et {c2} n'est pas dans le voisinage de {c1}")
else:
    print(f"Il y a une incohérence de réciprocité des voisinages de {c1} et {c2}")


# In[11]:


c1 = (1, 3)
c2 = (2, 3)
if c1 in laby.neighbors[c2] and c2 in laby.neighbors[c1]:
    print(f"{c1} est accessible depuis {c2} et vice-versa")
elif c1 not in laby.neighbors[c2] and c2 not in laby.neighbors[c1]:
    print(f"{c1} n'est pas accessible depuis {c2} et vice-versa")
else:
    print(f"Il y a une incohérence de réciprocité des voisinages de {c1} et {c2}")


# In[12]:


L = []
for i in range(laby.height):
    for j in range(laby.width):
        L.append((i,j))
print(f"Liste des cellules : \n{L}")


# ### Implementation du labyrinthe sans mur 

# In[13]:


laby = Maze(4, 4, empty = True)
print(laby)


# In[14]:


laby = Maze(4, 4, empty = False)
print(laby)


# ## 4 Manipulation de labyrinthes

# ### **Méthode d'instance fill**  : 

# In[15]:


laby = Maze(5, 5, empty = True)
laby.fill()
print(laby)


# ###  **Méthode d'instance remove_wall** :

# In[16]:


laby.remove_wall((0,0), (0,1))
print(laby)


# ### **Méthode d'instance add_wall** :

# In[17]:


laby.empty()
laby.add_wall((0, 0), (0, 1))
laby.add_wall((0, 1), (1, 1))
print(laby)


# ### **Méthode d'instance get_walls** : 

# In[18]:


print(laby.get_walls())
print(laby)


# ### **Méthode d'instance get_contiguous_cells** :

# In[19]:


print(laby.get_contiguous_cells((2,2)))


# ###  **Méthode d'instance get_reachable_cells** : 

# In[20]:


print(laby.get_reachable_cells((0,1)))


# ## **5 Génération**

# ### 5.1 :Arbre binaire

# In[125]:


laby = Maze.gen_btree(5, 5)
print(laby)


# ### 5.2 : Sidewinder

# In[124]:


laby = Maze.gen_sidewinder(4, 4)
print(laby)

