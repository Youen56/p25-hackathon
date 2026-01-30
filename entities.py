import parameters
import random as rd

#définir les classe des entités

class Sheep:
    def __init__(self):
        # Énergie initiale du mouton
        self.energy = parameters.SHEEP_INITIAL_ENERGY
        
        # Seuil d'énergie à partir duquel il peut se reproduire
        self.reproduction_threshold = parameters.SHEEP_REPRODUCTION_THRESHOLD
        
        # Énergie gagnée lorsqu'il mange de l'herbe
        self.energy_gain_from_grass = parameters.SHEEP_ENERGY_FROM_GRASS
        
        # Énergie perdue à chaque tour
        self.energy_loss_per_turn = parameters.SHEEP_ENERGY_LOSS_PER_TURN
        
        # Coût énergétique de la reproduction
        self.reproduction_energy_cost = parameters.REPRODUCTION_ENERGY_COST
        
        # Âge maximal du mouton (décroît à chaque tour)
        self.age = parameters.SHEEP_MAX_AGE
        
        # Position initiale (sera définie plus tard)
        self.position = (0,0)

    def graze(self):
        # Le mouton mange de l’herbe et gagne de l’énergie
        self.energy += self.energy_gain_from_grass

    def lose_energy(self):
        # Perte d’énergie naturelle à chaque tour
        self.energy -= self.energy_loss_per_turn

    def is_dead(self):
        # Le mouton meurt si son énergie ou son âge tombe à 0
        return self.energy <= 0 or self.age <= 0

    def can_reproduce(self):
        # Vérifie s’il a assez d’énergie pour se reproduire
        return self.energy >= self.reproduction_threshold

    def reproduce(self,grid):
        # Le mouton tente de se reproduire dans une case adjacente libre
        if self.can_reproduce():
            x,y = self.position
            directions = [(-1,0), (1,0), (0,-1), (0,1)]  # 4 directions cardinales
            
            # Cherche une case libre autour
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < parameters.GRID_SIZE and 0 <= ny < parameters.GRID_SIZE:
                    if grid.cells[ny][nx] == '.':  # Case vide
                        grid.cells[ny][nx] = 'S'   # Place un nouveau mouton
                        break
            
            # Coût énergétique de la reproduction
            self.energy -= self.reproduction_energy_cost
            
            # Retourne un nouvel objet Sheep
            return Sheep()
        
        return None

    def age(self):
        # Vieillit le mouton d’un tour
        self.age -= 1

    def move(self,grid):
        # Déplacement du mouton vers une case libre ou herbe
        x, y = self.position
        cases_libres = []
        directions = [(-1,0), (1,0), (0,-1), (0,1)]

        # Recherche des cases accessibles
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < parameters.GRID_SIZE and 0 <= ny < parameters.GRID_SIZE:
                if grid.cells[ny][nx] == '.' or grid.cells[ny][nx] == '#':
                    cases_libres.append((nx, ny))

        # Choix aléatoire d’une case libre
        if cases_libres:
            x, y = rd.choice(cases_libres)

        # Si le mouton marche sur de l’herbe, il la mange
        if grid.cells[y][x] == '#':
            self.energy += parameters.SHEEP_ENERGY_FROM_GRASS
            grid.cells[y][x] = '.'  # L’herbe disparaît

        # Mise à jour de la position
        self.position = (x,y)

    def first_position(self,x,y):
        # Position initiale lors de l’apparition
        self.position = (x,y)

class Wolf:
    def __init__(self):
        # Énergie initiale du loup
        self.energy = parameters.WOLF_INITIAL_ENERGY
        
        # Seuil d’énergie pour se reproduire
        self.reproduction_threshold = parameters.WOLF_REPRODUCTION_THRESHOLD
        
        # Énergie gagnée lorsqu’il mange un mouton
        self.energy_gain_from_sheep = parameters.WOLF_ENERGY_FROM_SHEEP
        
        # Énergie perdue à chaque tour
        self.energy_loss_per_turn = parameters.WOLF_ENERGY_LOSS_PER_TURN
        
        # Coût énergétique de la reproduction
        self.reproduction_energy_cost = parameters.REPRODUCTION_ENERGY_COST
        
        # Âge maximal
        self.age = parameters.WOLF_MAX_AGE
        
        # Position initiale
        self.position = (0,0)
        
        # Indique si un mouton a été trouvé sur la case cible
        self.is_sheep = False

    def hunt(self):
        # Si le loup a trouvé un mouton, il gagne de l’énergie
        if self.is_sheep:
            self.energy += self.energy_gain_from_sheep
            return True
        return False

    def lose_energy(self):
        # Perte d’énergie naturelle
        self.energy -= self.energy_loss_per_turn

    def is_dead(self):
        # Mort si énergie ou âge tombe à 0
        return self.energy <= 0 or self.age <= 0

    def can_reproduce(self):
        # Vérifie s’il peut se reproduire
        return self.energy >= self.reproduction_threshold

    def reproduce(self,grid):
        # Reproduction dans une case adjacente libre
        if self.can_reproduce():
            x,y = self.position  
            directions = [(-1,0), (1,0), (0,-1), (0,1)]
            
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < parameters.GRID_SIZE and 0 <= ny < parameters.GRID_SIZE:
                    if grid.cells[ny][nx] in ['.', '#']:  # case libre ou herbe
                        grid.cells[ny][nx] = 'W'
                        break
            
            self.energy -= self.reproduction_energy_cost
        
        return None

    def age(self):
        # Vieillissement
        self.age -= 1

    def move(self,grid):
        # Déplacement du loup
        x,y = self.position   
        cases_libres = []
        directions = [(-1,0), (1,0), (0,-1), (0,1)]

        # 1) Chercher un mouton adjacent
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < parameters.GRID_SIZE and 0 <= ny < parameters.GRID_SIZE:
                if grid.cells[ny][nx] == 'S':
                    x, y = nx, ny
                    self.is_sheep = True
                    break

        # 2) Sinon déplacement aléatoire
        if not self.is_sheep:
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < parameters.GRID_SIZE and 0 <= ny < parameters.GRID_SIZE:
                    if grid.cells[ny][nx] in ['.', '#']:
                        cases_libres.append((nx, ny))

            if cases_libres:
                x, y = rd.choice(cases_libres)

        self.position = (x,y)

    def first_position(self,x,y):
        self.position = (x,y)

class Grass: 
    def __init__(self):
        # Temps nécessaire pour repousser
        self.regrowth_time = parameters.GRASS_REGROWTH_TIME
        
        # Probabilité de pousser à chaque tour
        self.growth_proba = parameters.GRASS_GROWTH_PROBABILITY
        
        # Indique si l’herbe est présente
        self.grown = False
        
        # Temps écoulé depuis qu’elle a été mangée
        self.time_since_eaten = 0
        
        # Indique si elle vient d’être mangée
        self.eaten = False

    def grow(self):
        # L’herbe peut repousser aléatoirement
        if not self.grown:
            if rd.random() < self.growth_proba:
                self.grown = True
                self.time_since_eaten = 0
                self.eaten = False

    def update_time_since_eaten(self):
        # Gestion du temps de repousse
        if self.eaten:
            self.time_since_eaten += 1
            if self.time_since_eaten >= self.regrowth_time:
                self.grown = True
                self.time_since_eaten = 0
                self.eaten = False

    def is_eaten(self):
        # L’herbe est mangée
        self.grown = False
        self.eaten = True
        self.time_since_eaten = 0

    def first_state(self):
        # Probabilité initiale d’avoir de l’herbe sur la case
        if rd.random() < parameters.INITIAL_GRASS_COVERAGE:
            self.is_grown = True

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        # Grille initiale remplie de cases vides '.'
        self.cells = [['.' for _ in range(width)] for _ in range(height)]

    def update_cell(self, x, y, entity_symbol):
        # Met à jour une case de la grille
        self.cells[y][x] = entity_symbol




    
