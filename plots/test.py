import pandas as pd

if __name__ == '__main__':
    with open('../Data/calories.csv', 'r') as f:
        data = f.read()

        data = data.replace(' kJ', '')


    with open(r'../Data/calories.csv', 'w') as file:
        file.write(data)
