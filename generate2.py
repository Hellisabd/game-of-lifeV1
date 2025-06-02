import io

# --- Configuration générale ---
cell_size      = 10              # taille d'une cellule (pixels)
spacing        = 3               # espace (pixels) entre chaque cellule
image_dead    = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMCIgaGVpZ2h0PSIxMCI+CiAgPCEtLSBmb25kIC0tPgogIDxyZWN0IHg9IjAiIHk9IjAiIHdpZHRoPSIxMCIgaGVpZ2h0PSIxMCIgZmlsbD0iIzE1MWIyMyIvPgoKICA8IS0tIGJvcmR1cmVzIC0tPgogIDxyZWN0IHg9IjAiIHk9IjAiIHdpZHRoPSIxMCIgaGVpZ2h0PSIxMCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjMjEyNzJlIiBzdHJva2Utd2lkdGg9IjEiLz4KCiAgPCEtLSBjb2lucyA6IDFweCDDoCBjaGFxdWUgY29pbiBlbiBwbHVzIHNvbWJyZSAtLT4KICA8cmVjdCB4PSIwIiB5PSIwIiB3aWR0aD0iMSIgaGVpZ2h0PSIxIiBmaWxsPSIjMTUxOTIwIi8+IDwhLS0gY29pbiBoYXV0IGdhdWNoZSAtLT4KICA8cmVjdCB4PSI5IiB5PSIwIiB3aWR0aD0iMSIgaGVpZ2h0PSIxIiBmaWxsPSIjMTUxOTIwIi8+IDwhLS0gY29pbiBoYXV0IGRyb2l0IC0tPgogIDxyZWN0IHg9IjAiIHk9IjkiIHdpZHRoPSIxIiBoZWlnaHQ9IjEiIGZpbGw9IiMxNTE5MjAiLz4gPCEtLSBjb2luIGJhcyBnYXVjaGUgLS0+CiAgPHJlY3QgeD0iOSIgeT0iOSIgd2lkdGg9IjEiIGhlaWdodD0iMSIgZmlsbD0iIzE1MTkyMCIvPiA8IS0tIGNvaW4gYmFzIGRyb2l0IC0tPgo8L3N2Zz4K"
image_alive     = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAABGdBTUEAALGPC/xhBQAAAAFzUkdCAdnJLH8AAAAgY0hSTQAAeiYAAICEAAD6AAAAgOgAAHUwAADqYAAAOpgAABdwnLpRPAAAAAZiS0dEAP8A/wD/oL2nkwAAAAlwSFlzAAALEwAACxMBAJqcGAAAAAd0SU1FB+kFEBUbHMK8zksAAABySURBVBjT1cqxDcJAEAXR+We8mABdCEVgx7RCQIpEF3ThjijAciMH2Qa3FIAtkTLSZE/99Ryn+4BlYykvzjxO6PK8Rd0HQSxCIdJbJMu2igCCwLKR+LG/gF4coVUghBenkbePw3Ck221ptfm6virzOPEBH94gq8V9TNkAAAAASUVORK5CYII="

input_file      = "grid.txt"
output_file     = "animated_game_of_life.svg"
num_generations = 20              # nombre de générations à afficher
frame_duration  = 0.2             # durée d'affichage de chaque génération (secondes)


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

    # 4) Calcul de la durée totale et de la fraction en pourcentage
    total_duration = num_generations * frame_duration  # (ex. 20 * 0.2 = 4.0 s)
    # fraction X (%) que chaque génération occupe dans la timeline
    X = (frame_duration / total_duration) * 100        # (ex. (0.2/4.0)*100 = 5 %)

    # 5) Construction du SVG « à la main » dans un StringIO
    buf = io.StringIO()

    # 5a) En-tête XML + ouverture de <svg>
    buf.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    buf.write(f"<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"{single_width}\" height=\"{single_height}\" ")
    buf.write(f"viewBox=\"0 0 {single_width} {single_height}\" preserveAspectRatio=\"xMinYMin meet\">\n")

    # 5b) Bloc <style> avec un unique @keyframes blink
    buf.write("  <style type=\"text/css\"><![CDATA[\n")
    buf.write("    @keyframes blink {\n")
    buf.write("      0%       { opacity: 1; }\n")
    buf.write(f"      {X:.4f}% {{ opacity: 1; }}\n")
    buf.write(f"      {X + 0.0001:.4f}% {{ opacity: 0; }}\n")
    buf.write("      100%     { opacity: 0; }\n")
    buf.write("    }\n")
    buf.write("  ]]></style>\n\n")

    # 5c) Couche des cellules mortes (toujours visibles en arrière-plan)
    buf.write("  <!-- Couche des cellules mortes -->\n")
    buf.write("  <g id=\"dead\">\n")
    for r in range(rows):
        for c in range(cols):
            x = c * (cell_size + spacing)
            y = r * (cell_size + spacing)
            buf.write(f"    <image href=\"{image_dead}\" x=\"{x}\" y=\"{y}\" width=\"{cell_size}\" height=\"{cell_size}\" />\n")
    buf.write("  </g>\n\n")

    # 5d) Pour chaque génération, créer un <g> invisible au départ,
    #      qui deviendra visible pendant frame_duration puis redeviendra transparent.
    buf.write("  <!-- Couches \"vivant\" par génération, chacune animée en CSS -->\n")
    for gen_index, grid in enumerate(generations):
        begin_time = gen_index * frame_duration
        # style : 
        #   opacity:0 initialement, 
        #   animation: blink total_duration s infinite, 
        #   animation-delay = begin_time s
        buf.write(f"  <g style=\"opacity:0; animation: blink {total_duration}s infinite; animation-delay: {begin_time:.1f}s;\">\n")
        # dessiner uniquement les cellules vivantes
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 1:
                    x = c * (cell_size + spacing)
                    y = r * (cell_size + spacing)
                    buf.write(f"    <image href=\"{image_alive}\" x=\"{x}\" y=\"{y}\" width=\"{cell_size}\" height=\"{cell_size}\" />\n")
        buf.write("  </g>\n\n")

    # 5e) Fermeture de </svg>
    buf.write("</svg>\n")

    # 6) Écrire dans le fichier final
    svg_content = buf.getvalue()
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"SVG animé (CSS) généré : {output_file}")
