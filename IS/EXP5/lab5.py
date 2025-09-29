# Simple VND-based SAT solver for small CNF problems

import random
import itertools

def eval_literal(lit, assign):
    if lit.startswith('~'):
        return not assign[lit[1:]]
    return assign[lit]

def num_unsat(clauses, assign):
    return sum(1 for cl in clauses if not any(eval_literal(l, assign) for l in cl))

def vnd(clauses, vars_list, max_iters=1000):
    # start with random assignment
    best = {v: random.choice([False, True]) for v in vars_list}
    best_score = num_unsat(clauses, best)
    if best_score == 0:
        return best
    it = 0
    while it < max_iters and best_score > 0:
        improved = False
        # neighborhood sizes: flip 1, then 2, then 3 vars
        for k in (1,2,3):
            # generate candidate flips (randomized order)
            combos = list(itertools.combinations(vars_list, k))
            random.shuffle(combos)
            local_best = None
            local_best_score = best_score
            for combo in combos:
                cand = best.copy()
                for v in combo:
                    cand[v] = not cand[v]
                s = num_unsat(clauses, cand)
                if s < local_best_score:
                    local_best = cand
                    local_best_score = s
                    # greedy break-on-improvement (VND uses local search per neighborhood)
                    # to be slightly greedy, accept first improvement
                    break
            if local_best is not None:
                best = local_best
                best_score = local_best_score
                improved = True
                break  # restart from smallest neighborhood
        if not improved:
            it += 1
            # random restart small perturbation
            v = random.choice(vars_list)
            best[v] = not best[v]
            best_score = num_unsat(clauses, best)
    return best if best_score==0 else None

if __name__ == "__main__":
    # Formula 1: (A V ~B) ^ (B V ~C) ^ (~B) ^ (~C V E) ^ (A V C) ^ (~C V ~D)
    clauses1 = [
        ["A", "~B"],
        ["B", "~C"],
        ["~B"],
        ["~C", "E"],
        ["A", "C"],
        ["~C", "~D"]
    ]
    vars1 = sorted({l.strip('~') for cl in clauses1 for l in cl})
    sol1 = vnd(clauses1, vars1)
    print("Formula 1 solution found:" , sol1)

    # Formula 2 interpreted as CNF with unit-conjunctions:
    # (A V B) ^ (A) ^ (~C) ^ (B) ^ (D) ^ (A V ~E)
    clauses2 = [
        ["A", "B"],
        ["A"],
        ["~C"],
        ["B"],
        ["D"],
        ["A", "~E"]
    ]
    vars2 = sorted({l.strip('~') for cl in clauses2 for l in cl})
    sol2 = vnd(clauses2, vars2)
    print("Formula 2 solution found:" , sol2)

# Example expected outputs (one valid solution):
# Formula 1 solution found: {'A': True, 'B': False, 'C': False, 'D': False, 'E': False}
# Formula 2 solution found: {'A': True, 'B': True, 'C': False, 'D': True, 'E': False}