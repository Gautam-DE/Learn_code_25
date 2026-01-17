from typing import List


class SubarrayMeanCalculator:

    def read_dimensions(self) -> List[int]:
        return list(map(int, input().split()))

    def read_query_range(self) -> List[int]:
        return list(map(int, input().split()))

    def read_array(self) -> List[int]:
        return list(map(int, input().split()))

    def create_prefix_sums(self, numbers: List[int]) -> List[int]:
        prefix_sum = [0] * (len(numbers) + 1)
        for index in range(1, len(numbers) + 1):
            prefix_sum[index] = prefix_sum[index - 1] + numbers[index - 1]
        return prefix_sum

    def compute_floor_mean(self, prefix_sum: List[int], left: int, right: int) -> int:
        subarray_sum = prefix_sum[right] - prefix_sum[left - 1]
        subarray_length = right - left + 1
        return subarray_sum // subarray_length

    def process_queries(self, prefix_sum: List[int], total_queries: int) -> None:
        for _ in range(total_queries):
            left, right = self.read_query_range()
            print(self.compute_floor_mean(prefix_sum, left, right))

    def run(self) -> None:
        element_count, query_count = self.read_dimensions()
        numbers = self.read_array()
        prefix_sum = self.create_prefix_sums(numbers)
        self.process_queries(prefix_sum, query_count)


if __name__ == "__main__":
    SubarrayMeanCalculator().run()

