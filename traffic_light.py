import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# #Crear variables difusas
arrivals = ctrl.Antecedent(np.arange(1,8,1), "arrivals")
queue = ctrl.Antecedent(np.arange(1,8,1), "queue")
time = ctrl.Consequent(np.arange(0,61,1), "time")

#Funciones de pertenencia
arrivals.automf(number=4, names=["AN", "F", "M", "TM"])
queue.automf(number=4, names=["VS", "S", "M", "L"])

time['Z'] = fuzz.trimf(time.universe, [0, 0, 10])
time['S'] = fuzz.trimf(time.universe, [0, 20, 40])
time['M'] = fuzz.trimf(time.universe, [20, 40, 60])
time['L'] = fuzz.trimf(time.universe, [40, 60, 65])



#Reglas
regla1 = ctrl.Rule(arrivals["AN"],time["Z"])
regla2 = ctrl.Rule(arrivals["F"] & (queue["VS"] | queue["S"]) , time["S"])
regla3 = ctrl.Rule(arrivals["F"] & (queue["M"] | queue["L"]) , time["Z"])
regla4 = ctrl.Rule(arrivals["M"] & (queue["VS"] | queue["S"]) , time["M"])
regla5 = ctrl.Rule(arrivals["M"] & queue["M"] , time["S"])
regla6 = ctrl.Rule(arrivals["M"] & queue["L"] , time["Z"])
regla7= ctrl.Rule(arrivals["TM"] & (queue["VS"] | queue["L"]) , time["L"])
regla8 = ctrl.Rule(arrivals["TM"] & (queue["S"] | queue["M"]) , time["M"])

#Sistema de Lógica Difusa
sistemaControl = ctrl.ControlSystem([regla1, regla2, regla3, regla4, regla5, regla6, regla7, regla8])

#Simulador
simulador = ctrl.ControlSystemSimulation(sistemaControl)
simulador.input["arrivals"]=0
simulador.input["queue"]=0
simulador.compute()

traffic_lights = simulador.output["time"]
print(traffic_lights)

time.view(sim=simulador)
plt.show()