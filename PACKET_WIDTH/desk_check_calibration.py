exec(open('simw.py').read().split("W=600;G=300")[0])
_orig=fc1211
def fc(d,*a):
    before=d.get('Count',0)+d.get('Skipped',0); op=d.get('Open',False)
    _orig(d,*a); d['Front']= d.get('Open',False) and not op and not d.get('Skip',False) and not a[2]
def cal(name,packets,true_mmp=0.288,speed=517,scan=10,dist=527,start_pos=-30):
    x=0;segs=[]
    for w,sags,gap in packets: segs.append((x,x+w,sags)); x+=w+gap
    cov=lambda p:any(a<=p<b and not any(s<=p-a<e for s,e in sg) for a,b,sg in segs)
    d5={'WasOn':False};d6={'WasOn':False};pend=False;T=0;ps=ms=cnt=0
    pos=start_pos; steps=int((x+dist+400)/(speed*scan/1000))
    for i in range(steps+2):
        act=0<i<=steps; st=i==1; sp=i==steps+1; enc=round(pos/true_mmp)
        fc(d5,cov(pos),act,st,sp,enc,round(150/0.31),scan); fc(d6,cov(pos-dist),act,st,sp,enc,round(150/0.31),scan)
        if act:
            T+=scan
            if d6['Front'] and pend: ps+=abs(enc-pe); ms+=T-pt; cnt+=1; pend=False
            if d5['Front']: pe,pt,pend=enc,T,True
            pos+=speed*scan/1000
    print(f"{name:40} pairs={cnt} mm/pulse={dist*cnt/ps:.4f} (true {true_mmp}) speed={dist*cnt*1000/ms:.0f} mm/s (true {speed})")
cal('6 packets 477 + gaps 163-217',[(477,[],163),(477,[],217)]*3)
cal('first packet between sensors at start',[(477,[],190)]*6,start_pos=300)
cal('U-shape sag 100',[(477,[(180,280)],190)]*6)
