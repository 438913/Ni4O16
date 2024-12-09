from itertools import product
import parameters as pam

A = pam.A
Uoo = pam.Uoo
Upp = pam.Upp
ep = pam.eps[0]
eo = pam.eos[0]

energy_max = 7.0


def get_energy(Ni_dist_, Obilayer_dist_, O_dist_):
    energy_ = 0.0
    for n in Ni_dist_:
        energy_ += abs(n - 2) * A / 2.0
    energy_ += O_num_ * eo
    energy_ += L_num_ * ep
    return energy_


type_energy = []
Ni_dist_list = product([0, 1, 2, 3], repeat=4)
Obilayer_dist_list = list(product([0, 1, 2], repeat=2))
O_dist_list = list(product([0, 1, 2, 3], repeat=3))
for Ni_dist in Ni_dist_list:
    for Obilayer_dist in Obilayer_dist_list:
        for O_dist in O_dist_list:
            num = sum(Ni_dist) + sum(Obilayer_dist) + sum(O_dist)
            if num == 10:
                energy = get_energy(Ni_dist, Obilayer_dist, O_dist)
                hole_type = (Ni_num, O_num, L_num, energy)
                type_energy.append(hole_type)
type_energy.sort(key=lambda x: x[-1])
idx_max = 0
for hole_type in type_energy:
    if hole_type[-1] > energy_max:
        break
    idx_max += 1
type_energy_limit = type_energy[:idx_max]
for hole_type in type_energy_limit:
    print(hole_type)
