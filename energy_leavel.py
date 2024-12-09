import matplotlib.pyplot as plt
from brokenaxes import brokenaxes
from itertools import combinations_with_replacement as cwr
ep = 2.47
eo = 2.94
Uoo = 4.0
Upp = 4.0
A = 6.0


def get_energy(Ni_num_, O_num_, L_num_):
    energy_ = 0.0
    for n in Ni_num_:
        energy_ += abs(n - 2) * A / 2.0
    for n in O_num_:
        energy_ += n * eo
        if n > 1:
            energy_ += Uoo
    for n in L_num_:
        energy_ += n * ep
        if n > 1:
            energy_ += Upp
    return energy_


def get_hole_type(Ni_num_, O_num_, L_num_):
    hole_type_ = (Ni_num_, O_num_, L_num_)
    return hole_type_


type_energys = []
Ni_num_list = cwr(range(4), 4)
O_num_list = list(cwr([0, 1, 2], 2))
L_num_list = list(cwr([0, 1, 2, 3], 3))
for Ni_num in Ni_num_list:
    for O_num in O_num_list:
        for L_num in L_num_list:
            num = sum(Ni_num) + sum(O_num) + sum(L_num)
            if num != 10:
                continue
            energy = get_energy(Ni_num, O_num, L_num)
            hole_type = get_hole_type(Ni_num, O_num, L_num)
            type_energys.append((hole_type, energy))
type_energys.sort(key=lambda type_energy: type_energy[1])

for hole_type, energy in type_energys:
    print(f'{hole_type}: {energy}')
fig = plt.figure()
bax = brokenaxes(ylims=((4.5, 6.1), (8.5, 12.01)), hspace=0.03)
x = [2, 1, 0, 3, 4, 5, 2, 2, 2, 1, 0, 3, 4, 5, 2, 1, 0]
energy_list = [4.94, 5.41, 5.47, 5.88, 5.94]
dim = len(type_energys)
for i in range(dim):
    hole_type, energy = type_energys[i]
    if energy == type_energys[i - 1][1]:
        continue
    if energy > 11.95:
        break
    bax.plot([x[i], x[i] + 0.9], [energy, energy], 'k-')
# bax.set_xlim([-0.1, 6])
bax.set_ylabel('E(eV)', fontsize=14)
bax.tick_params(axis='x', which='both', length=0, labelbottom=False)
fig.show()
