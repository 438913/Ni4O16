Mc = 1
hole_num = 10
# 如果Sz_set中包含'All_states'，则包含所有自旋的情况
# 4holes: 0, 1, 2; 5holes: 0.5, 1.5, 2.5; 6holes: 0, 1, 2, 3
Sz_set = ['All_states']
A = 6.0
B = 0.15
C = 0.58
Uoo = 4.0
Upp = 4.0
pressures = [0, 4, 8, 16, 29.5]
# 在这里, 用列表[value1, value2, value3, value4, value5]分别表示
# 在0GPa, 4GPa, 8GPa, 16GPa, 29.5GPa下的参数
eds = {'d3z2r2': [0.046, 0.054, 0.060, 0.072, 0.095],
       'dx2y2': [0.0 for _ in range(5)],
       'dxy': [0.823, 0.879, 0.920, 0.997, 1.06],
       'dxz': [0.706, 0.761, 0.804, 0.887, 0.94],
       'dyz': [0.706, 0.761, 0.804, 0.887, 0.94]}
eps = [2.47, 2.56, 2.62, 2.75, 2.9]
eos = [2.94, 3.03, 3.02, 3.14, 3.24]
tpds = [1.38, 1.43, 1.46, 1.52, 1.58]
tpps = [0.537, 0.548, 0.554, 0.566, 0.562]
tdos = [1.48, 1.53, 1.55, 1.61, 1.66]
tpos = [0.445, 0.458, 0.468, 0.484, 0.487]
Norb = 4
if Norb == 4:
    O1_orbs = ['px']
    O2_orbs = ['py']
    apO_orbs = ['apz']
    O_orbs = O1_orbs + O2_orbs
    Ni_orbs = ['d3z2r2', 'dx2y2']
num_vals = 10
