import argparse

def main():
    parser = argparse.ArgumentParser(description='Print a sequence of numbers.')
    parser.add_argument('-n', '--number', type=int, required=True, help='An integer number n')
    parser.add_argument('-r', '--reverse', action='store_true', help='Print numbers in decreasing order')

    args = parser.parse_args()
    
   
    if args.reverse:
        sequence = range(args.number, 0, -1)
    else:
        sequence = range(1, args.number + 1)

   
    for number in sequence:
        print(number)

if __name__ == '__main__':
    main()
    
    