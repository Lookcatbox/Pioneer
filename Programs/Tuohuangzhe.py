import uiObj0,uiObj10,uiObj20,os,pygame

gtkey={}

gtkey[96]=['`','~']
gtkey[49]=['1','!']
gtkey[50]=['2','@']
gtkey[51]=['3','#']
gtkey[52]=['4','$']
gtkey[53]=['5','%']
gtkey[54]=['6','^']
gtkey[55]=['7','&']
gtkey[56]=['8','*']
gtkey[57]=['9','(']
gtkey[48]=['0',')']
gtkey[45]=['-','_']
gtkey[61]=['=','+']
gtkey[32]=[' ',' ']
gtkey[91]=['[','{']
gtkey[93]=[']','}']
gtkey[92]=['\\','|']
gtkey[59]=[';',':']
gtkey[39]=['\'','"']
gtkey[44]=[',','<']
gtkey[46]=['.','>']
gtkey[47]=['/','?']
gtkey[256]=['0','0']
gtkey[257]=['1','1']
gtkey[258]=['2','2']
gtkey[259]=['3','3']
gtkey[260]=['4','4']
gtkey[261]=['5','5']
gtkey[262]=['6','6']
gtkey[263]=['7','7']
gtkey[264]=['8','8']
gtkey[265]=['9','9']
gtkey[266]=['.','.']
gtkey[270]=['+','+']
gtkey[269]=['-','-']
gtkey[268]=['*','*']
gtkey[267]=['/','/']
gtkey[97]=['a','A']
gtkey[98]=['b','B']
gtkey[99]=['c','C']
gtkey[100]=['d','D']
gtkey[101]=['e','E']
gtkey[102]=['f','F']
gtkey[103]=['g','G']
gtkey[104]=['h','H']
gtkey[105]=['i','I']
gtkey[106]=['j','J']
gtkey[107]=['k','K']
gtkey[108]=['l','L']
gtkey[109]=['m','M']
gtkey[110]=['n','N']
gtkey[111]=['o','O']
gtkey[112]=['p','P']
gtkey[113]=['q','Q']
gtkey[114]=['r','R']
gtkey[115]=['s','S']
gtkey[116]=['t','T']
gtkey[117]=['u','U']
gtkey[118]=['v','V']
gtkey[119]=['w','W']
gtkey[120]=['x','X']
gtkey[121]=['y','Y']
gtkey[122]=['z','Z']
gtkey[32]=[' ',' ']
#gtkey is Key->Char Dict

def EXIT():
    pygame.quit()
    os._exit(0)
def Call(obj,*args):
    res=obj.main(*args)
    if type(res)==bool:
        EXIT()
    return res
Call(uiObj10,pygame)
sed=Call(uiObj20,pygame,gtkey)
Call(uiObj0,pygame,gtkey,sed)