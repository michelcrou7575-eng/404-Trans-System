import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, PageBreak, Flowable)

OUT=sys.argv[1]
NAVY=colors.HexColor('#1f3a5f'); AMBER=colors.HexColor('#f2a900'); GREY=colors.HexColor('#e9edf2')
GREEN=colors.HexColor('#2e7d32'); RED=colors.HexColor('#c62828'); LIGHT=colors.HexColor('#fff8e1')

ss=getSampleStyleSheet()
H1=ParagraphStyle('H1',parent=ss['Title'],fontSize=20,textColor=NAVY,spaceAfter=2,alignment=0)
SUB=ParagraphStyle('SUB',parent=ss['Normal'],fontSize=10,textColor=colors.grey,spaceAfter=8)
H2=ParagraphStyle('H2',parent=ss['Heading2'],fontSize=13,textColor=NAVY,spaceBefore=8,spaceAfter=4)
B=ParagraphStyle('B',parent=ss['Normal'],fontSize=10,leading=13)
BS=ParagraphStyle('BS',parent=B,fontSize=9,leading=11.5)
BC=ParagraphStyle('BC',parent=B,alignment=1)
STEP=ParagraphStyle('STEP',parent=B,fontSize=10.5,leading=13.5)

class Lamp(Flowable):
    def __init__(self,state,size=9*mm):
        super().__init__(); self.state=state; self.s=size
    def wrap(self,aw,ah): return (self.s*1.6,self.s)
    def draw(self):
        c=self.canv; r=self.s/2-1
        if self.state=='off':
            c.setFillColor(colors.HexColor('#9e9e9e')); c.setStrokeColor(colors.black); c.circle(self.s*0.8,self.s/2,r,fill=1)
        elif self.state=='solid':
            c.setFillColor(AMBER); c.setStrokeColor(colors.black); c.circle(self.s*0.8,self.s/2,r,fill=1)
        else:  # blink: lamp with rays
            c.setFillColor(AMBER); c.setStrokeColor(colors.black); c.circle(self.s*0.8,self.s/2,r,fill=1)
            c.setStrokeColor(AMBER); c.setLineWidth(1.2)
            import math
            for k in range(8):
                a=k*math.pi/4; x=self.s*0.8; y=self.s/2
                c.line(x+math.cos(a)*(r+1.5),y+math.sin(a)*(r+1.5),x+math.cos(a)*(r+4),y+math.sin(a)*(r+4))

def tbl(data,widths,style_extra=(),header=True):
    t=Table(data,colWidths=widths)
    st=[('VALIGN',(0,0),(-1,-1),'MIDDLE'),('GRID',(0,0),(-1,-1),0.5,colors.HexColor('#b0bec5')),
        ('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]
    if header: st+= [('BACKGROUND',(0,0),(-1,0),NAVY),('TEXTCOLOR',(0,0),(-1,0),colors.white),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold')]
    t.setStyle(TableStyle(st+list(style_extra))); return t
def P(x,s=B): return Paragraph(x,s)

def footer(c,doc):
    c.saveState(); c.setFont('Helvetica',8); c.setFillColor(colors.grey)
    c.drawString(18*mm,10*mm,'TS 404 - Clearing (F4) - Operator Guide - Rev. 1 - 2026-11-20 (PLC: clearing block FC911)')
    c.drawRightString(letter[0]-18*mm,10*mm,f'Page {doc.page}'); c.restoreState()

doc=SimpleDocTemplate(OUT,pagesize=letter,leftMargin=18*mm,rightMargin=18*mm,topMargin=15*mm,bottomMargin=18*mm,
                      title='Clearing (F4) - Operator Guide',author='TS 404')
W=letter[0]-36*mm
s=[]
s.append(P('Clearing (F4) - Order Change',H1))
s.append(P('Transfer System 404 - Operator Guide - what you do, what the TS does, what the lamps mean',SUB))

s.append(P('What clearing does',H2))
s.append(P('At the end of an order, clearing empties conveyors <b>C1 to C10</b> into C11/C12/C13 and C21/C22/C23, '
           'while the bottomer finishes the order. Then the next order fills C1 to C10 and <b>waits on C10</b> until you '
           'confirm with <b>S3.2</b>. This keeps the two orders <b>apart</b>: no packets of the old order are left on C10, '
           'and the new order never joins the old one.'))

s.append(P('Step by step',H2))
steps=[
 ['1','<b>Last packet of order A has left the 2145.</b> Press <b>F4</b> on the LAUER panel (or the broom switch on the new HMI).','You'],
 ['2','Clearing runs: feeding from the 2145 stops, C1 to C9 empty one after the other, then C10 empties into C11 or C21. '
      '<b>New HMI clearing lamp blinks.</b> No action needed - just let it run. Clearing ends by itself.','TS'],
 ['3','<b>Clearing done</b>: feeding is allowed again, the HMI clearing lamp is steady. Set up order B on the 2145 and start it when ready.','You'],
 ['4','Order B fills C1 to C10. <b>C10 holds order B</b> - nothing leaves C10. The <b>S3.2 lamp is ON (steady)</b>: '
      'the TS is waiting for the bottomer to finish order A.','TS'],
 ['5','When C11-C23 and the loader are <b>empty</b>, the <b>S3.2 lamp BLINKS</b>.','TS'],
 ['6','<b>Press S3.2 once</b> (short push). C10 sends order B. The order change is done.','You'],
]
rows=[[P('#',BC),P('What happens',B),P('Who',BC)]]
for n,txt,who in steps:
    rows.append([P(f'<b>{n}</b>',BC),P(txt,STEP),P(f'<b>{who}</b>',BC)])
ex=[('BACKGROUND',(2,i),(2,i),LIGHT) for i,(n,t,w) in enumerate(steps,1) if w=='You']
s.append(tbl(rows,[10*mm,W-30*mm,20*mm],ex))

s.append(P('S3.2 lamp (feeder box X121) - what it means',H2))
lamp=[[P('<b>Lamp</b>',BC),P('<b>Meaning</b>',B),P('<b>What you do</b>',B)],
      [Lamp('off'),P('<b>OFF</b> - normal production, or clearing running'),P('Nothing.')],
      [Lamp('solid'),P('<b>STEADY</b> - C10 is holding the new order. The TS is not ready yet (bottomer still on the old order).'),P('<b>Wait.</b> A short push does nothing.')],
      [Lamp('blink'),P('<b>BLINKING</b> - C11-C23 and the loader are empty. Ready.'),P('<b>Press S3.2 once</b> (short push).')]]
s.append(tbl(lamp,[20*mm,W*0.5,W-20*mm-W*0.5],header=True,style_extra=[('BACKGROUND',(0,0),(-1,0),NAVY),('TEXTCOLOR',(0,0),(-1,0),colors.white)]))

s.append(PageBreak())
s.append(P('Special cases',H2))
sp=[[P('<b>Situation</b>',B),P('<b>What to do</b>',B)],
    [P('Lamp <b>steady for a long time</b>, but C11-C23 and the loader are <b>visibly empty</b> (TS stuck)'),
     P('<b>Check by eye</b> that C11, C12, C13, C21, C22, C23 and the loader are empty, then <b>hold S3.2 for 3 seconds</b>. '
       'C10 sends the new order. <font color="#c62828"><b>Never do this while packets of the old order are still on C11-C23 or in the loader: '
       'the orders would join.</b></font>')],
    [P('Clearing started <b>by mistake</b>'),P('Cancel on the LAUER panel: while F4 is active, press <b>ENT and CLR together</b>. (New HMI: switch the broom switch off.)')],
    [P('<b>F4 pressed again</b> while C10 is holding the new order'),
     P('A new clearing starts and empties C10 too (the new order on C10 is cleared out). Only press F4 when you really want a new order change.')],
    [P('Clearing seems <b>slow</b> to finish'),
     P('Normal: C10 must have run its full length with nothing on it before clearing ends. If C11/C21 are full, it finishes '
       'the next time C11 or C21 can take a load.')],
    [P('Lamp never lights at all, but S3.2 works'),P('Lamp or wiring fault: check the S3.2 lamp (lamp test), call maintenance.')],
]
s.append(tbl(sp,[W*0.35,W*0.65]))

s.append(P('Do / Don\'t',H2))
dd=[[P('<b><font color="#2e7d32">DO</font></b>',BC),P('<b><font color="#c62828">DON\'T</font></b>',BC)],
    [P('Press F4 only after the <b>last packet of the order</b> has left the 2145.<br/>'
       'Wait for the lamp to <b>blink</b>, then push S3.2 <b>once</b>.<br/>'
       'Check C11-C23 and the loader <b>by eye</b> before a 3-second S3.2.'),
     P('Don\'t hold S3.2 for 3 s while the old order is still on C11-C23 or in the loader.<br/>'
       'Don\'t press F4 twice for one order change.<br/>'
       'Don\'t reset or hold SIGNAL to "help" the clearing - let it finish by itself.')]]
s.append(tbl(dd,[W/2,W/2],header=False,style_extra=[('BACKGROUND',(0,0),(-1,0),GREY),('VALIGN',(0,1),(-1,1),'TOP')]))

s.append(P('Quick card',H2))
card=[[P('<font size="12"><b>F4</b> = start order change (after the last packet).<br/>'
         '<b>HMI clearing lamp blinking</b> = clearing running - wait.<br/>'
         '<b>S3.2 steady</b> = new order waiting on C10 - wait.<br/>'
         '<b>S3.2 blinking</b> = push S3.2 <u>once</u>.<br/>'
         '<b>Steady a long time + TS empty</b> = check by eye, then hold S3.2 for 3 s.</font>',B)]]
s.append(tbl(card,[W],header=False,style_extra=[('BACKGROUND',(0,0),(-1,-1),LIGHT),('BOX',(0,0),(-1,-1),1.5,AMBER),('GRID',(0,0),(-1,-1),0,colors.white),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]))

s.append(P('For maintenance',H2))
s.append(P('New clearing block FC911 runs when switch <b>M280.0</b> = 1 (old FC1011 when 0). After a power-off, check '
           '<b>MB280-MB282</b> are set again. Sequence monitoring: VAT "Clearing sequence" (file VAT_CLEARING_SEQUENCE.md). '
           'S3.2 lamp = Q49.5, hold = M8.4, ready = M8.2, clearing = M10.0.',BS))
doc.build(s,onFirstPage=footer,onLaterPages=footer)
