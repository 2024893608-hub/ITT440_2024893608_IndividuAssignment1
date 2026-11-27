import socket
import struct
import time

NTP_PORT = 123

def handle_request(data):
    print("NTP request received")

    ntp_time = time.time() + 2208988800

    seconds = int(ntp_time)
    fraction = int((ntp_time - seconds) * (2 ** 32))

    transmit_timestamp = struct.pack("!II", seconds, fraction)

    if len(data) < 48:
        print("Invalid NTP request")
        return None

    response = bytearray(48)
    response[0] = 0x24
    response[1] = 1

    response[24:32] = data[40:48]
    response[32:40] = transmit_timestamp
    response[40:48] = transmit_timestamp

    return bytes(response)



def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server.bind(("0.0.0.0", NTP_PORT))

    print(f"NTP Server running on UDP port {NTP_PORT}")

    while True:
        data, address = server.recvfrom(1024)

        response = handle_request(data)

        if response is not None:
            server.sendto(response, address)
            print(f"Response sent to {address}")


if __name__ == "__main__":
    start_server()
