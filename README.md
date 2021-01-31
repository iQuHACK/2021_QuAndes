# Welcome to iQuHACK 2021!
___
##### Rafael Felipe Córdoba, Luis Carlos Mantilla, Juan Pablo Acuña, Ana Torres, Daniel Sabogal      
Check out some info in the [event's repository](https://github.com/iQuHACK/2021) to get started.

Having a README in your team's repository facilitates judging. A good README contains:
* a clear title for your project,
* a short abstract,
* the motivation/goals for your project,
* a description of the work you did, and
* proposals for future work.

You can find a potential README template in [one of last year's projects](https://github.com/iQuHACK/QuhacMan).

Feel free to contact the staff with questions over our [event's slack](https://iquhack.slack.com), or via iquhack@mit.edu.

Good luck!
<!---
____
# Table of Contents
1. [Abstract](#abstract)
2. [Motivation](#motivation)
3. [Introduction](#introduction)
4. [References](#references)

<!---
4. [References](#fourth-examplehttpwwwfourthexamplecom)
-->
-->
## Introduction
Crossy Road, Jumper Frog, and Crossy (Q)Duck are all different names for the marvellous game consisting of crossing a road without bumping into obstacles. We have implemented an improved version of the game on which frogs can explore the quantum realm and experience quantum effects such as superposition and tunnelling. Additionally, we have included a primitive AI bot that can play against the user. It decides its moves by minimizing a cost function that depends on its environment using the QAOA algorithm.   

## Elements and rules
* Map: This is the place where frogs and qubits coexist.  It contains cars that you must avoid at all costs!
* Cars: They move to one side or the other discretely and are shown as dark grey pixels.
* Frog: Represented by a dark green square, the frog you control can jump between the multiple highways and must reach the top of the map. 
* Talos: In honour of the Greek myth of Talos, this is the name of your opponent. It is the red square (a venenous frog) that is competing against you for victory. It moves according to its neighbouring pixels.
* Tunnelling superpower: You can use this superpower, depicted as a purple square, to tunnel across some cars and use it for your advantage against Talos.
* Superposition superpower: Every quantum game must have a reference to Schrodinger's cat. In this game, the frog can replace the cat and increase its chances of crashing into a car. Its state will become |+>, and upon smashing into a vehicle (measuring on the computational basis), the frog could still live.  



## References
___
* Farhi, E., Goldstone, J., & Gutmann, S. (2014). A quantum approximate optimization algorithm. arXiv preprint arXiv:1411.4028.
* Lima, R. (2017). Frogger. GitHub repository.

