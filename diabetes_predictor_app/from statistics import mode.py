from typing import List

my_array = [64, 34, 25, 12, 22, 11, 90, 5]
def bubble_sort(arr:List[int]):
    for i in range(len(arr)-1):
        for j in range(len(arr)-i-1):
            if arr[j]>arr[j+1]:
                arr[j], arr[j+1]=arr[j+1], arr[j]
    return arr
print(bubble_sort(my_array))

def binary_search(arr:List[int], target:int)-> int:
    arr.sort()
    left:int=0
    right:int=len(arr)-1
    while left<=right:
        mid:int=(left+right)//2
        if arr[mid]==target:
            return mid
        elif arr[mid]<target:
            left=mid+1
        else:
            right=mid-1
print(binary_search(my_array,11))
            