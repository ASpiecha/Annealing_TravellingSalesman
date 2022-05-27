import pandas as pd
import random
import math
import copy


class Reader:
    """ A class used to import data with distances between cities"""
    def __init__(self, path):
        self.df = self.importData(path, "Arkusz1")
        self.data = self.df.values.tolist()

    def importData(self, path, sheetname):
        file = pd.read_excel(path, sheet_name=sheetname, engine="openpyxl")
        return pd.DataFrame(file)


class Solver:
    def __init__(self, data, temperature=10000, alpha=0.9, epochs=100, iterations=100, maxIterationsWithoutImprovement=100):
        self.data = data
        self.temperature = temperature
        self.alpha = alpha
        self.epochs = epochs
        self.iterations = iterations
        self.iterationsWithoutImprovement = 0
        self.maxIterationsWithoutImprovement = maxIterationsWithoutImprovement
        self.locationsQuantity = len(self.data)

        self.solution = self.compute()

    def compute(self):
        for repetition in range(100):
            T = self.temperature
            self.iterationsWithoutImprovement = 0
            order = self.generateOrder()
            computedTime = self.calculateTime(order)
            bestTime = computedTime
            for epoch in range(self.epochs):
                for iteration in range(self.iterations):
                    if self.iterationsWithoutImprovement < self.maxIterationsWithoutImprovement:
                        oldOrder = copy.deepcopy(order)
                        self.changeOrder(order)
                        computedTime = self.calculateTime(order)
                        bestTimeOld = bestTime
                        bestTime, isNew = self.evaluateSolution(bestTime, computedTime, T)
                        if isNew:
                            self.iterationsWithoutImprovement = 0
                        else:
                            self.iterationsWithoutImprovement += 1
                            order = oldOrder
                    else:
                        break
                if self.iterationsWithoutImprovement >= self.maxIterationsWithoutImprovement or epoch == self.epochs - 1:
                    return self.exportDF(bestTime)
                T *= self.alpha

    def generateOrder(self):
        order = list(range(self.locationsQuantity))
        random.shuffle(order)
        return order

    def calculateTime(self, solution):
        timeOverall = 0
        previousCity = solution[0]
        for i in solution[1:]:
            timeOverall += self.data[previousCity][i]
            previousCity = i
        return timeOverall

    def changeOrder(self, orderToChange):
        x1, x2 = random.sample(range(self.locationsQuantity), k=2)
        orderToChange[x1], orderToChange[x2] = orderToChange[x2], orderToChange[x1]

    def evaluateSolution(self, bestTime, computedTime, T):
        if computedTime < bestTime:
            return computedTime, True
        else:
            probability = math.exp((bestTime - computedTime) / T)
            draw = random.random()
            if draw < probability:
                return computedTime, True
            else:
                return bestTime, False

    def exportDF(self, bestTime):
        df = {
            'Temperature': self.temperature,
            'alpha': self.alpha,
            'epochs': self.epochs,
            'iterations': self.iterations,
            'iterations without improvement': self.iterationsWithoutImprovement,
            'best time': bestTime
        }
        return pd.DataFrame(df, index=[0])


class Writer:
    def __init__(self, dataFrame):
        dataFrame.to_csv('dataFile.csv', index=False)
