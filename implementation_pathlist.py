from graph_parameter import graph_parameter
import gurobipy
import re
import csv
from ast import literal_eval

graphparameter = graph_parameter()

commodities = graphparameter[0]
nodes = graphparameter[1]
arcs = graphparameter[2]
origin = graphparameter[3]
destination = graphparameter[4]
distance = graphparameter[5]


quantity = {}
for j in commodities:
	quantity[j] = float(commodities[j])

m = gurobipy.Model("m")

x = {}
for a in arcs:
	x[a] = {}
	for k in commodities:
		x[a][k] = m.addVar(name = str((str(a),k)),vtype = gurobipy.GRB.BINARY)
		#change to continuous for analysis path A

n = {}
for a in arcs:
	n[a] = m.addVar(name = str((str(a))),vtype = gurobipy.GRB.CONTINUOUS)

objective = gurobipy.quicksum(distance[a] * n[a] for a in arcs)
m.setObjective(objective, gurobipy.GRB.MINIMIZE)

for k in commodities:
	for node in nodes:
		if node == origin[k]:
			m.addConstr(gurobipy.quicksum(x[a][k] for a in arcs.select(node, "*")) - gurobipy.quicksum(x[a][k] for a in arcs.select("*", node)) == 1)
		elif node == destination[k]:
			m.addConstr(gurobipy.quicksum(x[a][k] for a in arcs.select(node, "*")) - gurobipy.quicksum(x[a][k] for a in arcs.select("*", node)) == -1)
		else:
			m.addConstr(gurobipy.quicksum(x[a][k] for a in arcs.select(node, "*")) - gurobipy.quicksum(x[a][k] for a in arcs.select("*", node)) == 0)

for arc in arcs:
	m.addConstr(n[arc] - gurobipy.quicksum(quantity[k] * x[arc][k] for k in commodities) >= 0)

m.update()
m.optimize()
print('Runtime: ' + str(m.Runtime))

# Retrieve variables value
#print('Optimal Solution:')
#for v in m.getVars():
#	print('%s = %g' % (v.varName, v.x))
#print('Optimal objective value: \n{}'.format(m.objVal))


# Office Hours Sanity Check
m.Params.MIPGap = 0.1
m.Params.TimeLimit = 10

pathList = []
for k in commodities:
	pathList.append([])

#pathList calculation
for a in arcs:
	for k in commodities:
		if x[a][k].x > 0.000001:
			com = int(re.findall(r'k\d{1,2}', x[a][k].varName)[0][1:])
			arc = re.findall(r'\(\d{1,2},\s\d{1,2}\)', x[a][k].varName)[0]
			pathList[com - 1].append(arc)
			print(x[a][k].varName, x[a][k].x)

print(pathList)
flat_pathList = [item for sublist in pathList for item in sublist]
pathList = list(set(flat_pathList))
print(pathList)
pathList = [literal_eval(item) for item in pathList]
print(pathList)
#pathList = gurobipy.tuplelist([tuple(pair) for pair in pathList])
#print(pathList)

with open("output_arcs.csv", 'w') as file:
	writer = csv.writer(file)
	for path in pathList:
		writer.writerow(path)
	
#for a in arcs:
#	if n[a].x > 0.00001:
#		print(n[a].varName, n[a].x)

# m.write("m.lp")

# print(str(m.ObjVal))
