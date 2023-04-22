import unittest
from MQTTClient.ada_controller import *
from MQTTClient.declaration import *

class TestUartController(unittest.TestCase):

    def test_set_frequency(self):
        AdaController.set_frequency("100")
        self.assertEqual(AdaController.ada_frequency, 100)

    def test_confirm_connection_1(self):
        AdaController.confirm_connection_frequency = 10
        self.assertEqual(AdaController.confirm_connection(client, 10), True)

    def test_confirm_connection_2(self):
        AdaController.confirm_connection_frequency = 10
        self.assertEqual(AdaController.confirm_connection(client, 9), False)

    def test_update_ada_count_1(self):
        AdaController.ada_frequency = 10
        self.assertEqual(AdaController.update_ada_count(9), 9.5)

    def test_update_ada_count_2(self):
        AdaController.ada_frequency = 20
        self.assertEqual(AdaController.update_ada_count(21), 0)

    def test_update_confirm_count_1(self):
        self.assertEqual(AdaController.update_confirm_frequency_count(9), 9.5)

    def test_update_confirm_count_2(self):
        self.assertEqual(AdaController.update_confirm_frequency_count(10), 0)
