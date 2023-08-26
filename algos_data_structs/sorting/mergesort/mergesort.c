#include <stdio.h>
#include <stddef.h>
#include <string.h>


/**
* @brief Merges two sorted adjacent subarrays of a given array
*        back into the input array. The first subarray ranges
*        from index `begin` to `mid` inclusive and the second
*        one ranges from `mid+1` to `end` inclusive. Hence sorts
*        the range `begin` to `end` inclusive in the input array.
*
* @param[in|out]    arr    Array containing two sorted subarrays
* @param[in]        begin  Beginning index of the first subarray
* @param[in]        mid    Ending index of the first subarray
* @param[in]        end    Ending index of the second subarray
*/
void merge(int* arr,  const size_t begin, const size_t mid, const size_t end) {
    //const size_t mid = begin + (hi-begin)/2;
    size_t ifinal = 0, ileft = begin, iright = mid;
    const size_t length = end - begin + 1;
    int merged[length];
    // iterate both and copy the smaller element of each
    // the "most merged" subarray will be done first
    while ((ileft < mid) && (iright <= end)) {
        if (arr[ileft] < arr[iright])
            merged[ifinal++] = arr[ileft++];
        else
            merged[ifinal++] = arr[iright++];
    }
    // copy the remaining elements of the left subarray if necessary
    while (ileft < mid)
        merged[ifinal++] = arr[ileft++];
    // copy the remaining elements of the right subarray if necessary
    while (iright <= end)
        merged[ifinal++] = arr[iright++];
    // copy back to original array
    memcpy(arr+begin, merged, length * sizeof(arr[0]));
}


void mergesort(int* arr, size_t begin, size_t end) {
    // base case - already sorted
    if (end == begin) {
        return;
    }
    size_t left = begin;
    size_t mid = begin + (end-begin)/2;
    size_t right = end;
    mergesort(arr, left, mid);
    mergesort(arr, mid+1, right);
    merge(arr, left, mid+1, right);
}

int main() {
    int arr[8] = {12, 3, 7, 9, 14, 6, 11, 2};
    const int len = sizeof(arr)/(sizeof(arr[0]));
    //merge(arr, 0, 8);
    for (int i = 0; i < len; i++)
        printf("%d\n", arr[i]);
    mergesort(arr, 0, len-1);
    for (int i = 0; i < len; i++)
        printf("%d\n", arr[i]);

}
