import parameters
import random as rd

# --- CLASSES DES ENTITÉS ---

class Sheep:
    def __init__(self):
        self.energy = parameters.SHEEP_INITIAL_ENERGY
        self.reproduction_threshold = parameters.SHEEP_REPRODUCTION_THRESHOLD
        self.energy_gain_from_grass = parameters.SHEEP_ENERGY_FROM_GRASS
        self.energy_loss_per_turn = parameters.SHEEP_ENERGY_LOSS_PER_TURN
        self.reproduction_energy_cost = parameters.REPRODUCTION_ENERGY_COST
        self.age = parameters.SHEEP_MAX_AGE
        self.position = (0,0)

    def graze(self):
        self.energy += self.energy_gain_from_grass

    def lose_energy(self):
        self.energy -= self.energy_loss_per_turn

    def is_dead(self):
        return self.energy <= 0 or self.age <= 0

    def can_reproduce(self):
        return self.energy >= self.reproduction_threshold

    def reproduce(self, grid):
        if self.can_reproduce():
            x, y = self.position
            directions = [(-1,0), (1,0), (0,-1), (0,1)]
            rd.shuffle(directions)
            
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < parameters.GRID_SIZE and 0 <= ny < parameters.GRID_SIZE:
                    if grid.cells[ny][nx] == '.':
                        grid.cells[ny][nx] = 'S'
                        # IMPORTANT: On crée le bébé et on lui donne sa position tout de suite
                        baby = Sheep()
                        baby.position = (nx, ny)
                        self.energy -= self.reproduction_energy_cost
                        return baby
        return None

    def move(self, grid):
        x, y = self.position
        grass_cells = []
        empty_cells = []
        directions = [(-1,0), (1,0), (0,-1), (0,1)]

        # 1. On scanne les alentours
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < parameters.GRID_SIZE and 0 <= ny < parameters.GRID_SIZE:
                cell_content = grid.cells[ny][nx]
                if cell_content == '#':
                    grass_cells.append((nx, ny))
                elif cell_content == '.':
                    empty_cells.append((nx, ny))

        # 2. INTELLIGENCE ARTIFICIELLE (Si si, c'est de l'IA !)
        # Priorité absolue à l'herbe
        if grass_cells:
            x, y = rd.choice(grass_cells)
        elif empty_cells:
            x, y = rd.choice(empty_cells)
        # Sinon on reste sur place

        # Si on arrive sur de l'herbe, on mange (gestion interne entité)
        # Note: le main.py gère aussi ça, c'est une double sécurité
        if grid.cells[y][x] == '#':
            self.energy += parameters.SHEEP_ENERGY_FROM_GRASS
            grid.cells[y][x] = '.' 

        self.position = (x, y)

    def first_position(self, x, y):
        self.position = (x, y)


class Wolf:
    def __init__(self):
        self.energy = parameters.WOLF_INITIAL_ENERGY
        self.reproduction_threshold = parameters.WOLF_REPRODUCTION_THRESHOLD
        self.energy_gain_from_sheep = parameters.WOLF_ENERGY_FROM_SHEEP
        self.energy_loss_per_turn = parameters.WOLF_ENERGY_LOSS_PER_TURN
        self.reproduction_energy_cost = parameters.REPRODUCTION_ENERGY_COST
        self.age = parameters.WOLF_MAX_AGE
        self.position = (0,0)
        self.is_sheep = False

    def hunt(self):
        if self.is_sheep:
            self.energy += self.energy_gain_from_sheep
            return True
        return False

    def lose_energy(self):
        self.energy -= self.energy_loss_per_turn

    def is_dead(self):
        return self.energy <= 0 or self.age <= 0

    def can_reproduce(self):
        return self.energy >= self.reproduction_threshold

    def reproduce(self, grid):
        if self.can_reproduce():
            x, y = self.position  
            directions = [(-1,0), (1,0), (0,-1), (0,1)]
            rd.shuffle(directions)
            
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < parameters.GRID_SIZE and 0 <= ny < parameters.GRID_SIZE:
                    if grid.cells[ny][nx] in ['.', '#']:
                        grid.cells[ny][nx] = 'W'
                        baby = Wolf()
                        baby.position = (nx, ny)
                        self.energy -= self.reproduction_energy_cost
                        return baby
        return None

    def move(self, grid):
        # CORRECTION MAJEURE : On remet le flag à False au début du tour !
        self.is_sheep = False 
        
        x, y = self.position
        cases_libres = []
        directions = [(-1,0), (1,0), (0,-1), (0,1)]

        # 1. CHASSE : On cherche un mouton adjacent (Priorité Absolue)
        target_found = False
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < parameters.GRID_SIZE and 0 <= ny < parameters.GRID_SIZE:
                if grid.cells[ny][nx] == 'S':
                    x, y = nx, ny
                    self.is_sheep = True # Miam
                    target_found = True
                    break # On saute directement dessus

        # 2. ERRENCE : Si pas de mouton, déplacement aléatoire
        if not target_found:
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < parameters.GRID_SIZE and 0 <= ny < parameters.GRID_SIZE:
                    if grid.cells[ny][nx] in ['.', '#']:
                        cases_libres.append((nx, ny))

            if cases_libres:
                x, y = rd.choice(cases_libres)

        self.position = (x, y)

    def first_position(self, x, y):
        self.position = (x, y)


class Grass: 
    def __init__(self):
        self.regrowth_time = parameters.GRASS_REGROWTH_TIME
        self.growth_proba = parameters.GRASS_GROWTH_PROBABILITY
        self.grown = False
        self.time_since_eaten = 0
        self.eaten = False

    def grow(self):
        if not self.grown:
            if rd.random() < self.growth_proba:
                self.grown = True
                self.time_since_eaten = 0
                self.eaten = False

    def update_time_since_eaten(self):
        if self.eaten:
            self.time_since_eaten += 1
            if self.time_since_eaten >= self.regrowth_time:
                self.grown = True
                self.time_since_eaten = 0
                self.eaten = False

    def is_eaten(self):
        self.grown = False
        self.eaten = True
        self.time_since_eaten = 0

    def first_state(self):
        if rd.random() < parameters.INITIAL_GRASS_COVERAGE:
            self.grown = True # Correction : grown directement à True


class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = [['.' for _ in range(width)] for _ in range(height)]

    def update_cell(self, x, y, entity_symbol):
        self.cells[y][x] = entity_symbol