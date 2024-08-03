import time
x = 0
while True:
    if x % 600 == 0:
        print(f"Time", x/60)
    time.sleep(1)