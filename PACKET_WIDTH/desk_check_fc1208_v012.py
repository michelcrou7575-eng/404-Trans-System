# Desk check FC1208 v0.12 (2026-11-23): raw sensor -> FC1212 blanking pulse -> FC8 (Space 400 / Preset 200). Run: python3 desk_check_fc1208_v012.py
# desk check: raw sensor -> FC1212 blanking -> pulse -> FC8 count (up on next conveyor, down on this one)
SCAN=10
def fc1212(raw,W,bp=90,bt=140,PL=400):
    T=60000;was=False;pms=0;out=[];c=0
    for s in raw:
        T=min(T+SCAN,60000);cnt=False;btd=False
        if s and not was:
            if T>=W*bp//100: cnt=True
        if s and not cnt and T>=W*bt//100: cnt=btd=True
        if cnt:
            c+=1;T=0
            if btd:T=W*bt//100-W
            pms=PL
        p=pms>0
        if p:pms-=SCAN
        out.append(p);was=s
    return out,c
def fc8(b0,b1,xfer,space=400,pre=200):
    gap=max(space//2,100);cnt=0
    on0=False;done=False;e0=0;off0=0;on1=False;e1=0;off1=0
    for a,b,x in zip(b0,b1,xfer):
        if a: on0=True;off0=0;e0+=SCAN
        elif on0: off0+=SCAN
        if on0 and not done and e0>=pre: cnt+=1;done=True
        if off0>=gap: on0=done=False;e0=off0=0
        if b:
            off1=0
            if x: on1=True;e1+=SCAN
        elif on1: off1+=SCAN
        if off1>=gap:
            if e1>=pre: cnt-=1
            on1=False;e1=off1=0
    return cnt
def packets(n,W,gapms,u=False,butt=False):
    r=[]
    for i in range(n):
        if u: r+= [1]*(W*3//10//SCAN)+[0]*(150//SCAN)+[1]*((W-W*3//10-150)//SCAN)
        else: r+=[1]*(W//SCAN)
        if not butt: r+=[0]*(gapms//SCAN)
    return [bool(x) for x in r]+[False]*100
for W,g,u,b in [(1035,400,False,False),(1035,400,True,False),(855,300,True,False),(1035,0,False,True),(700,250,False,False),(667,200,False,False)]:
    raw=packets(6,W,g,u,b);p,c=fc1212(raw,W)
    up=fc8(p,[False]*len(p),[True]*len(p));dn=fc8([False]*len(p),p,[True]*len(p))
    rawup=fc8(raw,[False]*len(raw),[True]*len(raw),600,300)
    print(f"W={W} gap={g} U={u} butt={b}: blanking={c} FC8 up={up} down={dn} | old raw up={rawup}")
print('--- long sag 350 ms (beam sees through the U):')
def upack(n,W,gapms,sag):
    r=[]
    for i in range(n): r+=[1]*(300//SCAN)+[0]*(sag//SCAN)+[1]*((W-300-sag)//SCAN)+[0]*(gapms//SCAN)
    return [bool(x) for x in r]+[False]*100
raw=upack(6,1035,400,350);p,c=fc1212(raw,1035)
print('blanking',c,'FC8 up',fc8(p,[False]*len(p),[True]*len(p)),'| old raw up',fc8(raw,[False]*len(raw),[True]*len(raw),600,300))
print('--- stale width: blanking uses 1035 but packets are 855 (gap 300):')
raw=packets(6,855,300);p,c=fc1212(raw,1035)
print('blanking',c,'FC8 up',fc8(p,[False]*len(p),[True]*len(p)))
