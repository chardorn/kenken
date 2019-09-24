import math
from typing import *
from argparse import ArgumentParser
from localSearchF import *

def parse_input() -> Tuple[str, "KenKenGame"]:
    specs = ""
    n = input()
    specs += n + '\n'
    n = int(n)

    boardT = []

    # row major parsing
    for _ in range(n):
        row = input()
        specs += row + '\n'
        boardT.append(list(row))

    board = [[None for _ in range(n)] for _ in range(n)]
    alphs = set([])

    for x in range(n):
        for y in range(n):
            board[x][y] = boardT[y][x]
            alphs.add(board[x][y])

    rules = {}
    n_rules = len(alphs)
    for _ in range(n_rules):
        rule = input()
        specs += rule + '\n'
        k, r = rule.split(':')

        operator = r[-1]

        if operator not in set(["+", "-", "*", "/"]):
            operator = ""

        if operator != "":
            goal = int(r[:-1])
        else:
            goal = int(r)

        rules[k] = {'goal': goal, 'op': operator}

    game = KenKenGame(board, rules)
    return specs, game

if __name__ == '__main__':
    parser = ArgumentParser()
    args = parser.parse_args()

    specs, game = parse_input()
    solver = HeuristicsLocalSearchKenKenSolver(game)

    #solution = solver.solve()
    solution = p_solve(solver, 4)

    if solution is not None:
        print(specs)
        game.print_attempt(solution)
        print(math.factorial(len(solution))*(len(solution)*len(solution)))
