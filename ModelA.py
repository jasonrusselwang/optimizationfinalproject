from graph_parameter import graph_parameter
import gurobipy

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


# Office Hours Sanity Check
m.Params.MIPGap = 0.1
m.Params.TimeLimit = 10

# for a in arcs:
# 	for k in commodities:
# 		if x[a][k].x > 0.000001:
# 			print(x[a][k].varName, x[a][k].x)

# for a in arcs:
# 	if n[a].x > 0.00001:
# 			print(n[a].varName, n[a].x)

# m.write("m.lp")

# print(str(m.ObjVal))
