import threading
from time import sleep

def test():
    print("Test ")
    sleep(3)

thread = threading.Thread(target=test)

count = 0
while True:
    count += 1
    print(count)
    if (count % 3 == 0):
        thread.run()
    sleep(1)







# max_val = 100

# thread1 => 102
#     lock 
#     max_val = 104
#     release

# theaad2 => 104
#     lock
#     max_val = 104
#     release