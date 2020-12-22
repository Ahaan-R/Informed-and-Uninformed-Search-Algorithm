# Ahaan Rajesh
# 1001768638
# AI 1: CSE-5360


import sys
from queue import PriorityQueue


def TakeInput(inputfile):
    graph = dict()
    try:
        input = open(inputfile, 'r')
        for line in input:
            line = line.rstrip('\n')
            line = line.rstrip('\r')
            if line == 'END OF INPUT':
                input.close()
                return graph
            else:
                data = line.split(' ')
                start = data[0]
                end = data[1]
                dist = float(data[2])
                graph.setdefault(start, {})[end] = dist
                graph.setdefault(end, {})[start] = dist
    except:
        print("No file found")


def TakeHeuristic(heuristicfile):
    HeuristicsData = dict()
    try:
        HeuristicFile = open(heuristicfile, 'r')
        for line in HeuristicFile:
            line = line.rstrip('\n')
            line = line.rstrip('\r')
            if line == 'END OF INPUT':
                HeuristicFile.close()
                return HeuristicsData
            else:
                data = line.split(' ')
                city = data[0]
                hvalue = float(data[1])
                HeuristicsData[city] = hvalue
    except:
        print("No Input file found")


def UninformedSearch(start, goal, graph):
    NodesExpanded = 0
    NodesGenerated = 0
    visited_nodes = set()
    queue = PriorityQueue()
    queue.put((0, [start]))
    NodesGenerated += 1
    final_path = dict()

    while queue:
        cost, path = queue.get()
        current = path[len(path) - 1]
        NodesExpanded += 1


        if current not in visited_nodes:
            visited_nodes.add(current)
            if current == goal:
                final_path['cost'] = cost
                final_path['path'] = path
                return FinalPathGen(NodesExpanded, NodesGenerated, graph, final_path)
            for child in graph[current]:
                temp = path[:]
                temp.append(child)
                NodesGenerated += 1
                queue.put((float(cost) + float(graph[current][child]), temp))


        if queue.empty():
            return FinalPathGen(NodesExpanded, NodesGenerated, graph, None)


def InformedA(start, goal, graph, heuristic):
    NodesExpanded = 0
    NodesGenerated = 0
    final_path = {}
    openSet = [start]
    cameFrom = {}

    gScore = {}
    fScore = {}

    for h in heuristic.keys():
        gScore[h] = float('inf')
        fScore[h] = float('inf')

    gScore[start] = 0
    fScore[start] = heuristic[start]
    fScore.values()
    while len(openSet) != 0:
        minim = float('inf')
        NodesExpanded += 1
        for node in openSet:
            if minim > fScore[node]:
                current = node
                minim = fScore[node]
        if current == goal:
            final_path['cost'] = 0
            final_path['path'] = []
            while current != "":
                if current == start:
                    final_path['path'].append(start)
                    final_path['path'].reverse()
                    return FinalPathGen(NodesExpanded, NodesGenerated + 1, graph, final_path)
                final_path['path'].append(current)
                final_path['cost'] += graph[current][cameFrom[current]]
                current = cameFrom[current]
        openSet.remove(current)
        for neighbor in graph[current].keys():
            NodesGenerated += 1
            tentative_gScore = gScore[current] + graph[current][neighbor]
            if tentative_gScore < gScore[neighbor]:
                cameFrom[neighbor] = current
                gScore[neighbor] = tentative_gScore
                fScore[neighbor] = gScore[neighbor] + heuristic[neighbor]
                if neighbor not in openSet:
                    openSet.append(neighbor)

    return FinalPathGen(NodesExpanded, NodesGenerated, graph, None)


def FinalPathGen(expanded, generated, graph, final_path):
    if final_path:
        print("Nodes Expanded:", expanded)
        print("Nodes Generated:", generated)
        print('Distance: ', final_path['cost'])
        print('Route: ')
        for i in range(len(final_path['path']) - 1):
            start = final_path['path'][i]
            end = final_path['path'][i + 1]
            cost = graph[final_path['path'][i]][final_path['path'][i + 1]]
            print(f'{start} to {end} : {cost} kms')
    else:
        print("Nodes Expanded:", expanded)
        print("Nodes Generated:", generated)
        print("Distance: infinity \nRoute: None")


def main():
    arg_l = len(sys.argv)
    if arg_l < 4 or arg_l > 5:
        print('Incorrect number of arguments\n')
        sys.exit()

    input_file = sys.argv[1]
    start = sys.argv[2]
    goal = sys.argv[3]
    graph = TakeInput(input_file)
    if start not in graph.keys():
        print('Start node is not present')
        sys.exit()
    if goal not in graph.keys():
        print('Destination node is not present')
        sys.exit()

    if arg_l == 4:
        UninformedSearch(start, goal, graph)
    elif arg_l == 5:
        heuristic_file = sys.argv[4]
        heuristic = TakeHeuristic(heuristic_file)
        InformedA(start, goal, graph, heuristic)


if __name__ == '__main__':
    main()