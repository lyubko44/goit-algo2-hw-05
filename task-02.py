import pandas as pd
import re
import time
from hyperloglog import HyperLogLog


def load_ip_addresses(file_path):
    """
    Завантажує IP-адреси з лог-файлу, ігноруючи некоректні рядки.
    """
    ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
    ip_addresses = []
    with open(file_path, 'r') as file:
        for line in file:
            match = ip_pattern.search(line)
            if match:
                ip_addresses.append(match.group())
    return ip_addresses


def exact_count(ip_addresses):
    """
    Точний підрахунок унікальних IP-адрес за допомогою set.
    """
    return len(set(ip_addresses))


def approximate_count(ip_addresses):
    """
    Наближений підрахунок унікальних IP-адрес за допомогою HyperLogLog.
    """
    hll = HyperLogLog(0.01)  # Параметр похибки
    for ip in ip_addresses:
        hll.add(ip)
    return len(hll)


if __name__ == "__main__":
    file_path = "lms-stage-access.log"  # Файл існує локально, але не в репозиторії адже він великий
    ip_addresses = load_ip_addresses(file_path)

    start_time = time.time()
    exact_result = exact_count(ip_addresses)
    exact_time = time.time() - start_time

    start_time = time.time()
    approximate_result = approximate_count(ip_addresses)
    approximate_time = time.time() - start_time

    print("Результати порівняння:")
    print(f"{'':<25}{'Точний підрахунок':<20}{'HyperLogLog':<20}")
    print(f"{'Унікальні елементи':<25}{exact_result:<20}{approximate_result:<20}")
    print(f"{'Час виконання (сек.)':<25}{exact_time:<20.5f}{approximate_time:<20.5f}")
