# Tanks2
The sequel to Tanks. A two player duel tanks game.

# Installation
PyGame wird benötigt. Installierbar mit ```pip install pygame```.

# Anleitung
[W] / [↑] Vorwärts bewegen

[A] / [↓] Rückwärts bewegen

[S] / [→] Nach rechts bewegen

[D] / [←] Nach links bewegen

[F] / [L] Feuern

# Einstellungen
Dies sind die Standardeinstellungen. Sie sind als JSON-Datei gespeichert.
```json
{
    "fps": 60,
    "speed": 2,
    "firerate": 10
}
```
"fps" stellt die frames per second, also die Bilder pro Sekunde, dar. Bitte nicht verändern.

"speed" ist die Geschwindigkeit der Spieler. Je höher, desto schneller.

"firerate" ist die Feuerrate. Je niedriger, desto schneller.

# Level erstellen
Dies ist ein Beispiel-Level. Er ist als JSON-Datei gespeichert.
```json
{
    "spawn_one": [
        310,
        110
    ],
    "spawn_two": [
        310,
        300
    ],
    "walls": [
        {
            "type": "I_x",
            "position": [
                360,
                180
            ]
        }
    ]
}
```
Das Spielfeld ist 800x400 groß.

"spawn_one" ist der Spawnpunkt des ersten Spielers. Der erste Wert ist die x-Koordinate, der zweite Wert die y-Koordinate.

"spawn_two" ist der Spawnpunkt des zweiten Spielers. Der erste Wert ist die x-Koordinate, der zweite Wert die y-Koordinate.

"walls" enthält alle Wände eines Levels.
Jede Wand hat einen Typ "type", der entweder "I_x" oder "I_y" ist. "I_x" stellt waagerechte und "I_y" senkrechte Wände dar.
Die Position der Wand wird mit "position" dargestellt. Der erste Wert ist die x-Koordinate, der zweite Wert die y-Koordinate. (Jede Wand ist 10x100 bzw. 100x10 groß.)