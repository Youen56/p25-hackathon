import parameters
import random as rd

#définir les classe des entités

class Sheep:
    def __init__(self):
        self.energy = parameters.SHEEP_INITIAL_ENERGY
        self.reproduction_threshold = parameters.SHEEP_REPRODUCTION_THRESHOLD
        self.energy_gain_from_grass = parameters.SHEEP_ENERGY_GAIN_FROM_GRASS
        self.energy_loss_per_turn = parameters.SHEEP_ENERGY_LOSS_PER_TURN
        self.reproduction_energy_cost = parameters.REPRODUCTION_ENERGY_COST
        self.age = parameters.SHEEP_MAX_AGE
        self.position = (0,0) #position avant placement

    def graze(self):
        self.energy += self.energy_gain_from_grass

    def lose_energy(self):
        self.energy -= self.energy_loss_per_turn

    def is_dead(self):
        return self.energy <= 0 or self.age <= 0

    def can_reproduce(self):
        return self.energy >= self.reproduction_threshold

    def reproduce(self,grid):
        if self.can_reproduce():
            x,y = self.position
            directions = [(-1,0), (1,0), (0,-1), (0,1)]
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < parameters.GRID_SIZE and 0 <= ny < parameters.GRID_SIZE:
                    if grid[nx][ny] == '.':
                        grid[nx][ny] = 'S'
                        break
            self.energy -= self.reproduction_energy_cost
            return Sheep()
        return None

    def age(self):
        self.age -= 1

    def move(self,grid):
        x, y = self.position
        cases_libres = []
        directions = [(-1,0), (1,0), (0,-1), (0,1)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < parameters.GRID_SIZE and 0 <= ny < parameters.GRID_SIZE:
                if grid[nx][ny] == '.' or grid[nx][ny] == '#':
                    cases_libres.append((nx, ny))

        if cases_libres:
            x_new, y_new = rd.choice(cases_libres)
            x, y = x_new, y_new

        if grid[x][y] == '#':
            self.energy += parameters.SHEEP_ENERGY_FROM_GRASS
            grid[x][y] = '.'
        self.position = (x,y)


    def first_position(self,x,y):
        self.position = (x,y)



class Wolf:
    def __init__(self,x,y):
        self.energy = parameters.WOLF_INITIAL_ENERGY
        self.reproduction_threshold = parameters.WOLF_REPRODUCTION_THRESHOLD
        self.energy_gain_from_sheep = parameters.WOLF_ENERGY_GAIN_FROM_SHEEP
        self.energy_loss_per_turn = parameters.WOLF_ENERGY_LOSS_PER_TURN
        self.reproduction_energy_cost = parameters.REPRODUCTION_ENERGY_COST
        self.age = parameters.WOLF_MAX_AGE
        self.position = (0,0) #position avant placement
        self.is_sheep = False

    def hunt(self):
        if self.is_sheep:
            self.energy += self.energy_gain_from_sheep
            return(True)
        return(False)

    def lose_energy(self):
        self.energy -= self.energy_loss_per_turn

    def is_dead(self):
        return self.energy <= 0 or self.age <= 0

    def can_reproduce(self):
        return self.energy >= self.reproduction_threshold

    def reproduce(self,grid):
        if self.can_reproduce():
            x,y = self.position()
            directions = [(-1,0), (1,0), (0,-1), (0,1)]
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < parameters.GRID_SIZE and 0 <= ny < parameters.GRID_SIZE:
                    if grid[nx][ny] == '.' or grid[nx][ny] == '#':
                        grid[nx][ny] = 'W'
                        break
            self.energy -= self.reproduction_energy_cost
            return Wolf()
        return None

    def age(self):
        self.age -= 1

    def move(self,grid):
        x,y = self.position()
        cases_libres = []
        # directions possibles
        directions = [(-1,0), (1,0), (0,-1), (0,1)]

        # 1) Chercher un mouton adjacent
        for dx, dy in directions:
            nx, ny = x + dx, y + dy #nouvelles coordonnées
            if 0 <= nx < parameters.GRID_SIZE and 0 <= ny < parameters.GRID_SIZE:
                if grid[nx][ny] == 'S':
                    x, y = nx, ny
                    self.is_sheep = True
                    break

        # 2) Sinon, déplacement aléatoire vers une case libre
        if not self.is_sheep:
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < parameters.GRID_SIZE and 0 <= ny < parameters.GRID_SIZE:
                    if grid[nx][ny] == '.' or grid[nx][ny] == '#':
                        cases_libres.append((nx, ny))

            if cases_libres:
                x, y = rd.choice(cases_libres)
        self.position = (x,y)

    def first_position(self,x,y):
        self.position = (x,y)


class Grass: 
    def __init__(self):
        self.regrowth_time = parameters.GRASS_REGROWTH_TIME  # time steps to regrow
        self.growth_proba = parameters.GRASS_GROWTH_PROBABILITY  # probability to grow each time step
        self.is_grown = False  # initially grass is grown or not
        self.time_since_eaten = 0
        self.eaten = False
        

    def grow(self):
        if not self.is_grown:
            if rd.random() < self.growth_proba:
                self.is_grown = True
                self.time_since_eaten = 0
                self.eaten = False


    def update_time_since_eaten(self):
        if self.eaten:
            self.time_since_eaten += 1
            if self.time_since_eaten >= self.regrowth_time:
                self.is_grown = True
                self.time_since_eaten = 0
                self.eaten = False

    def is_eaten(self):
        self.is_grown = False
        self.eaten = True
        self.time_since_eaten = 0

    def first_state(self):
        if rd.random() < parameters.INITIAL_GRASS_COVERAGE:
            self.is_grown = True


class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = [['.' for _ in range(width)] for _ in range(height)] #etat avant définition des entités

    def update_cell(self, x, y, entity_symbol):
        self.cells[y][x] = entity_symbol

    
