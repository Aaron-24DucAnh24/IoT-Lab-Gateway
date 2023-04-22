from uart.uart_controller import *
import unittest

class TestUart(unittest.TestCase):

    def test_set_serial_port(self):
        UartController.set_serial_port()
        self.assertNotEqual(UartController.ser, None)

    def test_check_serial_port(self):
        self.assertEqual(UartController.check_serial_port(), True)

    def test_request_data_1(self):
        UartController.uart_frequency = 15
        self.assertEqual(UartController.request_data(10), False)

    def test_request_data_2(self):
        UartController.uart_frequency = 15
        self.assertEqual(UartController.request_data(15), True)

    def test_handle_disconnection_1(self):
        UartController.handle_disconnection(None, 'ok')
        expected = UartController.yolobit_connection==1
        self.assertEqual(expected, True)

    def test_handle_disconnection_2(self):
        UartController.uart_frequency = 15

        UartController.handle_disconnection(None, 'fail')
        expected = UartController.yolobit_connection==1

        self.assertEqual(expected, True)

    def test_handle_disconnection_3(self):
        UartController.uart_frequency = -2

        UartController.handle_disconnection(None, 'fail')
        expected = disconnect_count == 0 \
            and UartController.yolobit_connection == 0

        self.assertEqual(expected, True)

    def test_update_uart_count_1(self):
        UartController.uart_frequency = 10
        self.assertEqual(
            UartController.update_uart_count(9), 9.5)

    def test_update_uart_count_2(self):
        UartController.uart_frequency = 10
        self.assertEqual(
            UartController.update_uart_count(10), 0)

    def test_set_btn(self):
        UartController.set_btn('button1', 1)
        UartController.set_btn('button2', 0)
        UartController.set_btn('button3', 0)

        expected = UartController.pump_btn== '1' \
            and UartController.fan_btn=='0'\
            and UartController.light == '0'

        self.assertEqual(expected, True)