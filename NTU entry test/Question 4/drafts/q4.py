pixel_set=[(1, 0), (4, 0), (5, 0), (6, 0), (9, 0), (2, 1), (5, 1), (6, 1), (7, 1), (1, 2), (2, 2), (5, 2), (8, 2), (9, 2), (2, 3), (4, 3), (5, 3), (8, 3), (0, 4), (2, 4), (3, 4), (8, 4), (9, 4), (0, 5), (2, 5), (3, 5), (5, 5), (7, 5), (2, 6), (6, 6), (7, 6), (9, 6), (8, 7), (9, 7), (1, 8), (2, 8), (9, 8), (0, 9), (1, 9), (8, 9), (9, 9), (2, 10), (3, 10), (4, 10), (0, 11), (4, 11), (6, 11), (7, 11), (2, 12), (4, 12), (6, 12), (7, 12), (8, 12), (9, 12), (0, 13), (5, 13), (0, 14), (1, 14), (3, 14), (4, 14), (9, 14), (0, 15), (3, 15), (4, 15), (3, 16), (4, 16), (5, 16), (8, 16), (1, 17), (5, 17), (6, 17), (7, 17), (8, 17), (0, 18), (2, 18), (3, 18), (4, 18), (7, 18), (8, 18), (0, 19), (3, 19), (4, 19), (5, 19), (6, 19), (7, 19), (9, 19)]
i=0

adjacency_set=[]
while i< len(pixel_set):
    xy=pixel_set[i]
    x=xy[0]
    y=xy[1]
    adjacency_set_unconfirmed = [(x,y),(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
    adjacency_set_confirmed=[]
    for pixel in adjacency_set_unconfirmed:
        if pixel in pixel_set:
            adjacency_set_confirmed.append(pixel)
    adjacency_set.append(adjacency_set_confirmed)
    i+=1
print(len(pixel_set), len(adjacency_set))
# should be 86,86

# all we need to do is to simplify the set to make sure all connected points are in the same set.
points_unvisited=pixel_set # We make a list for all points
adjacency_set_untrimed=adjacency_set
adjacency_set_trimed=[]
print(len(points_unvisited), len(adjacency_set_untrimed), len(adjacency_set_trimed))

for point in points_unvisited:
    # for each point, we want their adj_points to be removed and added to a new trimed adj_set
    adj_merged=set()
    for adj_set in adjacency_set_untrimed:  # we screen all adj_sets
        if point in adj_set:                # find the matched adj_set
            for adj_point in adj_set:       # remove all adj_points
                print(adj_point)
                points_unvisited.remove(adj_point)
                adj_merged.add(adj_point)   # add each adj_point to new adj_points set
        adjacency_set_untrimed.remove(adj_set)  # removed the trimed adj_set
    # for each point, we have a full list of adjacency_set_trimed until it finish emmuration 
    adjacency_set_trimed.append(adj_merged)
    
print(len(points_unvisited), len(adjacency_set_untrimed), len(adjacency_set_trimed))
# should be 0, 0, 32