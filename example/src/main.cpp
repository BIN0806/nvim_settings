#include <iostream>
#include <numeric>
#include <vector>

int main() {
  const std::vector<int> prices{10, 20, 30, 40};
  const int total = std::accumulate(prices.begin(), prices.end(), 0);
  std::cout << "Total: " << total << '\n';
  return total == 100 ? 0 : 1;
}
