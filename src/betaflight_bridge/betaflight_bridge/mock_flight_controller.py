import time
import math
import struct
import os

FIFO_NAME = '/tmp/flight_controller_fifo'
TARGET_FREQ = 10000  # Hz
LOG_INTERVAL = 1  # Log every 1 second

def main():
    if not os.path.exists(FIFO_NAME):
        os.mkfifo(FIFO_NAME)

    print(f"Opening FIFO for writing: {FIFO_NAME}")
    with open(FIFO_NAME, 'wb') as fifo:
        t = 0
        period = 1.0 / TARGET_FREQ
        next_time = time.perf_counter() + period
        last_log_time = time.time()
        iterations = 0
        
        while True:
            ax = math.sin(t) * 9.81
            ay = math.cos(t) * 9.81
            az = -9.81

            data = struct.pack('<fff', ax, ay, az)
            fifo.write(data)
            fifo.flush()

            t += period
            iterations += 1
            
            current_time = time.time()
            if current_time - last_log_time >= LOG_INTERVAL:
                print(f"Mock FC: Sent {iterations} packets in the last {LOG_INTERVAL} second(s). Last values: ax={ax:.2f}, ay={ay:.2f}, az={az:.2f}")
                last_log_time = current_time
                iterations = 0
            
            # Precise sleep
            sleep_time = next_time - time.perf_counter()
            if sleep_time > 0:
                time.sleep(sleep_time)
            next_time += period

if __name__ == "__main__":
    main()