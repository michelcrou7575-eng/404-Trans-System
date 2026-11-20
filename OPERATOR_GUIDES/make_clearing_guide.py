# Generates the Clearing (F4) operator guide in English and French.
# Usage: python3 make_clearing_guide.py <output_dir>
import sys, os, math
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, PageBreak, Flowable

NAVY=colors.HexColor('#1f3a5f'); AMBER=colors.HexColor('#f2a900'); GREY=colors.HexColor('#e9edf2'); LIGHT=colors.HexColor('#fff8e1')
ss=getSampleStyleSheet()
H1=ParagraphStyle('H1',parent=ss['Title'],fontSize=20,textColor=NAVY,spaceAfter=2,alignment=0)
SUB=ParagraphStyle('SUB',parent=ss['Normal'],fontSize=10,textColor=colors.grey,spaceAfter=8)
H2=ParagraphStyle('H2',parent=ss['Heading2'],fontSize=13,textColor=NAVY,spaceBefore=8,spaceAfter=4)
B=ParagraphStyle('B',parent=ss['Normal'],fontSize=10,leading=13)
BC=ParagraphStyle('BC',parent=B,alignment=1)
STEP=ParagraphStyle('STEP',parent=B,fontSize=10.5,leading=13.5)

class Lamp(Flowable):
    def __init__(self,state,size=9*mm): super().__init__(); self.state=state; self.s=size
    def wrap(self,aw,ah): return (self.s*1.6,self.s)
    def draw(self):
        c=self.canv; r=self.s/2-1; x=self.s*0.8; y=self.s/2
        c.setStrokeColor(colors.black); c.setFillColor(colors.HexColor('#9e9e9e') if self.state=='off' else AMBER)
        c.circle(x,y,r,fill=1)
        if self.state=='blink':
            c.setStrokeColor(AMBER); c.setLineWidth(1.2)
            for k in range(8):
                a=k*math.pi/4; c.line(x+math.cos(a)*(r+1.5),y+math.sin(a)*(r+1.5),x+math.cos(a)*(r+4),y+math.sin(a)*(r+4))

def tbl(data,widths,extra=(),header=True):
    t=Table(data,colWidths=widths)
    st=[('VALIGN',(0,0),(-1,-1),'MIDDLE'),('GRID',(0,0),(-1,-1),0.5,colors.HexColor('#b0bec5')),
        ('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]
    if header: st+=[('BACKGROUND',(0,0),(-1,0),NAVY),('TEXTCOLOR',(0,0),(-1,0),colors.white)]
    t.setStyle(TableStyle(st+list(extra))); return t
P=lambda x,s=B: Paragraph(x,s)

T={
'en':dict(
 file='Clearing_F4_Operator_Guide_EN_Rev3.pdf', title='Clearing (F4) - Order Change',
 sub='Transfer System 404 - Operator Guide - what you do, what the TS does, what the lamps mean',
 footer='TS 404 - Clearing (F4) - Operator Guide - Rev. 3 - 2026-11-20', page='Page',
 h_what='What clearing does',
 what='At the end of an order, clearing empties conveyors <b>C1 to C10</b> into C11/C12/C13 and C21/C22/C23, while the bottomer finishes the order. '
      'Then the next order fills C1 to C10 and <b>waits on C10</b> until the operator confirms with the <b>New Order Button</b>. '
      'This keeps the two orders <b>apart</b>: no packets of the old order are left on C10, and the new order never joins the old one.',
 h_steps='Step by step', col=('#','What happens','Who'), OP='Operator', TS='TS',
 steps=[('OP','<b>Last packet of order A has left the 2145.</b> Press <b>F4</b> on the LAUER panel (or the Broom button {B} on the HMI).'),
        ('TS','Clearing runs: feeding from the 2145 stops, C1 to C9 empty one after the other, then C10 empties into C11 or C21. '
              '<b>HMI clearing lamp blinks.</b> No action needed - let it run. Clearing ends by itself.'),
        ('OP','<b>Clearing done</b>: feeding is allowed again, the HMI clearing lamp is solid. Set up order B on the 2145 and start it when ready.'),
        ('TS','Order B fills C1 to C10. <b>C10 holds order B</b> - nothing leaves C10. The <b>New Order Button lamp is SOLID</b>: '
              'the TS is waiting for the bottomer to finish order A.'),
        ('TS','When C11-C23 and the Loader are <b>empty</b>, the <b>New Order Button lamp BLINKS</b>.'),
        ('OP','<b>Press the New Order Button once</b> (short push). C10 sends order B. The order change is done.')],
 h_lamp='New Order Button lamp (feeder box X121) - what it means', lcol=('Lamp','Meaning','What to do'),
 lamps=[('off','<b>OFF</b> - normal production, or clearing running','Nothing.'),
        ('solid','<b>SOLID</b> - C10 is holding the new order. The TS is not ready yet (bottomer still on the old order).','<b>Wait.</b> A short push does nothing.'),
        ('blink','<b>BLINKING</b> - C11-C23 and the Loader are empty. Ready.','<b>Press the New Order Button once</b> (short push).')],
 h_sp='Special cases', scol=('Situation','What to do'),
 sp=[('Lamp <b>solid for a long time</b>, but C11-C23 and the Loader are <b>visibly empty</b> (TS stuck)',
      '<b>Check by eye</b> that C11, C12, C13, C21, C22, C23 and the Loader are empty, then <b>hold the New Order Button for 3 seconds</b>. '
      'C10 sends the new order. <font color="#c62828"><b>Never do this while packets of the old order are still on C11-C23 or in the Loader: the orders would join.</b></font>'),
     ('Clearing started <b>by mistake</b>','Cancel on the LAUER panel: while F4 is active, press <b>ENT and CLR together</b>. (HMI: switch the Broom button {B} off.)'),
     ('<b>F4 pressed again</b> while C10 is holding the new order','A new clearing starts and empties C10 too (the new order on C10 is cleared out). Only press F4 when you really want a new order change.'),
     ('Clearing seems <b>slow</b> to finish','Normal: C10 must have run its full length with nothing on it before clearing ends. If C11/C21 are full, it finishes the next time C11 or C21 can take a load.'),
     ('Lamp never lights at all, but the New Order Button works','Lamp or wiring fault: do a lamp test, call maintenance.')],
 h_dd="Do / Don't", do='DO', dont="DON'T",
 dos='Press F4 only after the <b>last packet of the order</b> has left the 2145.<br/>Wait for the lamp to <b>blink</b>, then push the New Order Button <b>once</b>.<br/>Check C11-C23 and the Loader <b>by eye</b> before a 3-second push.',
 donts="Don't hold the New Order Button for 3 s while the old order is still on C11-C23 or in the Loader.<br/>Don't press F4 twice for one order change.<br/>Don't reset or hold SIGNAL to \"help\" the clearing - let it finish by itself.",
 h_card='Quick card',
 card='<b>F4</b> = start order change (after the last packet).<br/><b>HMI clearing lamp blinking</b> = clearing running - wait.<br/>'
      '<b>New Order Button solid</b> = new order waiting on C10 - wait.<br/><b>New Order Button blinking</b> = push it <u>once</u>.<br/>'
      '<b>Solid a long time + TS empty</b> = check by eye, then hold the New Order Button for 3 s.'),
'fr':dict(
 file='Clearing_F4_Guide_Operateur_FR_Rev3.pdf', title='Vidage (F4) - Changement de commande',
 sub="Transfer System 404 - Guide de l'opérateur - ce que vous faites, ce que fait le TS, ce que veulent dire les lampes",
 footer="TS 404 - Vidage (F4) - Guide de l'opérateur - Rév. 3 - 2026-11-20", page='Page',
 h_what='À quoi sert le Vidage (F4)',
 what="À la fin d'une commande, le Vidage (F4) vide les convoyeurs <b>C1 à C10</b> vers C11/C12/C13 et C21/C22/C23, pendant que le bottomer termine la commande. "
      "Ensuite, la commande suivante remplit C1 à C10 et <b>attend sur C10</b> jusqu'à ce que l'opérateur confirme avec le <b>bouton Nouvelle Commande</b>. "
      "Ainsi les deux commandes restent <b>séparées</b> : aucun paquet de l'ancienne commande ne reste sur C10, et la nouvelle commande ne se colle jamais à l'ancienne.",
 h_steps='Étape par étape', col=('#','Ce qui se passe','Qui'), OP='Opérateur', TS='TS',
 steps=[('OP',"<b>Le dernier paquet de la commande A est sorti de la 2145.</b> Appuyer sur <b>F4</b> au panneau LAUER (ou sur le bouton « balai » {B} de l'HMI)."),
        ('TS',"Le Vidage (F4) se fait : l'alimentation par la 2145 s'arrête, C1 à C9 se vident l'un après l'autre, puis C10 se vide dans C11 ou C21. "
              "<b>La lampe Vidage (F4) de l'HMI clignote.</b> Aucune action - laisser faire. Le Vidage (F4) se termine tout seul."),
        ('OP',"<b>Vidage (F4) terminé</b> : l'alimentation est de nouveau permise, la lampe Vidage (F4) de l'HMI est fixe. Préparer la commande B sur la 2145 et la démarrer quand prêt."),
        ('TS',"La commande B remplit C1 à C10. <b>C10 retient la commande B</b> - rien ne sort de C10. La <b>lampe du bouton Nouvelle Commande est FIXE</b> : "
              "le TS attend que le bottomer finisse la commande A."),
        ('TS',"Quand C11-C23 et le Loader sont <b>vides</b>, la <b>lampe du bouton Nouvelle Commande CLIGNOTE</b>."),
        ('OP',"<b>Appuyer une fois sur le bouton Nouvelle Commande</b> (appui court). C10 envoie la commande B. Le changement de commande est terminé.")],
 h_lamp='Lampe du bouton Nouvelle Commande (boîte X121 du Loader) - signification', lcol=('Lampe','Signification','Quoi faire'),
 lamps=[('off',"<b>ÉTEINTE</b> - production normale, ou Vidage (F4) en cours",'Rien.'),
        ('solid',"<b>FIXE</b> - C10 retient la nouvelle commande. Le TS n'est pas encore prêt (le bottomer finit l'ancienne commande).","<b>Attendre.</b> Un appui court ne fait rien."),
        ('blink',"<b>CLIGNOTE</b> - C11-C23 et le Loader sont vides. Prêt.","<b>Appuyer une fois sur le bouton Nouvelle Commande</b> (appui court).")],
 h_sp='Cas particuliers', scol=('Situation','Quoi faire'),
 sp=[("Lampe <b>fixe depuis longtemps</b>, mais C11-C23 et le Loader sont <b>vides à l'oeil</b> (TS bloqué)",
      "<b>Vérifier à l'oeil</b> que C11, C12, C13, C21, C22, C23 et le Loader sont vides, puis <b>tenir le bouton Nouvelle Commande 3 secondes</b>. "
      "C10 envoie la nouvelle commande. <font color=\"#c62828\"><b>Ne jamais le faire tant que des paquets de l'ancienne commande sont encore sur C11-C23 ou dans le Loader : les commandes se colleraient.</b></font>"),
     ("Vidage (F4) lancé <b>par erreur</b>","Annuler au panneau LAUER : F4 actif, appuyer <b>ENT et CLR en même temps</b>. (HMI : remettre le bouton « balai » {B} à l'arrêt.)"),
     ("<b>F4 appuyé de nouveau</b> pendant que C10 retient la nouvelle commande","Un nouveau Vidage (F4) démarre et vide aussi C10 (la nouvelle commande sur C10 est vidée). N'appuyer sur F4 que pour un vrai changement de commande."),
     ("Le Vidage (F4) semble <b>long</b> à finir","Normal : C10 doit avoir roulé toute sa longueur sans rien dessus avant la fin du Vidage (F4). Si C11/C21 sont pleins, il finit dès que C11 ou C21 peut prendre une charge."),
     ("La lampe ne s'allume jamais, mais le bouton Nouvelle Commande fonctionne","Lampe ou câblage défectueux : faire un test lampes, appeler la maintenance.")],
 h_dd='À faire / À ne pas faire', do='À FAIRE', dont='À NE PAS FAIRE',
 dos="Appuyer sur F4 seulement quand le <b>dernier paquet de la commande</b> est sorti de la 2145.<br/>Attendre que la lampe <b>clignote</b>, puis appuyer <b>une fois</b> sur le bouton Nouvelle Commande.<br/>Vérifier C11-C23 et le Loader <b>à l'oeil</b> avant un appui de 3 secondes.",
 donts="Ne pas tenir le bouton Nouvelle Commande 3 s tant que l'ancienne commande est encore sur C11-C23 ou dans le Loader.<br/>Ne pas appuyer deux fois sur F4 pour un seul changement de commande.<br/>Ne pas faire de reset ni tenir SIGNAL pour « aider » le Vidage (F4) - le laisser finir tout seul.",
 h_card='Aide-mémoire',
 card="<b>F4</b> = début du changement de commande (après le dernier paquet).<br/><b>Lampe Vidage (F4) de l'HMI clignote</b> = Vidage (F4) en cours - attendre.<br/>"
      "<b>Bouton Nouvelle Commande fixe</b> = nouvelle commande en attente sur C10 - attendre.<br/><b>Bouton Nouvelle Commande clignote</b> = appuyer <u>une fois</u>.<br/>"
      "<b>Fixe longtemps + TS vide</b> = vérifier à l'oeil, puis tenir le bouton Nouvelle Commande 3 s.")}

ICONFILE=os.path.join(os.path.dirname(os.path.abspath(__file__)),'broom_icon.png')
def sub_icon(L,outdir):
    tag='<img src="%s" width="13" height="13" valign="-2"/>'%ICONFILE
    f=lambda v: v.replace('{B}',tag) if isinstance(v,str) else ([f(x) for x in v] if isinstance(v,list) else (tuple(f(x) for x in v) if isinstance(v,tuple) else v))
    return {k:f(v) for k,v in L.items()}
def build(lang,outdir):
    L=sub_icon(T[lang],outdir); out=os.path.join(outdir,L['file'])
    def footer(c,doc):
        c.saveState(); c.setFont('Helvetica',8); c.setFillColor(colors.grey)
        c.drawString(18*mm,10*mm,L['footer']); c.drawRightString(letter[0]-18*mm,10*mm,f"{L['page']} {doc.page}"); c.restoreState()
    doc=SimpleDocTemplate(out,pagesize=letter,leftMargin=18*mm,rightMargin=18*mm,topMargin=15*mm,bottomMargin=18*mm,title=L['title'],author='TS 404')
    W=letter[0]-36*mm; s=[P(L['title'],H1),P(L['sub'],SUB),P(L['h_what'],H2),P(L['what']),P(L['h_steps'],H2)]
    rows=[[P(L['col'][0],BC),P(L['col'][1]),P(L['col'][2],BC)]]; ex=[]
    for i,(who,txt) in enumerate(L['steps'],1):
        rows.append([P(f'<b>{i}</b>',BC),P(txt,STEP),P(f"<b>{L[who]}</b>",BC)])
        if who=='OP': ex.append(('BACKGROUND',(2,i),(2,i),LIGHT))
    s.append(tbl(rows,[10*mm,W-34*mm,24*mm],ex))
    s.append(P(L['h_lamp'],H2))
    lr=[[P(f"<b>{L['lcol'][0]}</b>",BC),P(f"<b>{L['lcol'][1]}</b>"),P(f"<b>{L['lcol'][2]}</b>")]]
    for st,m,a in L['lamps']: lr.append([Lamp(st),P(m),P(a)])
    s.append(tbl(lr,[20*mm,W*0.5,W-20*mm-W*0.5]))
    s.append(PageBreak()); s.append(P(L['h_sp'],H2))
    sr=[[P(f"<b>{L['scol'][0]}</b>"),P(f"<b>{L['scol'][1]}</b>")]]+[[P(a),P(b)] for a,b in L['sp']]
    s.append(tbl(sr,[W*0.35,W*0.65]))
    s.append(P(L['h_dd'],H2))
    s.append(tbl([[P(f"<b><font color='#2e7d32'>{L['do']}</font></b>",BC),P(f"<b><font color='#c62828'>{L['dont']}</font></b>",BC)],[P(L['dos']),P(L['donts'])]],
                 [W/2,W/2],header=False,extra=[('BACKGROUND',(0,0),(-1,0),GREY),('VALIGN',(0,1),(-1,1),'TOP')]))
    s.append(P(L['h_card'],H2))
    s.append(tbl([[P(f"<font size='12'>{L['card']}</font>")]],[W],header=False,
                 extra=[('BACKGROUND',(0,0),(-1,-1),LIGHT),('BOX',(0,0),(-1,-1),1.5,AMBER),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]))
    doc.build(s,onFirstPage=footer,onLaterPages=footer); return out

if __name__=='__main__':
    for lang in ('en','fr'): print(build(lang,sys.argv[1] if len(sys.argv)>1 else '.'))
