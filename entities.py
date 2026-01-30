import parameters

#définir les classe des animaux

class Sheep:
    def __init__(self):
        self.energy = parameters.SHEEP_INITIAL_ENERGY
        self.reproduction_threshold = parameters.SHEEP_REPRODUCTION_THRESHOLD
        self.energy_gain_from_grass = parameters.SHEEP_ENERGY_GAIN_FROM_GRASS
        self.energy_loss_per_turn = parameters.SHEEP_ENERGY_LOSS_PER_TURN
        self.reproduction_energy_cost = parameters.REPRODUCTION_ENERGY_COST

class Wolf:
    def __init__(self):
        self.energy = parameters.WOLF_INITIAL_ENERGY
        self.reproduction_threshold = parameters.WOLF_REPRODUCTION_THRESHOLD
        self.energy_gain_from_sheep = parameters.WOLF_ENERGY_GAIN_FROM_SHEEP
        self.energy_loss_per_turn = parameters.WOLF_ENERGY_LOSS_PER_TURN
        self.reproduction_energy_cost = parameters.REPRODUCTION_ENERGY_COST

class Grass: 
    def __init__(self):
        self.regrowth_time = parameters.GRASS_REGROWTH_TIME  # time steps to regrow
        self.growth_proba = parameters.GRASS_GROWTH_PROBABILITY  # probability to grow each time step

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = [['.' for _ in range(width)] for _ in range(height)]
    
