import numpy as np


class TransportationChecker(object):
    """
    TransportationChecker 负责求检验数，并判断是否达到最优
    """

    def __init__(self, supply: list, demand: list, costs: list):
        super().__init__()
        self.supply = [i[1] for i in supply]
        self.demand = [i[1] for i in demand]
        self.costs = np.array(costs)
        self.transportation = np.array([])
        self.sigma = np.ones(self.costs.shape) * np.nan  # 检验数，nan 表示基变量，不需要算检验数

    def check(self, transportation: list) -> (list, bool):
        """
        求检验数，并判断是否达到最优
        :return: 检验数，是否达到最优
        """
        self.transportation = np.array(transportation)
        self.sigma = np.ones(self.costs.shape) * np.nan     # 重置检验数！
        self._calc_sigma()
        return self.sigma, self._is_best()

    def _calc_sigma(self):
        """
        计算检验数，结果放到 self.sigma
        :return: None
        """
        raise NotImplementedError

    def _is_best(self) -> bool:
        """
        判断是否达到了最优解
        :return: True for best solution, False else
        """
        return not np.any(self.sigma < 0)


class PotentialChecker(TransportationChecker):
    """
    位势法
    """

    def __init__(self, supply: list, demand: list, costs: list):
        super().__init__(supply, demand, costs)

    def _calc_sigma(self):
        """
        位势法计算检验数

        u 和 v 的意义如下所示：

         |    costs &     | u |
         | transportation | : |
         | v ··           |
        """
        # TODO: 这个暴力解法性能太差了，可以用数学的方法优化！
        #  可以参考： https://zhuanlan.zhihu.com/p/62034448
        #  但由于他那个 Matlab 代码太魔幻了，我暂时看不懂，所以暂时不改这里了。
        u = np.ones(np.array(self.supply).shape) * np.nan
        u[0] = 0
        v = np.ones(np.array(self.demand).shape) * np.nan
        # 对基变量：$\sigma_{ij} = c_{ij} - (u_i + v_j) = 0$，求出 u 和 v
        while np.any(np.isnan(u)) or np.any(np.isnan(v)):
            for r_idx, row in enumerate(self.transportation):
                for c_idx, element in enumerate(row):
                    if not np.isnan(element):  # 基
                        if (not np.isnan(u[r_idx])) and np.isnan(v[c_idx]):
                            v[c_idx] = self.costs[r_idx][c_idx] - u[r_idx]
                        elif (not np.isnan(v[c_idx])) and np.isnan(u[r_idx]):
                            u[r_idx] = self.costs[r_idx][c_idx] - v[c_idx]
        # 计算非基变量检验数: $\sigma_{ij} = c_{ij} - (u_i + v_j)$
        for r_idx, row in enumerate(self.transportation):
            for c_idx, element in enumerate(row):
                if np.isnan(element):  # 非基
                    self.sigma[r_idx][c_idx] = self.costs[r_idx][c_idx] - u[r_idx] - v[c_idx]


# Tests
def _potential_checker_test():
    sp = [('A1', 14), ('A2', 27), ('A3', 19)]
    dm = [('B1', 22), ('B2', 13), ('B3', 12), ('B4', 13)]
    ct = [[6, 7, 5, 3], [8, 4, 2, 7], [5, 9, 10, 6]]
    ts = [[1.0, 0.0, 0.0, 13.0], [2.0, 13.0, 12.0, 0.0], [19.0, 0.0, 0.0, 0.0]]
    checker = PotentialChecker(sp, dm, ct, ts)
    print(checker.check())


if __name__ == '__main__':
    _potential_checker_test()
