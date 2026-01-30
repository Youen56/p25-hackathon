import pygame as pg
import sys
import random
import parameters

# --- 1. CONFIGURATION DU JEU ---
GRID_SIZE = 30
MAX_TURNS = 500

# --- 2. CONFIGURATION AFFICHAGE ---
CELL_SIZE = 20                     
GRID_WIDTH_PX = GRID_SIZE * CELL_SIZE
PANEL_WIDTH = 300                  
WINDOW_WIDTH = GRID_WIDTH_PX + PANEL_WIDTH
WINDOW_HEIGHT = max(GRID_SIZE * CELL_SIZE, 400)

# COULEURS (R, G, B)
COLOR_SOIL   = (101, 67, 33)       # MARRON (Terre / Fond par défaut)
COLOR_GRASS  = (34, 139, 34)       # VERT (Herbe)
COLOR_GRID   = (40, 40, 40)        # Lignes grille
COLOR_PANEL  = (30, 30, 30)        # Fond stats
COLOR_TEXT   = (255, 255, 255)

# COULEURS ANIMAUX
COLOR_SHEEP  = (255, 255, 255)     # BLANC
COLOR_WOLF   = (128, 128, 128)     # GRIS

# COULEURS GRAPHE
COLOR_SHEEP_LINE = (200, 200, 255) 
COLOR_WOLF_LINE  = (255, 100, 100) 

# Initialisation
pg.init()
screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pg.display.set_caption("Simulation Écosystème")
clock = pg.time.Clock()
UI_FONT = pg.font.SysFont("consolas", 16)

# Historique pour le graphe
history_sheep = []
history_wolves = []

# --- 3. FONCTIONS D'AFFICHAGE ---

def draw_grid(matrix_data):
    """
    Affiche la grille selon les caractères simples :
    '.' = Terre
    '#' = Herbe
    's' = Mouton
    'w' = Loup
    """
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            code = matrix_data[y][x]
            
            rect_x = x * CELL_SIZE
            rect_y = y * CELL_SIZE
            rect = pg.Rect(rect_x, rect_y, CELL_SIZE, CELL_SIZE)

            # --- A. LE FOND (TERRAIN) ---
            # Seul le code '#' déclenche le fond vert.
            # Tout le reste ('.', 's', 'w') aura un fond marron (Terre).
            if code == '#':
                pg.draw.rect(screen, COLOR_GRASS, rect)
            else:
                pg.draw.rect(screen, COLOR_SOIL, rect)
            
            # Grille fine
            pg.draw.rect(screen, COLOR_GRID, rect, 1)

            # --- B. L'ANIMAL (CERCLE) ---
            center = (rect_x + CELL_SIZE // 2, rect_y + CELL_SIZE // 2)
            radius = int(CELL_SIZE * 0.4) 

            # Attention aux majuscules/minuscules, je gère les deux au cas où
            if code == 's' or code == 'S': 
                # MOUTON -> Cercle BLANC
                pg.draw.circle(screen, COLOR_SHEEP, center, radius)
            
            elif code == 'w' or code == 'W': 
                # LOUP -> Cercle GRIS
                pg.draw.circle(screen, COLOR_WOLF, center, radius)

def draw_stats_panel(turn, sheep_count, wolf_count):
    """Affiche le panneau latéral et le graphe."""
    # Fond panneau
    panel_rect = pg.Rect(GRID_WIDTH_PX, 0, PANEL_WIDTH, WINDOW_HEIGHT)
    pg.draw.rect(screen, COLOR_PANEL, panel_rect)
    
    start_x = GRID_WIDTH_PX + 20
    
    # Textes
    lbl_turn = UI_FONT.render(f"Tour : {turn} / {MAX_TURNS}", True, COLOR_TEXT)
    lbl_sheep = UI_FONT.render(f"Moutons (Blanc): {sheep_count}", True, COLOR_SHEEP_LINE)
    lbl_wolf = UI_FONT.render(f"Loups   (Gris) : {wolf_count}", True, COLOR_WOLF_LINE)
    
    screen.blit(lbl_turn, (start_x, 20))
    screen.blit(lbl_sheep, (start_x, 50))
    screen.blit(lbl_wolf, (start_x, 75))

    # --- GRAPHE DYNAMIQUE ---
    history_sheep.append(sheep_count)
    history_wolves.append(wolf_count)
    
    graph_w = PANEL_WIDTH - 40
    graph_h = 200
    graph_x = GRID_WIDTH_PX + 20
    graph_y = 120
    
    # Scroll (supprime les vieux points)
    if len(history_sheep) > graph_w:
        history_sheep.pop(0)
        history_wolves.pop(0)

    # Cadre du graphe
    pg.draw.rect(screen, (10, 10, 20), (graph_x, graph_y, graph_w, graph_h))
    pg.draw.rect(screen, (100, 100, 100), (graph_x, graph_y, graph_w, graph_h), 1)

    if len(history_sheep) < 2: return

    # Mise à l'échelle
    max_val = max(max(history_sheep), max(history_wolves), 1)
    
    def get_pt(idx, val):
        px = graph_x + idx
        py = graph_y + graph_h - (val / max_val * graph_h)
        return (px, py)

    # Tracé des lignes
    for i in range(len(history_sheep) - 1):
        pg.draw.line(screen, COLOR_SHEEP_LINE, 
                     get_pt(i, history_sheep[i]), 
                     get_pt(i+1, history_sheep[i+1]), 2)
        pg.draw.line(screen, COLOR_WOLF_LINE, 
                     get_pt(i, history_wolves[i]), 
                     get_pt(i+1, history_wolves[i+1]), 2)

# --- 4. SIMULATION FAKE (CORRIGÉE AVEC CARACTÈRES) ---
def get_fake_simulation_state():
    matrix = []
    for r in range(GRID_SIZE):
        row = []
        for c in range(GRID_SIZE):
            rand = random.random()
            # Simulation aléatoire avec les caractères demandés
            if rand < 0.3: val = '#'      # Herbe
            elif rand < 0.35: val = 's'   # Mouton ('s')
            elif rand < 0.40: val = 'w'   # Loup ('w')
            else: val = '.'               # Terre/Vide
            row.append(val)
        
        matrix.append(row)
        
    return matrix

# --- 5. BOUCLE PRINCIPALE ---
def main():
    print(">>> Démarrage...")
    running = True
    turn = 0
    
    while running and turn <= MAX_TURNS:
        # Events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    running = False

        # Logique
        current_matrix = get_fake_simulation_state()
        turn += 1
        
        # Comptage basé sur les caractères 's' et 'w' (et S/W majuscules au cas où)
        # On compte 's' ET 'S', 'w' ET 'W' pour éviter les bugs si ton collègue change la casse
        nb_sheep = sum(row.count('s') + row.count('S') for row in current_matrix)
        nb_wolves = sum(row.count('w') + row.count('W') for row in current_matrix)

        # Dessin
        screen.fill((0, 0, 0))
        draw_grid(current_matrix)
        draw_stats_panel(turn, nb_sheep, nb_wolves)
        
        pg.display.flip()
        clock.tick(5) 

    pg.quit()
    sys.exit()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("\nERREUR :", e)
        pg.quit()