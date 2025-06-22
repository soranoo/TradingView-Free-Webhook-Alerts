import time

from . import StoppableThread

pending_tasks = []
stop_flag = False

def run_at(timestamp:float , func, func_args):
    """
    ### Description ###
    Run a function at a specific time.
    
    ### Parameters ###
        - `timestamp` (float): The timestamp to run the function at.
        - `func` (function): The function to run.
        - `func_args` (tuple): The arguments to pass to the function.
    """
    pending_tasks.append((timestamp, func, func_args))
    
def terminate():
    """
    ### Description ###
    Terminate the PlanToRun thread.
    """
    global stop_flag
    stop_flag = True
            
def _thread_check():
    now_timestamp = time.time()
    for task in pending_tasks:
        target_timestamp = task[0]
        if now_timestamp >= target_timestamp:
            func = task[1]
            func_args = task[2]
            func(*func_args)
            pending_tasks.remove(task)
            
def _thread_main():
    while not stop_flag:
        _thread_check()
        time.sleep(0.05)

thread = StoppableThread(target=_thread_main)
thread.start()

if __name__ == "__main__":
    def test_func(a, b, c):
        print(time.time(), a, b, c)
    print(time.time())
    run_at(time.time()+3, test_func, func_args=("Hello World!", 1, 2))
    run_at(time.time()+6, test_func, func_args=("Hello World!", 3, 4))
    time.sleep(10)
    terminate()
