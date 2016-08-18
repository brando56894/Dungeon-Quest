# Dungeon-Quest

This is a roll and move style game I had originally created as a final project for my Python class at Rutgers University in New Brunswick,  NJ.
I had converted it to Java and then a GUI game using the Swing library. Sadly over the years I had lost the code and decided to 
recreate it while I was re-learning Python, and make it better than it ever was before since we never learned about classes.

The current features are as follows:

* A shop where the player can purchase health potions and better weapons
* Player finds random items such as gold, health potions and weapons as (s)he is navigating the dungeon
* Random monster attack with 3 types of monsters (gremlin, demon and zombie) which have different attributes
* 4 types of weapons (dagger, sword, pistol, rifle) with different damages
* Mid-game boss and Final boss
* Non-interactive attack system (only initially gives you the choice to fight or run away, all other turns are automated)
* Player gains experience based upon which monster was killed, will be used later for leveling up character

To start the game simply execute main.py with Python v2.x (preferably 2.7.x), the game will not work at all with Python 3

You can also enable debug mode by setting **DEBUG_MODE = "enabled"** in main.py (just comment or uncomment)
