import random
import time
import sys
from memory_profiler import memory_usage

class TwoPivotBlockQuicksort:
    # initialize dengan array yang ingin disort
    def __init__(self, arr):
        self.arr = arr

    def sort(self):
        self.two_pivot_block_quicksort(0, len(self.arr) - 1)

    def two_pivot_block_quicksort(self, low, high):
        # jika subarray memiliki 0 atau 1 item, maka dianggap sudah sorted
        if low >= high:
            return
         # mempartisi array untuk mendapatkan pivotnya
        left_pivot, right_pivot = self.partition(low, high)
        # mengelompokkan element menjadi 3 grup yaitu lebih kecil dibandingankan left-pivot, diantara keduanya, dan lebih kecil
        # dibandingkan dengan right-pivot, dikelompokkan secara rekursif
        self.two_pivot_block_quicksort(low, left_pivot - 1)
        self.two_pivot_block_quicksort(left_pivot + 1, right_pivot - 1)
        self.two_pivot_block_quicksort(right_pivot + 1, high)

    def partition(self, low, high):
        # memeastikan left-pivot lebih kecil dibandingkan dengan right-pivot
        if self.arr[low] > self.arr[high]:
            self.swap(low, high)
        left_pivot_index = low + 1
        right_pivot_index = high - 1
        iterator = low + 1
        # mengubah posisi element sesuai dengan relasi pada pivot
        while iterator <= right_pivot_index:
            if self.arr[iterator] < self.arr[low]:
                self.swap(iterator, left_pivot_index)
                left_pivot_index += 1
            elif self.arr[iterator] > self.arr[high]:
                while self.arr[right_pivot_index] > self.arr[high] and iterator < right_pivot_index:
                    right_pivot_index -= 1
                self.swap(iterator, right_pivot_index)
                right_pivot_index -= 1
                if self.arr[iterator] < self.arr[low]:
                    self.swap(iterator, left_pivot_index)
                    left_pivot_index += 1
            iterator += 1
        # menaruh pivot pada final-position
        left_pivot_index -= 1
        right_pivot_index += 1
        self.swap(low, left_pivot_index)
        self.swap(high, right_pivot_index)
        # return final pivot posisito
        return left_pivot_index, right_pivot_index

    def swap(self, first_index, second_index):
        #swap elemen pada indeks yang telah diberikan
        self.arr[first_index], self.arr[second_index] = self.arr[second_index], self.arr[first_index]

class MergeSort:
    @staticmethod
    def sort(arr):
        MergeSort._mergeSort(arr, 0, len(arr) - 1)

    @staticmethod
    def _mergeSort(arr, l, r):
        if l < r:
            m = l + (r - l) // 2
            MergeSort._mergeSort(arr, l, m)
            MergeSort._mergeSort(arr, m + 1, r)
            MergeSort._merge(arr, l, m, r)

    @staticmethod
    def _merge(arr, l, m, r):
        n1 = m - l + 1
        n2 = r - m

        L = arr[l:m + 1]
        R = arr[m + 1:r + 1]

        i = j = 0
        k = l

        while i < n1 and j < n2:
            if L[i] <= R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < n1:
            arr[k] = L[i]
            i += 1
            k += 1

        while j < n2:
            arr[k] = R[j]
            j += 1
            k += 1

def generate_dataset(size, status='random'):
    dataset = list(range(size))
    if status == 'sorted':
        return dataset
    elif status == 'reversed':
        return list(reversed(dataset))
    elif status == 'random':
        random.shuffle(dataset)
        return dataset
    else:
        raise ValueError("Unknown status type.")
    
def measure_sort_time_and_memory(sorter, dataset):
    if isinstance(sorter, type):
        # jika sorternya merupakan class, maka inisiasi
        sorter_instance = sorter(dataset.copy())
        start_time = time.time()
        mem_usage = memory_usage((sorter_instance.sort,))
        end_time = time.time()
        dataset = sorter_instance.arr
    else:
        # jika sorternya statics
        dataset_copy = dataset.copy()
        start_time = time.time()
        mem_usage = memory_usage((sorter, (dataset_copy,)))
        end_time = time.time()
        dataset = dataset_copy

    time_taken = (end_time - start_time) * 1000
    max_memory = max(mem_usage) if mem_usage else None

    return dataset, time_taken, max_memory

if __name__ == "__main__":
    sys.setrecursionlimit(2**20)  # Increase recursion limit untuk dataset besar

    dataset_sizes = [2**9, 2**13, 2**16]
    statuses = ['sorted', 'random', 'reversed']

    for size in dataset_sizes:
        print(f"\n{'=' * 20} Processing datasets of size {size} {'=' * 20}\n")
        for status in statuses:
            dataset = generate_dataset(size, status)
            print(f"Original {status} dataset of size {size}: {dataset[:10]}...{dataset[-10:]}")

            # mengukur TwoPivotBlockQuicksort performance data
            sorted_dataset, time_taken, max_memory = measure_sort_time_and_memory(TwoPivotBlockQuicksort, dataset)
            print(f"TwoPivotBlockQuicksort | Size: {size} | Status: {status} => Time: {time_taken:.2f} ms, Memory: {max_memory:.2f} MiB")
            print(f"Sorted dataset: {sorted_dataset[:10]}...{sorted_dataset[-10:]}")

            # mengukur MergeSort performance data
            sorted_dataset, time_taken, max_memory = measure_sort_time_and_memory(MergeSort.sort, dataset)
            print(f"MergeSort | Size: {size} | Status: {status} => Time: {time_taken:.2f} ms, Memory: {max_memory:.2f} MiB")
            print(f"Sorted dataset: {sorted_dataset[:10]}...{sorted_dataset[-10:]}")

            print("\n")
