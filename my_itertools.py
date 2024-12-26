
def product(*args, repeat=1, nesting=False):
    # 计算重复的池（输入池扩展到 repeat 次）
    pools = [tuple(pool) * repeat for pool in args]
    pool_size = len(pools)
    # 每次生成组合，使用生成器返回
    indices = [0] * pool_size
    while True:
        # 生成并展平当前组合
        flat_product = []
        for i in range(pool_size):
            item = pools[i][indices[i]]
            if nesting:
                if any(isinstance(t, tuple) for t in item):
                    flat_product.extend(item)
                else:
                    flat_product.append(item)
            else:
                if isinstance(item, tuple):
                    flat_product.extend(item)
                else:
                    flat_product.append(item)
        yield tuple(flat_product)

        # 更新索引，模拟进位
        for i in reversed(range(len(indices))):
            indices[i] += 1
            if indices[i] == len(pools[i]):
                indices[i] = 0
            else:
                break
        else:
            break


def combinations(iterable, r):
    """
    indices 列表用来记录当前组合中元素的索引。初始时，它包含从 0 到 r-1 的索引。
    在每次生成一个组合后，通过修改 indices 来生成下一个组合，直到所有组合都被生成
    :param iterable: 初始元组
    :param r: 挑选的个数
    :return: 生成长度为r的组合(元组类型)
    """
    if r == 1:
        yield from iterable
        return
    n = len(iterable)

    # 如果 r > n，返回一个空的迭代器
    if r > n:
        return iter([])
    # 初始化 indices 为 [0, 1, 2, ..., r-1]
    indices = list(range(r))

    while True:
        yield tuple(iterable[i] for i in indices)
        # 从右往左检查是否可以增加索引
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return

        # 递增当前索引
        indices[i] += 1

        # 更新后续索引
        for j in range(i + 1, r):
            indices[j] = indices[j - 1] + 1
