# Desk check FC1208 v1.0 (2026-11-23): cleaned LEVEL = raw sensor OR (belt run time since last counted front < 90% W)
# FC8 count up: ON >= 300 ms -> +1, re-arm after OFF >= 300 ms (Space_DX 600). Gate = filling step.
SCAN=10
def level(raw,run,W,bp=90):
    T=60000;was=False;out=[]
    for s,r in zip(raw,run):
        if r: T=min(T+SCAN,60000)
        if s and not was and T>=W*bp//100: T=0      # counted front (FC1212)
        out.append(s or T<W*bp//100); was=s
    return out
def fc8_up(b0,gate,space=600,pre=300):
    gap=space//2;cnt=0;on=False;done=False;e=0;off=0
    for a,g in zip(b0,gate):
        a=a and g
        if a: on=True;off=0;e+=SCAN
        elif on: off+=SCAN
        if on and not done and e>=pre: cnt+=1;done=True
        if off>=gap: on=done=False;e=off=0
    return cnt
def load(n,W,gap,sag=0,first_parked=0):
    raw=[True]*(first_parked//SCAN)    # first packet already on the sensor (belt stopped)
    run=[False]*(first_parked//SCAN)
    gate=[False]*(first_parked//SCAN)
    for i in range(n):
        if sag: p=[1]*(300//SCAN)+[0]*(sag//SCAN)+[1]*((W-300-sag)//SCAN)
        else: p=[1]*(W//SCAN)
        if i==0 and first_parked: p=p[100//SCAN:]   # parked with its front just past the sensor (C10 collation stops at B10.6)
        raw+=p+[0]*(gap//SCAN)
    tail=len(raw)-len(run); run+=[True]*tail; gate+=[True]*tail
    raw=[bool(x) for x in raw]+[False]*100; run+=[True]*100; gate+=[True]*100
    return raw,run,gate
for name,W,gap,sag,park in [('flat',1035,400,0,0),('U sag 150',1035,400,150,0),('U sag 350',1035,400,350,0),('first packet parked on sensor',1035,400,0,3000),('parked + U sag 350',1035,400,350,3000),('small 855, gap 300',855,300,0,0)]:
    raw,run,gate=load(6,W,gap,sag,park)
    print(f"{name:32s} v1.0 = {fc8_up(level(raw,run,W),gate)}   old raw = {fc8_up(raw,gate)}")
