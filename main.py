import lib

if __name__ == "__main__":
    reader = lib.Reader("Dane_TSP_48.xlsx")
    solution = lib.Solver(reader.data)
    writer = lib.Writer(solution.solution)
