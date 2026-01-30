import entities
import parameters
from Youen import *
from test_youen import *

import random as rd

def main():
    # création des entités
    sheep = [entities.Sheep(0,0) for _ in range(parameters.INITIAL_SHEEP)]
    wolf = [entities.Wolf(0,0) for _ in range(parameters.INITIAL_WOLF)]
    grass = [[[entities.Grass()] for _ in range(parameters.GRID_SIZE)] for _ in range(parameters.GRID_SIZE)]
    # On place les moutons et les loups a des endroits aléatoires sans chevauchement
    emplacements = [[(x,y) for y in range(parameters.GRID_SIZE)] for x in range(parameters.GRID_SIZE)]
    for i in sheep:
        sous_liste = rd.choice(emplacements)
        x, y = rd.choice(sous_liste)
        emplacements[x].pop(y)
        sheep[i].first_position(x,y)
    for i in wolf:
        sous_liste = rd.choice(emplacements)
        x, y = rd.choice(sous_liste)
        emplacements[x].pop(y)
        wolf[i].first_position(x,y)

    for row in grass:
        for cell in row:
            for grass_patch in cell:
                grass_patch.first_state()

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
        draw_grid(grid)
    # Mettre à jour l'état de la grille
        for y in range(parameters.GRID_SIZE):
            for x in range(parameters.GRID_SIZE):
                g = grass[x][y]
                g.update_time_since_eaten()
                g.grow()
                if g.is_grown():
                    grid.update_cell(x, y, '#')
                else:
                    grid.update_cell(x, y, '.')

                # Vérifier la présence de moutons
        for s in sheep:
            s.age()
            x,y = s.position()
            s.move(grid)
            if grass[x][y].is_grown():
                grid.update_cell(x,y,'#')
            else:
                grid.update_cell(x,y,'.')
            k,l = s.position()
            grid.update_cell(k, l, 'S')
            if grass[k][l]:
                for g in grass[k][l]:
                    if g.is_grown:
                        s.graze()
                        g.is_eaten()
            if s.can_reproduce():
                new_sheep = s.reproduce(grid)
                if new_sheep:
                    sheep.append(new_sheep)
            s.lose_energy()
            if s.is_dead():
                sheep.remove(s)
                if grass[k][l].is_grown():
                    grid.update_cell(k,l,'#')
                else:
                    grid.update_cell(k,l,'.')
            
        # Vérifier la présence de loups
        for w in wolf:
            w.age()
            x,y = w.position()
            w.move(grid)
            if grass[x][y].is_grown():
                grid.update_cell(x,y,'#')
            else:
                grid.update_cell(x,y,'.')
            k,l = w.position()
            if w.hunt():
                for s in sheep:
                    if s.position() == (k, l):
                        sheep.remove(s)
            if w.can_reproduce():
                new_wolf = w.reproduce(grid)
                if new_wolf:
                    wolf.append(new_wolf)
            w.lose_energy()
            if w.is_dead():
                wolf.remove(w)
            grid.update_cell(k, l, 'W')
        
        nb_sheep = sum(row.count('s') + row.count('S') for row in current_matrix)
        nb_wolves = sum(row.count('w') + row.count('W') for row in current_matrix)

        # Dessin
        screen.fill((0, 0, 0))
        draw_stats_panel(nb_tours, nb_sheep, nb_wolves)
        
        pg.display.flip()
        clock.tick(1) 



        nb_tours += 1

    # Print initial states
    print(f"Sheep Energy: {sheep.energy}")
    print(f"Wolf Energy: {wolf.energy}")
    print(f"Grass Regrowth Time: {grass.regrowth_time}")
    print(f"Grid Size: {grid.width}x{grid.height}")

if __name__ == "__main__":
    main()

