import transportation_problem as tp


def tests():
    s = [('A1', 14), ('A2', 27), ('A3', 19)]
    d = [('B1', 22), ('B2', 13), ('B3', 12), ('B4', 13)]
    c = [[6, 7, 5, 3], [8, 4, 2, 7], [5, 9, 10, 6]]
    p = tp.TransportationProblem(s, d, c)
    r = p.solve(tp.NorthwestCornerIniter, tp.PotentialChecker, tp.ClosedLoopAdjustmentOptimizer)
    print(r)


if __name__ == '__main__':
    tests()
