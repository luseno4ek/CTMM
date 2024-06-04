import numpy as np
import multiprocessing as mp

G = 6.6743e-11

def _a_patch_worker(start_patch, end_patch, y, m):
    num_points = y.shape[0] // 4
    a_partial = np.zeros((num_points, 2), dtype=np.float64)
  
    for i in range(start_patch, end_patch, 4):
        for j in range(0, y.shape[0], 4):
            if i == j:
                continue
            x_length = y[j] - y[i]
            y_length = y[j+1] - y[i+1]
            r2 = x_length**2 + y_length**2
            r = np.sqrt(r2)
            f = G * m[j // 4] / r2
            a_partial[i//4, 0] += f * x_length / r
            a_partial[i//4, 1] += f * y_length / r

    return a_partial

def a_mp(y, m):
    num_processes = mp.cpu_count() 
    pool = mp.Pool(processes=num_processes)
    
    num_points = y.shape[0] // 4
    patch_size = (num_points * 4) // num_processes  
    tasks = []
    for i in range(0, y.shape[0], patch_size):
        start_patch = i
        end_patch = min(i + patch_size, y.shape[0])
        tasks.append(pool.apply_async(_a_patch_worker, (start_patch, end_patch, y, m)))

    results = [task.get() for task in tasks]

    pool.close()
    pool.join()

    a_combined = np.sum(results, axis=0)
    
    return a_combined

def verlet_mp(t, y0, m):
    dt = t[1].astype(np.float64)
    solution = np.empty((t.shape[0], y0.shape[0]), dtype=np.float64)
    solution[0, :] = y0

    a_n = a_mp(solution[0, :], m)

    for i in range(1, solution.shape[0]):
        solution[i, 0:4] = solution[i-1, 0:4]

        for j in range(4, solution.shape[1], 4):
            index = j // 4
            solution[i, j] = (solution[i-1, j] + solution[i-1, j+2] * dt 
                              + 0.5 * a_n[index, 0] * dt**2)
            solution[i, j+1] = (solution[i-1, j+1] + solution[i-1, j+3] * dt 
                                + 0.5 * a_n[index, 1] * dt**2)

        a_n1 = a_mp(solution[i, :], m)

        for j in range(4, solution.shape[1], 4):
            index = j // 4
            solution[i, j + 2] = (solution[i-1, j + 2] + 0.5 * (a_n1[index, 0] + a_n[index, 0]) * dt)
            solution[i, j + 3] = (solution[i-1, j + 3] + 0.5 * (a_n1[index, 1] + a_n[index, 1]) * dt)

        a_n = a_n1

    return solution
