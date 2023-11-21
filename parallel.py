import threading
import queue

def print_numbers(n, q):
    #for i in range(n):
    #    print(i)
    q.put(n)

if __name__ == "__main__":
    q = queue.Queue()
    thread = threading.Thread(target=print_numbers, args=(5, q))
    thread.start()
    thread.join()

    result = q.get()
    print(result)