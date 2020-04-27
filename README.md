# TSPUsingACO
Metaheuristic solution to TSP
This is the project i made(with the collegue of mine) for Advanced Algorithms class. It uses Ant Colony Optimalization aproach.
It means that we create 'ants' which traverse the graph, picking the next vertex based on the distance and the 'populatiry' of 
the aviable vertices. The popularity is calulated by the number of ants that have picked the fragment of the given path before.
Since we simulate the natue, the ants may not choose the path that we think is the best at the moment(although this variant has the 
highest probability). This is done on purpose, because we might discover some new, better paths. 
