import numpy as np
import matplotlib.pyplot as plt 
from docplex.mp.model import Model
from qiskit import BasicAer
from qiskit.aqua.algorithms import QAOA, NumPyMinimumEigensolver
from qiskit.optimization.algorithms import CobylaOptimizer, MinimumEigenOptimizer
from qiskit.optimization.problems import QuadraticProgram

#from qiskit_ionq_provider import IonQProvider
#provider = IonQProvider("myKey")
#backend = provider.get_backend("ionq_simulator")
cobyla = CobylaOptimizer()
qaoa = MinimumEigenOptimizer(QAOA(quantum_instance=BasicAer.get_backend('qasm_simulator')))
exact = MinimumEigenOptimizer(NumPyMinimumEigensolver())

class QAOA_BOT:
    def __init__(self, direcciones, vision):
        self.direcciones = direcciones
        self.vision = vision
        self.malos = dict([(0,-5), (1,-7), (2,-5), (3,-5), (4,-5)])
        self.buenos = dict([(0,10), (1,1), (2,2), (3,2), (4,2)]) 
        
    #Carros moviendose hacia la izquierda <==
    def carro_moviendo_izquierda(self,x1,x2,x3, bien, mal):
        if x2!=2:
            recomp = bien*(x3==0 and x2 ==0) + mal*(x2==1) + mal*(x3==1) + 1
        else:
            recomp= mal*(x3==1) + 1
        return recomp

    #Carros moviendose hacia la derecha ==>
    def carro_moviendo_derecha(self,x1,x2,x3, bien, mal):
        if x2!=2:
            recomp = bien*(x1==0 and x2==0) + mal*(x1==1) + mal*(x2==1)  + 1
        else:
            recomp= mal*(x1==1) + 1
        return recomp

    def carro_nada(self,x1,x2,x3, bien, mal):
        return bien

    def carro_izquierda_lados(self,x1,x2,x3,bien ,mal, lado):
        #right derecha
        if lado==3:   
            recomp = bien*(x1==1) + mal*(x3==1)

        #left izquierda
        if lado==2:
            recomp = bien*(x3==1) + mal*(x1==1)
        return recomp

    def carro_derecha_lados(self,x1,x2,x3,bien ,mal, lado):
        if lado==3:   
            recomp = bien*(x1==1) + mal*(x3==1)
        if lado==2:
            recomp = bien*(x3==1) + mal*(x1==1)
        return recomp

    def carro_nada_lados(self,x1,x2,x3, bien ,mal, lado):
        if lado==3:   
            recomp = bien
        if lado==2:
            recomp = bien
        return recomp    
    
    def movimiento(self):
        malos = self.malos
        buenos = self.buenos
        mdl = Model('intento')
        up = mdl.binary_var(name='up')
        down = mdl.binary_var(name='down')
        left = mdl.binary_var(name='left')
        right = mdl.binary_var(name='right')
        stay = mdl.binary_var(name='stay')

        funMin = 0

        #fila 1:
        if filas[0]=='right':
            funMin += self.carro_moviendo_derecha(*cuadricula[0,:], buenos[0], malos[0])*up

        elif filas[0]=='left':
            funMin += self.carro_moviendo_izquierda(*cuadricula[0,:], buenos[0], malos[0])*up

        elif filas[0]=='none':
            funMin += self.carro_nada(*cuadricula[0,:], buenos[0], malos[0])*up

        if filas[1]=='right':
            funMin += self.carro_derecha_lados(*cuadricula[1,:], buenos[2], malos[2],2)*left
            funMin += self.carro_derecha_lados(*cuadricula[1,:], buenos[3], malos[3],3)*right
            funMin += self.carro_moviendo_derecha(*cuadricula[1,:], buenos[4], malos[4])*stay

        elif filas[1]=='left':
            funMin += self.carro_izquierda_lados(*cuadricula[1,:], buenos[2], malos[2],2)*left
            funMin += self.carro_izquierda_lados(*cuadricula[1,:], buenos[3], malos[3],3)*right
            funMin += self.carro_moviendo_izquierda(*cuadricula[1,:], buenos[4], malos[4])*stay

        elif filas[1]=='none':
            funMin += self.carro_nada_lados(*cuadricula[1,:], buenos[2], malos[2],2)*left
            funMin += self.carro_nada_lados(*cuadricula[1,:], buenos[3], malos[3],3)*right
            funMin += self.carro_nada(*cuadricula[1,:], buenos[4], malos[4])*stay

        if filas[2]=='right':
            funMin += self.carro_moviendo_derecha(*cuadricula[2,:], buenos[1], malos[1])*down

        elif filas[2]=='left':
            funMin += self.carro_moviendo_izquierda(*cuadricula[2,:], buenos[1], malos[1])*down

        elif filas[2]=='none':
            funMin += self.carro_nada(*cuadricula[2,:], buenos[1], malos[1])*down

        mdl.minimize(-funMin)
        mdl.add_constraint(up+down+left+right+stay == 1, "cons1")
        qp = QuadraticProgram()
        qp.from_docplex(mdl)
        qaoa_result = qaoa.solve(qp)
        return qaoa_result.variables_dict


