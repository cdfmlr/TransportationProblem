import numpy as np
import warnings
from transportation_problem.closed_loop_method import ClosedLoopMethod

warnings.simplefilter(action="ignore", category=RuntimeWarning)


class TransportationOptimizer(object):
    """
    TransportationOptimizer 运输问题的优化器
    """

    def __init__(self, supply: list, demand: list, costs: list):
        super().__init__()
        # TODO: supply, demand, costs 在 optimizer 中好像都没用，可以考虑删除
        self.supply = [i[1] for i in supply]
        self.demand = [i[1] for i in demand]
        self.costs = np.array(costs)
        self.transportation = np.array([])
        self.sigma = np.array([])

    def optimize(self, transportation: list, sigma: list) -> list:
        """
        优化
        :return: (新的transportation)
        """
        raise NotImplementedError


class ClosedLoopAdjustmentOptimizer(TransportationOptimizer):
    """
    闭回路调整法
    """

    def __init__(self, supply: list, demand: list, costs: list):
        super().__init__(supply, demand, costs)

    def optimize(self, transportation: list, sigma: list) -> list:
        self.transportation = np.array(transportation)
        self.sigma = np.array(sigma)

        rs, cs = np.where(self.sigma < 0)
        # 这里可能会抛出 RuntimeWarning: invalid value encountered in less
        # 这没关系，参考：https://stackoverflow.com/questions/34955158/what-might-be-the-cause-of-invalid-value-encountered-in-less-equal-in-numpy
        # 我在文开始的地方 ignore 了 RuntimeWarning 来阻止这个的显示
        if len(rs) == 0:  # 。。。这没啥好优化的了，直接扔回去吧
            return list(self.transportation.tolist())
        # 选最小的检验数
        min_r_idx, min_c_idx = rs[0], cs[0]
        for i in range(len(rs)):
            if self.sigma[rs[i]][cs[i]] < self.sigma[min_r_idx][min_c_idx]:
                min_r_idx, min_c_idx = rs[i], cs[i]
        # 找闭回路
        closed_loop = ClosedLoopMethod(self.sigma).get_closed_loop(min_r_idx, min_c_idx)
        # 调整
        self._closed_loop_adjust(closed_loop)
        return list(self.transportation.tolist())

    def _closed_loop_adjust(self, loop):
        """
        在闭回路中调整运量，在 self.transportation 原址操作
        :param loop: 闭回路
        :return: None
        """
        # 闭回路中最小的运量，下标从0开始，所以取奇数(1, 3)
        min_trans = min([self.transportation[n.row_idx][n.col_idx] for n in loop][1::2])
        # 调整，下标从0开始，所以是偶加奇减(0+, 1-, 2+, 3-)
        for i, n in enumerate(loop):
            if np.isnan(self.transportation[n.row_idx][n.col_idx]):
                self.transportation[n.row_idx][n.col_idx] = 0
            self.transportation[n.row_idx][n.col_idx] += min_trans - 2 * (i % 2) * min_trans


# Tests
def _closed_loop_adjustment_optimizer_test():
    sp = [('I', 2500), ('II', 2500), ('III', 5000)]
    dm = [('A', 1500), ('B', 2000), ('C', 3000), ('D', 3500)]
    ct = [[0, 5, 4, 3], [2, 8, 3, 4], [1, 7, 6, 2]]
    tp = [[1500, 500, 500, 0], [0, 0, 2500, 0], [0, 1500, 0, 3500]]
    sg = [[np.nan, np.nan, np.nan, 3], [3, 4, np.nan, 5], [-1, np.nan, 0, np.nan]]
    optimizer = ClosedLoopAdjustmentOptimizer(sp, dm, ct)
    t = optimizer.optimize(tp, sg)
    print(t)


if __name__ == '__main__':
    # _get_closed_loop_test()
    _closed_loop_adjustment_optimizer_test()
