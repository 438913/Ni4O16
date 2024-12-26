from itertools import product, combinations
from itertools import combinations_with_replacement as cwr
import numpy as np
import parameters as pam

# 导入参数
A = pam.A
Uoo = pam.Uoo
Upp = pam.Upp
# 采用0GPa下的参数
ep = pam.eps[0]
eo = pam.eos[0]
# 限制能量的最大值
energy_max = 7


def get_energy(Ni_dist_, apO_dist, O_dist_):
    """
    估算这个态的大致能量(没有hopping时的能量)
    :param Ni_dist_: 四个Ni的数量分布情况
    :param apO_dist: 层间O的数量分布情况
    :param O_dist_: 层内O的数量分布情况
    :return: 返回能量
    """
    energy_ = 0.0
    # d8 = 0, d9和d10拉高 A/2, d7拉高 A/2 * 2(这边d8表示的Ni的数量n = 10 - 8)
    for n in Ni_dist_:
        energy_ += A / 2.0 * abs(n - 2)
    for n in apO_dist:
        energy_ += eo * n
        if n > 1:
            energy_ += Uoo * n * (n - 1) / 2.0
    for n in O_dist_:
        energy_ += ep * n
        if n > 1:
            energy_ += Upp * n * (n - 1) / 2.0
    return energy_


hole_type_list = []
energy_list = []

# 列出所有可能Ni的数量分布: (Ni0_num, Ni1_num, N2_num, Ni3_num),
# 依次表示Ni0, Ni1, Ni2, Ni3的数量
for Ni_dist in cwr([0, 1, 2, 3], 4):
    if sum(Ni_dist) > 10:
        continue
    # 层间O的数量分布
    for apO_dist in cwr([0, 1, 2], 2):
        if sum(Ni_dist) + sum(apO_dist) > 10:
            continue
        # 层内O的数量分布, 由于3个位置以上或者在同一个位置时O的数量在3个以上时,
        # 能量很高, 所以只考虑3个位置, 以及同一个位置数量最多到3的情况
        for O_dist in cwr([0, 1, 2, 3], 3):
            num = sum(Ni_dist) + sum(apO_dist) + sum(O_dist)
            if num == 10:
                energy = get_energy(Ni_dist, apO_dist, O_dist)
                hole_type = (Ni_dist, apO_dist, O_dist)
                hole_type_list.append(hole_type)
                energy_list.append(energy)

sorted_idx = np.argsort(energy_list)
hole_type_list = [hole_type_list[i] for i in sorted_idx]
energy_list = [energy_list[i] for i in sorted_idx]
idx_max = 0

for energy in energy_list:
    if energy > energy_max:
        break
    idx_max += 1
low_energy_hole = hole_type_list[:idx_max]

# for i, hole_type in enumerate(low_energy_hole):
#     energy = energy_list[i]
#     print(hole_type, energy)

low_energy_dist = []
for i, hole_type in enumerate(low_energy_hole):
    apO_num = sum(hole_type[1])
    O_num = sum(hole_type[2])
    hole_type_dist = (hole_type[0], apO_num, O_num)
    if hole_type_dist not in low_energy_dist:
        low_energy_dist.append(hole_type_dist)
        print(hole_type_dist, ': ', energy_list[i], 'eV')