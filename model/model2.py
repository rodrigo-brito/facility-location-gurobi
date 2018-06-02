from gurobipy import *
import math

numFacilities = 10
alpha = 0.20

fixedCost = [96167740070, 90901187292, 144098750901, 100858633155, 118336648863,
             96559150835, 418597605135, 292279854599, 161831506495, 251832772338]

for i in range(numFacilities):
    fixedCost[i] = fixedCost[i] / 10000.0

flowRaw = [[0,              369922,              545037,              192699,              200935,              176508,              567702,              170805,              188311,              163857],
           [257936,                   0,              249978,              265762,              182892,
            231687,              381618,              204121,              124827,              165975],
           [668125,              393153,                   0,              224085,              242028,
            205144,              705582,              202420,              229996,              194240],
           [173291,              331196,              187611,                   0,              163616,
            229295,              401610,              231462,              114204,              186702],
           [174854,              251370,              211827,              190930,                   0,
            183063,              734097,              200876,              238895,              194343],
           [116071,              184419,              121683,              161154,              111170,
            0,              371668,              218289,               95563,              180663],
           [823726,              775351,              904492,              677919,              950579,
            726356,                   0,              988266,             1100066,             1103684],
           [351431,              417345,              362994,              484152,              357110,
            575781,             1733731,                   0,              412263,              918253],
           [121962,              118995,              153452,              102390,              189358,
            111586,              678751,              150642,                   0,              203725],
           [217176,              249639,              228069,              277902,              230836,              328916,             1090983,              508465,              302472,                   0]]

flow = [[0 for i in range(numFacilities)] for j in range(numFacilities)]
for i in range(numFacilities):
    for j in range(numFacilities):
        flow[i][j] = flowRaw[i][j] / 100.0

costRaw = [[0,               19961,               15695,               23247,               23046,               30371,               31577,               32743,               35819,               36032],
           [19961,                   0,               20191,               12595,               24553,
            18813,               29874,               25425,               38247,               30557],
           [15695,               20191,                   0,               13742,                7366,
            18671,               15890,               18296,               20875,               20739],
           [23247,               12595,               13742,                   0,               14466,
            7400,               17776,               12874,               26799,               17962],
           [23046,               24553,                7366,               14466,                   0,
            16356,                8627,               13047,               14115,               14158],
           [30371,               18813,               18671,                7400,               16356,
            0,               15746,                7942,               25355,               13245],
           [31577,               29874,               15890,               17776,                8627,
            15746,                   0,                8784,                9609,                6701],
           [32743,               25425,               18296,               12874,               13047,
            7942,                8784,                   0,               18158,                5353],
           [35819,               38247,               20875,               26799,               14115,
            25355,                9609,               18158,                   0,               14475],
           [36032,               30557,               20739,               17962,               14158,               13245,                6701,                5353,               14475,                   0]]

cost = [[0 for i in range(numFacilities)] for j in range(numFacilities)]
for i in range(numFacilities):
    for j in range(numFacilities):
        cost[i][j] = costRaw[i][j] / 100.0

O = [0 for _ in range(numFacilities)]
D = [0 for _ in range(numFacilities)]

for i in range(numFacilities):
    O[i] = 0
    for j in range(numFacilities):
        O[i] += flow[i][j]

for i in range(numFacilities):
    D[i] = 0
    for j in range(numFacilities):
        D[i] += flow[j][i]

z = {}  # Hub instalation
x = {}  # i to j by hub k and m

model = Model("hub-location")

for i in range(numFacilities):
    for j in range(numFacilities):
        z[(i, j)] = model.addVar(vtype=GRB.BINARY, name="z_%d%d" % (i, j))

for i in range(numFacilities):
    for j in range(numFacilities):
        for k in range(numFacilities):
            for m in range(numFacilities):
                x[(i, j, k, m)] = model.addVar(
                    vtype=GRB.INTEGER, name="x_%d%d%d%d" % (i, j, k, m))

model.update()

# Auxiliar expressions
nodes = range(numFacilities)
hubs = [k for k in range(numFacilities) if z[(k, k)] >= 0.9]

# Add constraints

# Z_ik = 1
for i in nodes:
    model.addConstr(quicksum(z[(i, k)] for k in hubs) == 1)

# Z_ik <= Z_kk
for i in nodes:
    for k in hubs:
        if i != k:
            model.addConstr(z[(i, k)] <= z[k, k])

for i in nodes:
    for k in hubs:
        model.addConstr(quicksum(x[(i, j, k, m)]
                                 for j in nodes for m in hubs) == z[(i, k)])

for j in nodes:
    for m in hubs:
        model.addConstr(quicksum(x[(i, j, k, m)]
                                 for i in nodes for k in hubs) == z[(j, m)])

for i in nodes:
    for j in nodes:
        for k in hubs:
            for m in hubs:
                model.addConstr(x[(i, j, k, m)] >= 0)

nodes = [n for n in range(numFacilities)]
hubs = [k for k in range(numFacilities) if z[(k, k)] >= 0.9]

model.setObjective(
    quicksum(
        fixedCost[k]*z[(k, k)] for k in hubs
    ) + quicksum(
        (O[i] + D[i]) * cost[i][k] * z[(k, k)] for i in nodes for k in hubs
    ) + quicksum(
        flow[i][j] * cost[k][m] * alpha * x[(i, j, k, m)] for i in nodes for j in nodes for k in hubs for m in hubs
    )
)


# Funciona
# m.setObjective(quicksum(fixedCost[j]*z[(j, j)] + quicksum(flow[i][j] * cost[i][j] * alpha
#                                                           * z[(i, j)] for i in range(numFacilities)) for j in range(numFacilities)))


# FO / Ótimo = 90963539,4763
# m.setObjective(getCost(z))
# m.setObjective(quicksum(fixedCost[j]*z[(j, j)] + CostTrasnport()
# quicksum(getCost(z, i, j)*z[(i, j)] for i in range(numFacilities)) for j in range(numFacilities)))

model.modelSense = GRB.MINIMIZE
model.optimize()

print("Result = ", model.objVal)
# for var in model.getVars():
#     if (var.getAttr(GRB.Attr.X) > 0):
#         print("var ", var)
