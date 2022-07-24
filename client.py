import zmq
import os
import time


def run_client():

    try:
        context = zmq.Context()

        # Socket to talk to server
        print("Connecting to server(receiver) …")
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:5555")

        # send a message
        data = "USD to EUR, USD to GBP, USD to CAD, USD to JPY"
        socket.send_string(data)
        print("[***] Sent message to server(receiver): ", data)

        # Get the reply.
        message = socket.recv()
        print(f"Received reply from server(receiver) confirming that they "
              f"received the message: "
              f"{message.decode('utf-8')}")
        time.sleep(1)
    except KeyboardInterrupt:
        socket.close()
    finally:
        socket.setsockopt(zmq.LINGER, 0)
        socket.close()
        context.term()

    return message.decode('utf-8')


if __name__ == "__main__":
    run_client()
    os._exit(0)
