import concurrent.futures
import random
import time
from math import inf


def randompick(distance, trail, tabu, probability):
    if len(tabu) == len(distance) - 1:
        for i in range(len(distance)):
            if i not in tabu:
                return i
    if 0 in tabu:
        probability[0] = 0
    for i in range(1,len(distance)):
        if i in tabu:
            probability[i] = probability[i - 1]
        else:
            probability[i] += probability[i - 1]
    pick = 0
    #print(probability[-1])

    while (True):
        pick = 0
        pick_index = random.uniform(0, probability[-1])
        if (pick_index == probability[-1]):
            pick = len(distance) - 1
        while pick_index > probability[pick]:
            pick += 1
        if (pick not in tabu):
            break
    return pick


def calculate_probability(list_of_cities, trail,probability_by_distance):
    a= 1  # a=trail factor,b=distance factor
    probability = [[0 for i in range(len(list_of_cities))] for j in range(len(list_of_cities))]
    for i in range(len(list_of_cities)):
        for j in range(len(list_of_cities)):
            if i != j:
                probability[i][j] = (trail[i][j] ** a) * probability_by_distance[i][j]
    return probability

def calculate_distance(list_of_cities,b):
    probability = [[0 for i in range(len(list_of_cities))] for j in range(len(list_of_cities))]
    for i in range(len(list_of_cities)):
        for j in range(len(list_of_cities)):
            if i != j:
                probability[i][j] = ((list_of_cities[i][j]) ** (-b))
    return probability

def parallelpart(argss):
    list_of_distances = argss[0]
    list_of_visited_cities = argss[1]
    level_of_trail = argss[2]
    ant_count = argss[3]
    current_thread = argss[4]
    thread_counter = argss[5]
    probability = argss[6]

    # print([ i for i in range(current_thread*ant_count//thread_counter,((current_thread+1)*ant_count//thread_counter))])
    for i in range(len(list_of_distances) - 1):
        for ant in range(current_thread * ant_count // thread_counter,
                         ((current_thread + 1) * ant_count // thread_counter)):
            current_city = list_of_visited_cities[ant][-1]
            #print(i,ant,list_of_visited_cities[ant])
            y = randompick(list_of_distances[current_city], level_of_trail[current_city], list_of_visited_cities[ant],
                           probability[current_city].copy())
            list_of_visited_cities[ant].append(y)
    list_of_visited_cities = list_of_visited_cities[current_thread * ant_count // thread_counter: (
                (current_thread + 1) * ant_count // thread_counter)]

    # print([i[0] for i in list_of_visited_cities])
    return list_of_visited_cities


def antcolony(graph):
    Tmax =100
    Tmin = 1
    best_ant = inf
    start = time.time()
    MIN_LEN = inf
    MIN_PATH = []
    N = len(graph.matrix)
    if N < 300:
        ant_count = 30
        if(N<ant_count):
            ant_count=N
        vapor_factor = 0.7
        best_ant = 1
        b = 5
    else:
        ant_count = 4
        vapor_factor = 0.8
        best_ant = 1
        b = 9

    trail = []
    delta_trail = []
    ants = []
    ThreadCount = 4
    distance_probability = calculate_distance(graph.matrix,b)

    for i in range(N):
        trail.append([])
        delta_trail.append([])
        for j in range(N):
            trail[i].append(Tmax)
            delta_trail[i].append(0)

    ants = [i for i in range(ant_count)]

    while (True):
        probability = calculate_probability(graph.matrix, trail,distance_probability)
        index = 0
        LEN = []
        visited_cities = [[] for i in range(ant_count)]

        for k in range(ant_count):
            visited_cities[k].append(ants[k])


        argss = [[graph.matrix,visited_cities,trail,ant_count,thread,ThreadCount,probability] for thread in range(ThreadCount)]

        with concurrent.futures.ProcessPoolExecutor() as pool:
            tmp = pool.map(parallelpart,argss)
        visited_cities = []
        for t in list(tmp):
            visited_cities.extend(list(t))


        iteratonBestAntIndex=0
        iteratonBestAntLength=inf
        for ant in range(ant_count):
            visited_cities[ant].append(visited_cities[ant][0])
            LEN.append(sum(
                [graph.matrix[visited_cities[ant][i]][visited_cities[ant][i + 1]] for i in range(len(graph.matrix))]))
            if LEN[-1] < iteratonBestAntLength:
                iteratonBestAntIndex=ant
                iteratonBestAntLength=LEN[-1]

        for i in range(ant_count):
            if LEN[i] < MIN_LEN:
                timeOfLastChange=time.time()
                MIN_LEN = LEN[i]
                MIN_PATH = visited_cities[i]
                #print(str(MIN_LEN))


        for i in range(N):
            delta_trail[visited_cities[iteratonBestAntIndex][i]][visited_cities[iteratonBestAntIndex][i + 1]] += 20

        for i in range(N):
            for j in range(N):
                trail[i][j] =max(Tmin,vapor_factor * trail[i][j] + delta_trail[i][j])
                trail[i][j]=min(Tmax,trail[i][j])
        timeNow=time.time()
        if timeNow - start > 180 :
            break
        if timeNow - timeOfLastChange >45:
            print("reset")
            timeOfLastChange=timeNow+15
            for i in range(N):
                for j in range(N):
                    trail[i][j] =Tmax

        delta_trail = [[0 for i in range(N)] for j in range(N)]
    return MIN_LEN, MIN_PATH