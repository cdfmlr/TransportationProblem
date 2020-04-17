import numpy as np


class ClosedLoopNode(object):
    """
    闭回路节点
    """

    def __init__(self, row_idx, col_idx):
        self.row_idx = row_idx
        self.col_idx = col_idx

    def __str__(self):
        return f'ClosedLoopNode<{self.row_idx}, {self.col_idx}>'


class ClosedLoopMethod(object):
    """
    闭回路法，提供找闭回路的方法
    """

    def __init__(self, sigma):
        self.sigma = np.array(sigma)
        self.loop = []
        self.target = None

    def _rows_possible(self, node: ClosedLoopNode, direction):
        cs = np.where(np.isnan(self.sigma[node.row_idx]))[0]
        cs = list(filter(lambda x: direction * x > direction * node.col_idx, cs))
        indices = [(node.row_idx, i) for i in cs]
        return indices

    def _cols_possible(self, node: ClosedLoopNode, direction):
        rs = np.where(np.isnan(self.sigma.T[node.col_idx]))[0]
        rs = list(filter(lambda x: direction * x > direction * node.row_idx, rs))
        indices = [(i, node.col_idx) for i in rs]
        return indices

    def _walk(self, node: ClosedLoopNode, last: ClosedLoopNode):
        # 看看到没到头
        if node.col_idx == self.target.col_idx and last.col_idx != self.target.col_idx:
            self.loop.insert(0, node)
            return True
        if node.row_idx == self.target.row_idx and last.row_idx != self.target.row_idx:
            self.loop.insert(0, node)
            return True
        # 求出上一步的方向
        dx = node.row_idx - last.row_idx
        if dx != 0:
            dx //= abs(dx)
        dy = node.col_idx - last.col_idx
        if dy != 0:
            dy //= abs(dy)
        possible = []
        # 先不忙着走，咱先站在原地四处看一看
        # 不转向
        if dx == 0:
            possible += self._rows_possible(node, dy)
        if dy == 0:
            possible += self._cols_possible(node, dx)
        # 转向
        if dx == 0:
            possible += self._cols_possible(node, -1)
            possible += self._cols_possible(node, 1)
        if dy == 0:
            possible += self._rows_possible(node, -1)
            possible += self._rows_possible(node, 1)

        # 试着走走吧
        for p in possible:
            ok = self._walk(ClosedLoopNode(p[0], p[1]), node)
            if ok:
                # 算一下这成功的一步的方向
                step_x = p[0] - node.row_idx
                if step_x != 0:
                    step_x //= abs(step_x)
                step_y = p[1] - node.col_idx
                if step_y != 0:
                    step_y //= abs(step_y)
                # 转弯了就要记录拐点
                if step_x != dx or step_y != dy:
                    self.loop.insert(0, node)
                return True
        return False

    def get_closed_loop(self, r, c):
        """
        找闭回路
        :param r: 起点行索引
        :param c: 起点列索引
        :return: 闭回路, a list of ClosedLoopNodes
        """
        start = ClosedLoopNode(r, c)

        self.target = start
        self.loop = [start]

        self._walk(start, start)

        if len(self.loop) < 2:
            raise RuntimeError
        return self.loop[:-1]


# Tests
def _closed_loop_test():
    sg = [[np.nan, np.nan, np.nan, 3], [3, 4, np.nan, 5], [-1, np.nan, 0, np.nan]]
    loop = ClosedLoopMethod(sg).get_closed_loop(2, 0)
    for i in loop:
        print(i, end=', ')
    print('\n')


if __name__ == "__main__":
    _closed_loop_test()
