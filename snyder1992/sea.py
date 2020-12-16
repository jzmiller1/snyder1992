import math
from snyder1992.structures import Angle
from snyder1992.snyder import TABLE_1, table_2, r_prime


def get_z_and_Az(lat, long, lat_center, long_center):
    """return z and Az

    all inputs are Angle

    """
    # step 1 Snyder page 13
    z = math.acos(math.sin(lat_center.radians) * math.sin(lat.radians) +
                  math.cos(lat_center.radians) * math.cos(lat.radians) * math.cos(
        long.radians - long_center.radians)
                  )

    y = math.cos(lat.radians) * math.sin(long.radians - long_center.radians)
    x_a = math.cos(lat_center.radians) * math.sin(lat.radians)
    x_b = math.sin(lat_center.radians) * math.cos(lat.radians) * math.cos(long.radians - long_center.radians)
    x = x_a - x_b
    Az = Angle(math.degrees(math.atan2(y, x)))
    return z, Az


def adjust_Az(Az, az_adjust_angle):
    # step 2 Synder page 13
    Az_adjust_counter = 0
    while Az < 0.0:
        Az += az_adjust_angle
        Az_adjust_counter -= 1
    while Az > az_adjust_angle:
        Az -= az_adjust_angle
        Az_adjust_counter += 1
    # += and -= override my Angle subclass to a float, this sets it back for access to .degrees and .radians
    Az = Angle(Az)
    return Az, Az_adjust_counter


def get_q(g, Az, cot_theta):
    # step 3 Synder page 13
    q = math.atan(math.tan(g.radians) / (
            math.cos(Az.radians) + math.sin(Az.radians) * cot_theta))
    q = Angle(math.degrees(q))

    # Synder -vs- PROJ
    # in the proj implementation atan2 is used
    # in the Snyder formula it is atan
    # using atan2 clear up returning None for points like 10.81231696, 1
    alt_q = math.atan2(math.tan(g.radians),
                       math.cos(Az.radians) + math.sin(Az.radians) * cot_theta
                       )
    return alt_q


def the_rest(g, sG, theta, cot_theta, az_adjust_angle, R, Az, q, z, Az_adjust_counter, K=1):
    # step 4 Synder page 13
    # Snyder equation showing R_prime used Truncated Icoshedron g
    # this should be dynamically set based on the polyhedron used
    R_prime = r_prime(theta, sG, g, R)

    # eqn 6 (get H)
    a = math.sin(Az.radians) * math.sin(sG.radians) * math.cos(g.radians)
    b = math.cos(Az.radians) * math.cos(sG.radians)
    H = math.acos(a - b)
    H = Angle(math.degrees(H))

    # eqn 7 (get A sub G)
    # K adjusts for pentagon (Snyder pg 15)
    A_sub_G = (Az.degrees + sG.degrees + H.degrees - 180) * math.pi * R ** 2 / 180.0

    # eqn 8
    # K adjusts for pentagon (Snyder pg 15)
    y = 2.0 * A_sub_G * K
    x = R_prime ** 2 * math.tan(g.radians) ** 2.0 - 2.0 * K * A_sub_G * cot_theta
    Az_prime = Angle(math.degrees(math.atan2(y, x)))

    # eqn 10
    top = math.tan(g.radians)
    bottom = math.cos(Az_prime.radians) + math.sin(Az_prime.radians) * cot_theta
    d_prime = R_prime * top / bottom

    # eqn 11
    f = d_prime / (2.0 * R_prime * math.sin(q / 2.0))

    # eqn 12
    rho = 2.0 * R_prime * f * math.sin(z / 2.0)

    Az_adjuster = Angle(Az_adjust_counter * az_adjust_angle)
    adjusted_Az_prime = Az_prime.radians + Az_adjuster.radians
    x = rho * math.sin(adjusted_Az_prime)
    y = rho * math.cos(adjusted_Az_prime)

    return x, y


def sea(lat, long, polyhedron, R=6378137.0):
    lat = Angle(lat)
    long = Angle(long)
    TABLE_2 = table_2(R)
    for face in TABLE_2[polyhedron]:
        if polyhedron == 'truncated icosahedron':
            values = TABLE_1[polyhedron][face.polygon]
        else:
            values = TABLE_1[polyhedron]

        g = values['g']
        sG = values['G']
        theta = values['theta']
        cot_theta = 1.0 / math.tan(theta.radians)
        lat_center = Angle(face.center_lat)
        long_center = Angle(face.center_long)

        if face.polygon == 'triangle':
            az_adjust_angle = 120.0
            z, Az = get_z_and_Az(lat, long, lat_center, long_center)

            # "if z exceeds g, the point is too far from the center ...
            # and is located on another polygon"
            if z > g.radians:
                continue

            Az, Az_adjust_counter = adjust_Az(Az, az_adjust_angle)

            q = get_q(g, Az, cot_theta)
            # "if z exceeds q, it will not fit on this polygon
            # and is located on another one"
            if z > q:
                continue
            x, y = the_rest(g, sG, theta, cot_theta, az_adjust_angle, R, Az, q, z, Az_adjust_counter)
            # translate to proper origin
            x = face.center_x + x
            y = face.center_y + y
            return x, y
        elif face.polygon == 'hexagon':
            az_adjust_angle = 60.0
            z, Az = get_z_and_Az(lat, long, lat_center, long_center)

            # "if z exceeds g, the point is too far from the center ...
            # and is located on another polygon"
            if z > g.radians:
                continue

            Az, Az_adjust_counter = adjust_Az(Az, az_adjust_angle)

            q = get_q(g, Az, cot_theta)
            # "if z exceeds q, it will not fit on this polygon
            # and is located on another one"
            if z > q:
                continue
            x, y = the_rest(g, sG, theta, cot_theta, az_adjust_angle, R, Az, q, z, Az_adjust_counter)
            # translate to proper origin
            x = face.center_x + x
            y = face.center_y + y
            return x, y
        elif face.polygon == 'pentagon':
            az_adjust_angle = 72.0
            z, Az = get_z_and_Az(lat, long, lat_center, long_center)

            # "if z exceeds g, the point is too far from the center ...
            # and is located on another polygon"
            if z > g.radians:
                continue

            Az, Az_adjust_counter = adjust_Az(Az, az_adjust_angle)

            q = get_q(g, Az, cot_theta)
            # "if z exceeds q, it will not fit on this polygon
            # and is located on another one"
            if z > q:
                continue
            x, y = the_rest(g, sG, theta, cot_theta, az_adjust_angle, R, Az, q, z, Az_adjust_counter)
            # translate to proper origin
            x = face.center_x + x
            y = face.center_y + y
            return x, y


def wrapper(lat, long):
    return sea(Angle(lat), Angle(long), 'icosahedron')


if __name__ == '__main__':

    TABLE_2 = table_2(6378137)
    for row in TABLE_2['icosahedron']:
        print(row)

    results = []
    for face in TABLE_2['icosahedron']:
        print(f'Projecting {face.center_lat} {face.center_long} which according to table 2 should give {face.center_x} {face.center_y} on face {face.number}')
        x, y = sea(Angle(face.center_lat),
                   Angle(face.center_long),
                   'icosahedron')
        results.append((face.center_lat, face.center_long, face.center_x, x, face.center_y, y))

    for lat, long, center_x, x, center_y, y in results:
        print(f'lat: {lat} long: {long} face x: {center_x} x: {x} face y: {center_y} y: {y}')


