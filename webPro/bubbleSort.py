#-*- coding:utf-8 -*-

def bubbleSort(numbers):
    for j in xrange(len(numbers)-1,-1,-1):
        print(len(numbers)-1)
        print('j='+str(j))
        for i in xrange(j):
            print('i='+str(i))
            if numbers[i] > numbers[i+1]:
                numbers[i], numbers[i+1] = numbers[i+1], numbers[i]
            print numbers


def main():
    numbers = [23, 10, 3, 25, 6]
    bubbleSort(numbers)


if __name__ == "__main__":
    main()