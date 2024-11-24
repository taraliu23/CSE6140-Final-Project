# CSE6140-Final-Project

## Project Objectives

Solve TSP(Traveling Salesman Problem) with different algorithms and evaluate running times.

## Problem: TSP

Given x-y coordinates of N points in the plane, find the shortest simple cycle that visit all N points.

In graph G:

- Vertices: N points
- Edges: travel route
- Weight: Euclidean distance
- Direction: Undirected, and all edges costs are symmetric

## Algorithm

1. **Exact**: brute-force with a time cut-off. 
	- end time T=300s, then exit
	- output: solution found so far

2. **Approximate**: 2-approximation algorithm
	- guarantee quality
	- based on MST (Minimum Spanning Tree)

3. **Local Search**: heuristic algorithm
	- without guarantees
	- effective in practice
	- *e.g.:* Hill climbing, simulated annealing, evolutionary algo, neural networks

## Input Data

columns: id, x, y

## Programming Style
1. Include a top comment that explains what the given file does.

2. Be well-commented and self-explanatory.

3. Create an executable from code `exec.py`
	- Any run of executable with the three or four inputs (filename, cut-off time,method, and if applicable based on method, seed) must produce an output file in the current working directory.

4. Output format: 
	- name: `⟨instance⟩ ⟨method⟩ ⟨cutof f ⟩ [⟨random seed⟩].sol`
	- file: 
		line 1: `float`, quality of best solution found
		line 2: list of vertex iDs for the TSP tour, comma-separated

## Deliverables

1. `report.pdf`
2. `results.csv`(corresponding to the table in pdf 1)
3. `{name}.zip`/
	- `code/` *contain all code and exec*
	- `output/`
	- `evaluation.txt` score 1-10 and justification