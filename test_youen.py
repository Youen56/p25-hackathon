import pygame as pg
import sys

# --- CONFIGURATION AFFICHAGE ---
CELL_SIZE = 20                     
GRID_SIZE = 30 # (Doit être identique à parameters.py)
GRID_WIDTH_PX = GRID_SIZE * CELL_SIZE
PANEL_WIDTH = 300                  
WINDOW_WIDTH = GRID_WIDTH_PX + PANEL_WIDTH
WINDOW_HEIGHT = max(GRID_SIZE * CELL_SIZE, 400)

# COULEURS
COLOR_SOIL   = (101, 67, 33)       # MARRON (Terre)
COLOR_GRASS  = (34, 139, 34)       # VERT (Herbe)
COLOR_GRID   = (40, 40, 40)        # Gris lignes
COLOR_PANEL  = (30, 30, 30)        # Fond stats
COLOR_TEXT   = (255, 255, 255)

# ANIMAUX
COLOR_SHEEP  = (255, 255, 255)     # BLANC
COLOR_WOLF   = (255, 0, 0)     # GRIS

# GRAPHE
COLOR_SHEEP_LINE = (200, 200, 255) 
COLOR_WOLF_LINE  = (255, 100, 100) 

# Initialisation
pg.init()
screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pg.display.set_caption("Simulation Écosystème")
clock = pg.time.Clock()
UI_FONT = pg.font.SysFont("consolas", 16)

# Historique stats
history_sheep = []
history_wolves = []

def draw_grid(entity_matrix, grass_matrix):
    """
    Dessine en 2 couches :
    1. Le Fond (basé sur grass_matrix)
    2. Les Animaux (basé sur entity_matrix)
    """
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            
            rect = pg.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

            # --- COUCHE 1 : LE SOL (HERBE OU TERRE) ---
            # On regarde l'objet Grass directement
            # Attention : grass_matrix est souvent [x][y] dans ton code, il faut être cohérent
            grass_obj = grass_matrix[x][y] 
            
            # On vérifie si l'herbe a poussé (attribut grown ou is_grown selon ton fichier)
            has_grown = getattr(grass_obj, 'grown', False) or getattr(grass_obj, 'is_grown', False)

            if has_grown:
                pg.draw.rect(screen, COLOR_GRASS, rect) # Fond VERT
            else:
                pg.draw.rect(screen, COLOR_SOIL, rect)  # Fond MARRON
            
            pg.draw.rect(screen, COLOR_GRID, rect, 1)

            # --- COUCHE 2 : LES ANIMAUX ---
            code = entity_matrix[y][x]
            center = (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2)
            radius = int(CELL_SIZE * 0.4) 

            if code == 's' or code == 'S': 
                pg.draw.circle(screen, COLOR_SHEEP, center, radius)
            
            elif code == 'w' or code == 'W': 
                pg.draw.circle(screen, COLOR_WOLF, center, radius)

def draw_stats_panel(turn, sheep_count, wolf_count):
    # (Le reste ne change pas, c'est juste pour le graphe)
    panel_rect = pg.Rect(GRID_WIDTH_PX, 0, PANEL_WIDTH, WINDOW_HEIGHT)
    pg.draw.rect(screen, COLOR_PANEL, panel_rect)
    
    start_x = GRID_WIDTH_PX + 20
    screen.blit(UI_FONT.render(f"Tour : {turn}", True, COLOR_TEXT), (start_x, 20))
    screen.blit(UI_FONT.render(f"Moutons: {sheep_count}", True, COLOR_SHEEP), (start_x, 50))
    screen.blit(UI_FONT.render(f"Loups  : {wolf_count}", True, COLOR_WOLF), (start_x, 75))

    history_sheep.append(sheep_count)
    history_wolves.append(wolf_count)
    
    graph_w = PANEL_WIDTH - 40
    graph_h = 200
    graph_x = GRID_WIDTH_PX + 20
    graph_y = 120
    
    if len(history_sheep) > graph_w:
        history_sheep.pop(0)
        history_wolves.pop(0)

    pg.draw.rect(screen, (10, 10, 20), (graph_x, graph_y, graph_w, graph_h))
    pg.draw.rect(screen, (100, 100, 100), (graph_x, graph_y, graph_w, graph_h), 1)

    if len(history_sheep) >= 2:
        max_val = max(max(history_sheep), max(history_wolves), 1)
        def get_pt(idx, val):
            return (graph_x + idx, graph_y + graph_h - (val / max_val * graph_h))

        for i in range(len(history_sheep) - 1):
            pg.draw.line(screen, COLOR_SHEEP_LINE, get_pt(i, history_sheep[i]), get_pt(i+1, history_sheep[i+1]), 2)
            pg.draw.line(screen, COLOR_WOLF_LINE, get_pt(i, history_wolves[i]), get_pt(i+1, history_wolves[i+1]), 2)