import os
# for i in range(1, 11):
#     for j in range(1, 11):
#         count = i*j
#         # print(count)
#         print(count, end=' ')
#         break#跳出内循环

# for letter in 'python':
#     if letter == 'h':
#         # break#直接退出循环
#         continue#不执行print，直接下一次循环
#     print('letter is :',letter)

# for letter in 'Python':
#    if letter == 'h':
#       pass
#       print ('This is pass block')
#    print ('Current Letter :', letter)
#
# print ("Good bye!")

import sys
def fibonacci(n): #generator function
    a, b, counter = 0, 1, 0
    while True:
        if counter > n:
            return
        yield a
        a, b = b, a + b
        counter += 1

f = fibonacci(5) #f is iterator object

# while True:
#    try:
#       print(next(f), end=" ")
#    except StopIteration:
#       sys.exit()