def is_a_prime_number(n):
    for i in range(2,n):
        if(n%i==0):
            print(n, "is not a prime number")
            break;
    else:
        print(n, "is a prime number")

if __name__ == '__main__':
    n = int(input())
    is_a_prime_number(n)