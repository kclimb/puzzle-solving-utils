# puzzle-solving-utils
 
I like speedrunning adventure games. Sometimes these games use and reuse stock puzzles (or have puzzles that reduce to a stock puzzle). I've built ad-hoc scripts to find optimal solutions to these puzzles, but I made this repo to try to get semi-serious at developing more generalized scripts to save time going forward.

## Currently in this repo:
### heapq_astar.py:
A python (lol) implementation of A* using the heapq python module to hold the closed set.  
Any puzzle that reduces to graph search (so many stock puzzles are really just graph search it turns out!) can take advantage of this.
