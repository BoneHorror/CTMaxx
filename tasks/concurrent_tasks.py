import concurrent.futures
import numpy as np

def mt_matrix_multi(num_threads): #High core-to-core latency impact?
    
    def task(matrix_a, matrix_b):
        return np.dot(matrix_a, matrix_b)
    
    size = 1000
    matrix_a = np.random.rand(size, size)
    matrix_b = np.random.rand(size, size)
    chunk_size = size // num_threads

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(task, matrix_a[i * chunk_size:(i + 1) * chunk_size, :], matrix_b) for i in range(num_threads)]
        result_chunks = [future.result() for future in concurrent.futures.as_completed(futures)]

    result = np.vstack(result_chunks)
    print("Matrix multiplication completed")
    return result
