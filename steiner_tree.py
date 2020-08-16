import time

class Hex_Grid:
    '''
    Creates a hex grid (single hex=radius 0) centered at (0,0,0)
    where tiles can be empty, cities, obstacles or roads
    
    Tiles are represented by a tuple (i,j,k), where:
        i is the coordinate in the NW-SE axis
        j is the coordinate in the NE-SW axis
        k is the coordinate in the S-N axis
        
    Note: the coordinates always sum to 0
    '''
    def __init__(self, radius):
        #tiles stored as a dictionary from coordinates to state
        self.tiles=create_grid(radius)
        
    def set_cities(self, coord_list):
        for coord in coord_list:
            if coord in self.tiles.keys():
                self.tiles[coord]='city'
            else:
                print("Coord {} not in grid".format(coord))
            
    def set_obstacles(self, coord_list):
        for coord in coord_list:
            if coord in self.tiles.keys():
                self.tiles[coord]='obstacle'
            else:
                print("Coord {} not in grid".format(coord))
                
    def set_roads(self, coord_list):
        for coord in coord_list:
            if coord in self.tiles.keys():
                self.tiles[coord]='road'
            else:
                print("Coord {} not in grid".format(coord))
                
    def get_neighbors(self, tile):
        neighbors=[]
        current=(tile[0]+1,tile[1]-1,tile[2]) #right neighbor
        if current in self.tiles.keys():
            neighbors.append(current)
        current=nw_move(current)
        if current in self.tiles.keys():
            neighbors.append(current)
        current=w_move(current)
        if current in self.tiles.keys():
            neighbors.append(current)
        current=sw_move(current)
        if current in self.tiles.keys():
            neighbors.append(current)
        current=se_move(current)
        if current in self.tiles.keys():
            neighbors.append(current)
        current=e_move(current)
        if current in self.tiles.keys():
            neighbors.append(current)
        return neighbors
                
    def plot(self, labels=0):
        import matplotlib.pyplot as plt
        from matplotlib.patches import RegularPolygon
        import numpy as np
        
        coord = list(self.tiles.keys())
        color_code={'empty':'White', 'city':'Blue', 'obstacle':'Red', 'road':'Green'}
        colors = [color_code[self.tiles[c]] for c in coord]

        # Vertical cartesian coords
        vcoord = [c[2] for c in coord]
        # Horizontal cartersian coords
        hcoord = [2. * np.sin(np.radians(60)) * (c[0] - c[1]) /3. for c in coord]
        
        fig, ax = plt.subplots(1)
        ax.set_aspect('equal')
        # Add some coloured hexagons
        for x, y, c in zip(hcoord, vcoord, colors):
            color = c[0].lower()  # matplotlib understands lower case words for colours
            hex = RegularPolygon((x, y), numVertices=6, radius=2. / 3., 
                                 orientation=np.radians(0), 
                                 facecolor=color, alpha=0.2, edgecolor='k')
            ax.add_patch(hex) 
        # Also add scatter points in hexagon centres
        ax.scatter(hcoord, vcoord, c=[c[0].lower() for c in colors], alpha=0.5)
        plt.show()
        plt.clf()
        
    def __str__(self):
        mt=[[coord,state] for coord, state in self.tiles.items()]
        coords=[mt[i][0] for i in range(len(mt))]
        formated=format_tuples(coords)
        for i in range(len(mt)):
            mt[i][0]=formated[i]
        txt=''
        for i in range(len(mt)):
            txt+=mt[i][0]
            txt+=(' '*(9-len(mt[i][1])))
            txt+=mt[i][1]
            txt+='\n'
        return txt
            
#-----------------------------------------------------------------        
'''
Functions for Hex_Grid
'''

def create_grid(radius):
    tiles={(0,0,0):'empty'}
    for r in range(1,radius+1):
        current=(r,-r,0)
        for j in range(r):
            current=nw_move(current)
            tiles[current]='empty'
        for j in range(r):
            current=w_move(current)
            tiles[current]='empty'
        for j in range(r):
            current=sw_move(current)
            tiles[current]='empty'
        for j in range(r):
            current=se_move(current)
            tiles[current]='empty'
        for j in range(r):
            current=e_move(current)
            tiles[current]='empty'
        for j in range(r):
            current=ne_move(current)
            tiles[current]='empty'
    return tiles
            
def nw_move(old):
    return (old[0]-1,old[1],old[2]+1)

def w_move(old):
    return (old[0]-1,old[1]+1,old[2])

def sw_move(old):
    return (old[0],old[1]+1,old[2]-1)

def se_move(old):
    return (old[0]+1,old[1],old[2]-1)

def e_move(old):
    return (old[0]+1,old[1]-1,old[2])

def ne_move(old):
    return (old[0],old[1]-1,old[2]+1)


def format_tuples(tup_list):
    i_coords=[str(tup[0]) for tup in tup_list]
    j_coords=[str(tup[1]) for tup in tup_list]
    k_coords=[str(tup[2]) for tup in tup_list]
    
    i_len=max([len(i) for i in i_coords])
    j_len=max([len(j) for j in j_coords])
    k_len=max([len(k) for k in k_coords])
    
    str_list=[]
    
    for n in range(len(tup_list)):
        txt='('
        txt+=(' '*(i_len-len(i_coords[n])))
        txt+=str(i_coords[n])
        txt+=', '
        txt+=(' '*(j_len-len(j_coords[n])))
        txt+=str(j_coords[n])
        txt+=', '
        txt+=(' '*(k_len-len(k_coords[n])))
        txt+=str(k_coords[n])
        txt+=')'
        str_list.append(txt)
    
    return str_list

#-----------------------------------------------------------------
'''
Steiner tree implementation
'''
def steiner(points,grid):
    '''
    Function(set or list) -> set
    Returns the Steiner points to be added (without the original nodes)
    '''
    
    s0=list(points)[0]
    points=set(points)
    Q=[{s0}]    #Priority queue
    tested=[]
    cont=0
    
    while Q:
        current_tree=min(Q, key=lambda t:cost(t,points,grid))
        Q.remove(current_tree)
        cont+=1
        print("Size={}, attempt={}".format(len(current_tree),cont))
        if points.issubset(current_tree):
            return current_tree-points
        tested.append(current_tree)
        for n in tree_neighbors(current_tree,grid):
            tree_with_n=current_tree|{n}
            if tree_with_n not in tested:
                Q.append(tree_with_n)
    print("No tree found")
    return None

def tree_neighbors(tree,grid):
    '''
    Function(set)->set
    '''
    neighbors=set()
    for node in tree:
        neighbors.update(grid.get_neighbors(node))
    neighbors=neighbors-tree
    obstacles=set()
    for tile in neighbors:
        if grid.tiles[tile]=='obstacle':
            obstacles.add(tile)
    return neighbors-obstacles    

def cost(tree, points, grid):
    cost=0
    for p in points:
        if p not in tree:
            cost+=len(ax_to_tree(p,tree,grid))-1
    return cost
    
def ax_to_tree(start,tree,grid):
    '''
    Modified A* pathfinding algorithm
    instead of finding path from node A to node B,
    finds path from node A to any node in tree T
    '''
    queue={start:(0,None)} #dictionary from untested nodes to [distance to start, previous node]
    tested={} #dictionary from tested nodes to [distance to start, previous node]
    
    while queue:
        current=min(queue.keys(), key=lambda n:(queue[n][0]+min([distance(n,t) for t in tree])))
        g_current, parent=queue.pop(current)
        tested[current]=(g_current,parent)
        
        if current in tree:
            path=get_path(current,tested)
            return path
        
        for nb in grid.get_neighbors(current):
            if (nb not in tested.keys()) and grid.tiles[nb]!='obstacle':
                if (nb not in queue.keys()) or g_current+1<queue[nb][0]:
                    queue[nb]=(g_current+1,current)
    
    
def distance(A,B):
    return (abs(A[0] - B[0]) + abs(A[1] - B[1]) + abs(A[2] - B[2])) / 2

def get_path(end,graph):
    path={end}
    parent=graph[end][1]
    while parent:
        path.add(parent)
        parent=graph[parent][1]
    return path

#-----------------------------------------------------------------
'''
Main contains a basic usage example
Read comments on Hex_Grid class for an explanation
    on the coordinate system
'''    
   
def main():
    t0=time.time()
    grid=Hex_Grid(8)
    grid.set_cities([(0,1,-1),(2,0,-2),(-5,-2,7),(8,-8,0),(4,-8,4),(3,1,-4)])
    grid.set_obstacles([(-2,1,1),(-1,0,1),(0,-1,1),(1,-2,1),(2,-3,1),(1,1,-2),(1,2,-3),(1,3,-4),(3,-8,5)])
    grid.plot()
    roads=steiner([(0,1,-1),(2,0,-2),(-5,-2,7),(8,-8,0),(4,-8,4),(3,1,-4)],grid)
    if roads:
        grid.set_roads(roads)
    grid.plot()
    print("Time={}".format(time.time()-t0))
    

if __name__ == "__main__":
    main()
