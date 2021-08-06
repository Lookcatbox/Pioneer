import random

from BiomeBasic import *
from EntidyClass import *
data=[]
vis=[]
a=[]
vis2=[]
fl=[]
visit=[]
BlockEntidies={}

for i in range(4007):
    data.append(bas[i][:])
    vis.append(bas[i][:])
    a.append(bas[i][:])
    vis2.append(bas[i][:])
    fl.append(bas[i][:])
    visit.append(bas[i][:])

class P:
    def __init__(self,xx=0,yy=0):
        self.x=xx
        self.y=yy
class Queue:
    def __init__(self):
        self.clear()
    def clear(self):
        self.d=[]
        self.f=self.l=0
    def push(self,x):
        self.d.append(x)
        self.l+=1
    def front(self):
        return self.d[self.f]
    def pop(self):
        self.f+=1
    def empty(self):
        return self.f==self.l
              
dx=[0,1,0,-1]
dy=[1,0,-1,0]
#int size , beside , las ;
size=beside=las=0

"""	void Lake_Bfs(int x,int y,int col);
	void SpawnBiome (int x , int y , int worldseed) ;
	void Bfs (int x , int y , int col) ;
	void Fill (int x , int y , int col) ;
	void CountSize (int x , int y) ;
	void Fill2 (int x , int y , int col , bool flag) ;"""
def SimilarBiome(x):
    if x==1:
        return 2
    if x==2:
        return 1
    if x==3:
        return 4
    if x==4:
        return 3
    if x==5:
        return 6
    if x==6:
        return 9
    if x==7:
        return 8
    if x==8:
        return 7
    if x==9:
        return 5
    if x==10:
        return 11
    if x==11:
        return 10
    if x==17:
        return 17
    if x==18:
        return 18

def SpawnBiome(worldseed):
    global data,vis,a,fl,las,size,beside
    random.seed(worldseed)
    for i in range(1,MAXN+1):
        for j in range(1,MAXN+1):
            a[i][j]=random.randint(1,10000)
    data=[]
    vis=[]
    fl=[]

    for i in range(4007):
        data.append(bas[i][:])
        vis.append(bas[i][:])
        fl.append(bas[i][:])
    las=0
    print "Biome Module Init Ended"
    for i in range(1,MAXN+1):
        for j in range(1,MAXN+1):
            if not data[i][j]:
                col=random.randint(1,BiomeKinds)
                if random.randint(0,9999)<9900 and las:
                    col=SimilarBiome(las)
                las=col
                size=0
                beside=1
                Bfs(i,j,col)
                if size<MinBiomeBlock:
                    Fill(i,j,beside)
                else:
                    Fill(i,j,col)
    print "Once Filling Biome"
    for i in range(1,MAXN+1):
        for j in range(1,MAXN+1):
            if not fl[i][j]:
                size=0
                CountSize(i,j)
                if size<MinBiomeBlock:
                    Fill2(i,j,SimilarBiome(beside),1)
                else:
                    Fill2(i,j,beside,0)
    print "Secondary Fills Biome"
    River()
    print "River Has Been Made"
    for i in range(1,MAXN+1):
        for j in range(1,MAXN+1):
            if land[i][j]:
                data[i][j]=17
    fl=[]
    for i in range(4007):
        fl.append(bas[i][:])
    for i in range(1,MAXN+1):
        for j in range(1,MAXN+1):
            if not fl[i][j]:
                size=0
                CountSize(i,j)
                if size<Min_in_River and data[i][j]<=16:
                    Fill2(i,j,SimilarBiome(beside),1)
                else:
                    Fill2(i,j,beside,0)
    print "Third Fills Biome"
    fl=[]
    for i in range(4007):
        fl.append(bas[i][:])
    for i in range(1,MAXN+1):
        for j in range(1,MAXN+1):
            if not fl[i][j]:
                size=0
                CountSize(i,j)
                if size<Min_in_River and data[i][j]<=16 and beside<=16:
                    Fill2(i,j,SimilarBiome(beside),1)
                else:
                    Fill2(i,j,beside,0)
    print "Fourth Fills Biome"
    for i in range(1,MAXN+1):
        for j in range(1,MAXN+1):
            if data[i][j]==1 or data[i][j]==2:
                if random.randint(1,10)==1:
                    SetBlockentidy(BlockEntidies,Tree(i+0.5,j+0.5,0,0))
    print "Tree Had Been Placed"
def Bfs(x,y,col):
    global size,data,vis
    size=1
    q=Queue()
    q.push(P(x,y))
    if data[x][y]:
        return
    data[x][y]=vis[x][y]=col
    while not q.empty():
        k=q.front()
        q.pop()
        for i in range(4):
            nx=k.x+dx[i]
            ny=k.y+dy[i]
            if nx<1 or nx>MAXN or ny<1 or ny>MAXN:
                continue
            if data[nx][ny]:
                beside=data[nx][ny]
                continue
            if random.randint(1,30000)==1:
                break
            if random.randint(0,9999)<a[nx][ny]:
                q.push(P(nx,ny))
                data[nx][ny]=vis[nx][ny]=col
                size+=1
                if size>MaxBiomeBlock:
                    return
def Fill(x,y,col):
    global vis,data
    vis[x][y]=0
    data[x][y]=col
    for i in range(4):
        nx=x+dx[i]
        ny=y+dy[i]
        if nx<1 or nx>MAXN or ny<1 or ny>MAXN:
            continue
        if vis[nx][ny]:
            Fill(nx,ny,col)
def CountSize(x,y):
    global vis2,fl,size
    vis2[x][y]=fl[x][y]=1
    size+=1
    for i in range(4):
        nx=x+dx[i]
        ny=y+dy[i]
        if nx<1 or nx>MAXN or ny<1 or ny>MAXN:
            continue
        if data[nx][ny]:
            beside=data[nx][ny]
            continue
        if data[nx][ny]==data[x][y] and not vis2[nx][ny]:
            CountSize(nx,ny)
def Fill2(x,y,col,flag):
    global vis2,data
    vis2[x][y]=0
    if flag:
        data[x][y]=col
    for i in range(4):
        nx=x+dx[i]
        ny=y+dy[i]
        if nx<1 or nx>MAXN or ny<1 or ny>MAXN:
            continue
        if vis2[nx][ny]:
            Fill2(nx,ny,col,flag)
"""
	void Bfs (int x , int y , int col) {
		size = 1 ;
		std::queue <P> q ;
		q.push (P (x , y)) ;
		if (data[x][y]) return ;
		data[x][y] = vis[x][y] = col ;
		while (!q.empty ()) {
			P k = q.front () ;
			q.pop () ;
			for (int i = 0 ; i < 4 ; i++) {
				int nx = k.x + dx[i] , ny = k.y + dy[i] ;
				if (nx < 1 || nx > MAXN || ny < 1 || ny > MAXN) continue ;
				if (data[nx][ny]) {
					beside = data[nx][ny] ;
					continue ;
				}
				if (Rand () % 30000 == 1) break ;
				if (Rand () % 10000 < a[nx][ny]) {
					q.push (P (nx , ny)) ;
					data[nx][ny] = vis[nx][ny] = col ;
					size++ ;
					if (size > MaxBiomeBlock) return ;
				}
			}
		}
	}
	void Lake_Bfs (int x , int y , int col) {
		size = 1 ;
		std::queue <P> q ;
		q.push (P (x , y)) ;
		land[x][y] = vis[x][y] = col ;
		while (!q.empty ()) {
			P k = q.front () ;
			q.pop () ;
			for (int i = 0 ; i < 4 ; i++) {
				int nx = k.x + dx[i] , ny = k.y + dy[i] ;
				if (nx < 1 || nx > MAXN || ny < 1 || ny > MAXN) continue ;
				if (Rand () % 30000 == 1) break ;
				if (Rand () % 10000 < a[nx][ny]) {
					q.push (P (nx , ny)) ;
					land[nx][ny] = vis[nx][ny] = col ;
					size++ ;
					if (size > Lake_Max) return ;
				}
			}
		}
	}
	void Fill (int x , int y , int col) {
		vis[x][y] = 0 ;
		data[x][y] = col ;
		for (int i = 0 ; i < 4 ; i++) {
			int nx = x + dx[i] , ny = y + dy[i] ;
			if (nx < 1 || nx > MAXN || ny < 1 || ny > MAXN) continue ;
			if (vis[nx][ny]) Fill (nx , ny , col) ;
		}
	}
	void Lake_Fill (int x , int y , int col) {
		vis[x][y] = 0 ;
		land[x][y] = col ;
		for (int i = 0 ; i < 4 ; i++) {
			int nx = x + dx[i] , ny = y + dy[i] ;
			if (nx < 1 || nx > MAXN || ny < 1 || ny > MAXN) continue ;
			if (vis[nx][ny]) Lake_Fill (nx , ny , col) ;
		}
	}
	void CountSize (int x , int y) {
		vis2[x][y] = fl[x][y] = 1 ;
		size++ ;
		for (int i = 0 ; i < 4 ; i++) {
			int nx = x + dx[i] , ny = y + dy[i] ;
			if (nx < 1 || nx > MAXN || ny < 1 || ny > MAXN) continue ;
			if (data[nx][ny] != data[x][y]) {
				beside = data[nx][ny] ;
				continue ;
			}
			if (data[nx][ny] == data[x][y] && !vis2[nx][ny]) CountSize (nx , ny) ;
		}
	}
	void Fill2 (int x , int y , int col , bool flag) {
		vis2[x][y] = 0 ;
		if (flag) data[x][y] = col ;
		for (int i = 0 ; i < 4 ; i++) {
			int nx = x + dx[i] , ny = y + dy[i] ;
			if (nx < 1 || nx > MAXN || ny < 1 || ny > MAXN) continue ;
			if (vis2[nx][ny]) Fill2 (nx , ny , col , flag) ;
		}
	}
}"""


#River

riverdirect=[[0,1,2,3],[0,1,3,2],[0,2,1,3],[0,2,3,1],[0,3,1,2],[0,3,2,1], \
             [1,0,2,3],[1,0,3,2],[1,2,0,3],[1,2,3,0],[1,3,0,2],[1,3,2,0], \
             [2,0,1,3],[2,0,3,1],[2,1,0,3],[2,1,3,0],[2,3,0,1],[2,3,1,0], \
             [3,0,1,2],[3,0,2,1],[3,1,0,2],[3,1,2,0],[3,2,0,1],[3,2,1,0]  \
             ]

def River():
    for i in range(RiverN):
        cs_x=random.randint(1,MAXN)
        cs_y=random.randint(1,MAXN)
        _lx=random.randint(0,23)
        dfs(cs_x,cs_y,_lx,i,0)
def Lake_Bfs(x,y,col):
    global size,land,vis
    size=1
    q=Queue()
    q.push(P(x,y))
    land[x][y]=vis[x][y]=col
    while not q.empty():
        k=q.front()
        q.pop()
        for i in range(4):
            nx=k.x+dx[i]
            ny=k.y+dy[i]
            if nx<1 or nx>MAXN or ny<1 or ny>MAXN:
                continue
            if data[nx][ny]:
                beside=data[nx][ny]
                continue
            if random.randint(1,30000)==1:
                break
            if random.randint(0,9999)<a[nx][ny]:
                q.push(P(nx,ny))
                land[nx][ny]=vis[nx][ny]=col
                size+=1
                if size>Lake_Max:
                    return
def Lake_Fill(x,y,col):
    global vis,data
    vis[x][y]=0
    land[x][y]=col
    for i in range(4):
        nx=x+dx[i]
        ny=y+dy[i]
        if nx<1 or nx>MAXN or ny<1 or ny>MAXN:
            continue
        if vis[nx][ny]:
            Lake_Fill(nx,ny,col)
def dfs(x,y,k,color,le):
    global las,size,beside
    if x<1 or y<1 or x>MAXN or y>MAXN:
        return
    if le>River_Max:
        las=color
        size=0
        beside=1
        Lake_Bfs(x,y,color)
        Lake_Fill(x,y,Fill)
        return
    if land[x][y] and land[x][y]!=color and land[x][y]<=32767:
        return
    if not land[x][y]:
        circle(x,y,random.randint(2,5),color)
    land[x][y]=color
    if random.randint(0,3)==0:
        dfs(x+dx[riverdirect[k][0]],y+dy[riverdirect[k][0]],k,color,le+1)
    elif random.randint(0,3)==1:
        dfs(x+dx[riverdirect[k][1]],y+dy[riverdirect[k][1]],k,color,le+1)
    elif random.randint(0,3)==2:
        dfs(x+dx[riverdirect[k][2]],y+dy[riverdirect[k][2]],k,color,le+1)
    else:
        dfs(x+dx[riverdirect[k][3]],y+dy[riverdirect[k][3]],k,color,le+1)
    
def circle(x,y,r,color):
    for i in range(y-r/2,y+r/2+1):
        paint(x+r-1,i,color+35767)
        paint(x-r+1,i,color+35767)
    for i in range(x-r/2,x+r/2+1):
        paint(i,y+r-1,color+35767)
        paint(i,y-r+1,color+35767)
    for i in range(x+r/2+1,x+r-1):
        for j in range(y-r+2,y-r/2):
            paint(i,j,color+35767)
        for j in range(y-r/2+1,y+r-1):
            paint(i,j,color+35767)
    for i in range(x-r+2,x-r/2):
        for j in range(y-r/2+1,y+r-1):
            paint(i,j,color+35767)
        for j in range(y-r+2,y-r/2):
            paint(i,j,color+35767)
    Full(x,y,color+35767)
    Clearvisit(x,y)
def paint(x,y,color):
    if x>0 and x<=MAXN and y>0 and y<=MAXN:
        visit[x][y]=1
def Full(x,y,color):
    if x>0 and x<=MAXN and y>0 and y<=MAXN:
        if not land[x][y]:
            land[x][y]=color
        if visit[x][y]:
            return
        visit[x][y]=1
        Full(x+1,y,color)
        Full(x-1,y,color)
        Full(x,y+1,color)
        Full(x,y-1,color)
def Clearvisit(x,y):
    if x>0 and x<=MAXN and y>0 and y<=MAXN:
        if not visit[x][y]:
            return
        visit[x][y]=0
        Clearvisit(x+1,y)
        Clearvisit(x-1,y)
        Clearvisit(x,y+1)
        Clearvisit(x,y-1)
