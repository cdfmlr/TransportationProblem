import transportation_problem as tp


def tests():
    s = [('A1', 14), ('A2', 27), ('A3', 19)]
    d = [('B1', 22), ('B2', 13), ('B3', 12), ('B4', 13)]
    c = [[6, 7, 5, 3], [8, 4, 2, 7], [5, 9, 10, 6]]
    p = tp.TransportationProblem(s, d, c)
    # 西北角法初始化，位势法检验，闭回路法优化调整
    r = p.solve(tp.NorthwestCornerIniter, tp.PotentialChecker, tp.ClosedLoopAdjustmentOptimizer)
    assert r.transportation == [[1.0, 0.0, 0.0, 13.0], [2.0, 13.0, 12.0, 0.0], [19.0, 0.0, 0.0, 0.0]], r.transportation
    print(r)
    # 伏格尔法初始化，位势法检验，闭回路法优化调整
    r = p.solve(tp.VogelIniter, tp.PotentialChecker, tp.ClosedLoopAdjustmentOptimizer)
    assert r.transportation == [[1.0, 0.0, 0.0, 13.0], [2.0, 13.0, 12.0, 0.0], [19.0, 0.0, 0.0, 0.0]], r.transportation
    print(r)

    sp = [('I', 2500), ('II', 2500), ('III', 5000)]
    dm = [('A', 1500), ('B', 2000), ('C', 3000), ('D', 3500)]
    ct = [[0, 5, 4, 3], [2, 8, 3, 4], [1, 7, 6, 2]]
    # 默认最小元素法初始化，位势法检验，闭回路法优化调整
    pb = tp.TransportationProblem(sp, dm, ct)
    rt = pb.solve()
    print(rt)

    spy = [('A', 400), ('B', 450), ('C', 70)]
    dmd = [('甲', 290), ('甲\'', 30), ('乙', 250), ('丙', 270), ('丙\'', 80)]
    cst = [[15, 15, 18, 22, 22], [21, 21, 25, 16, 16], [999, 0, 999, 999, 0]]
    pbm = tp.TransportationProblem(spy, dmd, cst)
    # 伏格尔法初始化
    res = pbm.solve(tp.VogelIniter)
    print(res)


if __name__ == '__main__':
    tests()
