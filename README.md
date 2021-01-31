# Schrodinger's frog
Rafael Felipe Córdoba, Luis Carlos Mantilla, Juan Pablo Acuña, Ana Torres, Daniel Sabogal 

<!---
Having a README in your team's repository facilitates judging. A good README contains:
* a clear title for your project,
* a short abstract,
* the motivation/goals for your project,
* a description of the work you did, and
* proposals for future work.

<!---
You can find a potential README template in [one of last year's projects](https://github.com/iQuHACK/QuhacMan).
Feel free to contact the staff with questions over our [event's slack](https://iquhack.slack.com), or via iquhack@mit.edu.
Good luck!
# Table of Contents
1. [Abstract](#abstract)
2. [Motivation](#motivation)
3. [Introduction](#introduction)
4. [References](#references)

<!---
4. [References](#fourth-examplehttpwwwfourthexamplecom)
-->

## Introduction
Crossy Road, Jumper Frog, and Crossy (Q)Duck are all different names for the marvellous game consisting of crossing a road without bumping into obstacles. We have implemented an improved version of the game on which frogs can explore the quantum realm and experience quantum effects such as superposition and tunnelling. Additionally, we have included a primitive AI bot that can play against the user. It decides its moves by minimizing a cost function that depends on its environment using the QAOA algorithm.   

## Elements and rules
* **Map**: This is the place where frogs and qubits coexist.  It contains cars that you must avoid at all costs!
* **Cars**: They move to one side or the other discretely and are shown as dark grey pixels.
* **Frog**: Represented by a dark green square, the frog you control can jump between the multiple highways and must reach the top of the map. 
* **Talos**: In honour of the Greek myth of Talos, this is the name of your opponent. It is the red square (a venenous frog) that is competing against you for victory. It moves according to its neighbouring pixels.
* **Tunnelling superpower**: You can use this superpower, depicted as a purple square, to tunnel across some cars and use it for your advantage against Talos.
* **Superposition superpower**: Every quantum game must have a reference to Schrodinger's cat. In this game, the frog can replace the cat and increase its chances of crashing into a car. Its state will become |+>, and upon smashing into a vehicle (measuring on the computational basis), the frog could still live.  


## Principles

The quantum enhancement of the jumper frog stands on the fascinating |+> state. This first object will allow the frog to use its superpowers. Additionally, Talos, your counter, will walk using the QAOA algorithm. This algorithm works by variationally optimizing external parameters that parametrize a quantum circuit. In this case, the cost function is a hamiltonian whose ground state will be the direction of movement of Talos.


## ToDo
* We want to improve the user interaction—for example, adding Talos as an optional bot and allowing different difficulties. 
* Find better cost functions that improve the skills of Talos.
* Change graphical aspects of the game



## References
* Farhi, E., Goldstone, J., & Gutmann, S. (2014). A quantum approximate optimization algorithm. arXiv preprint arXiv:1411.4028.
* Lima, R. (2017). Frogger. GitHub repository. https://github.com/rhrlima/frogger

