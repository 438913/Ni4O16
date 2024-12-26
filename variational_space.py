from itertools import permutations, product, combinations
import parameters as pam
from energy_level import low_energy_dist

hole_num = pam.hole_num
# 各种原子轨道数
Ni_orbs = pam.Ni_orbs
O1_orbs = pam.O1_orbs
O2_orbs = pam.O2_orbs
O_orbs = pam.O_orbs
ap_orbs = pam.apO_orbs

# 各种原子位置
Ni_position = [(-1, 0, 1), (-1, 0, -1), (1, 0, -1), (1, 0, 1)]
O1_position = [(-2, 0, 1), (0, 0, 1), (2, 0, 1), (-2, 0, -1), (0, 0, -1), (2, 0, -1)]
O2_position = [(-1, 1, 1), (-1, -1, 1), (1, 1, 1), (1, -1, 1),
               (-1, 1, -1), (-1, -1, -1), (1, 1, -1), (1, -1, -1)]
O_position = O1_position + O2_position
Obilayer_position = [(-1, 0, 0), (1, 0, 0)]

# 10空穴类型, 用((Ni0_num, Ni1_num, Ni2_num, Ni3_num), Obilayer_num, O_num)表示
# 其中Obilayer_num和O_num只考虑一个位置最多只有一个空穴的情况


def create_lookup_tbl():
    """
    创建lookup_tbl，用于查找态所对应的索引
    :return: O_states: 只有一个空穴在O上的态, Ni_states: 只有一个空穴在Ni上的态
    states_one: 一个空穴的态, lookup_tbl: 排序过后的态列表, 包含多个空穴的所有态
    """
    def Ni_part(Ni_dist):
        """
        用来拼接4个Ni的空穴
        :return: 输出一个元组，包含4个Ni的空穴的态
        """
        Ni_orb_s = product(Ni_orbs, ['dn', 'up'])
        Ni_orb_s = tuple(Ni_orb_s)
        Ni0_part = []
        Ni1_part = []
        Ni2_part = []
        Ni3_part = []
        for i, Ni_num in enumerate(Ni_dist):
            position = Ni_position[i]
            if Ni_num == 0:
                continue
            for orb_s in combinations(Ni_orb_s, Ni_num):
                oneNi_hole = tuple((*position, orb, s) for orb, s in orb_s)
                if i == 0:
                    Ni0_part.append(oneNi_hole)
                elif i == 1:
                    Ni1_part.append(oneNi_hole)
                elif i == 2:
                    Ni2_part.append(oneNi_hole)
                else:
                    Ni3_part.append(oneNi_hole)
        Ni0_Ni1_Ni2_Ni3 = product(Ni0_part, Ni1_part, Ni2_part, Ni3_part)
        for Ni0_hole, Ni1_hole, Ni2_hole, Ni3_hole in Ni0_Ni1_Ni2_Ni3:
            yield Ni0_hole + Ni1_hole + Ni2_hole + Ni3_hole

    def apO_part(num):
        """
        用来拼接层间O的空穴
        :param num: 在层间O上的空穴数量
        :return:
        """
        assert num != 0, "num should not be 0"
        if num == 1:
            for position, orb, s in product(Obilayer_position, ap_orbs, ['dn', 'up']):
                yield *position, orb, s
        else:
            for orbs in product(ap_orbs, repeat=num):
                for ss in product(['dn', 'up'], repeat=num):
                    hole = []
                    for i in range(num):
                        position = Obilayer_position[i]
                        orb = orbs[i]
                        s = ss[i]
                        hole.append((*position, orb, s))
                    yield tuple(hole)

    def O_part(num):
        """
        用来拼接层内的空穴
        :param num: 在层内O上的空穴数量
        :return:
        """
        assert num != 0, "number should not be 0"
        assert num < 3, "could not compute the number"
        if num == 1:
            for position, orb, s in product(O1_position, O1_orbs,  ['dn', 'up']):
                yield *position, orb, s
            for position, orb, s in product(O2_position, O2_orbs, ['dn', 'up']):
                yield *position, orb, s
        elif num == 2:
            for positions in combinations(O1_position, num):
                for orbs in product(O1_orbs, repeat=num):
                    for ss in product(['dn', 'up'], repeat=num):
                        hole = []
                        for i in range(num):
                            position = positions[i]
                            orb = orbs[i]
                            s = ss[i]
                            hole.append((*position, orb, s))
                        yield tuple(hole)
            for positions in combinations(O2_position, num):
                for orbs in product(O2_orbs, repeat=num):
                    for ss in product(['dn', 'up'], repeat=num):
                        hole = []
                        for i in range(num):
                            position = positions[i]
                            orb = orbs[i]
                            s = ss[i]
                            hole.append((*position, orb, s))
                        yield tuple(hole)
            for positions in product(O1_position, O2_position):
                for orbs in product(O1_orbs, O2_orbs):
                    for ss in product(['dn', 'up'], repeat=num):
                        hole = []
                        for i in range(num):
                            position = positions[i]
                            orb = orbs[i]
                            s = ss[i]
                            hole.append((*position, orb, s))
                        yield tuple(hole)

    # 输出所有的态
    states = []
    for hole_type in low_energy_dist:
        Ni_dist_set, apO_num, O_num = hole_type
        Ni_dist_set = permutations(Ni_dist_set)
        Ni_dist_set = set(Ni_dist_set)
        for Ni_dist in Ni_dist_set:
            if apO_num == 0 and O_num == 0:
                for Ni_hole in Ni_part(Ni_dist):
                    # print(Ni_hole)
                    states.append(Ni_hole)
            elif apO_num != 0 and O_num == 0:
                for Ni_hole in Ni_part(Ni_dist):
                    for apO_hole in apO_part(apO_num):
                        # print(Ni_hole + apO_hole)
                        states.append(Ni_hole + apO_hole)
            elif apO_num == 0 and O_num != 0:
                for Ni_hole in Ni_part(Ni_dist):
                    for O_hole in O_part(O_num):
                        # print(Ni_hole + O_hole)
                        states.append(Ni_hole + O_hole)
            else:
                for Ni_hole in Ni_part(Ni_dist):
                    for apO_hole in apO_part(apO_num):
                        for O_hole in O_part(O_num):
                            # print(Ni_hole + apO_hole + O_hole)
                            states.append(Ni_hole + apO_hole + O_hole)
    print(len(states))


create_lookup_tbl()
