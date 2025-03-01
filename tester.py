import multiprocessing
import time
import psutil
import platform
from tasks.tasks import SingleThreadTask
from const import ANSI_COLORS, P_CORES, E_CORES, SMT
import logging

def print_with_log(text:str, level=1, do_print=True):
    if do_print:
        print(text)
    match level:
        case 0:
            logging.debug(text)
        case 1:
            logging.info(text)
        case 2:
            logging.warn(text)
        case 3:
            logging.error(text)
        case 4:
            logging.critical(text)

class CPUTaskTester:
    def __init__(self):
        logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', filename="ctm.ans", encoding='utf8', level = logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
        logging.FileHandler("ctm.ans", mode = "w")
        self.cpu_name = platform.processor()
        self.arch = platform.architecture()
        self.time_estimate: list[int] = [0]
        self.num_cores = multiprocessing.cpu_count()
        self.results_p = []
        self.results_e = []
        self.color = ANSI_COLORS
        self.last_task_name = ""
        print_with_log(f"Found {self.cpu_name} with {self.num_cores} logical cores. Architecture: {self.arch}")

    def measure_time(self, core_set: int, task: callable, repeats = 25):
        time_list = []
        if not(isinstance(core_set, list)):
            core_set = [core_set]
        for i in range(repeats + 1):
            time.sleep(.1) #A bit of time for OS scheduler to not go crazy
            process = psutil.Process()
            process.cpu_affinity(core_set)  # Set CPU affinity to the specified core
            start_time = time.time()
            task()
            end_time = time.time()
            elapsed_time = round((end_time - start_time), 4)
            if self.time_estimate[0] == 0:
                self.time_estimate[0] = round((elapsed_time * repeats), 3)
                print_with_log(f"{self.color.GREY}Calculating Core {core_set} average time required to process all runs, \nestimated time needed before the result is calculated: {self.time_estimate[0]}s{self.color.RESET}")
            time_list.append(elapsed_time)
        mean_time = sum(time_list)/len(time_list)
        print_with_log(f"{self.color.GREY}Real time elapsed: {sum(time_list)}{self.color.RESET}")
        self.time_estimate[0] = 0
        return core_set, mean_time
    
    def run_test(self, test_type:int):
        print_with_log("Iterating tests on cores...")
        sttask = SingleThreadTask()
        match test_type:
            case 0:
                task = sttask.matrix_multi
                self.last_task_name = "Matrix multiplication"
            case 1:
                task = sttask.sort_array
                self.last_task_name = "Sorting arrays"
            case 2:
                task = sttask.calculate_prime_numbers
                self.last_task_name = "Finding highest prime numbers"
            case 3:
                task = sttask.fast_fourier_transform
                self.last_task_name = "Fast Fourier transforms"
            case 4:
                task = sttask.image_processing
                self.last_task_name = "Gaussian blur"
        print_with_log(f"{self.color.GREEN}\nStarted running task: {self.last_task_name}{self.color.RESET}")
        for core_id in range(self.num_cores):
            if SMT:
                should_run = core_id % 2 == 0
            else:
                should_run = True
            if should_run:
                core_result = self.measure_time(core_id, task=task)
                if core_id in P_CORES:
                    print_with_log(f"{self.color.CYAN}Core {core_id}: {core_result[1]:.4f} seconds{self.color.RESET}")
                    self.results_p.append(core_result)
                elif core_id in E_CORES:
                    print_with_log(f"{self.color.YELLOW}Core {core_id}: {core_result[1]:.4f} seconds{self.color.RESET}")
                    self.results_e.append(core_result)
                else:
                    raise RuntimeError("Invalid core_id reference")
        print_with_log(f"{self.color.GREEN}\nFinished running task: {self.last_task_name}{self.color.RESET}")
                
    def compare_and_reset_results(self):
        fastest_pcore = min(self.results_p, key=lambda x: x[1])
        slowest_pcore = max(self.results_p, key=lambda x: x[1])
        fastest_ecore = min(self.results_e, key=lambda x: x[1])
        slowest_ecore = max(self.results_e, key=lambda x: x[1])
        print_with_log(self.results_p, do_print=False)
        print_with_log(self.results_e, do_print=False)
        sum_p = 0.0
        sum_e = 0.0
        for result in self.results_p:
            sum_p += result[1]
        for result in self.results_e:
            sum_e += result[1]
        mean_pcore = sum_p/len(self.results_p)
        mean_ecore = sum_e/len(self.results_e)
        print_with_log(f"{self.color.GREEN}\nFastest cluster 0 core: Core {fastest_pcore[0]} with {fastest_pcore[1]:.4f} seconds{self.color.RESET}")
        print_with_log(f"{self.color.RED}Slowest cluster 0 core: Core {slowest_pcore[0]} with {slowest_pcore[1]:.4f} seconds{self.color.RESET}")
        print_with_log(f"{self.color.YELLOW}Average time for a cluster 0 core to process {self.last_task_name}: {mean_pcore:.4f}{self.color.RESET}")
        print_with_log(f"{self.color.GREEN}\nFastest cluster 1 core: Core {fastest_ecore[0]} with {fastest_ecore[1]:.4f} seconds{self.color.RESET}")
        print_with_log(f"{self.color.RED}Slowest cluster 1 core: Core {slowest_ecore[0]} with {slowest_ecore[1]:.4f} seconds{self.color.RESET}")
        print_with_log(f"{self.color.YELLOW}Average time for a cluster 1 core to process {self.last_task_name}: {mean_ecore:.4f}{self.color.RESET}")
        self.results_p = []
        self.results_e = []

    def run_on_sets(self): #TODO
        core_sets = [
        [0],
        [1, 2],
        [3, 4, 5, 6]
        ]
        results = []

        for core_set in core_sets:
            core_result = self.measure_time(core_set)
            results.append(core_result)
            print_with_log(f"Cores {core_set}: {core_result[1]:.4f} seconds")

        fastest_set = min(results, key=lambda x: x[1])
        slowest_set = max(results, key=lambda x: x[1])

        print_with_log(f"\nFastest core set: Cores {fastest_set[0]} with {fastest_set[1]:.4f} seconds")
        print_with_log(f"Slowest core set: Cores {slowest_set[0]} with {slowest_set[1]:.4f} seconds")