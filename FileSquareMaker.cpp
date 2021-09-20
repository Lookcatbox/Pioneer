#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
int world_seed,seed;
int biome[600][600],mineral[600][600];
int river[600][600],river_seed,nearby[600][600];
int conside[600][600],entidy[600][600];
int square_x,square_y;
int biome_catch;
int plant_born[310][2][2],plant[600][600];
int Rand(int zydx,int zydy) {
	int sd=(zydx*998776019LL+zydy*761824979LL+seed*379221113LL)%597279797LL;
	srand(sd);
	seed=sd;
	return rand();
}
struct Point {
	int x,y,col;
};
bool Check(int fz,int fm) {
	if(!fm&&!fz) return 0;
	seed=(1ll*fm*fz%998244353+1ll*114514*fm%998244353)%(1000000007);
	int rd=Rand(fz,fm)%fm;
	return rd<fz;
} 
void DownPut(int t1,int t2,int a1,int a2) {
	plant_born[t1][t2][0]=a1;
	plant_born[t1][t2][1]=a2;
}
void ResetPlantBorn() {
	//植物生成概率 0是灌木 1是树木 
	DownPut(1,0,3,1024);
	DownPut(2,0,4,256),DownPut(2,1,2,256);
	DownPut(3,0,30,256),DownPut(3,1,100,256);
	DownPut(5,0,5,2048),DownPut(5,1,3,2048);
	DownPut(7,0,3,512),DownPut(7,1,1,256);
	DownPut(9,0,5,256),DownPut(9,1,10,256);
	DownPut(10,0,15,512),DownPut(10,1,15,512);
	DownPut(12,0,5,512),DownPut(12,1,1,256);
	DownPut(103,0,60,1024),DownPut(103,1,15,1024);
}
bool operator<(Point a1,Point a2) {
	return a1.x==a2.x?(a1.y==a2.y?a1.col<a2.col:a1.y<a2.y):(a1.x<a2.x);
}
map<Point,Point> river_know,biome_know;
const double P = 0.50 ;
double a[700][700] , b[700][700] ;
ll c[700][700] ;
int cross[9][2]= {{0,1},{0,-1},{1,0},{-1,0},{-1,-1},{-1,1},{1,-1},{1,1},{0,0}};
inline int TY(int num) {
	return num-square_y;
}
inline int TX(int num) {
	return num-square_x;
}
inline void output(int num) {
	putchar(num>>8);
	putchar(num&0xff);
}

inline void input(int& num) {
	int c1=getchar(),c2=getchar();
	num=(c1<<8)+c2;
}
void Special_Create(Point& tmp,int type) {
	int roll=Rand(tmp.x,tmp.y)%1000;
	if(type==1) {//湖泊，以及沼泽
		if(roll<20 || (tmp.col==12 && roll<50)) {
			if(tmp.col==3&&(Rand(tmp.x,tmp.y)%100<15)) tmp.col=102;
			else tmp.col=17;
		}
	}
	if(type==2) {//雪原针叶林
		if(roll<100&&tmp.col==5) tmp.col=103;
	}
	if(type==3) {//岩浆湖
		if(((roll<4)||
		        (tmp.col==6&&roll<20))||
		        (tmp.col==1&&roll<10)) tmp.col=104;
	}
	if(type==4) {//中型岛屿
		if(roll<10) tmp.col=105;
	}
	if(type==5) {//小型岛屿
		if(roll<2) tmp.col=105;
	}
}
Point GetPoint(int s_x,int s_y,int len);
void UnrealLoad(int s_x,int s_y,Point& now,int len) {
	seed=world_seed;
	len*=4;
	ll min_len=1e12;
	Point min_close;
	s_x=s_x/len*len,s_y=s_y/len*len;
	for(int i=0; i<9; i++) {
		if(s_x+cross[i][0]*len<0||s_y+cross[i][1]*len<0) continue;
		Point tmp=GetPoint(s_x+cross[i][0]*len,s_y+cross[i][1]*len,len);
		ll far=pow(abs(tmp.x-now.x),2)+pow(abs(tmp.y-now.y),2);
		if(far<min_len) min_len=far,min_close=tmp;
	}
	now.col=min_close.col;
}

Point GetPoint(int s_x,int s_y,int len) {
	if(biome_know.count((Point) {s_x,s_y,len})) return biome_know[(Point) {s_x,s_y,len}];
	seed=world_seed;
	Point tmp;
	tmp.x=s_x+Rand(s_x,s_y)%len,tmp.y=s_y+Rand(s_x,s_y)%len;
	if(s_x<square_x||s_x>=square_x+biome_catch
	        ||s_y<square_y||s_y>=square_y+biome_catch) {
		if(len==biome_catch) tmp.col=Rand(tmp.x,tmp.y)%13-13;
		else {
			UnrealLoad(s_x,s_y,tmp,len);
			if(tmp.col<-8) tmp.col=17;
			else if(tmp.col>=-8&&tmp.col<0) tmp.col=Rand(tmp.x,tmp.y)%16+1;
		}
		biome_know[(Point) {s_x,s_y,len}]=tmp;
		return tmp;
	}
//	if(s_x==0&&s_y==512) TX(tmp.x)<<" "<<TY(tmp.y)<<endl;
	if(biome[TX(tmp.x)][TY(tmp.y)]==0) tmp.col=Rand(tmp.x,tmp.y)%13-13;
	else {
		if(biome[TX(tmp.x)][TY(tmp.y)]<-8) tmp.col=17;
		else if(biome[TX(tmp.x)][TY(tmp.y)]>=-8&&biome[TX(tmp.x)][TY(tmp.y)]<0) tmp.col=Rand(tmp.x,tmp.y)%16+1;
		else {
			tmp.col=biome[TX(tmp.x)][TY(tmp.y)];
			if(len==32) {
				if(tmp.col!=17) Special_Create(tmp,Rand(tmp.x,tmp.y)%3+1);
				else Special_Create(tmp,4);
			}
			if(len==8) {
				if(tmp.col==17) Special_Create(tmp,5);
			}
		}
	}
	biome_know[(Point) {s_x,s_y,len}]=tmp;
	return tmp;
}
void SquareMade(int s_x,int s_y,int len) {
	seed=world_seed;
	Point root=GetPoint(s_x,s_y,len);
	vector<Point> root_queue;
	int flag=true;
	root_queue.push_back(root);
	for(int i=0; i<8; i++) {
//		if(cross[i][0]&&cross[i][1]) continue;
		if(s_x+cross[i][0]*len<0||s_y+cross[i][1]*len<0) continue;
		Point tmp=GetPoint(s_x+cross[i][0]*len,s_y+cross[i][1]*len,len);
		root_queue.push_back(tmp);
	}
	if(flag) {
		for(int i=s_x; i<s_x+len; i++)
			for(int j=s_y; j<s_y+len; j++) biome[TX(i)][TY(j)]=root.col;
		if(len==32&&root.col==12) {
			int water_pool_num=Rand(s_x,s_y)%21;
			while(water_pool_num--) {
				int x=s_x+Rand(s_x,s_y)%len,y=s_y+Rand(s_x,s_y)%len;
				biome[TX(x)][TY(y)]=17;
			}
		}
		if(len==8&&root.col==12) {
			int water_pool_num=Rand(s_x,s_y)%21;
			while(water_pool_num--) {
				int x=s_x+Rand(s_x,s_y)%len,y=s_y+Rand(s_x,s_y)%len;
				biome[TX(x)][TY(y)]=17;
			}
		}
		return ;
	}
	for(int i=s_x; i<s_x+len; i++) {
		for(int j=s_y; j<s_y+len; j++) {
			ll min_len=1e12,min_id,minness;//:)
			Point min_close;
			for(int k=0; k<root_queue.size(); k++) {
				Point tmp=root_queue[k];
				ll far=pow(abs(tmp.x-i),2)+pow(abs(tmp.y-j),2);
				if(far<min_len) min_len=far,min_id=k,min_close=tmp;
			}
			biome[TX(i)][TY(j)]=min_close.col;
		}
	}
//	if(len==128) {//生成矿物代码
//		seed=(world_seed+998244353)%19260817;
//		if(biome[root.x][root.y]==17) {
//			for(int i=1; i<=3; i++) {
//				int x=s_x+Rand(s_x,s_y)%len,y=s_y+Rand(s_x,s_y)%len;
//				mineral[x][y]=1;
//			}
//		}
//		int x=s_x+Rand(s_x,s_y)%len,y=s_y+Rand(s_x,s_y)%len;
//		mineral[x][y]=1;
//	}
	if(len==32&&root.col==12) {
		int water_pool_num=Rand(s_x,s_y)%21;
		while(water_pool_num--) {
			int x=s_x+Rand(s_x,s_y)%len,y=s_y+Rand(s_x,s_y)%len;
			biome[TX(x)][TY(y)]=17;
		}
	}
	if(len==8&&root.col==12) {
		int water_pool_num=Rand(s_x,s_y)%21;
		while(water_pool_num--) {
			int x=s_x+Rand(s_x,s_y)%len,y=s_y+Rand(s_x,s_y)%len;
			biome[TX(x)][TY(y)]=17;
		}
	}
}
Point RiverPoint(int s_x,int s_y,int len);

void UnrealLoadRiver(int s_x,int s_y,Point& now,int len) {
	seed=river_seed;
	len*=4;
	ll min_len=1e12;
	Point min_close;
	s_x=s_x/len*len,s_y=s_y/len*len;
	for(int i=0; i<9; i++) {
		if(s_x+cross[i][0]*len<0||s_y+cross[i][1]*len<0) continue;
		Point tmp=RiverPoint(s_x+cross[i][0]*len,s_y+cross[i][1]*len,len);
		ll far=pow(abs(tmp.x-now.x),2)+pow(abs(tmp.y-now.y),2);
		if(far<min_len) min_len=far,min_close=tmp;
	}
	now.col=min_close.col;
}
Point RiverPoint(int s_x,int s_y,int len) {
	if(river_know.count((Point) {s_x,s_y,len})) return river_know[(Point) {s_x,s_y,len}];
	seed=river_seed;
	Point tmp;
	tmp.x=s_x+Rand(s_x,s_y)%len,tmp.y=s_y+Rand(s_x,s_y)%len;
	if(s_x<square_x||s_x>=square_x+biome_catch
	        ||s_y<square_y||s_y>=square_y+biome_catch) {
		if(len==biome_catch) tmp.col=Rand(tmp.x,tmp.y)%3+1;
		else UnrealLoadRiver(s_x,s_y,tmp,len);
		river_know[(Point) {s_x,s_y,len}]=tmp;
		return tmp;
	}
	if(!river[TX(tmp.x)][TY(tmp.y)]) tmp.col=Rand(tmp.x,tmp.y)%3+1;
	else tmp.col=river[TX(tmp.x)][TY(tmp.y)];
	river_know[(Point) {s_x,s_y,len}]=tmp;
	return tmp;
}
void RiverMade(int s_x,int s_y,int len) {
	seed=river_seed;
	Point root=RiverPoint(s_x,s_y,len);
	vector<Point> root_queue;
	root_queue.push_back(root);
	for(int i=0; i<8; i++) {
		if(s_x+cross[i][0]*len<0||s_y+cross[i][1]*len<0) continue;
		Point tmp=RiverPoint(s_x+cross[i][0]*len,s_y+cross[i][1]*len,len);
		root_queue.push_back(tmp);
	}
	for(int i=s_x; i<s_x+len; i++) {
		for(int j=s_y; j<s_y+len; j++) {
			ll min_len=1e12;//:)
			Point min_close;
			for(int k=0; k<root_queue.size(); k++) {
				Point tmp=root_queue[k];
				ll far=pow(abs(tmp.x-i),2)+pow(abs(tmp.y-j),2);
				if(far<min_len) min_len=far,min_close=tmp;
			}
			river[TX(i)][TY(j)]=min_close.col;
		}
	}
}
void Turn2River(int s_x,int s_y,int len) {
	for(int i=s_x; i<s_x+len; i++) {
		for(int j=s_y; j<s_y+len; j++) {
			for(int k=0; k<8; k++) {
				int tx=i+cross[k][0],ty=j+cross[k][1];
				if(tx<0||ty<0) continue;
				if(tx<square_x||tx>=square_x+biome_catch
				||ty<square_y||ty>=square_y+biome_catch) continue;
				if(river[TX(tx)][TY(ty)]!=river[TX(i)][TY(j)]) conside[TX(i)][TY(j)]=1;
			}
		}
	}
}
void MakePlant(int s_x,int s_y,int len) {
	for(int i=s_x; i<s_x+len; i++) {
		for(int j=s_y; j<s_y+len; j++) {
			int biome_here=biome[TX(i)][TY(j)];
			if(Check(plant_born[biome_here][0][0],plant_born[biome_here][0][1])) plant[TX(i)][TY(j)]=1003;
			if(Check(plant_born[biome_here][1][0],plant_born[biome_here][1][1])) plant[TX(i)][TY(j)]=1001;
		}
	}
}
double hash21 (int x , int y) {
	int n = x + y * 57 ;
	n = (n << 13) ^ n ;
	return (1.0 - ((n * (n * n * 15731 + 789221) + 1376312589) & 0x7fffffff) / 1073741824.0) ;
}
double Smooth (int x , int y) {
	double t1 = (hash21 (x - 1 , y - 1) + hash21 (x - 1 , y + 1) + hash21 (x + 1 , y - 1) + hash21 (x + 1 , y + 1)) / 16 ;
	double t2 = (hash21 (x , y - 1) + hash21 (x , y + 1) + hash21 (x - 1 , y) + hash21 (x + 1 , y)) / 8 ;
	double t3 = hash21 (x , y) / 4 ;
	return t1 + t2 + t3 ;
}
double InsCos (double x , double y , double p) {
	double t = p * 3.1415927 ;
	double f = (1 - cos (t)) * 0.5 ;
	return x * (1 - f) + y * f ;
}
double ins (double x , double y) {
	int X = int (x) , Y = int (y) ;
	double xx = X - x , yy = Y - y ;
	double v1 = Smooth (X , Y) , v2 = Smooth (X + 1 , Y) , v3 = Smooth (X , Y + 1) , v4 = Smooth (X + 1 , Y + 1) ;
	if (x < 0) {
		double i1 = InsCos (v2 , v1 , xx) , i2 = InsCos (v4 , v3 , xx) ;
		return y < 0 ? InsCos (i2 , i1 , yy) : InsCos (i1 , i2 , yy) ;
	}
	else {
		double i1 = InsCos (v1 , v2 , xx) , i2 = InsCos (v3 , v4 , xx) ;
		return y >= 0 ? InsCos (i1 , i2 , yy) : InsCos (i2 , i1 , yy) ;
	}
}
double ValueNoise (double x , double y) {
	double tot = 0 ;
	for (int i = 0 ; i < 8 ; i++) {
		double t1 = pow (2 , i) , t2 = pow (0.3 , i) ;
		tot += (ins (x * t1 , y * t1) * t2) ;
	}
	return tot ;
}
void make_noise() {
	int X=square_x,Y=square_y;
	for (int i = 0 ; i < biome_catch ; i++)
		for (int j = 0 ; j < biome_catch ; j++)
			a[i][j] = ValueNoise (i / 250.0 + X * 1.0 , j / 250.0 + Y * 1.0) ;
	for (int i = 0 ; i < biome_catch ; i++)
		for (int j = 0 ; j < biome_catch ; j++)
			c[i][j] = floor ((a[i][j] + 1.0) * 0.5 * 255) ;
}
int main() {
	freopen("SMP.in","r",stdin);
	freopen("SlowSave.map","w",stdout);
	input(square_x),input(square_y),input(world_seed);
	input(biome_catch);
	river_seed=fabs(world_seed+Rand(1245,4927)-Rand(1245,4927));
	seed=world_seed;
	int tmp_biome_catch=biome_catch;
	while(tmp_biome_catch>=8) {
		for(int i=0; i<biome_catch; i+=tmp_biome_catch)
			for(int j=0; j<biome_catch; j+=tmp_biome_catch) {
				SquareMade(square_x+i,square_y+j,tmp_biome_catch);
				RiverMade(square_x+i,square_y+j,tmp_biome_catch);
			}
		tmp_biome_catch/=4;
	}
	Turn2River(square_x,square_y,biome_catch);
	ResetPlantBorn(),MakePlant(square_x,square_y,biome_catch);
//	make_noise();
	for(int i=0; i<biome_catch/16; i++) {
		for(int j=0; j<biome_catch/16; j++) {
			if(conside[i][j]) output(17);
//			else if(c[i][j]/1.28<=105) output(17);
//			else if(c[i][j]/1.28<=108) output(1);
//            else if(nearby[i][j]) output(1007); 
			else output(biome[i][j]);
		}
	}
	for(int i=0; i<biome_catch/16; i++) 
		for(int j=0; j<biome_catch/16; j++) output(plant[i][j]);
	return 0;
}

