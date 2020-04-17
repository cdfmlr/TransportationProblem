from transportation_problem.initer import TransportationIniter
from transportation_problem.checker import TransportationChecker
from transportation_problem.optimizer import TransportationOptimizer

import numpy as np


class TransportationProblem(object):
    """
    TransportationProblem 表示一个运输问题

    属性：
        - supply: 产地: [('name', 产量), ...]
        - demand: 销地: [('name', 销量), ...]
        - costs:  运价: [[1, 2, 3, ...], [4, 5, 6, ...], ...]
        - result: 运输问题求解结果，在调用 transportationProblem.solve(...) ，求解成功后才有非 None 值。

    方法：
        -  solve(initer, checker): 对当前问题求解
    """

    def __init__(self, supply: list, demand: list, costs: list):
        super().__init__()
        self.supply = supply
        self.demand = demand
        self.costs = costs
        self.result = None

    def solve(self, initer, checker, optimizer):
        """
        对运输问题当前问题求解
        :param initer:    初始方案求解器，TransportationIniter 的子类
        :param checker:   最优方案检验器，TransportationChecker 的子类
        :param optimizer: 运输方案优化器，TransportationOptimizer 的子类
        :return: 若求解成功则返回 TransportationResult ，否则为 None
        """
        assert issubclass(initer, TransportationIniter)
        assert issubclass(checker, TransportationChecker)
        assert issubclass(optimizer, TransportationOptimizer)
        # TODO: check 产销平衡

        try:
            transportation = initer(self.supply, self.demand, self.costs).init()
            sigma, ok = checker(self.supply, self.demand, self.costs, transportation).check()
            while not ok:
                transportation = optimizer(self.supply, self.demand, self.costs, transportation, sigma).optimize()
                sigma, ok = checker(self.supply, self.demand, self.costs, transportation).check()

            return TransportationResult(self, transportation)
        except Exception as e:
            # print(e)
            raise e


class TransportationResult(object):
    """
    TransportationResult 是运输问题的求解结果
    """

    def __init__(self, problem: TransportationProblem, transportation):
        self.problem = problem
        self.transportation = transportation
        self.total_cost = np.sum(np.array(problem.costs) * np.array(transportation))

    def __str__(self):
        echo = [['运量'] + [i[0] for i in self.problem.demand]]
        for i in range(len(self.problem.costs)):
            echo.append([self.problem.supply[i][0]] + [j for j in self.transportation[i]])

        s = f'Transportation problem optimized successfully. Result cost (total): {self.total_cost}\n'
        for r in echo:
            for c in r:
                s += '%8s\t' % c
            s += '\n'

        return s
