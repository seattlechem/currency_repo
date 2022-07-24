import time
import zmq


class CurrencyRate:
    def __init__(self):
        self.connection_string = 'tcp://*:5555'
        self.error_msg = b'Incorrect argument was received'
        self.currency_exchange = {
            'USD to EUR': '1.2',
            'USD to GBP': '1.8',
            'USD to CAD': '0.8',
            'USD to JPY': '20'
        }
        self.exchange_rates = b'1.2, 1.8, 0.8, 20'
        self.socket = None
        self.context()

    def context(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.REP)
        self.socket.bind(self.connection_string)

    def main(self):
        while True:
            print('Waiting for messages. To exit press CTRL+C')

            message = self.socket.recv()

            try:
                message = message.decode("utf-8")
            except Exception:
                self.socket.send(self.error_msg)
            finally:
                if message:
                    print(f"[***] Received message: {message}")
                    self.check_comma(message)
                    currency_list = message.split(',')
                    self.split_size_check(currency_list)
                    self.socket.send(self.exchange_rates)

            time.sleep(1)

    def check_comma(self, message):
        if ',' not in message:
            self.socket.send(self.error_msg + b'comma')

    def split_size_check(self, currency_list):
        if len(currency_list) > 4 or len(currency_list) < 4:
            self.socket.send(self.error_msg + b'size')

    def key_present_check(self, currency_list):
        flag = True
        while flag:
            for key in currency_list:
                if key not in self.currency_exchange.keys():
                    flag = False

        self.socket.send(self.error_msg)


if __name__ == "__main__":
    cr = CurrencyRate()
    cr.main()
