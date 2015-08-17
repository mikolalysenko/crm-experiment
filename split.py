from scipy import *
from scipy.optimize import linprog

def unpackMatrix(constraints, numVars):
    numConstraints = len(constraints)
    A = zeros((numConstraints, numVars))
    b = zeros(numConstraints)
    for i, (row, f) in enumerate(constraints):
        b[i] = f
        for (j,v) in row:
            A[i,j] = v
    return A, b

def splitDomain(weights, edges, numProcessors, maxLoad):
    edgeIndex = {}
    edgeWeightIndex = {}
    numVertices = len(weights)
    numEdges    = len(edges)
    n = 0
    for (i,k) in edges:
        edgeIndex[(i,k)] = n
        edgeIndex[(k,i)] = n + numEdges
        edgeWeightIndex[(k,i)] = edgeWeightIndex[(i,k)] = edges[(i,k)]
        n += 1
    def P(i,j):
        return numProcessors * i + j
    def D(i,k):
        return numProcessors * numVertices + edgeIndex[(i,k)]
    numVars = numVertices * numProcessors + 2 * numEdges

    # Assemble constraints
    constraint_ub = []
    constraint_eq = []
    for i in range(numVertices):
        row = []
        for j in range(numProcessors):
            constraint_ub.append(([(P(i,j), -1)], 0))
            row.append((P(i,j), 1))
        constraint_eq.append((row, 1))

    for j in range(numProcessors):
        row = []
        for i in range(numVertices):
            row.append((P(i,j), weights[i]))
        constraint_ub.append((row, maxLoad))

    for (i,k) in edgeIndex:
        constraint_ub.append(([(D(i,k), -1)], 0))
        row = [(D(i,k), -1)]
        for j in range(numProcessors):
            row.append((P(i,j), 1))
            row.append((P(k,j),-1))
        constraint_ub.append((row, 0))

    A_ub, b_ub = unpackMatrix(constraint_ub, numVars)
    A_eq, b_eq = unpackMatrix(constraint_eq, numVars)

    c = zeros(numVars)
    for (i,k) in edgeIndex:
        c[D(i,k)] = edgeWeightIndex[(i,k)]

    print 'A_ub=', A_ub
    print 'b_ub=', b_ub
    print 'A_eq=', A_eq
    print 'b_eq=', b_eq
    print 'c=', c

    soln = linprog(c=c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq)
    print soln

    x = soln.x
    assignment = zeros(numVertices)
    processorLoad = zeros(numProcessors)
    for i in range(numVertices):
        maxJ = 0
        maxV = 0
        for j in range(numProcessors):
            if x[P(i,j)] > maxV:
                maxV = x[P(i,j)]
                maxJ = j
        processorLoad[maxJ] += weights[i]
        assignment[i] = maxJ

    print processorLoad

    return assignment

'''
print splitDomain(
    weights=[
        0,
        50,
        60,
        45,
        50,
        40,
        30,
        30,
        100,
        80,
        35,
        30,
        55,
        65,
        20,
        30,
        45,
        50,
        65,
        80,
        90,
        100,
        90
    ],
    edges={
        (1,2): 1,
        (1,6): 1,
        (2,3): 1,
        (2,8): 1,
        (3,8): 1,
        (3,4): 1,
        (4,10): 1,
        (4,5): 1,
        (6,7): 1,
        (6,17): 1,
        (7,8): 1,
        (7,16): 1,
        (8,9): 1,
        (9,10): 1,
        (9,14): 1,
        (10,11): 1,
        (10,13): 1,
        (11,12): 1,
        (12,13): 1,
        (12,22): 1,
        (13,21): 1,
        (13,14): 1,
        (14,9): 1,
        (14,15): 1,
        (15,30): 1,
        (15,19): 1,
        (15,16): 1,
        (16,17): 1,
        (17,18): 1,
        (18,19): 1,
        (19,20): 1,
        (20,21): 1,
        (21,22): 1
    },
    numProcessors=3,
    maxLoad=400)
'''

N = 5
def GRID(i,j):
    return i + j * N

weights = zeros(N*N)
weights[:] = 1
edges = {}
for i in range(N):
    for j in range(N):
        if i > 0:
            edges[(GRID(i,j), GRID(i-1,j))] = 1
        if j > 0:
            edges[(GRID(i,j), GRID(i,j-1))] = 1

print reshape(splitDomain(weights, edges, 4, 7), (N,N))
