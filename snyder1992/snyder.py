from snyder1992.structures import Angle, PolyhedronFace
import math

TABLE_1 = {'truncated icosahedron': {'hexagon':  {'g': Angle(23.80018260),
                                                  'G': Angle(62.15468023),
                                                  'theta': Angle(60.0)},
                                     'pentagon': {'g': Angle(20.07675127),
                                                  'G': Angle(55.69063953),
                                                  'theta': Angle(54.0)}
                                     },
           'tetrahedron':  {'g': Angle(70.52877937), 'G': Angle(60.0),
                            'theta': Angle(30.0)},
           'cube':         {'g': Angle(54.73561032), 'G': Angle(60.0),
                            'theta': Angle(45.0)},
           'octahedron':   {'g': Angle(54.73561032), 'G': Angle(45.0),
                            'theta': Angle(30.0)},
           'dodecahedron': {'g': Angle(37.37736814),  'G': Angle(60.0),
                            'theta': Angle(54.0)},
           'icosahedron':  {'g': Angle(37.3773614),  'G': Angle(36.0),
                            'theta': Angle(30.0)}}


def r_prime(theta, sG, g, R):
    AGT = ((90.0 - theta.degrees) + 90.0 + sG.degrees - 180) * math.pi * R ** 2 / 180.0
    R_prime = math.sqrt(AGT / ((1 / 2.0) * math.tan(g.radians) ** 2 * math.sin(
        theta.radians) * math.cos(theta.radians)))
    return R_prime


def table_2(R):

    def A(g):
        a = 90.0
        b = 2 * math.degrees(math.atan(math.tan(g) * math.cos(math.radians(36.0))))
        return Angle(a-b)

    def E(g):
        return Angle(90.0-g)

    R_primes = {}
    for polyhedron in TABLE_1:
        if polyhedron == 'truncated icosahedron':
            for face in ['hexagon', 'pentagon']:
                values = TABLE_1[polyhedron][face]
                g = values['g']
                sG = values['G']
                theta = values['theta']
                R_primes[face] = r_prime(theta, sG, g, R)
        else:
            values = TABLE_1[polyhedron]
            g = values['g']
            sG = values['G']
            theta = values['theta']
            R_primes[polyhedron] = r_prime(theta, sG, g, R)

    A_dodecahedron = A(TABLE_1['dodecahedron']['g'].radians)
    A_truncated_pentagon = A(TABLE_1['truncated icosahedron']['pentagon']['g'].radians)
    B = 0.726542528 * R_primes['dodecahedron']
    C = 1.736067977 * R_primes['dodecahedron']
    D = 0.5 * R_primes['dodecahedron']
    E_icosahedron = E(TABLE_1['icosahedron']['g'])
    E_truncated_hexagon = E(TABLE_1['truncated icosahedron']['hexagon']['g'])
    F = 10.81231696
    G = 0.6615845383 * R_primes['icosahedron']
    H = 0.1909830056 * R_primes['icosahedron']
    J_truncated_pentagon = 0.4167683948 * R_primes['pentagon']
    J_truncated_hexagon = 0.4167683948 * R_primes['hexagon']
    K_truncated_pentagon = 0.1804660087 * R_primes['pentagon']
    K_truncated_hexagon = 0.1804660087 * R_primes['hexagon']
    L_truncated_pentagon = 0.2868162417 * R_primes['pentagon']
    L_truncated_hexagon = 0.2868162417 * R_primes['hexagon']


    table_2 = {'dodecahedron': [PolyhedronFace(1,                90,      0,    0,  C, 'pentagon'),
                                PolyhedronFace(2,    A_dodecahedron, -144.0, -4*B,  D, 'pentagon'),
                                PolyhedronFace(3,    A_dodecahedron,  -72.0, -2*B,  D, 'pentagon'),
                                PolyhedronFace(4,    A_dodecahedron,    0.0,    0,  D, 'pentagon'),
                                PolyhedronFace(5,    A_dodecahedron,   72.0,  2*B,  D, 'pentagon'),
                                PolyhedronFace(6,    A_dodecahedron,  144.0,  4*B,  D, 'pentagon'),
                                PolyhedronFace(7,   -A_dodecahedron, -108.0, -3*B, -D, 'pentagon'),
                                PolyhedronFace(8,   -A_dodecahedron,  -36.0,   -B, -D, 'pentagon'),
                                PolyhedronFace(9,   -A_dodecahedron,   36.0,    B, -D, 'pentagon'),
                                PolyhedronFace(10,  -A_dodecahedron,  108.0,  3*B, -D, 'pentagon'),
                                PolyhedronFace(11,  -A_dodecahedron,  180.0,  5*B, -D, 'pentagon'),
                                PolyhedronFace(12,              -90,  -36.0,   -B, -C, 'pentagon')
                                ],
                'icosahedron': [PolyhedronFace(1,   E_icosahedron, -144.0, -4*G,  5*H, 'triangle'),
                                PolyhedronFace(2,   E_icosahedron,  -72.0, -2*G,  5*H, 'triangle'),
                                PolyhedronFace(3,   E_icosahedron,    0.0,    0,  5*H, 'triangle'),
                                PolyhedronFace(4,   E_icosahedron,   72.0,  2*G,  5*H, 'triangle'),
                                PolyhedronFace(5,   E_icosahedron,  144.0,  4*G,  5*H, 'triangle'),
                                PolyhedronFace(6,               F, -144.0, -4*G,    H, 'triangle'),
                                PolyhedronFace(7,               F,  -72.0, -2*G,    H, 'triangle'),
                                PolyhedronFace(8,               F,      0,    0,    H, 'triangle'),
                                PolyhedronFace(9,               F,   72.0,  2*G,    H, 'triangle'),
                                PolyhedronFace(10,              F,  144.0,  4*G,    H, 'triangle'),
                                PolyhedronFace(11,             -F, -108.0, -3*G,   -H, 'triangle'),
                                PolyhedronFace(12,             -F,  -36.0,   -G,   -H, 'triangle'),
                                PolyhedronFace(13,             -F,   36.0,    G,   -H, 'triangle'),
                                PolyhedronFace(14,             -F,  108.0,  3*G,   -H, 'triangle'),
                                PolyhedronFace(15,             -F,  180.0,  5*G,   -H, 'triangle'),
                                PolyhedronFace(16, -E_icosahedron, -108.0, -3*G, -5*H, 'triangle'),
                                PolyhedronFace(17, -E_icosahedron,  -36.0,   -G, -5*H, 'triangle'),
                                PolyhedronFace(18, -E_icosahedron,   36.0,    G, -5*H, 'triangle'),
                                PolyhedronFace(19, -E_icosahedron,  108.0,  3*G, -5*H, 'triangle'),
                                PolyhedronFace(20, -E_icosahedron,  180.0,  5*G, -5*H, 'triangle'),
                                ],
                'truncated icosahedron': [PolyhedronFace(1,   90,      0,      0,  7*K_truncated_pentagon+L_truncated_pentagon, 'pentagon'),
                                          PolyhedronFace(2,    E_truncated_hexagon, -144.0,   -6*J_truncated_hexagon,    5*K_truncated_hexagon, 'hexagon'),
                                          PolyhedronFace(3,    E_truncated_hexagon,  -72.0,   -3*J_truncated_hexagon,    5*K_truncated_hexagon, 'hexagon'),
                                          PolyhedronFace(4,    E_truncated_hexagon,    0.0,      0,    5*K_truncated_hexagon, 'hexagon'),
                                          PolyhedronFace(5,    E_truncated_hexagon,   72.0,    3*J_truncated_hexagon,    5*K_truncated_hexagon, 'hexagon'),
                                          PolyhedronFace(6,    E_truncated_hexagon,  144.0,    6*J_truncated_hexagon,    5*K_truncated_hexagon, 'hexagon'),
                                          PolyhedronFace(7,    A_truncated_pentagon, -180.0, -7.5*J_truncated_pentagon,    K_truncated_pentagon+L_truncated_pentagon, 'pentagon'),
                                          PolyhedronFace(8,    A_truncated_pentagon, -108.0, -4.5*J_truncated_pentagon,    K_truncated_pentagon+L_truncated_pentagon, 'pentagon'),
                                          PolyhedronFace(9,    A_truncated_pentagon,  -36.0, -1.5*J_truncated_pentagon,    K_truncated_pentagon+L_truncated_pentagon, 'pentagon'),
                                          PolyhedronFace(10,   A_truncated_pentagon,   36.0,  1.5*J_truncated_pentagon,    K_truncated_pentagon+L_truncated_pentagon, 'pentagon'),
                                          PolyhedronFace(11,   A_truncated_pentagon,  108.0,  4.5*J_truncated_pentagon,    K_truncated_pentagon+L_truncated_pentagon, 'pentagon'),
                                          PolyhedronFace(12,   F, -144.0,   -6*J_truncated_hexagon,      K_truncated_hexagon, 'hexagon'),
                                          PolyhedronFace(13,   F,  -72.0,   -3*J_truncated_hexagon,      K_truncated_hexagon, 'hexagon'),
                                          PolyhedronFace(14,   F,    0.0,      0,      K_truncated_hexagon, 'hexagon'),
                                          PolyhedronFace(15,   F,   72.0,    3*J_truncated_hexagon,      K_truncated_hexagon, 'hexagon'),
                                          PolyhedronFace(16,   F,  144.0,    6*J_truncated_hexagon,      K_truncated_hexagon, 'hexagon'),
                                          PolyhedronFace(17,  -F,  180.0, -7.5*J_truncated_hexagon,     -K_truncated_hexagon, 'hexagon'),
                                          PolyhedronFace(18,  -F, -108.0, -4.5*J_truncated_hexagon,     -K_truncated_hexagon, 'hexagon'),
                                          PolyhedronFace(19,  -F,  -36.0, -1.5*J_truncated_hexagon,     -K_truncated_hexagon, 'hexagon'),
                                          PolyhedronFace(20,  -F,     36,  1.5*J_truncated_hexagon,     -K_truncated_hexagon, 'hexagon'),
                                          PolyhedronFace(21,  -F,    108,  4.5*J_truncated_hexagon,     -K_truncated_hexagon, 'hexagon'),
                                          PolyhedronFace(22,  -A_truncated_pentagon,   -144,   -6*J_truncated_pentagon,   -K_truncated_pentagon-L_truncated_pentagon, 'pentagon'),
                                          PolyhedronFace(23,  -A_truncated_pentagon,    -72,   -3*J_truncated_pentagon,   -K_truncated_pentagon-L_truncated_pentagon, 'pentagon'),
                                          PolyhedronFace(24,  -A_truncated_pentagon,      0,      0,   -K_truncated_pentagon-L_truncated_pentagon, 'pentagon'),
                                          PolyhedronFace(25,  -A_truncated_pentagon,     72,    3*J_truncated_pentagon,   -K_truncated_pentagon-L_truncated_pentagon, 'pentagon'),
                                          PolyhedronFace(26,  -A_truncated_pentagon,    144,    6*J_truncated_pentagon,   -K_truncated_pentagon-L_truncated_pentagon, 'pentagon'),
                                          PolyhedronFace(27,  -E_truncated_hexagon,    180, -7.5*J_truncated_hexagon,   -5*K_truncated_hexagon, 'hexagon'),
                                          PolyhedronFace(28,  -E_truncated_hexagon,   -108, -4.5*J_truncated_hexagon,   -5*K_truncated_hexagon, 'hexagon'),
                                          PolyhedronFace(29,  -E_truncated_hexagon,    -36, -1.5*J_truncated_hexagon,   -5*K_truncated_hexagon, 'hexagon'),
                                          PolyhedronFace(30,  -E_truncated_hexagon,     36,  1.5*J_truncated_hexagon,   -5*K_truncated_hexagon, 'hexagon'),
                                          PolyhedronFace(31,  -E_truncated_hexagon,    108,  4.5*J_truncated_hexagon,   -5*K_truncated_hexagon, 'hexagon'),
                                          PolyhedronFace(32, -90,    -36, -1.5*J_truncated_pentagon, -7*K_truncated_pentagon-L_truncated_pentagon, 'pentagon')
                                          ]
               }

    return table_2
