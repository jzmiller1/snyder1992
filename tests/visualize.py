from matplotlib import pyplot as plt
from tests import data

from snyder1992.sea import sea
from snyder1992.structures import Angle
BENIN_ICO = [sea(Angle(lat), Angle(long), 'icosahedron') for lat, long in data.BENIN]
B_x = [x for x, y in BENIN_ICO]
B_y = [y for x, y in BENIN_ICO]
SWISS_ICO = [sea(Angle(lat), Angle(long), 'icosahedron') for lat, long in data.SWITZERLAND]
S_x = [x for x, y in SWISS_ICO]
S_y = [y for x, y in SWISS_ICO]


plt.plot(B_x, B_y, 'go')
plt.plot(S_x, S_y, 'yo')
plt.gca().set_aspect('equal', adjustable='box')

plt.show()
