# Model of FC1211 / FC1210 logic (same steps as the STL), run on simulated packets.
def fc1211(d,sensor,active,start,stop,enc,gapP,scan):
    close=False
    if start:
        d.update(Count=0,Skipped=0,Sag=0,Max=0,Avg=0,SagMax=0,Sum=0,Min=32767,GapMin=32767,Sum_ms=0,Time=0,Fall_ms=0,
                 Start=enc,Fall=enc,Open=sensor,Skip=sensor,Low=False)
    run=(active or stop) and not start
    if run and sensor and not d['WasOn']:
        if d['Open'] and d['Low']:
            mm=round(abs(enc-d['Fall'])*0.31); d['Sag']+=1; d['SagMax']=max(d['SagMax'],mm); d['Low']=False
        elif not d['Open']:
            if d['Count']>0: d['GapMin']=min(d['GapMin'],round(abs(enc-d['Fall'])*0.31))
            d.update(Open=True,Low=False,Skip=False,Start=enc,Time=0)
    if run and d['Open']: d['Time']=min(d['Time']+scan,30000)
    if run and not sensor and d['WasOn'] and d['Open']: d.update(Fall=enc,Fall_ms=d['Time'],Low=True)
    if run and not sensor and d['Open'] and d['Low'] and abs(enc-d['Fall'])>=gapP: close=True
    if stop and d['Open'] and d['Low']: close=True
    if stop and d['Open'] and not d['Low']: d['Open']=False
    if close:
        if d['Skip']: d['Skipped']+=1
        else:
            mm=round(abs(d['Fall']-d['Start'])*0.31); d['Count']+=1; d['Sum']+=mm
            d['Min']=min(d['Min'],mm); d['Max']=max(d['Max'],mm); d['Avg']=d['Sum']//d['Count']
            d['Sum_ms']+=d['Fall_ms']; d['Avg_ms']=d['Sum_ms']//d['Count']
        d.update(Open=False,Low=False,Skip=False)
    d['WasOn']=sensor
def run(name,packets,offset_mm,gap_min=100,first_covered=False,scan=10,speed=517):
    # packets: list of (width_mm, [(sag_from_mm, sag_to_mm),...]), gap list mm
    x=0; segs=[]
    for w,sags,gap in packets:
        segs.append((x,x+w,sags)); x+=w+gap
    total=x+300
    def cov(pos):  # pos = belt travelled past sensor
        for a,b,sags in segs:
            if a<=pos<b:
                rel=pos-a
                return not any(s<=rel<e for s,e in sags)
        return False
    d={'WasOn':False}; res={}
    gapP=round(gap_min/0.31)
    t=0; pos=-offset_mm if not first_covered else 150
    steps=int(total/(speed*scan/1000))+5
    for i in range(steps+2):
        active=0<i<=steps; start=(i==1); stop=(i==steps+1)
        enc=round(pos/0.31)
        fc1211(d,cov(pos) if active or start or stop else False,active,start,stop,enc,gapP,scan)
        if active: pos+=speed*scan/1000
    print(f"{name:42} Count={d['Count']} Skipped={d['Skipped']} Avg={d['Avg']}mm Min={d['Min']} Max={d['Max']} Avg_ms={d.get('Avg_ms')} Sags={d['Sag']} SagMax={d['SagMax']} GapMin={d['GapMin']}")
W=600;G=300
run('6 flat packets 600mm, gaps 300',[(W,[],G)]*6,0)
run('6 U-shape (sag 200-400mm), gaps 300',[(W,[(200,400)],G)]*6,0)
run('U-shape sag 150mm, gap_min 100 -> sag>gap_min!',[(W,[(225,375)],G)]*6,0,gap_min=100)
run('same, gap_min 250 (tuned)',[(W,[(225,375)],G)]*6,0,gap_min=250)
run('first packet already covering at start',[(W,[],G)]*6,0,first_covered=True)
print('expected ms for 600mm @517mm/s =',round(600/517*1000))
print('--- with packet front 50mm before sensor at start (not covered)')
run('6 flat, gap_min 150',[(W,[],G)]*6,50,gap_min=150)
run('6 U-shape sag 120mm, gap_min 150',[(W,[(240,360)],G)]*6,50,gap_min=150)
run('6 U-shape sag 200mm, gap_min 150 (too small)',[(W,[(200,400)],G)]*6,50,gap_min=150)
run('mixed gaps 250-350, sag 100, gap_min 150',[(W,[(250,350)],250),(W,[(250,350)],350)]*3,50,gap_min=150)
