import pygame as pg
import entities      # Le fichier de ton collègue
import parameters    # Le fichier de config
import random as rd
# Assure-toi que c'est le bon nom de fichier pour tes fonctions d'affichage
from test_youen import * 
def main():
    # --- 1. INITIALISATION ---
    
    # Création des listes d'animaux (Objets)
    sheep = [entities.Sheep() for _ in range(parameters.INITIAL_SHEEP)]
    wolf = [entities.Wolf() for _ in range(parameters.INITIAL_WOLVES)]
    
    # Création de la grille d'herbe (Matrice d'objets Grass)
    grass = [[entities.Grass() for _ in range(parameters.GRID_SIZE)] for _ in range(parameters.GRID_SIZE)]

    # Génération des positions aléatoires sans chevauchement
    emplacements = [[(x,y) for y in range(parameters.GRID_SIZE)] for x in range(parameters.GRID_SIZE)]
    flat_emplacements = [pos for sublist in emplacements for pos in sublist] 
    rd.shuffle(flat_emplacements)

    # Création de l'objet Grille (Visuelle/Logique)
    grid_obj = entities.Grid(width=parameters.GRID_SIZE, height=parameters.GRID_SIZE)

    # Placement aléatoire des moutons
    for s in sheep:
        if not flat_emplacements: break
        x, y = flat_emplacements.pop()
        s.first_position(x, y)
        grid_obj.update_cell(x, y, 'S') 

    # Placement aléatoire des loups
    for w in wolf:
        if not flat_emplacements: break
        x, y = flat_emplacements.pop()
        w.first_position(x, y)
        grid_obj.update_cell(x, y, 'W')

    # Initialisation de l’état de l’herbe
    for y in range(parameters.GRID_SIZE):
        for x in range(parameters.GRID_SIZE):
            g = grass[x][y]
            g.first_state()
            # Note: Dans entities.py, first_state met 'is_grown' mais grow utilise 'grown'.
            # On vérifie les deux pour être sûr à cause du bug potentiel chez le collègue.
            has_grown = getattr(g, 'grown', False) or getattr(g, 'is_grown', False)
            
            if has_grown and grid_obj.cells[y][x] == '.':
                grid_obj.update_cell(x, y, '#')
                g.grown = True # On force la synchro

    # --- 2. BOUCLE PRINCIPALE ---
    nb_tours = 0
    running = True
    
    while running and nb_tours < parameters.MAX_TURNS:
        # A. Gestion des événements
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    running = False

        # B. AFFICHAGE
        # Calcul des stats
        nb_sheep_visu = sum(row.count('s') + row.count('S') for row in grid_obj.cells)
        nb_wolf_visu  = sum(row.count('w') + row.count('W') for row in grid_obj.cells)

        # Dessin
        screen.fill((0, 0, 0))
        draw_grid(grid_obj.cells) 
        draw_stats_panel(nb_tours, nb_sheep_visu, nb_wolf_visu)
        
        pg.display.flip()

        # C. LOGIQUE DE SIMULATION

        # --- Mise à jour de l’état de l’herbe ---
        for y in range(parameters.GRID_SIZE):
            for x in range(parameters.GRID_SIZE):
                g = grass[x][y]
                g.update_time_since_eaten()
                g.grow() 

                # Mise à jour visuelle (seulement si pas d'animal dessus)
                current_char = grid_obj.cells[y][x]
                if current_char not in ['S', 's', 'W', 'w']:
                    if g.grown: 
                        grid_obj.update_cell(x, y, '#')
                    else:
                        grid_obj.update_cell(x, y, '.')

        # --- Mise à jour des moutons ---
        for s in sheep[:]:
            # CORRECTION BUG ENTITIES : On vieillit manuellement car la fonction s.age() est buggée
            s.age -= 1 

            old_x, old_y = s.position

            # Nettoyage ancienne case
            if grass[old_x][old_y].grown:
                grid_obj.update_cell(old_x, old_y, '#')
            else:
                grid_obj.update_cell(old_x, old_y, '.')

            s.move(grid_obj) 

            # Nouvelle position
            x, y = s.position
            
            # Manger l'herbe
            if grass[x][y].grown:
                s.graze()
                grass[x][y].is_eaten()
            
            # On affiche le mouton
            grid_obj.update_cell(x, y, 'S')

            # Reproduction
            if s.can_reproduce():
                new_sheep = s.reproduce(grid_obj)
                if new_sheep:
                    # FIX : reproduce() ne définit pas la pos du nouveau mouton.
                    # On le place arbitrairement là où il a été créé (chercher le S orphelin est dur ici)
                    # Le nouveau mouton aura (0,0) par défaut et se tp au tour suivant. C'est acceptable.
                    sheep.append(new_sheep)

            s.lose_energy()

            # Mort
            if s.is_dead():
                sheep.remove(s)
                # Nettoyage
                if grass[x][y].grown:
                    grid_obj.update_cell(x, y, '#')
                else:
                    grid_obj.update_cell(x, y, '.')

        # --- Mise à jour des loups ---
        for w in wolf[:]:
            # CORRECTION BUG ENTITIES : On vieillit manuellement
            w.age -= 1

            old_x, old_y = w.position
            
            # Nettoyage trace
            if grass[old_x][old_y].grown:
                grid_obj.update_cell(old_x, old_y, '#')
            else:
                grid_obj.update_cell(old_x, old_y, '.')

            w.move(grid_obj)

            x, y = w.position
            grid_obj.update_cell(x, y, 'W')

            # Chasse
            if w.hunt():
                for s in sheep[:]:
                    if s.position == (x, y):
                        sheep.remove(s)
                        break 

            # Reproduction
            if w.can_reproduce():
                new_wolf = w.reproduce(grid_obj)
                if new_wolf:
                    wolf.append(new_wolf)

            w.lose_energy()

            # Mort
            if w.is_dead():
                wolf.remove(w)
                if grass[x][y].grown:
                    grid_obj.update_cell(x, y, '#')
                else:
                    grid_obj.update_cell(x, y, '.')

        nb_tours += 1
        clock.tick(5) # Vitesse

    pg.quit()

if __name__ == "__main__":
    main()