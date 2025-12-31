from typing import List


class SubarrayMeanCalculator:

    def read_array_dimensions(self) -> List[int]:
        return list(map(int, input().split()))

    def read_query_bounds(self) -> List[int]:
        return list(map(int, input().split()))

    def read_array_elements(self) -> List[int]:
        return list(map(int, input().split()))

    def create_prefix_sums(self, array_elements: List[int]) -> List[int]:
        prefix_sums = [0] * (len(array_elements) + 1)
        for index in range(1, len(array_elements) + 1):
            prefix_sums[index] = prefix_sums[index - 1] + array_elements[index - 1]
        return prefix_sums

    def compute_floor_mean(self, prefix_sums: List[int], left: int, right: int) -> int:
        subarray_sum = prefix_sums[right] - prefix_sums[left - 1]
        subarray_length = right - left + 1
        return subarray_sum // subarray_length

    def process_queries(self, prefix_sums: List[int], total_queries: int) -> None:
        for _ in range(total_queries):
            left, right = self.read_query_bounds()
            print(self.compute_floor_mean(prefix_sums, left, right))

    def run(self) -> None:
        element_count, query_count = self.read_array_dimensions()
        array_elements = self.read_array_elements()
        prefix_sums = self.create_prefix_sums(array_elements)
        self.process_queries(prefix_sums, query_count)


if __name__ == "__main__":
    SubarrayMeanCalculator().run()

