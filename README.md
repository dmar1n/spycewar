# SPYCEWAR!

**Author**: Daniel Marín

**Initial version**: July 2024  

**Repository**: [https://github.com/dmar1n/spycewar](https://github.com/dmar1n/spycewar)

## Description

Spycewar is a game inspired by the classic *Spacewar!*, probably the first video game in history. It was designed in 1961 by Martin Graetz, Stephen Russell, and Wayne Wiitanen, and implemented for the PDP-1 computer in 1962.

In the original game, two players battle each other, each controlling a spaceship navigating around a central star with gravitational pull. Players can fire missiles, rotate and thrust their ships, and use a hyperspace jump button.

Spycewar implements similar mechanics: propulsion systems, projectile firing, and hyperspace jumps (instant teleportation to a random point on the screen). The main differences are:

- No central star.
- Addition of a temporary shield.
- Health and shield bars.
- Random appearances of a supply ship that restores a portion of the ship's health.

Hyperspace jumps allow instant repositioning, as in the original game. Additionally, players can activate shields to become immune to missiles temporarily; however, the shield depletes over time and cannot be replenished (it acts like a second health bar).

Each ship has different characteristics (speed, rotation, health, firing rate, etc.), enabling diverse strategies depending on the chosen ship.

## Implementation

The game is built using class polymorphism, inheritance, and the state pattern, while also following the composition principle. Pygame's own event system is used to keep the code as decoupled as possible. Diagrams for players and ships are provided in the appendix, showcasing the combination of inheritance and composition principles.

## Optimizations

Several optimizations have been implemented to improve efficiency and performance:

### Images

- Ship, projectile, and supply ship images are loaded into memory only once.
- Rotated ship images are cached. If a ship remains static or only moves without rotating, the already rotated image is reused.
- Projectiles that go off-screen are deleted from memory.

### Collisions

- Collision detection first checks bounding rectangles (efficient).
- If rectangles collide, mask-based collision detection (more accurate, but slower) is used.
- This two-step collision system is applied for all collisions (ship vs ship, ship vs projectile, ship vs supply).

## Technical Challenges

### Ship Rotation and Acceleration

Implementing ship rotation, acceleration, and momentum required more complex physics than simpler 2D shooters like *Space Invaders*.  

Key considerations:

- Calculating thrust force based on the ship's current angle.
- Handling velocity vectors for acceleration and drift (no friction forces are applied).
- Ships have a maximum speed to prevent infinite acceleration.
- Projectile movement adds to the ship's existing velocity.

**Boundary behaviour**:

- Projectiles are destroyed when reaching the screen limits.
- Ships wrap around to the opposite side of the screen.

Movement and projectile behaviors are handled via a dedicated movement calculation function.

### Particle System

A particle system was developed to illustrate ship thrust and collisions.

- Each particle is a game object.
- Different parameters are applied depending on the event (explosions, propulsion effects).

### Ship Encapsulation and Polymorphism

To keep the code modular:

- Ship specifications (acceleration, rotation speed, cooldown times, etc.) are isolated in separate classes.
- Ship states (remaining health, damage handling, healing, etc.) are encapsulated.
- This allows flexible instantiation of different player types without needing to hard-code separate classes.

**Player Model**: Accepts a state and a set of specifications (composition relation).

### Shared Data Between States

A typical state pattern does not allow for direct data sharing between states. However, in games, it is necessary (e.g., determining the winning player).

- A *Context* class was created to encapsulate shared information in a dictionary.
- This context is passed into each state at entry and returned at exit, carrying any necessary data.

## Possible Improvements

Future extensions and enhancements for *Spycewar!* could include:

- AI implementation for single-player mode.
- Fuel and ammunition bars, with corresponding power-ups.
- A central star with gravitational force, as in the original game.
- Critical hit system (inspired by RPGs).
- Sound effects for propulsion, collisions, and firing.
- A complex scoring system spanning multiple rounds.
- Display of damage numbers, RPG-style.
- Visual improvements (different colors for critical hits, shielded missiles, etc.).
- An installer for different operating systems.
- Ship redesigns.
- In-game options menu.
