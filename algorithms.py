import queue
import pygame

def heuristic(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x2-x1) + abs(y2-y1)

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def algorithm(draw, grid, start, end):
    count = 0
    pq = queue.PriorityQueue()
    pq.put((0, count, start)) # (total_score_with_heuristic, count, node)
    origin = {}
    actual_distance_without_heuristic = {cell: float('inf') for row in grid for cell in row}
    actual_distance_without_heuristic[start] = 0
    total_score_with_heuristic = {cell: float('inf') for row in grid for cell in row}
    total_score_with_heuristic[start] = heuristic(start.position(), end.position())
    
    in_pq = {start} # to keep track of nodes in the pq
     
    while not pq.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
        current = pq.get()[2]
        in_pq.remove(current)
        
        if current == end:
            reconstruct_path(origin, end, draw)
            end.make_end()
            start.make_start()
            return True
        
        for neighbor in current.neighbors:
            temp_acutal_distance = actual_distance_without_heuristic[current] + 1
            
            if temp_acutal_distance < actual_distance_without_heuristic[neighbor]: 
                origin[neighbor] = current
                actual_distance_without_heuristic[neighbor] = temp_acutal_distance
                total_score_with_heuristic[neighbor] = temp_acutal_distance + heuristic(neighbor.position(), end.position())
                
                if neighbor not in in_pq:
                    count += 1
                    pq.put((total_score_with_heuristic[neighbor], count, neighbor))
                    in_pq.add(neighbor)
                    neighbor.make_open()
                    
        draw()
        
        if current != start:
            current.make_closed()
            
    return False