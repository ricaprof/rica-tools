import psutil
import time

def print_cpu_usage():
    while True:
        print("Uso de CPU: {:.2f}%".format(psutil.cpu_percent(interval=1)))
        print("Clock da CPU: {:.2f} MHz".format(psutil.cpu_freq().current))
        print("Uso por núcleo:")
        for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
            print(f"  Núcleo {i}: {percentage:.2f}%")
        print("-" * 30)
        time.sleep(2)

if __name__ == "__main__":
    print_cpu_usage()