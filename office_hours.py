from graph_parameter import graph_parameter
from gurobipy import Model, GRB

# data
data = graph_parameter()
# manipulate data here
commodity_quantity, nodes, arcs, commodity_source, commodity_sink, m_distance = data

# initialize model
m = gp.Model('ModelA')

# decision variables
# question 1: x_a,k is determined while the model is being optimized, how should we write the variable here?
x_ak = m.addVars(insert_variable_here, name="x_ak", vtype=GRB.BINARY)
# question 1a: n_a is also calculated during the optimization process, how should we code this
n_a = m.addVars(insert_variable_here, name="n_a", vtype=GRB.INTEGER, lb=0)
# question 2: we have the cost (distance) for each head tail pair, should this just be the m_distance variable? {(arc pair): euclidean distance}
m_a = m.addVars(m_distance, name="m_a")
q_k = m.addVars(commodity_quantity, name="q_k")
o_k = m.addVars(commodity_source, name="o_k")
d_k = m.addVars(commodity_sink, name="q_k")
# do all of these look ok? ^

# constraints
# question 1231242: how should we take the number of entering arcs and exiting arcs to find which label to put on the node for a specific path?
# question cont.: Should we be iterating over each node or arc? Should we even have any form of iteration at all in the solution?
# question: how do we count the number of arcs entering and exiting each node if that is something that the model is optimizing?
node_labelling = m.addConstrs(, name="node_label")
# not sure how to show the number of arcs entering and exiting each node
num_trucks = m.addConstrs(, name="num_trucks")
# objective function
m.setObjective("m_a * n_a for all arcs", GRB.MINIMIZE)
# need to figure out how to put that in actual math/code ^

# sample summation: (x.sum('*',j) == 1 for j in J)
# ^ need more details on how this actually works
# apologies for so many questions, thanks for the help!

m.optimize()