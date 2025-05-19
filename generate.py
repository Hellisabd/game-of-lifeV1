from xml.etree.ElementTree import Element, SubElement, ElementTree

# --- Configuration de la grille GitHub ---
cols = 52             # Nombre de colonnes (semaines)
rows = 7              # Nombre de lignes (jours)
cell_size = 10        # Taille d'une cellule (pixels)
spacing = 3           # Espace entre cellules          # Décalage vertical initial

# --- Taille totale du SVG ---
width = cols * (cell_size + spacing) - spacing
height = rows * (cell_size + spacing) - spacing

# --- Création du SVG ---
svg = Element("svg", {
    "xmlns": "http://www.w3.org/2000/svg",
    "width": str(width),
    "height": str(height),
    "viewBox": f"0 0 {width} {height}",
    "preserveAspectRatio": "xMinYMin meet"
})

# --- Génération de la grille ---
for row in range(rows):
    for col in range(cols):
        x = col * (cell_size + spacing)
        if x > width - (cell_size + 1) and y == height - 10:
            break
        y = row * (cell_size + spacing)
        SubElement(svg, "image", {
            "href": "base_grid_unit.svg",  # ton image de cellule vivante
            "x": str(x),
            "y": str(y),
            "width": str(cell_size),
            "height": str(cell_size)
        })
        
for row in range(rows):
    for col in range(cols):
        x = col * (cell_size + spacing)
        y = row * (cell_size + spacing)
        if x > width - (cell_size + 1) and y == height - 10:
            break
        SubElement(svg, "image", {
            "href": "Alive.svg",  # ton image de cellule vivante
            "x": str(x),
            "y": str(y),
            "width": str(cell_size),
            "height": str(cell_size)
        })

# --- Sauvegarde du fichier ---
output_file = "full_grid_green.svg"
ElementTree(svg).write(output_file, encoding="utf-8", xml_declaration=True)
print(f"SVG généré : {output_file}")
