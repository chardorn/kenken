import random as r
import multiprocessing as mp

from typing import *
from copy import deepcopy
from functools import reduce
from queue import PriorityQueue, Queue

class KenKenGame(object):
    def __init__(self,
            board : List[List[str]],
            rules : Dict[str, Dict[str, str]]) -> "KenKenGame":
        self._n = len(board)
        self._goals = {}
        self._operators = {}

        for k in rules:
            self._goals[k] = rules[k]['goal']
            self._operators[k] = rules[k]['op']

        self._sections = {}

        for x in range(self._n):
            for y in range(self._n):
                k = board[x][y]
                if k not in self._sections:
                    self._sections[k] = []
                self._sections[k].append((x, y))

    def get_empty_solution(self) -> List[List[int]]:
        return [[1 for _ in range(self._n)] for _ in range(self._n)]

    def get_random_solution(self) -> List[List[int]]:
        return [[r.randint(1, self._n) for _ in range(self._n)] for _ in
                range(self._n)]

    #Validations on size of grid and inputs of each section
    def _is_correct_size(self, attempt : List[List[int]]) -> bool:
        return len(attempt) == self._n and len(attempt[0]) == self._n

    def _is_input_in_range(self, attempt : List[List[int]]) -> bool:
        for col in attempt:
            for v in col:
                if v < 1 or v > self._n:
                    return False
        return True

    def _check_grid(self, attempt : List[List[int]]) -> int:
        constraintCount = 0

        #Check rows
        for x in range(self._n):
            seen = set([])
            for y in range(self._n):
                if attempt[x][y] in seen:
                    constraintCount += 1
                seen.add(attempt[x][y])

        #Check columns
        for y in range(self._n):
            seen = set([])
            for x in range(self._n):
                if attempt[x][y] in seen:
                    constraintCount += 1
                seen.add(attempt[x][y])

        return constraintCount

    def _get_region_contents(self,
            attempt : List[List[int]]) -> Dict[str, List[int]]:
        regions = {}

        for k in self._sections:
            regions[k] = []
            for (x, y) in self._sections[k]:
                regions[k].append(attempt[x][y])

        return regions

    def _check_rules(self, attempt : List[List[int]]) -> int:
        contents = self._get_region_contents(attempt)

        constraintCount = 0

        for k in self._sections:
            operator = self._operators[k]
            goal = self._goals[k]
            content = contents[k]
            curr = 0

            if operator == '+':
                curr = sum(content)
            #We know that for '-' and '/' there can only be 2 elts
            elif operator == '-':
                assert len(content) == 2
                curr = max(content) - min(content)
            elif operator == '*':
                curr = reduce(lambda x,y : x * y, content, 1)
            elif operator == '/':
                assert len(content) == 2
                a = max(content)
                b = min(content)

                #Since we only need to know if the attempt succeeded on the given attempt, we can
                #just make sure curr != goal if they don't evenly divide
                #if a % b != 0:
                #  curr = goal + 1
                #else:
                #  curr = a // b
                curr = a / b
            elif operator == '':
                assert len(content) == 1
                curr = content[0]

            constraintCount += abs(curr - goal)

        return constraintCount

    def score_attempt(self, attempt : List[List[int]]) -> int:
        if not self._is_correct_size(attempt):
            raise Exception("Invalid grid dimensions")
        if not self._is_input_in_range(attempt):
            raise Exception("Invalid inputs detected")

        return self._check_grid(attempt) + self._check_rules(attempt)

    def get_str_repr(self, attempt : List[List[int]]) -> str:
        repr = ""
        for y in range(self._n):
            repr += "".join([str(attempt[x][y]) for x in range(self._n)]) + "\n"
        return repr

    def print_attempt(self, attempt : List[List[int]]) -> None:
        if not self._is_correct_size(attempt):
            raise Exception("Invalid grid dimensions")
        print(self.get_str_repr(attempt))

class AbsKenKenSolver(object):
    def __init__(self, game : "KenKenGame") -> "AbsKenKenSolver":
        raise NotImplementedError()

    def solve(self) -> List[List[int]]:
        raise NotImplementedError()

#Basic hill climbing search (complete DFS)
class DFSSearchKenKenSolver(AbsKenKenSolver):
    def __init__(self,
            game : "KenKenGame",
            tries_before_new_init : int = 1000000,
            num_new_inits_before_giving_up : int = 1000) -> "LocalSearchKenKenSolver":
        self._game = game
        self._tries_before_new_init = tries_before_new_init
        self._num_new_inits_before_giving_up = num_new_inits_before_giving_up

    def solve(self) -> List[List[int]]:
        game = self._game
        frontier = []
        past_attempts = set([])

        initialization = game.get_random_solution()
        past_attempts.add(game.get_str_repr(initialization))
        frontier.append(initialization)

        solution = None

        while len(frontier) > 0:
            attempt = frontier.pop()
            n = len(attempt)

            score = game.score_attempt(attempt)

            if score == 0:
                solution = attempt
                break

            for x in range(n):
                for y in range(n):
                    for delta in range(n):
                        altered = deepcopy(attempt)
                        altered[x][y] = (((altered[x][y] - 1) + delta) % n) + 1
                        if game.get_str_repr(altered) not in past_attempts:
                            past_attempts.add(game.get_str_repr(altered))
                            frontier.append(altered)

        if solution is None:
            print("Oops. No Solution.")

        return solution

#Main difference between this one and generic hill climbing
#is the use of a PriorityQueue to store the constraintCounts of
#all possible steps and move forward with the most optimal grid
class HeuristicsLocalSearchKenKenSolver(AbsKenKenSolver):
    def __init__(self,
            game : "KenKenGame",
            tries_before_new_init : int = 1000000,
            num_new_inits_before_giving_up : int = 1000) -> "LocalSearchKenKenSolver":
        self._game = game
        self._tries_before_new_init = tries_before_new_init
        self._num_new_inits_before_giving_up = num_new_inits_before_giving_up

    def solve(self) -> List[List[int]]:
        global iterCount
        game = self._game
        frontier = PriorityQueue()
        past_attempts = set([])

        initialization = game.get_random_solution()
        init_score = game.score_attempt(initialization)
        past_attempts.add(game.get_str_repr(initialization))
        frontier.put((init_score, initialization))

        solution = None
        iterCount = 0

        while not frontier.empty():
            score, attempt = frontier.get()
            n = len(attempt)

            if score == 0:
                solution = attempt
                break

            for x in range(n):
                for y in range(n):
                    for delta in range(n):
                        altered = deepcopy(attempt)
                        altered[x][y] = (((altered[x][y] - 1) + delta) % n) + 1
                        iterCount += 1
                        if game.get_str_repr(altered) not in past_attempts:
                            past_attempts.add(game.get_str_repr(altered))
                            a_score = game.score_attempt(altered)
                            frontier.put((a_score, altered))

        if solution is None:
            print("Oops. No solution.")
        print(iterCount)
        return solution

#Trying my hand at multiprocessing where if we find any solution
#whatsoever we terminate all threads (currently limited to 4 bc too much)
def solver_proc(solver, q):
    res = solver.solve()
    q.put(res)

def p_solve(solver, n_workers):
    q = mp.Queue()

    workers = [mp.Process(target = solver_proc, args=(solver, q)) for _ in
            range(n_workers)]

    [w.start() for w in workers]

    solution = q.get()

    [w.terminate() for w in workers]

    return solution