from itertools import permutations, product, combinations
from bisect import bisect_left
import parameters as pam
from energy_level import low_energy_dist
# low_energy_dist类型, 用((Ni0_num, Ni1_num, Ni2_num, Ni3_num), apO_num, O_num)表示
# 其中apO_num和O_num只考虑一个位置最多只有一个空穴的情况

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
apO_position = [(-1, 0, 0), (1, 0, 0)]

# 所有原子位置的元组，用来查找索引
position_tuple = Ni_position + O_position + apO_position
position_tuple = sorted(position_tuple)
position_tuple = tuple(position_tuple)
# 轨道索引
orb_int = {'d3z2r2': 0,
           'dx2y2': 1,
           'px': 2,
           'py': 3,
           'apz': 4}
int_orb = {0: 'd3z2r2',
           1: 'dx2y2',
           2: 'px',
           3: 'py',
           4: 'apz'}


class VariationalSpace:
    """
    定义变分空间类
    包含get_uid, get_state, create_lookup_tbl, gei_index四个函数
    """

    def __init__(self):
        self.low_energy_tbl = self.create_low_energy_tbl()
        # self.dim = len(self.lookup_tbl)
        # print(f"Variational space dimension: {self.dim}")

    def get_uid(self, multi_hole, if_inversion=False, if_Sz=False):
        """
        获取空穴类型对应的uid
        :param multi_hole: 空穴
        :param if_inversion: 是否输出逆序数
        :param if_Sz:是否输出Sz
        :return: uid
        """
        hole_uid_list = []
        b1 = len(position_tuple)
        b2 = b1 * len(orb_int)
        b3 = b2 * 2
        Sz = 0
        for hole in multi_hole:
            x, y, z, orb, s = hole
            position = (x, y, z)
            position_uid = bisect_left(position_tuple, position)
            orb_uid = orb_int[orb]
            s_uid = 1 if s == 'up' else 0
            Sz += 0.5 if s == 'up' else -0.5
            hole_uid = position_uid + orb_uid * b1 + s_uid * b2
            hole_uid_list.append(hole_uid)
        inversion = 0
        uid_num = len(hole_uid_list)
        if if_inversion:
            for i in range(1, uid_num):
                behind_uid = hole_uid_list[i]
                for front_uid in hole_uid_list[: i]:
                    if front_uid > behind_uid:
                        inversion += 1
        sorted_idx = sorted(range(uid_num), key=lambda idx: hole_uid_list[idx])
        multi_hole = [multi_hole[idx] for idx in sorted_idx]
        multi_hole = tuple(multi_hole)
        hole_uid_list.sort()
        uid = 0
        for i, hole_uid in enumerate(hole_uid_list):
            uid += hole_uid * b3 ** i
        assert multi_hole == self.get_state(uid), "uid is not correct"
        if if_inversion:
            if if_Sz:
                return uid, inversion, Sz
            else:
                return uid, inversion
        else:
            if if_Sz:
                return uid, Sz
            else:
                return uid

    def get_state(self, uid):
        """
        根据uid获取态
        :param uid:
        :return:
        """
        b1 = len(position_tuple)
        b2 = len(orb_int)
        b3 = b1 * b2 * 2
        multi_hole = []
        while uid:
            hole_uid = uid % b3
            position = position_tuple[hole_uid % b1]
            hole_uid //= b1
            orb = int_orb[hole_uid % b2]
            hole_uid //= b2
            s = 'up' if hole_uid % 2 == 1 else 'dn'
            hole = (*position, orb, s)
            multi_hole.append(hole)
            uid //= b3
        return tuple(multi_hole)

    def create_low_energy_tbl(self):
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
                for position, orb, s in product(apO_position, ap_orbs, ['dn', 'up']):
                    yield (*position, orb, s),
            else:
                for orbs in product(ap_orbs, repeat=num):
                    for ss in product(['dn', 'up'], repeat=num):
                        hole = []
                        for i in range(num):
                            position = apO_position[i]
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
                for position, orb, s in product(O1_position, O1_orbs, ['dn', 'up']):
                    yield (*position, orb, s),
                for position, orb, s in product(O2_position, O2_orbs, ['dn', 'up']):
                    yield (*position, orb, s),
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
        low_energy_tbl = []
        for hole_type in low_energy_dist:
            Ni_dist_set, apO_num, O_num = hole_type
            Ni_dist_set = permutations(Ni_dist_set)
            Ni_dist_set = set(Ni_dist_set)
            for Ni_dist in Ni_dist_set:
                if apO_num == 0 and O_num == 0:
                    for Ni_hole in Ni_part(Ni_dist):
                        uid, Sz = self.get_uid(Ni_hole, if_Sz=True)
                        low_energy_tbl.append(uid)
                elif apO_num != 0 and O_num == 0:
                    for Ni_hole in Ni_part(Ni_dist):
                        for apO_hole in apO_part(apO_num):
                            uid, Sz = self.get_uid(Ni_hole + apO_hole, if_Sz=True)
                            low_energy_tbl.append(uid)
                elif apO_num == 0 and O_num != 0:
                    for Ni_hole in Ni_part(Ni_dist):
                        for O_hole in O_part(O_num):
                            uid, Sz = self.get_uid(Ni_hole + O_hole, if_Sz=True)
                            low_energy_tbl.append(uid)
                else:
                    for Ni_hole in Ni_part(Ni_dist):
                        for apO_hole in apO_part(apO_num):
                            for O_hole in O_part(O_num):
                                uid, Sz = self.get_uid(Ni_hole + apO_hole + O_hole, if_Sz=True)
                                low_energy_tbl.append(uid)
        return low_energy_tbl

    def create_tpd_tbl(self):
        """
        为通过d轨道向p轨道跃迁得到的态建立一个列表
        :return:
        """
        low_energy_tbl = self.low_energy_tbl
        dim = len(low_energy_tbl)
        for i in range(dim):
            uid = low_energy_tbl[i]
            multi_hole = self.get_state(uid)
            for x, y, z, orb, s in multi_hole:



    # def get_index(self, uid):
    #     """
    #     根据uid获取索引
    #     :param uid:
    #     :return:
    #     """
    #     lookup_tbl = self.lookup_tbl
    #     if uid > lookup_tbl[-1] or uid < lookup_tbl[0]:
    #         return None
    #     index = bisect_left(lookup_tbl, uid)
    #     if lookup_tbl[index] == uid:
    #         return index
    #     else:
    #         return None
vs = VariationalSpace()
vs.create_tpd_tbl()
