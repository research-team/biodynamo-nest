from functions import *

# show connections and dendrites in plot
# from functions_with_draw import *

if __name__ == "__main__":
    initialize(N, M, R)
    connect_generator()
    simulate(time)
    save()