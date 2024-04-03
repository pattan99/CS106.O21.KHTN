from ortools.algorithms.python import knapsack_solver
import os
from tqdm import tqdm

def read_test(path):
    f = open(path, 'r')
    s = f.readlines()[1:]
    n = int(s[0])
    c = int(s[1])
    values = []
    weights = []

    for i in range(0, n):
        line = s[i+3].split(' ')
        value = int(line[0])
        weight = int(line[1])

        values.append(value)
        weights.append(weight)

    f.close()
    return values, weights, c

def OR_Tools_solve(values, weights, capacities, name):
    solver = knapsack_solver.KnapsackSolver(
        knapsack_solver.SolverType.KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER,
        "KnapsackExample",
    )

    # print(values, weights, capacities)
    solver.init(values, weights, capacities)
    solver.set_time_limit(180)
    computed_value = solver.solve()

    total_weight = 0
    for i in range(len(values)):
        if solver.best_solution_contains(i):
            total_weight += weights[0][i]

    f = open('result.txt', 'a')
    f.write(f'*** {name} ***\n')
    f.write(f'Total value: {computed_value}\n')
    f.write(f'Total weight: {total_weight}\n')
    f.write(f'Is optimal: {solver.is_solution_optimal()}\n\n')
    f.close()

def main():
    for folder in tqdm(os.listdir('kplib')):
        if 'git' in folder or 'README' in folder:
            continue

        paths = os.path.join('kplib', folder)
        for unit in tqdm(os.listdir(paths)):
            path = os.path.join(paths, unit) + '\\R01000\\s000.kp'
            values, weights, capacities = read_test(path)

            OR_Tools_solve(values, [weights], [capacities], folder+'_'+unit)

if __name__ == "__main__":
    main()