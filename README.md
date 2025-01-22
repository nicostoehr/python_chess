Chess multiplayer in python using UDP for network transmission, pygame for graphics. Multithreaded and with textures.

Be sure you have pygame installed!
> pip install pygame

Offical site: https://www.pygame.org/docs/

Easly conntect over UDP by choosing to host or join a game. Both parties have to select a PORT. The party that joins the game has to input the IP and PORT of the host game.

Missing features(future updates):
- Castling
- Pawn Transformation (Last Row)
- en passant

Additional note:
There is no system in place to register wether any party is in check. It is possible to capture the enemy king if given the chance. The game ends when either king is captured.
