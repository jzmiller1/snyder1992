import unittest

from snyder1992.snyder import TABLE_1, table_2, r_prime


class TestRPrime(unittest.TestCase):
    def setUp(self):
        """ Executed before every test case """
        self.TABLE_1 = TABLE_1
        self.TABLE_2 = table_2(6378137.0)

    def test_r_prime_icosahedron(self):
        """
        Test that get_z_and_Az returns expected values
        """
        R = 6378137.0
        R_prime = r_prime(self.TABLE_1['icosahedron']['theta'],
                          self.TABLE_1['icosahedron']['G'],
                          self.TABLE_1['icosahedron']['g'],
                          R)
        R_prime_expected = 0.9103828153090290025 * R
        self.assertAlmostEqual(R_prime, R_prime_expected, 2)

    def test_r_prime_truncated_icosahedron_hexagon(self):
        """
        Test that get_z_and_Az returns expected values
        """
        R = 6378137.0
        R_prime = r_prime(self.TABLE_1['truncated icosahedron']['hexagon']['theta'],
                          self.TABLE_1['truncated icosahedron']['hexagon']['G'],
                          self.TABLE_1['truncated icosahedron']['hexagon']['g'],
                          R)
        # from Snyder eqn 5
        R_prime_expected = 0.9449322893 * R
        self.assertAlmostEqual(R_prime, R_prime_expected, 2)

    def test_r_prime_truncated_icosahedron_pentagon(self):
        """
        Test that get_z_and_Az returns expected values
        """
        R = 6378137.0
        R_prime = r_prime(self.TABLE_1['truncated icosahedron']['pentagon']['theta'],
                          self.TABLE_1['truncated icosahedron']['pentagon']['G'],
                          self.TABLE_1['truncated icosahedron']['pentagon']['g'],
                          R)
        # from Snyder eqn 26
        R_prime_expected = 0.970027811 * R
        self.assertAlmostEqual(R_prime, R_prime_expected, 2)


class TestTable2(unittest.TestCase):
    def setUp(self):
        """ Executed before every test case """
        self.TABLE_1 = TABLE_1
        self.TABLE_2 = table_2(6378137.0)

    def test_table_2_icosahedron(self):
        """
        Test that get_z_and_Az returns expected values
        """
        lat, long = (52.62263186, -144.0)
        face_1 = self.TABLE_2['icosahedron'][0]
        self.assertAlmostEqual(lat, face_1.center_lat, 4)
        self.assertAlmostEqual(long, face_1.center_long, 4)

    def test_table_2_truncated_icosahedron(self):
        """
        Test that get_z_and_Az returns expected values
        """
        # test a hexagon
        lat, long = (90.0, 0)
        face_1 = self.TABLE_2['truncated icosahedron'][0]
        self.assertAlmostEqual(lat, face_1.center_lat, 4)
        self.assertAlmostEqual(long, face_1.center_long, 4)

        # test a pentagon
        lat, long = (69.92324873, -144.0)
        face_2 = self.TABLE_2['truncated icosahedron'][1]
        self.assertAlmostEqual(lat, face_2.center_lat, 4)
        self.assertAlmostEqual(long, face_2.center_long, 4)
