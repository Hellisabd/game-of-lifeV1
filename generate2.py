from xml.etree.ElementTree import Element, SubElement, ElementTree

# --- Configuration générale ---
cell_size   = 10            # taille d'une cellule (pixels)
spacing     = 3             # espace (pixels) entre chaque cellule
image_alive = "full_alive_green.png"
image_dead  = "base_grid_unit.svg"

input_file      = "grid.txt"
output_file     = "animated_game_of_life.svg"
num_generations = 20         # nombre de générations à afficher
frame_duration  = 0.2       # durée d'affichage de chaque génération (en secondes)

def read_single_grid(path=input_file):
    """
    Lit 'grid.txt' et renvoie la grille initiale (list[list[int]]).
    Ignorer les lignes vides ; vérifier que chaque ligne a la même longueur 
    et ne contient que '0' ou '1'.
    """
    with open(path, "r", encoding="utf-8") as f:
        lines = [l.rstrip("\n") for l in f if l.strip() != ""]
    if not lines:
        raise ValueError("Le fichier est vide ou ne contient pas de lignes valides.")

    width = len(lines[0])
    for li in lines:
        if len(li) != width:
            raise ValueError("Toutes les lignes doivent avoir la même longueur.")
        if any(c not in ("0", "1") for c in li):
            raise ValueError("Chaque caractère doit être '0' ou '1'.")
    return [[int(c) for c in line] for line in lines]

def compute_next_generation_torus(grid):
    """
    Calcule la génération suivante du Jeu de la Vie en mode tore (wrap-around).
    Retourne une nouvelle grille de même taille (list[list[int]]).
    """
    rows = len(grid)
    cols = len(grid[0])

    def count_neighbors(r, c):
        total = 0
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr = (r + dr) % rows
                nc = (c + dc) % cols
                total += grid[nr][nc]
        return total

    new_grid = [[0]*cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            vivant = (grid[r][c] == 1)
            voisins = count_neighbors(r, c)
            if vivant:
                new_grid[r][c] = 1 if (voisins == 2 or voisins == 3) else 0
            else:
                new_grid[r][c] = 1 if (voisins == 3) else 0
    return new_grid

if __name__ == "__main__":
    # 1) Lecture de la grille initiale
    try:
        initial_grid = read_single_grid(input_file)
    except Exception as e:
        print(f"Erreur lors de la lecture de la grille : {e}")
        exit(1)

    rows = len(initial_grid)
    cols = len(initial_grid[0])

    # 2) Pré-calcul des générations successives
    generations = [initial_grid]
    for i in range(1, num_generations):
        next_g = compute_next_generation_torus(generations[-1])
        generations.append(next_g)

    # 3) Dimensions d'une grille unique
    single_width  = cols * (cell_size + spacing) - spacing
    single_height = rows * (cell_size + spacing) - spacing

    # 4) Création du SVG
    svg = Element("svg", {
        "xmlns": "http://www.w3.org/2000/svg",
        "width": str(single_width),
        "height": str(single_height),
        "viewBox": f"0 0 {single_width} {single_height}",
        "preserveAspectRatio": "xMinYMin meet"
    })

    # 4a) Couche des cellules mortes : affichée en permanence
    g_dead = SubElement(svg, "g")
    for r in range(rows):
        for c in range(cols):
            x = c * (cell_size + spacing)
            y = r * (cell_size + spacing)
            SubElement(g_dead, "image", {
                "href": image_dead,
                "x": str(x),
                "y": str(y),
                "width": str(cell_size),
                "height": str(cell_size)
            })

    # 4b) Pour chaque génération, un <g> avec opacity="0", puis animate opacity 0→1→0 (mode discret)
    for gen_index, grid in enumerate(generations):
        g_alive = SubElement(svg, "g", {"opacity": "0"})

        # Calcul du moment de début en secondes, avec incréments de frame_duration
        begin_time = gen_index * frame_duration
        SubElement(g_alive, "animate", {
            "attributeName": "opacity",
            "values": "1;0",
            "keyTimes": "0;1",
            "calcMode": "discrete",
            "begin": f"{begin_time:.1f}s",
            "dur": f"{frame_duration:.1f}s",
            "fill": "freeze"
        })

        # Seules les cellules vivantes sont dessinées ici
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 1:
                    x = c * (cell_size + spacing)
                    y = r * (cell_size + spacing)
                    SubElement(g_alive, "image", {
                        "href": image_alive,
                        "x": str(x),
                        "y": str(y),
                        "width": str(cell_size),
                        "height": str(cell_size)
                    })

    # 5) Sauvegarde du fichier SVG
    ElementTree(svg).write(output_file, encoding="utf-8", xml_declaration=True)
    print(f"SVG animé généré : {output_file}")
