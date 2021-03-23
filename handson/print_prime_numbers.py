def print_prime_numbers(n):
    for i in range(1,n+1):
        for j in range(2,i):
            if(i%j==0):
                break
        else:
            print(i)

if __name__ == '__main__':
    n=int(input())
    print_prime_numbers(n)