import argparse

def copy_file(input_file, output_file, to_uppercase):
    with open(input_file, 'r', encoding='utf-8') as infile:
        content = infile.read()
        if to_uppercase:
            content = content.upper()
        
    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(content)

def main():
    parser = argparse.ArgumentParser(description='Copy and process a file.')
    parser.add_argument('input_file', type=str, help='Path to the input file.')
    parser.add_argument('output_file', type=str, help='Path to the output file.')
    parser.add_argument('-u', '--uppercase', action='store_true', 
                        help='Convert text to uppercase before writing to the output file.')

    args = parser.parse_args()

    copy_file(args.input_file, args.output_file, args.uppercase)

if __name__ == '__main__':
    main()
