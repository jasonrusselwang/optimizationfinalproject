# creation of the model and solving
from graph_parameter import graph_parameter
import gurobipy

# setup data
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

# initialize model
m = gurobipy.Model("m")

# path
x = {}
for a in arcs:
	x[a] = {}
	for k in commodities:
		x[a][k] = m.addVar(name = str((str(a),k)),vtype = gurobipy.GRB.BINARY)

# trucks
n = {}
for a in arcs:
	n[a] = m.addVar(name = str((str(a))),vtype = gurobipy.GRB.CONTINUOUS)

# objective
objective = gurobipy.quicksum(distance[a] * n[a] for a in arcs)
m.setObjective(objective, gurobipy.GRB.MINIMIZE)

# source, sink, or otherwise
for k in commodities:
	for node in nodes:
		if node == origin[k]:
			m.addConstr(gurobipy.quicksum(x[a][k] for a in arcs.select(node, "*")) - gurobipy.quicksum(x[a][k] for a in arcs.select("*", node)) == 1) # source
		elif node == destination[k]:
			m.addConstr(gurobipy.quicksum(x[a][k] for a in arcs.select(node, "*")) - gurobipy.quicksum(x[a][k] for a in arcs.select("*", node)) == -1) # sink
		else:
			m.addConstr(gurobipy.quicksum(x[a][k] for a in arcs.select(node, "*")) - gurobipy.quicksum(x[a][k] for a in arcs.select("*", node)) == 0) # otherwise

# quantity
for arc in arcs:
	m.addConstr(n[arc] - gurobipy.quicksum(quantity[k] * x[arc][k] for k in commodities) >= 0)

m.update()
m.optimize()
