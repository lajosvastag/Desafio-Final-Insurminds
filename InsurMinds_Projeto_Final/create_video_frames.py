from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT=Path('Projeto_Final_Artefatos/video_frames'); OUT.mkdir(parents=True, exist_ok=True)
W,H=1280,720
BG='#F9F8F4'; INK='#172A3A'; GOLD='#D49A31'; MUTED='#66737E'; RED='#B65745'; SURF='#F0EFE9'
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; serif='/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
def F(path,size): return ImageFont.truetype(path,size)

def base(title, kicker, idx):
    im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
    d.rectangle((0,0,W,12),fill=INK); d.rectangle((0,12,W,17),fill=GOLD)
    d.text((60,48),kicker.upper(),font=F(bold,18),fill=GOLD)
    d.text((60,82),title,font=F(serif,42),fill=INK)
    d.line((60,150,1220,150),fill='#D8D0C3',width=1)
    d.text((60,670),'InsurMinds  ·  Autoria: Curié Edge',font=F(font,16),fill=MUTED)
    d.text((1180,670),f'{idx:02d}',font=F(bold,16),fill=INK)
    return im,d

def save(im,n): im.save(OUT/f'{n}.png')
# 1
im,d=base('Análise inteligente de apólices D&O','Projeto final · MVP',1)
d.text((60,225),'Compare proteção.',font=F(serif,68),fill=INK); d.text((60,310),'Encontre as lacunas.',font=F(serif,68),fill=GOLD)
d.text((66,430),'Do documento jurídico ao sinal executivo de risco.',font=F(font,25),fill=INK)
d.rectangle((940,230,1140,430),outline=GOLD,width=5); d.text((998,270),'I',font=F(serif,130),fill=GOLD); d.text((956,420),'INSURMINDS',font=F(bold,18),fill=INK)
save(im,'01_capa')
#2
im,d=base('O problema: complexidade sem escala','O desafio',2)
items=[('01','Horas de leitura','Apólices extensas e\nredigidas em linguagem\njurídica.'),('02','Dados dispersos','Limites, franquias e\nexclusões aparecem em\npontos diferentes.'),('03','Lacunas críticas','Diferenças sutis podem\nalterar a proteção\nefetiva.')]
for i,(n,t,desc) in enumerate(items):
 x=60+i*380; d.rectangle((x,220,x+340,490),fill=SURF,outline=INK,width=2); d.text((x+24,245),n,font=F(bold,36),fill=GOLD); d.text((x+24,315),t,font=F(bold,25),fill=INK); d.multiline_text((x+24,365),desc,font=F(font,19),fill=INK,spacing=7)
save(im,'02_problema')
#3
im,d=base('Fluxo de processamento','Como funciona',3)
steps=[('1','Receber','PDF ou imagem'),('2','Extrair','PyMuPDF / OCR'),('3','Estruturar','IA + regras'),('4','Comparar','diferenças')]
for i,(n,t,desc) in enumerate(steps):
 x=70+i*290; d.ellipse((x,270,x+72,342),fill=GOLD); d.text((x+25,283),n,font=F(bold,26),fill=INK); d.text((x,370),t,font=F(bold,24),fill=INK); d.text((x,410),desc,font=F(font,18),fill=MUTED)
 if i<3: d.line((x+78,306,x+250,306),fill=INK,width=3); d.polygon([(x+250,298),(x+270,306),(x+250,314)],fill=GOLD)
d.rectangle((265,500,1015,570),fill=INK); d.text((305,520),'IA Generativa com fallback determinístico auditável',font=F(bold,22),fill=BG)
save(im,'03_fluxo')
#4
im,d=base('Leitura estruturada','O que a plataforma identifica',4)
fields=[('Seguradora','Atlas Seguros S.A.'),('Segurado','Curié Edge Tecnologia Ltda.'),('Limite','R$ 10.000.000,00'),('Retenção','R$ 250.000,00'),('Coberturas','4 identificadas'),('Exclusões','4 identificadas')]
for i,(k,v) in enumerate(fields):
 x=60+(i%3)*380; y=210+(i//3)*155; d.text((x,y),k.upper(),font=F(bold,14),fill=GOLD); d.text((x,y+34),v,font=F(bold,23),fill=INK); d.line((x,y+78,x+320,y+78),fill='#C9C0B4',width=1)
d.text((60,555),'Método: PDF text layer (PyMuPDF) + regras auditáveis',font=F(font,19),fill=MUTED)
save(im,'04_estrutura')
#5
im,d=base('Comparação executiva','Demonstração com duas apólices',5)
headers=['Critério','Norte','Sul']; xs=[60,420,810]
for x,h in zip(xs,headers): d.rectangle((x,215,x+320,270),fill=INK); d.text((x+18,232),h,font=F(bold,18),fill=BG)
rows=[('Limite','R$ 10 mi','R$ 15 mi'),('Retenção','R$ 250 mil','R$ 500 mil'),('Coberturas','4','3'),('Exclusões','4','6')]
for j,row in enumerate(rows):
 y=270+j*70
 for i,val in enumerate(row):
  fill=RED if (j==1 and i==2) or (j==3 and i==2) else (SURF if j%2==0 else BG)
  d.rectangle((xs[i],y,xs[i]+320,y+70),fill=fill); d.text((xs[i]+18,y+24),val,font=F(bold if i else font,19),fill=INK)
d.rectangle((60,575,1130,625),fill='#F8E5DF'); d.text((82,590),'Alerta: maior limite na Sul, mas retenção e exclusões são mais restritivas.',font=F(bold,18),fill=RED)
save(im,'05_comparacao')
#6
im,d=base('Resultado para a decisão','O valor do MVP',6)
metrics=[('82/100','Score Norte'),('74/100','Score Sul'),('JSON','Saída estruturada'),('SQLite','Histórico local')]
for i,(big,small) in enumerate(metrics):
 x=60+i*290; d.text((x,260),big,font=F(serif,40),fill=GOLD); d.text((x,325),small,font=F(bold,18),fill=INK); d.line((x,365,x+230,365),fill=INK,width=2)
d.multiline_text((60,470),'A plataforma reduz o trabalho repetitivo e evidencia\nonde a leitura humana precisa se concentrar.',font=F(font,25),fill=INK,spacing=8)
save(im,'06_resultado')
#7
im,d=base('Próximos passos','Evolução',7)
road=[('Agora','MVP funcional','PDF, OCR, JSON\ne comparação'),('Depois','Evidência por página','Busca semântica\ne revisão humana'),('Futuro','Copiloto jurídico','Benchmark e parecer\nassistido')]
for i,(a,b,c) in enumerate(road):
 x=80+i*390; d.rectangle((x,250,x+310,470),outline=INK,width=2); d.rectangle((x,250,x+310,302),fill=GOLD); d.text((x+18,266),a,font=F(bold,17),fill=INK); d.text((x+18,335),b,font=F(bold,22),fill=INK); d.multiline_text((x+18,390),c,font=F(font,18),fill=INK,spacing=7)
d.text((60,570),'InsurMinds: compare proteção. Encontre as lacunas.',font=F(serif,27),fill=INK)
save(im,'07_fecho')
print(len(list(OUT.glob('*.png'))),'frames created')
