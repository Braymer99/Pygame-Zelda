# Nombre/Apellido: Braymer David Domínguez Morales
# Matricula: 22-SISN-2-052

from scripts.settings import TILESISE


def heuristic(a, b):
    # Distancia Manhattan para cuadricula
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(start, goal, obstacle_sprites):
    # Convertir obstáculos a conjunto de nodos ocupados (x, y) en tiles
    obstacles = set()
    for sprite in obstacle_sprites:
        x = sprite.rect.centerx // TILESISE
        y = sprite.rect.centery // TILESISE
        obstacles.add((x, y))

    open_set = [start]
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        current = min(open_set, key=lambda pos: f_score.get(pos, float('inf')))

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            print(f"[A*] Camino encontrado: {path}")
            print("[A*] No se encontró un camino")
            return path

        open_set.remove(current)

        neighbors = [
            (current[0] + 1, current[1]),
            (current[0] - 1, current[1]),
            (current[0], current[1] + 1),
            (current[0], current[1] - 1),
        ]

        for neighbor in neighbors:
            if neighbor in obstacles:
                continue
            tentative_g_score = g_score[current] + 1
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                if neighbor not in open_set:
                    open_set.append(neighbor)

    return []  # No path found
