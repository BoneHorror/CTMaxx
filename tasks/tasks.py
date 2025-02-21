import numpy as np
from scipy.ndimage import gaussian_filter

class SingleThreadTask:
    def __init__(self) -> None:
        #TODO Type challenges: allow multiple operation types per task, specify if they can be done in parallel or not, find better workload docs/profiling
        self.types_multicore_dict = {"None": False, "Integer Arithmetic": None, "Logical Operations": None, 
                                     "Memory Operations": None, "Complex Arithmetic": None, "Sorting Algorithm": None, 
                                     "Convolution Operations": None} 
        self.last_task_infobits = []

    def matrix_multi(self, size = 2250):
        # Multiply two large matrices
        self.last_task_infobits = ["FPU", "Memory", "SIMD Accel"]
        matrix_a = np.random.rand(size, size)
        matrix_b = np.random.rand(size, size)
        result = np.dot(matrix_a, matrix_b)
        return result

    def sort_array(self, size = 22_500_000):
        # Sort a large array of random numbers
        self.last_task_infobits = ["Integer", "SIMD Accel"]
        array = np.random.rand(size)
        sorted_array = np.sort(array)
        return sorted_array

    def calculate_prime_numbers(self, limit = 1_500_000):
        # Find all prime numbers up to limit
        self.last_task_infobits = ["Integer", "Cond Branching"]
        primes = []
        for num in range(2, limit):
            is_prime = True
            for i in range(2, int(num**0.5) + 1):
                if num % i == 0:
                    is_prime = False
                    break
            if is_prime:
                primes.append(num)
        return primes

    def fast_fourier_transform(self, size = 2_250_000):
        # Perform FFT on a large array
        self.last_task_infobits = ["Complex arithmetic", "Memory"]
        array = np.random.rand(size)
        fft_result = np.fft.fft(array)
        return fft_result
    
    def image_processing(self, size = (5000, 5000)):
        # Apply Gaussian blur to a large image
        self.last_task_infobits = ["FPU", "Memory", "SIMD Accel"]
        image = np.random.rand(*size)
        blurred_image = gaussian_filter(image, sigma=5)
        return blurred_image

