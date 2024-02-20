/*old code
#include <iostream>
#include <vector>

using std::vector;
  
#include <algorithm>

int maxSubArray(vector<int>& nums) {    
    return solve(nums, 0, false);
}
int solve(vector<int>& A, int i, bool mustPick) {
    // our subarray must contain atleast 1 element. If mustPick is false at end means no element is picked and this is not valid case
    if(i >= size(A)) return mustPick ? 0 : -1e5;       
    if(mustPick)
        return std::max(0, A[i] + solve(A, i+1, true));                  // either stop here or choose current element and recurse
    return std::max(solve(A, i+1, false), A[i] + solve(A, i+1, true));   // try both choosing current element or not choosing
}
*/

//code refactored by chatgbt
#include <iostream>
#include <vector>

using std::vector;
  
#include <algorithm>

int maxSubArray(std::vector<int>& nums) {
    int n = nums.size();
    
    if (n == 0) {
        // Handle the case when the input vector is empty
        return 0;
    }

    int maxSum = nums[0];
    int currentSum = nums[0];

    for (int i = 1; i < n; ++i) {
        // Choose between extending the current subarray or starting a new one
        currentSum = std::max(nums[i], currentSum + nums[i]);
        
        // Update the maximum subarray sum
        maxSum = std::max(maxSum, currentSum);
    }

    return maxSum;
}
