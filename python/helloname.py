#!/bin/env python3

# Privacy exposing script

def main(name, current_year, birth_year):
    age = current_year - birth_year
    print(f"Hello {name}, you are {age} years old.")

if __name__ == "__main__":
    name = input("Your name: ")
    current_year = int(input("Current Year: "))
    birth_year = int(input("Birth Year: "))
    main(name, current_year, birth_year)
