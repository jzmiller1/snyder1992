import math
import unittest

from pyproj import CRS, Transformer

from snyder1992 import sea
from snyder1992.structures import Angle
from snyder1992.snyder import table_2


class TestSeaComponents(unittest.TestCase):
    def setUp(self):
        """ Executed before every test case """
        self.TABLE_2 = table_2(6378137.0)

    def test_get_z_and_Az(self):
        """
        Test that get_z_and_Az returns expected values
        """
        # sin(0) is 0, cos(0) is 1
        # so z should be acos(0+1) which is zero
        # so Az should be atan2(0, 0) which is zero
        lat, long = Angle(0), Angle(0)
        center_lat, center_long = Angle(0), Angle(0)
        z, Az = sea.get_z_and_Az(lat, long, center_lat, center_long)
        self.assertAlmostEqual(z, 0.0, 10)
        self.assertAlmostEqual(Az, 0.0, 10)

        # using snyder icosahedron face 8 from Table 2
        lat, long = Angle(0), Angle(0)
        center_lat, center_long = Angle(10.81231696), Angle(0)
        z, Az = sea.get_z_and_Az(lat, long, center_lat, center_long)
        self.assertAlmostEqual(z, 0.18871053072122412, 10)
        self.assertAlmostEqual(Az, 180.0, 10)

        # reverse of previous
        lat, long = Angle(10.81231696), Angle(0)
        center_lat, center_long = Angle(0), Angle(0)
        z, Az = sea.get_z_and_Az(lat, long, center_lat, center_long)
        self.assertAlmostEqual(z, 0.18871053072122412, 10)
        self.assertAlmostEqual(Az, 0.0, 10)

    def test_adjust_Az(self):
        """
        Test that Az adjustment works
        """
        Az = Angle(180.0)
        az_adjust_angle = 120.0
        Az, Az_adjust_counter = sea.adjust_Az(Az, az_adjust_angle)
        self.assertAlmostEqual(Az, 60.0, 10)
        self.assertEqual(Az_adjust_counter, 1)

        Az = Angle(-180.0)
        az_adjust_angle = 120.0
        Az, Az_adjust_counter = sea.adjust_Az(Az, az_adjust_angle)
        self.assertAlmostEqual(Az, 60.0, 10)
        self.assertEqual(Az_adjust_counter, -2)

        Az = Angle(-33.0)
        az_adjust_angle = 120.0
        Az, Az_adjust_counter = sea.adjust_Az(Az, az_adjust_angle)
        self.assertAlmostEqual(Az, 87.0, 10)
        self.assertEqual(Az_adjust_counter, -1)

        Az = Angle(180)
        az_adjust_angle = 60.0
        Az, Az_adjust_counter = sea.adjust_Az(Az, az_adjust_angle)
        self.assertAlmostEqual(Az, 60.0, 10)
        self.assertEqual(Az_adjust_counter, 2)

    def test_get_q(self):
        """
        Test that get_q gets q
        """
        # test for icosahedron
        theta = Angle(30.0)
        Az = Angle(180.0)
        g = Angle(37.37736814)
        cot_theta = 1.0 / math.tan(theta.radians)
        q = sea.get_q(g, Az, cot_theta)
        self.assertAlmostEqual(q, 2.4892345138167644, 10)

        # test for truncated icosahedron hexagon face
        theta = Angle(60.0)
        Az = Angle(180.0)
        g = Angle(23.80018260)
        cot_theta = 1.0 / math.tan(theta.radians)
        q = sea.get_q(g, Az, cot_theta)
        self.assertAlmostEqual(q, 2.7262011046439287, 10)


class TestSeaForward(unittest.TestCase):
    def setUp(self):
        """ Executed before every test case """
        self.TABLE_2 = table_2(6378137.0)

        crs_4326 = CRS("EPSG:4326")
        crs_isea = CRS("+proj=isea +orient=pole +R=6378137")
        self.proj_isea = Transformer.from_crs(crs_4326, crs_isea)

    def test_dodecahedron_forward_centers(self):
        """
        Test that dodecahedron coordinates given by Table 2 Snyder are returned from forward projection
        """
        polyhedron = 'dodecahedron'
        for face in self.TABLE_2[polyhedron]:
            x, y = sea.sea(face.center_lat, face.center_long, polyhedron)
            message = f'polyhedron: {polyhedron} lat: {face.center_lat} long: {face.center_long}'
            self.assertAlmostEqual(x, face.center_x, 0,
                                   f'Failing x for {message}')
            self.assertAlmostEqual(y, face.center_y, 0,
                                   f'Failing y for {message}')

    def test_icosahedron_forward_centers(self):
        """
        Test that icosahedron coordinates given by Table 2 Snyder are returned from forward projection
        """
        polyhedron = 'icosahedron'
        for face in self.TABLE_2[polyhedron]:
            x, y = sea.sea(face.center_lat, face.center_long, polyhedron)
            message = f'polyhedron: {polyhedron} lat: {face.center_lat} long: {face.center_long}'
            self.assertAlmostEqual(x, face.center_x, 0,
                                   f'Failing x for {message}')
            self.assertAlmostEqual(y, face.center_y, 0,
                                   f'Failing y for {message}')

    def test_truncated_icosahedron_forward_centers(self):
        """
        Test that truncated icosahedron coordinates given by Table 2 Snyder are returned from forward projection
        """

        polyhedron = 'truncated icosahedron'
        for face in self.TABLE_2[polyhedron]:
            x, y = sea.sea(face.center_lat, face.center_long, polyhedron)
            message = f'polyhedron: {polyhedron} lat: {face.center_lat} long: {face.center_long}'
            self.assertAlmostEqual(x, face.center_x, 0,
                                   f'Failing x for {message}')
            self.assertAlmostEqual(y, face.center_y, 0,
                                   f'Failing y for {message}')

    def test_icosahedron_against_PROJ(self):
        """
        Test that my calculated icosahedron x,y coordinates are similar to PROJ for the same lat, long
        """
        polyhedron = 'icosahedron'
        for face in self.TABLE_2['icosahedron']:
            x, y = self.proj_isea.transform(face.center_lat, face.center_long)
            my_x, my_y = sea.sea(face.center_lat, face.center_long, polyhedron)
            message = f'polyhedron: {polyhedron} lat: {face.center_lat} long: {face.center_long} with my_x {my_x} and my_y {my_y}'
            self.assertAlmostEqual(my_x, x, 0,
                                   f'Failing x for {message}')
            self.assertAlmostEqual(my_y, y, 0,
                                   f'Failing y for {message}')


if __name__ == '__main__':
    unittest.main()
