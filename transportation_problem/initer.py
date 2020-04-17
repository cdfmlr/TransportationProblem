import numpy as np


class TransportationIniter(object):
    """
    TransportationIniter 运输问题初始化的器
    """

    def __init__(self, supply: list, demand: list, costs: list):
        super().__init__()
        self.supply = [i[1] for i in supply]
        self.demand = [i[1] for i in demand]
        self.costs = np.array(costs)
        self.transportation = np.ones(self.costs.shape) * np.nan  # 运量表

    def init(self) -> list:
        """
        初始化
        :return: 初始运输方案
        """
        # raise NotImplementedError
        return list(self.transportation.tolist())

    def _arrange_transportation(self, r, c) -> None:
        """
        安排 (r, c) 处的运量，**原址操作**
        :param r: 行，对应 supply
        :param c: 列，对应 demand
        """
        s, d = self.supply[r], self.demand[c]  # 这个元素对应的供求量
        if s != 0 and d != 0:  # 还没"划掉"
            if s < d:
                self.transportation[r][c] = s
                self.supply[r] = 0
                self.demand[c] -= s
            elif d < s:
                self.transportation[r][c] = d
                self.demand[c] = 0
                self.supply[r] -= d
            else:  # d == s
                self.transportation[r][c] = d
                self.demand[c] = 0
                self.supply[r] = 0


class MinimumElementIniter(TransportationIniter):
    """
    最小元素法
    """

    def __init__(self, supply: list, demand: list, costs: list):
        super().__init__(supply, demand, costs)

    def init(self) -> list:
        # 将运价从小到大排序
        sorted_costs = sorted([c for r in self.costs for c in r])
        for min_element in sorted_costs:  # 从最小元素开始填运量
            # 获取最小元素坐标
            mint = np.where(self.costs == min_element)
            min_indices = np.array(mint).T
            # TAG_LOOP:
            for index in min_indices:
                if self.supply[index[0]] != 0 and self.demand[index[1]] != 0:  # 还没"划掉"
                    self._arrange_transportation(index[0], index[1])
                    break  # break TAG_LOOP
            if not (np.any(self.supply) or np.any(self.demand)):  # 所有supply、demand值都为0
                break

        return list(self.transportation.tolist())


class NorthwestCornerIniter(TransportationIniter):
    """
    西北角法
    """

    def __init__(self, supply: list, demand: list, costs: list):
        super().__init__(supply, demand, costs)

    def init(self) -> list:
        # transportation = np.zeros(self.costs.shape)  # 运量表
        r, c = 0, 0  # 从西北角，即 (r, c) = (0, 0) 开始处理，注意r对应supply，c对应demand
        while (r, c) < self.costs.shape:
            self._arrange_transportation(r, c)
            r += 1 if self.supply[r] == 0 else 0
            c += 1 if self.demand[c] == 0 else 0

        return list(self.transportation.tolist())


class VogelIniter(TransportationIniter):
    """
    伏格尔法
    """

    def __init__(self, supply: list, demand: list, costs: list):
        super().__init__(supply, demand, costs)

    def init(self) -> list:
        while np.any(self.supply) or np.any(self.demand):  # 不是所有supply、demand值都为0
            rd = self._get_row_diffs()
            cd = self._get_col_diffs()
            max_diff = max(rd + cd)
            rs_max = np.where(np.array(rd) == max_diff)
            cs_max = np.where(np.array(cd) == max_diff)

            if len(rs_max) > 0 and len(rs_max[0]) > 0:  # 最差值在行
                r_idx = rs_max[0][-1]
                c_min = np.inf
                c_idx = -1
                for i, c in enumerate(self.costs[r_idx]):
                    if self.demand[i] == 0:
                        continue
                    if c < c_min:
                        c_min = c
                        c_idx = i
                if c_idx == -1:
                    raise RuntimeError
                self._arrange_transportation(r_idx, c_idx)
            elif len(cs_max) > 0 and len(cs_max[0]) > 0:  # 最差值在列
                c_idx = cs_max[0][-1]
                r_min = np.inf
                r_idx = -1
                for i, r in enumerate(self.costs.T[c_idx]):
                    if self.supply[i] == 0:
                        continue
                    if r < r_min:
                        r_min = r
                        r_idx = i
                if r_idx == -1:
                    raise RuntimeError
                self._arrange_transportation(r_idx, c_idx)

        return list(self.transportation.tolist())

    def _get_row_diffs(self) -> list:
        """
        算行差额，若某行已经被"划掉"，则返回中对应的值为 -1
        :return: list of diffs
        """
        return self._get_diffs_of_axis(self.costs, self.supply, self.demand)

    def _get_col_diffs(self) -> list:
        """
        算列差额，若某列已经被"划掉"，则返回中对应的值为 -1
        :return: list of diffs
        """
        return self._get_diffs_of_axis(self.costs.T, self.demand, self.supply)

    def _get_diffs_of_axis(self, axis, source, resource) -> list:
        """
        算行/列差额，若某行/列已经被"划掉"，则返回中对应的值为 -1
        (emmmm, 因为要抽象行和列的通用处理，所以参数设计的有点怪，我不想解释其含义，说起来麻烦。反正照下面的说明用就行了👇)
        :param axis: 算列差额为 self.costs.T，算行差额为 self.costs
        :param source: 算列差额为 self.demand，算行差额为 self.supply
        :param resource: 算列差额为 self.supply，算行差额为 self.demand
        :return: list of diffs
        """
        diffs = []
        for i, line in enumerate(axis):
            if source[i] == 0:
                diffs.append(-1)
                continue
            lowest, second_lowest = np.inf, np.inf
            operated_flag = False
            for j, element in enumerate(line):
                if resource[j] == 0:
                    continue
                if element <= lowest:
                    second_lowest = lowest
                    lowest = element
                    operated_flag = True
                elif element <= second_lowest:
                    second_lowest = element
                    operated_flag = True
            if second_lowest == np.inf:
                diff = lowest
            else:
                diff = second_lowest - lowest
            diffs.append(diff if operated_flag else -1)
        return diffs


# Tests
def __minimum_element_initer_test():
    sp = [('A1', 14), ('A2', 27), ('A3', 19)]
    dm = [('B1', 22), ('B2', 13), ('B3', 12), ('B4', 13)]
    ct = [[6, 7, 5, 3], [8, 4, 2, 7], [5, 9, 10, 6]]
    initer = MinimumElementIniter(sp, dm, ct)
    assert initer.init() == [[1.0, 0.0, 0.0, 13.0], [2.0, 13.0, 12.0, 0.0], [19.0, 0.0, 0.0, 0.0]]
    print("minimum_element_initer_test pass")


def __northwest_corner_initer_test():
    sp = [('A1', 7), ('A2', 4), ('A3', 9)]
    dm = [('B1', 3), ('B2', 6), ('B3', 5), ('B4', 6)]
    ct = [[3, 11, 3, 10], [1, 9, 2, 8], [7, 4, 10, 5]]
    initer = NorthwestCornerIniter(sp, dm, ct)
    assert initer.init() == [[3.0, 4.0, 0.0, 0.0], [0.0, 2.0, 2.0, 0.0], [0.0, 0.0, 3.0, 6.0]]
    print("northwest_corner_initer_test pass")


def __vogel_initer_test():
    sp = [('A1', 7), ('A2', 4), ('A3', 9)]
    dm = [('B1', 3), ('B2', 6), ('B3', 5), ('B4', 6)]
    ct = [[3, 11, 3, 10], [1, 9, 2, 8], [7, 4, 10, 5]]
    initer1 = VogelIniter(sp, dm, ct)
    r1 = initer1.init()
    assert r1 == [[2.0, 0.0, 5.0, 0.0], [1.0, 0.0, 0.0, 3.0], [0.0, 6.0, 0.0, 3.0]], str(r1)

    sp = [('A1', 14), ('A2', 27), ('A3', 19)]
    dm = [('B1', 22), ('B2', 13), ('B3', 12), ('B4', 13)]
    ct = [[6, 7, 5, 3], [8, 4, 2, 7], [5, 9, 10, 6]]
    initer2 = VogelIniter(sp, dm, ct)
    r2 = initer2.init()
    assert r2 == [[1.0, 0.0, 0.0, 13.0], [2.0, 13.0, 12.0, 0.0], [19.0, 0.0, 0.0, 0.0]], str(r2)
    print("vogel_initer_test pass")


if __name__ == '__main__':
    __minimum_element_initer_test()
    __northwest_corner_initer_test()
    __vogel_initer_test()
