def closest_aviable(point, path, list):  # finds the closest point that hasn't been visited yet
    min = 0
    while min in path or min == point:
        min += 1
    for i in range(len(list)):
        if i not in path and i != point and list[point][min] >= list[point][i]:
            min = i
    return min



def find_path(start_point, distance, path, matrix):
    path = [start_point]
    for i in range(len(matrix)-1):
        path.append(closest_aviable(path[-1],path,matrix))
        distance += matrix[path[-1]][path[-2]]
    path.append(start_point)
    distance += matrix[path[-1]][path[-2]]
    return distance,path


def Greedy_Solution(graph):
     return find_path(0, 0, [], graph.matrix)