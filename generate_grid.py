import requests
import re
import datetime

def fetch_github_contrib_grid(username):
    """
    Récupère le SVG des contributions GitHub de l’URL
      https://github.com/users/<username>/contributions
    puis extrait tous les <rect data-date="YYYY-MM-DD" data-count="N"> et en
    reconstruit une matrice 7×52 (0/1) pour les 364 derniers jours.
    """
    url = f"https://github.com/users/{username}/contributions"
    resp = requests.get(url)
    if resp.status_code != 200:
        raise RuntimeError(f"Impossible d'accéder à {url} (statut {resp.status_code})")
    svg = resp.text  # C’est directement le contenu SVG, pas du HTML autour.

    # Nous recherchons tous les rect qui contiennent data-date="YYYY-MM-DD" et data-count="N"
    rect_pattern = re.compile(
        r'<rect\b[^>]*\bdata-date="(?P<date>\d{4}-\d{2}-\d{2})"'
        r'[^>]*\bdata-count="(?P<count>\d+)"[^>]*/?>',
        flags=re.IGNORECASE
    )

    jours = []
    for m in rect_pattern.finditer(svg):
        date_str  = m.group("date")
        count_str = m.group("count")
        try:
            date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            continue
        try:
            cnt = int(count_str)
        except:
            cnt = 0
        jours.append((date_obj, cnt))

    if not jours:
        raise RuntimeError("Aucun <rect data-date> trouvé dans le SVG retourné. "
                           "Soit l’URL est incorrecte, soit GitHub a encore modifié son format.")

    # Trier par date croissante
    jours.sort(key=lambda x: x[0])

    # On veut les 7×52 = 364 derniers jours
    derniere_date = jours[-1][0]
    cutoff = derniere_date - datetime.timedelta(days=7*52 - 1)
    window = [(d, c) for (d, c) in jours if d >= cutoff]

    # S’il manque des jours (< 364), on prépend des zéros pour atteindre 364
    if len(window) < 7*52:
        manque = 7*52 - len(window)
        debut_cal = []
        for i in range(manque):
            date_manquante = cutoff - datetime.timedelta(days=manque - i)
            debut_cal.append((date_manquante, 0))
        window = debut_cal + window
    elif len(window) > 7*52:
        window = window[-7*52:]

    # Construction de la grille 7×52 : window[0] = dimanche le plus ancien, window[363] = samedi le plus récent
    grid = [[0]*52 for _ in range(7)]
    for semaine_idx in range(52):
        for offset_jour in range(7):
            idx = semaine_idx * 7 + offset_jour
            _, cnt = window[idx]
            grid[offset_jour][semaine_idx] = 1 if cnt > 0 else 0

    return grid

def save_grid_to_file(grid, path="grid.txt"):
    """
    Sauvegarde la grille 7×52 (0/1) dans un fichier texte,
    chaque ligne = un jour de la semaine (dimanche→samedi), 52 colonnes sans espace.
    """
    with open(path, "w", encoding="utf-8") as f:
        for row in grid:
            f.write("".join(str(v) for v in row) + "\n")
    print(f"Grille enregistrée dans {path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage : python3 fetch_github_calendar.py <github_username>")
        sys.exit(1)

    username = sys.argv[1]
    try:
        grid = fetch_github_contrib_grid(username)
    except Exception as e:
        print("Erreur :", e)
        sys.exit(1)

    save_grid_to_file(grid, "grid.txt")
