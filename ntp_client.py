import socket
import struct
import time
from datetime import datetime

SERVER_IP = "172.24.229.107"
NTP_PORT = 123

def get_ntp_time():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.settimeout(5)

    request = bytearray(48)
    request[0] = 0x23

    unix_time = time.time()
    ntp_time = unix_time + 2208988800

    seconds = int(ntp_time)
    fraction = int((ntp_time - seconds) * (2 ** 32))

    request[40:48] = struct.pack("!II", seconds, fraction)

    try:
        client.sendto(request, (SERVER_IP, NTP_PORT))
        print("NTP request sent")

        data, address = client.recvfrom(1024)
        print(f"NTP response received from {address}")

        if len(data) < 48:
            print("Invalid NTP response")
            return None

    except socket.timeout:
        print("Error: NTP server did not respond")
        return None

    finally:
        client.close()

    seconds, fraction = struct.unpack("!II", data[40:48])

    ntp_time = seconds - 2208988800 + fraction / (2 ** 32)

    return datetime.fromtimestamp(ntp_time)

if __name__ == "__main__":
    ntp_datetime = get_ntp_time()

    if ntp_datetime is not None:
        print("Time received from NTP Server:")
        print(ntp_datetime.strftime("%Y-%m-%d %H:%M:%S"))