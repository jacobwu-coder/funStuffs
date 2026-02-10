"""funStaff — simple starter script

Run: python main.py
"""

import argparse


def main():
    parser = argparse.ArgumentParser(description='funStaff starter app')
    parser.add_argument('--name', default='World', help='Name to greet')
    args = parser.parse_args()
    print(f"Hello, {args.name}! funStaff is ready.")


if __name__ == '__main__':
    main()
