###########################               
#script by Zhengyang Chen #        
#tel: +86 13818034245     #
#wechat: czy4050715       #
#########    +1s   ########
###########################


#import rhino modules and delete ovelap tool

import rhinoscriptsyntax as rs
import czy_delete_overlaps as ov


#defines
OK=0
ERROR=-1
TRUE=1
FALSE=0
OVERFLOW=-2

MAX=99999999999999 # indicates the +∞
SCALE=50000 

#struct closedge
class closedge:
    def __init__(self):
        self.len=0
        self.adjvex=[] #point
        self.lowcost=[] #min value of the weight

#struct graph
class Graph:
    def __init__(self):
        self.vertex=[]  #the vertex in the Graph
        self.vexnum=0   #number of the vertex, or just len(self.vertex)
        self.arcnum=0   #number of the edges
        self.arc=[[]]   #edge information in matrix
        self.edges=[]   #the edge in the Graph (exact curves in rhino)
        


#display the matrix for test run
def matdisplay(G):
    
    #define the origin of the matrix display panel
    opt=rs.GetObject("choose display o point", rs.filter.point)
    
    #display the imported matrix
    for i in range(len(G.arc)):
        for j in range(len(G.arc[i])):
            if G.arc[i][j]<MAX:
                rs.AddText(int(G.arc[i][j]),rs.PointAdd(opt,(i*SCALE,j*SCALE,0)),0.2*SCALE)
            else:
                rs.AddText("MAX",rs.PointAdd(opt,(i*SCALE,j*SCALE,0)),0.2*SCALE)
                #if the no path,print "MAX"
    return OK
    

#read in the graph
def _read():
    
    #followings to be modified
    """objs=rs.GetObjects("get the graph")
    
    #clearbin=ov.pool(objs)
    
    #pts=ov.delobj(clearbin).pts
    #crvs=ov.delobj(clearbin).crvs"""
    
    #get vertex and edges
    pts=rs.GetObjects("points",rs.filter.point)
    crvs=rs.GetObjects("curves",rs.filter.curve)
    
    
    #call graph
    G=Graph()
    
    #store the vertex
    for pt in pts:
        _defdisplay(pt)
        G.vertex.append(pt)
    
    for crv in crvs:
        _defdisplay(crv)
        G.edges.append(crv)
        
    #init the matrix
    mat=[[MAX for i in range(len(pts))] for j in range(len(pts))]
    for crv in crvs:
        stpt=rs.CurveStartPoint(crv)
        edpt=rs.CurveEndPoint(crv)
        for i in range(len(pts)):
            if rs.PointCompare(stpt,pts[i])==True:
                for j in range(len(pts)):
                    if rs.PointCompare(edpt,pts[j])==True:
                        mat[i][j]=rs.CurveLength(crv)
                        mat[j][i]=mat[i][j]
    
    #Store the graph
    G.arc=mat
    G.vexnum=len(pts)
    G.arcnum=len(crvs)
    
    
    #IF TEST-matdisplay(G)
    #print G.vexnum, G.arcnum
    
    return G

def locateVex(G,stpt):
    k=0
    
    #return the item value of the pt
    for pt in G.vertex:
        
        if rs.PointCompare(pt,stpt)==True:
            return k
        k+=1
    #if not found
    print "not found"
    return ERROR

#return the minimum value position in the tuple closedge
def minnum(closedge):
    min=MAX
    pos=0
    for i in range(closedge.len):
        #print i
        if closedge.lowcost[i]<MAX and closedge.lowcost[i]<>0:
            min=closedge.lowcost[i]
            pos=i
    return pos

#display the graph in black
def _defdisplay(obj):
    rs.ObjectColor(obj,[0,0,0])
    return OK
#display the minimum spining tree in red    
def _display(obj):
    rs.ObjectColor(obj,[255,0,0])
    return OK
            
class _mintree():
    #two different algorithm of mintree
    
    def prim(self,G,stpt):
        #prim algorithm
        clsedge=closedge()
        
        for i in range(G.vexnum):
            clsedge.len+=1
            clsedge.adjvex.append((0,0,0))
            clsedge.lowcost.append(0)
        k=locateVex(G,stpt)
        
        #init the tuple closedge
        for j in range(G.vexnum):
            if j<>k:
                clsedge.adjvex[j]=stpt
                clsedge.lowcost[j]=G.arc[k][j]
                
        clsedge.lowcost[k]=0
        
        #next points
        lines=[]
        for i in range(G.vexnum-1):
            k=minnum(clsedge)
            #edges output
            
            lines.append(rs.AddLine(G.vertex[k],clsedge.adjvex[k]))
            
            clsedge.lowcost[k]=0
            for j in range(G.vexnum):
                if G.arc[k][j]<clsedge.lowcost[j]:
                    clsedge.lowcost[j]=G.arc[k][j]
                    clsedge.adjvex[j]=G.vertex[k]
        print "finish"
        #display
        compare=ov._compare()
        
        for line in lines:
            _display(line)
        
        #delete duplicated lines to show red spining tree
        crvs=lines
        crvs.extend(G.edges)
        for i in range(len(crvs)):
            for j in range(i+1,len(crvs)):
                if rs.IsCurve(crvs[i]) and rs.IsCurve(crvs[j])\
                and compare.curve(crvs[i],crvs[j])==True:
                    #count+=1
                    _display(crvs[i])
                    rs.DeleteObject(crvs[j])
        
            
        return OK
        
    def krus(self,mat):
        #kruscal algorithm, to be modified
        return OK
        
    


#main function

def main():
    
    mat=_read()
    #pt=rs.GetObject("test pt",rs.filter.point)
    #locateVex(mat,pt)
    mintree=_mintree()
    stpt=rs.GetObject("start point",rs.filter.point)
    mintree.prim(mat,stpt)
    
    return OK

main()
