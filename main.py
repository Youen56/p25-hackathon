import entities
import parameters
import random as rd
from test_youen import *


def main():
    # Création des entités :
    # - une liste de moutons
    # - une liste de loups
    # - une grille 2D d’objets Grass (herbe)
    sheep = [entities.Sheep()for _ in range(parameters.INITIAL_SHEEP)]
    wolf = [entities.Wolf() for _ in range(parameters.INITIAL_WOLVES)]
    grass = [[entities.Grass() for _ in range(parameters.GRID_SIZE)] for _ in range(parameters.GRID_SIZE)]

    # On génère une liste de toutes les positions possibles de la grille
    # pour placer les animaux sans chevauchement
    emplacements = [[(x,y) for y in range(parameters.GRID_SIZE)] for x in range(parameters.GRID_SIZE)]

    # Placement aléatoire des moutons
    for i in sheep:
        sous_liste = rd.choice(emplacements)
        x, y = rd.choice(sous_liste)
        sous_liste.remove((x, y))   # on retire la valeur, pas un index
        i.first_position(x, y)

    # Placement aléatoire des loups
    for i in wolf:
        sous_liste = rd.choice(emplacements)
        x, y = rd.choice(sous_liste)
        sous_liste.remove((x, y))   # on retire la valeur, pas un index
        i.first_position(x, y)

    # Initialisation de l’état de l’herbe (probabilité de pousser)
    for row in grass:
        for cell in row:
            cell.first_state()

    # Création de la grille d’affichage
    grid = entities.Grid(width=parameters.GRID_SIZE, height=parameters.GRID_SIZE)

    nb_tours = 0
    running = True
    
    while running and nb_tours < parameters.MAX_TURNS:
        # Events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    running = False
        nb_sheep = sum(row.count('s') + row.count('S') for row in grid)
        nb_wolves = sum(row.count('w') + row.count('W') for row in grid)

        
        draw_grid(grid)
        draw_stats_panel(nb_tours, nb_sheep, nb_wolves)
        # --- Mise à jour de l’état de l’herbe ---
        for y in range(parameters.GRID_SIZE):
            for x in range(parameters.GRID_SIZE):
                g = grass[x][y]                 # Récupère l’objet Grass
                g.update_time_since_eaten()     # Met à jour le temps depuis qu’elle a été mangée
                g.grow()                        # Tente de faire repousser l’herbe

                # Mise à jour de la grille visuelle
                if g.grown:
                    grid.update_cell(x, y, '#')  # '#' = herbe
                else:
                    grid.update_cell(x, y, '.')  # '.' = vide

        # --- Mise à jour des moutons ---
        for s in sheep:
            s.age                        # Vieillissement du mouton

            x,y = s.position

            s.move(grid)                        # Déplacement du mouton

            # Mise à jour de la case quittée
            if grass[x][y].grown:
                grid.update_cell(x,y,'#')
            else:
                grid.update_cell(x,y,'.')

            # Nouvelle position après déplacement
            k,l = s.position
            grid.update_cell(k, l, 'S')         # Place le mouton sur la grille

            # Si de l’herbe est présente, le mouton la mange
            if grass[l][k].grown:
                s.graze()
                grass[l][k].is_eaten()

            # Reproduction éventuelle
            if s.can_reproduce():
                new_sheep = s.reproduce(grid)
                if new_sheep:
                    sheep.append(new_sheep)

            s.lose_energy()                     # Perte d’énergie naturelle

            # Mort du mouton
            if s.is_dead():
                sheep.remove(s)
                if grass[k][l].is_grown():
                    grid.update_cell(k,l,'#')
                else:
                    grid.update_cell(k,l,'.')

        # --- Mise à jour des loups ---
        for w in wolf:
            w.age
            x,y = w.position

            w.move(grid)

            # Mise à jour de la case quittée
            if grass[x][y].grown:
                grid.update_cell(x,y,'#')
            else:
                grid.update_cell(x,y,'.')

            k,l = w.position

            # Si le loup a trouvé un mouton, il le mange
            if w.hunt():
                for s in sheep:
                    if s.position == (k, l):
                        sheep.remove(s)

            # Reproduction éventuelle
            if w.can_reproduce():
                new_wolf = w.reproduce(grid)
                if new_wolf:
                    wolf.append(new_wolf)

            w.lose_energy()

            # Mort du loup
            if w.is_dead():
                wolf.remove(w)

            grid.update_cell(k, l, 'W')         # Place le loup sur la grille

        nb_tours += 1
    pg.display.flip()
    clock.tick(1) 

    pg.quit()
    sys.exit()
main()