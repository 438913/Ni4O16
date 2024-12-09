import parameters as pam
import energy

type_range = energy.type_energy_limit

hole_num = pam.hole_num
# 各种原子轨道数
Ni_orbs = pam.Ni_orbs
O1_orbs = pam.O1_orbs
O2_orbs = pam.O2_orbs
Obilayer_orbs = pam.Obilayer_orbs

# 各种原子位置
Ni_position = [(-1, 0, 1), (-1, 0, -1), (1, 0, -1), (1, 0, 1)]
O1_position = [(-2, 0, 1), (0, 0, 1), (2, 0, 1), (-2, 0, -1), (0, 0, -1), (2, 0, -1)]
O2_position = [(-1, 1, 1), (-1, -1, 1), (1, 1, 1), (1, -1, 1),
               (-1, 1, -1), (-1, -1, -1), (1, 1, -1), (1, -1, -1)]
Obilayer_position = [(-1, 0, 0), (1, 0, 0)]


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


def create_lookup_tbl():
    """
    创建lookup_tbl，用于查找态所对应的索引
    :return: O_states: 只有一个空穴在O上的态, Ni_states: 只有一个空穴在Ni上的态
    states_one: 一个空穴的态, lookup_tbl: 排序过后的态列表, 包含多个空穴的所有态
    """
    Ni_hole = {}
    for i in range(len(Ni_position)):
        position = Ni_position[i]
        hole = product((position,), Ni_orbs, ['up', 'dn'])
        Ni_hole[i] = list(hole)

    O1_hole = product(O1_position, O1_orbs, ['up', 'dn'])
    O2_hole = product(O2_position, O2_orbs, ['up', 'dn'])
    O_hole = list(O1_hole) + list(O2_hole)

    Obilayer_hole = product(Obilayer_position, Obilayer_orbs, ['up', 'dn'])
    Obilayer_hole = list(Obilayer_hole)

    state_list = []
    for type_range_ in type_range:
        Ni_num = type_range_[0]
        Obilayer_num = type_range_[1]
        O_num = type_range_[2]
        multi_hole = {}
        for i, num in enumerate(Ni_num):
            multi_hole[f'Ni{i}'] = combinations(Ni_hole[i], num)
        if O_num != 0:
            multi_hole['O'] = combinations(O_hole, O_num)
        if Obilayer_num != 0:
            multi_hole['Obilayer'] = combinations(Obilayer_hole, Obilayer_num)
        multi_hole = product(*multi_hole.values(), nesting=True)
        multi_hole = list(multi_hole)
        state_list.extend(multi_hole)
    dim = len(state_list)
    print(dim)
    for hole in state_list:
        print(hole)


create_lookup_tbl()
