# p25-hackathon
git repository for the hackathon

Pour lancer la simulation, l suffit d'appuyer sur le bouton "Run Pyhton File". 

Nous pouvons modifier plusieurs paramètres avant de lancer la simulation, 
Pour ce qui est de la situation initiale, nous pouvons modifier la taille de la grille (GRID_SIZE), le nombre inital de mouton (INITIAL_SHEEP) et de loup (INITIAL_WOLVES) ainsi que le pourcentage d'herbe (INITIAL_GRASS_COVERAGE).
Pour la suite de la simulation, nous pouvons modifier toutes les énérgies (celles initiales des animaux (SHEEP_INITIAL_ENERGY & WOLF_INITIAL_ENERGY), celles gagnées lorsque le mouton mange de l'herbe (SHEEP_ENERGY_FROM_GRASS) et lorsque le loup mange un mouton (WOLF_ENERGY_FROM_SHEEP), celles perdues lors de chaque tour (SHEEP_ENERGY_LOSS_PER_TURN & WOLF_ENERGY_LOSS_PER_TURN) et lors de la reproduction (REPRODUCTION_ENERGY_COST), ainsi celle nécessaire à la reproduction (SHEEP_REPRODUCTION_THRESHOLD & WOLF_REPRODUCTION_THRESHOLD). Nous pouvons modifier la vitesse de pousse de l'herbe (GRASS_GROWTH_PROBABILITY) et son temps de repousse (GRASS_REGRWTH_TIME).
Pour la fin de la simulation, nous pouvons modifier l'âge maximal atteint par les animaux (SHEEP_MAX_AGE & WOLF_MAX_AGE) ainsi que le nombre maximal de tours (MAX_TURNS). 

Les règles sont les suivantes : 
Il y a au départ, un certain nombre de moutons, de loups et de'herbe sur le terrain. Les moutons broutent de l'herbe pour survivre, les loups chassent les moutons pour se nourrir et l'herbe repousse aléatoirement sur la grille. Les animaux perdent de l'énergie à chque tour et peuvent se reproduirent seuls, mais cela leur coûte de l'énergie, qu'ils regagnent en mangeant. Nous voulons analyser la dynamique de l'éco-système selon les paramètres initiaux.                              
