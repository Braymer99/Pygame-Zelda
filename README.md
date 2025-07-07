Nombre/Apellido: Braymer David Domínguez Morales
Matrícula: 22-SISN-2-052

README - Zelda

🎮 Descripción del Proyecto

Este proyecto consiste en el desarrollo de un videojuego 2D de acción inspirado en The Legend of Zelda (NES), creado completamente desde cero utilizando la biblioteca Pygame. Aunque el juego se basa en el estilo y la mecánica del clásico de Nintendo, fue diseñado con una estética y estructura propia, tomando como referencia el siguiente video:

📺 https://www.youtube.com/watch?v=QU1pPzEGrqw

El jugador puede desplazarse libremente por el mapa, enfrentarse a enemigos mediante ataques cuerpo a cuerpo y avanzar hasta completar el objetivo principal: eliminar a todos los enemigos del entorno. Si la salud del jugador llega a cero, se considera una derrota.

El juego incluye un menú animado, pantalla de "Game Over", inteligencia artificial de enemigos con Árbol de Comportamiento y algoritmo A*, sonidos, música, sprites descargados y soporte para gamepad.

🧠 Inteligencia Artificial

El proyecto incluye dos sistemas de IA hechos desde cero:
- Árbol de Comportamiento: define los estados de los enemigos.
- Algoritmo A*: permite a los enemigos moverse inteligentemente por el mapa.

⚔ Jugabilidad

- Movimiento libre del jugador
- Ataques a enemigos
- Detección enemiga basada en distancia
- Condición de victoria: eliminar todos los enemigos
- Condición de derrota: perder toda la vida

🕹 Características implementadas

• ✔ Árbol de Comportamiento implementado
• ✔ Algoritmo A* implementado
• ✔ Música de fondo
• ✔ Efectos de sonido
• ✔ Sprites descargados de spriters-resource.com
• ✔ Menú dinámico
• ✔ Pantalla de Game Over
• ✔ Soporte para gamepad
• ✔ Buen rendimiento
• ✔ Proyecto subido a GitHub con historial de commits
• ✔ Video explicativo personal grabado en MP4 con cámara (resolución 720p+)

📁 Estructura del Proyecto

Project IA pygame/
├── main.py
├── README.md
├── check_imports.py
├── requirements.txt
├── .gitignore
├── assets/
│   ├── fonts/
│   ├── images/
│   ├── maps/
│   ├── music/
│   ├── particles/
│   ├── sounds/
│   └── ui/
└── scripts/
    ├── __init__.py
    ├── behavior_tree.py
    ├── debug.py
    ├── enemy.py
    ├── entity.py
    ├── game_over.py
    ├── gamepad.py      
    ├── level.py
    ├── magic.py
    ├── menu.py
    ├── pathfinding.py
    ├── player.py
    ├── particles.py
    ├── settings.py
    ├── support.py
    ├── tile.py
    ├── ui.py
    └── upgrade.py


⚙ Instalación y ejecución

1. Instala las dependencias con:

  pip install -r requirements.txt

2. Ejecuta el juego con:

  python main.py
  


3. Verifica el proyecto con:

  python check_project.py

📹 Video de presentación
El video incluye una explicación en cámara mostrando el juego en ejecución, el código, el árbol de comportamiento y el algoritmo A*. Está en formato MP4 (16:9, 720p o superior).

📌 Créditos

- Sprites: https://www.spriters-resource.com
- Música y efectos: Recursos libres de derechos

✅ Cumplimiento del Mandato del Parcial
Este proyecto cumple con todos los requisitos del examen parcial, incluyendo IA, sonido, sprites, menú, gamepad, rendimiento, video, y estructura en GitHub.
