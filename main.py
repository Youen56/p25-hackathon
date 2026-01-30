import pygame as pg
import entities      
import parameters    
import random as rd
from test_youen import * 
def main():
    # --- 1. INITIALISATION ---
    sheep = [entities.Sheep() for _ in range(parameters.INITIAL_SHEEP)]
    wolf = [entities.Wolf() for _ in range(parameters.INITIAL_WOLVES)]
    
    # Matrice d'herbe
    grass = [[entities.Grass() for _ in range(parameters.GRID_SIZE)] for _ in range(parameters.GRID_SIZE)]

    emplacements = [[(x,y) for y in range(parameters.GRID_SIZE)] for x in range(parameters.GRID_SIZE)]
    flat_emplacements = [pos for sublist in emplacements for pos in sublist] 
    rd.shuffle(flat_emplacements)

    grid_obj = entities.Grid(width=parameters.GRID_SIZE, height=parameters.GRID_SIZE)

    # Placement Moutons
    for s in sheep:
        if not flat_emplacements: break
        x, y = flat_emplacements.pop()
        s.first_position(x, y)
        grid_obj.update_cell(x, y, 'S') 

    # Placement Loups
    for w in wolf:
        if not flat_emplacements: break
        x, y = flat_emplacements.pop()
        w.first_position(x, y)
        grid_obj.update_cell(x, y, 'W')

    # Initialisation Herbe
    for y in range(parameters.GRID_SIZE):
        for x in range(parameters.GRID_SIZE):
            g = grass[x][y]
            g.first_state()
            # On met à jour la grille visuelle pour les cases vides
            has_grown = getattr(g, 'grown', False) or getattr(g, 'is_grown', False)
            if has_grown and grid_obj.cells[y][x] == '.':
                grid_obj.update_cell(x, y, '#')
                g.grown = True

    # --- 2. BOUCLE PRINCIPALE ---
    nb_tours = 0
    running = True
    
    while running and nb_tours < parameters.MAX_TURNS:
        # A. Events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    running = False

        # B. AFFICHAGE
        nb_sheep_visu = sum(row.count('s') + row.count('S') for row in grid_obj.cells)
        nb_wolf_visu  = sum(row.count('w') + row.count('W') for row in grid_obj.cells)

        screen.fill((0, 0, 0))
        
        # --- C'EST ICI QUE CA CHANGE ---
        # On envoie les 2 matrices : celle des animaux ET celle de l'herbe
        draw_grid(grid_obj.cells, grass) 
        
        draw_stats_panel(nb_tours, nb_sheep_visu, nb_wolf_visu)
        pg.display.flip()

        # C. LOGIQUE
        
        # Herbe
        for y in range(parameters.GRID_SIZE):
            for x in range(parameters.GRID_SIZE):
                g = grass[x][y]
                g.update_time_since_eaten()
                g.grow() 
                
                # Update grille visuelle (seulement si pas d'animal)
                if grid_obj.cells[y][x] not in ['S', 's', 'W', 'w']:
                    if g.grown: 
                        grid_obj.update_cell(x, y, '#')
                    else:
                        grid_obj.update_cell(x, y, '.')

        # Moutons
        for s in sheep[:]:
            s.age -= 1 
            old_x, old_y = s.position

            grid_obj.update_cell(old_x, old_y, '.') #met à jour les cellules

            s.move(grid_obj) 
            x, y = s.position
            
            # Manger
            if grass[x][y].grown:
                s.graze()
                grass[x][y].is_eaten()
            
            grid_obj.update_cell(x, y, 'S')

            if s.can_reproduce():
                new_sheep = s.reproduce(grid_obj)
                if new_sheep:
                    sheep.append(new_sheep)

            s.lose_energy()

            if s.is_dead():
                sheep.remove(s)
                grid_obj.update_cell(x, y, '.') # On vide la case visuelle

        # Loups
        for w in wolf[:]:
            w.age -= 1
            old_x, old_y = w.position
            grid_obj.update_cell(old_x, old_y, '.') # On vide l'ancienne case

            w.move(grid_obj)
            x, y = w.position
            grid_obj.update_cell(x, y, 'W')

            if w.hunt():
                for s in sheep[:]:
                    if s.position == (x, y):
                        sheep.remove(s)
                        break 

            if w.can_reproduce():
                new_wolf = w.reproduce(grid_obj)
                if new_wolf:
                    wolf.append(new_wolf)

            w.lose_energy()

            if w.is_dead():
                wolf.remove(w)
                grid_obj.update_cell(x, y, '.')

        nb_tours += 1
        clock.tick(4) # Vitesse

    pg.quit()

if __name__ == "__main__":
    main()