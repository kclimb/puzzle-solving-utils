import heapq
import time

ENTRY_FINDER = {} # Used by heap functions

def heap_add(heap, pri_board_tup):
    """
    Wrapper around heapq's heappush method to support updating priorities of items
    already in the queue.

    ENTRY_FINDER caches references to the exact tuple objects we add to the queue.
    We do this so that when we resubmit a board to the queue (to update its priority),
    we can use the reference to the original tuple to mark the older priority as stale.
    """
    board = pri_board_tup[1]
    if board in ENTRY_FINDER:
        mark_entry_removed(board)
    ENTRY_FINDER[board] = pri_board_tup
    heapq.heappush(heap, pri_board_tup)

def mark_entry_removed(board):
    """
    We can only remove the smallest element of the priority queue. If we want
    to update the priority of an arbitrary element, we mark the old priority
    as deleted, and then elsewhere we resubmit the element with its new priority
    to the queue. This lets us preserve the heap invariant.
    """
    oldentry = ENTRY_FINDER.pop(board)
    #print 'removal:', oldentry
    oldentry[1] = None # Mark the board as invalid to signal this priority is stale.

def heap_pop(heap):
    """
    Wrapper around heapq's heappop method to support updating priorities of
    items in the queue.

    Main difference here is that we toss out any queue entries that have been
    updated since insertion.
    """
    while len(heap) > 0:
        pri_board_tup = heapq.heappop(heap)
        board = pri_board_tup[1]
        if not board == None:
            del ENTRY_FINDER[board]
            return pri_board_tup
    raise KeyError('Pop from empty queue :(')

def astar(start, is_end, get_nbrs, h=None):
    """
    Does astar search until a valid end node is found, or all reachable nodes
    from the start node have been searched.

    Parameters:
        start    - the node to begin the search from
        is_end   - a function is_end(node) that returns whether 'node' meets the
                   goal criteria of the search
        get_nbrs - a function get_nbrs(node) that returns all nodes immediately
                   reachable from 'node'
        h        - a function that estimates the distance from 'node' to a state
                   that meets the goal criteria. h(node) must always be <= the
                   actual distance from 'node' to any goal state.
                   If not supplied, then it's assumed h(node) = 0 for all inputs
    """
    g = {start: 0}
    f = []
    if h == None:
        h = lambda x : 0
    heap_add(f, (h(start),start))

    #minf = -1
    openset = set([start])
    closedset = set([])
    parents = {start: None}
    pushloc = None

    starttime = time.time()
    while len(openset) > 0:

        cur = heap_pop(f)
        #if cur[0] > minf:
            #if cur[0] - minf > 0.02:
                #print "New lower bound on solution:", minf, "found after",time.time()-starttime,"seconds"
                #print 'closed:',len(closedset)+1
                #print 'open:',len(openset)-1
                #print_board(cur[1])
            #else:
            #    minf = cur[0]
        if is_end(cur[1]):
            #print 'closed:',len(closedset)+1
            #print 'open:',len(openset)-1
            #print 'search took',time.time()-starttime,'seconds'
            return cur, parents
        #print 'CUR:', cur[0],cur[1]
        cur = cur[1] # We don't need the distance anymore if not returning
        #for guy in openset:
        #    print guy
        openset.remove(cur)
        #if cur in closedset:
        #    print 'Error: duplicate board in closedset:', cur
        closedset.add(cur)

        for nbr,edge_cost in get_nbrs(cur):
            if nbr not in closedset:
                if nbr not in openset:
                    openset.add(nbr)
                    g[nbr] = g[cur] + edge_cost
                    parents[nbr] = cur
                    heap_add(f, [h(nbr)+g[nbr],nbr])
                else:
                    new_g = g[cur] + edge_cost
                    if new_g < g[nbr]:
                        g[nbr]=new_g
                        parents[nbr] = cur
                        heap_add(f, [h(nbr)+g[nbr],nbr])
        del g[cur] # once a node's in the closedset, we don't care about its g cost anymore. we delete to save a marginal amount of space in this very space-inefficient algorithm

    return (),parents

def get_path(parents, end):
    """
    Returns a list starting with the start node implied by the parents dictionary,
    and ending with the specified end node.

    If no path exists, returns an empty list.

    Parameters:
        parents - a dictionary rooted at an arbitrary graph node, "start".
                    parents[start] = None
                    parents[some_other_node] = preceding node on shortest path
                    from start to some_other_node
        end - the node we want to find the path to
    """
    path = [end]
    if end in parents:
        endpar = parents[end]
    else:
        return path
    while not endpar == None:
        path.append(endpar)
        endpar = parents[endpar]
    path.reverse()
    return path
