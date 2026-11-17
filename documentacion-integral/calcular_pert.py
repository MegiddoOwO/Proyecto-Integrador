"""Reproduce PERT/CPM desde la copia de la pestaña gid=1001, sin modificar Sheets."""
from pathlib import Path
from fractions import Fraction
import json
import math

ROOT = Path(__file__).resolve().parent
source = json.loads((ROOT/'pert-hoja-fuente.json').read_text())
nodes = {}
for row in source['values'][1:24]:
    key,name,dep,_,a,m,b,*rest=row
    pre=[] if dep=='-' else dep.split(',')
    a,m,b=map(int,(a,m,b))
    assert all(p in nodes for p in pre), f'Dependencia inválida o fuera de orden: {key}'
    te=Fraction(a+4*m+b,6)
    es=max((nodes[p]['EF'] for p in pre),default=Fraction(0))
    nodes[key]=dict(id=key,nombre=name,predecesoras=pre,a=a,m=m,b=b,te=te,
                    varianza=Fraction((b-a)**2,36),ES=es,EF=es+te)
T=max(x['EF'] for x in nodes.values())
for key,x in reversed(list(nodes.items())):
    successors=[y for y in nodes.values() if key in y['predecesoras']]
    x['LF']=min((s['LS'] for s in successors),default=T)
    x['LS']=x['LF']-x['te']
    x['holgura']=x['LS']-x['ES']
    assert x['holgura']>=0
critical=[k for k,x in nodes.items() if x['holgura']==0]
def critical_paths(k):
    x=nodes[k]
    if not x['predecesoras']: return [[k]]
    return [path+[k] for p in x['predecesoras'] if nodes[p]['EF']==x['ES'] for path in critical_paths(p)]
paths=critical_paths('W')
variances=[sum(nodes[k]['varianza'] for k in path) for path in paths]
variance=variances[0]

def num(x): return f'{float(x):.2f}'.replace('.',',')

with (ROOT/'pert-estimaciones.tex').open('w') as f:
    for k,x in nodes.items():
        pre=', '.join(x['predecesoras']) or '--'
        f.write(f"{k} & {pre} & {x['a']} & {x['m']} & {x['b']} & {num(x['te'])} & {num(x['varianza'])} " + chr(92)*2 + "\n")
with (ROOT/'pert-calculos.tex').open('w') as f:
    for k,x in nodes.items():
        mark='Sí' if x['holgura']==0 else 'No'
        f.write(f"{k} & {num(x['ES'])} & {num(x['EF'])} & {num(x['LS'])} & {num(x['LF'])} & {num(x['holgura'])} & {mark} " + chr(92)*2 + "\n")
with (ROOT/'gantt.tex').open('w') as f:
    f.write('\\begin{tikzpicture}[x=0.24cm,y=-0.40cm,font=\\scriptsize]\n')
    for t in range(0,61,5):
        f.write(f'\\draw[gray!20] ({t},0) -- ({t},23.8);\\node[above] at ({t},0) {{{t}}};\n')
    for row,(k,x) in enumerate(nodes.items(),1):
        color='critico' if x['holgura']==0 else 'azul'
        f.write(f"\\node[anchor=east] at (-0.4,{row}) {{{k}}};\\fill[{color}] ({float(x['ES'])},{row-0.23}) rectangle ({float(x['EF'])},{row+0.23});\n")
    f.write('\\end{tikzpicture}\n')
serializable={k:{kk:float(vv) if isinstance(vv,Fraction) else vv for kk,vv in v.items()} for k,v in nodes.items()}
(ROOT/'pert-resultados.json').write_text(json.dumps(dict(fuente='PERT Escanea y Entra, gid=1001, A2:J24',duracion=float(T),actividades_criticas=critical,rutas_criticas=paths,varianzas_rutas=[float(v) for v in variances],suma_tiempos=float(sum(x['te'] for x in nodes.values())),actividades=serializable),ensure_ascii=False,indent=2)+'\n')
print('Actividades críticas:', ', '.join(critical))
print('Duración:',float(T),'días; varianza:',float(variance),'desviación:',round(math.sqrt(variance),3))
print('Total de duraciones',float(sum(x['te'] for x in nodes.values())))
for k,x in nodes.items():print(k,'ES',num(x['ES']),'EF',num(x['EF']),'H',num(x['holgura']))
# Escenario condicional: A-F efectivamente cerradas, lo demás pendiente.
rem={}
for k,x in nodes.items():
    if k in 'ABCDEF': rem[k]=Fraction(0)
    else: rem[k]=max((rem[p] for p in x['predecesoras']),default=Fraction(0))+x['te']
print('Escenario A-F cerradas, duración restante:',float(rem['W']))
assert len(nodes)==23
assert T==Fraction(347,6)
assert abs(sum(x['te'] for x in nodes.values())-Fraction(647,6))==0

for path,v in zip(paths,variances): print('Ruta:', ' -> '.join(path), 'duración', float(sum(nodes[k]['te'] for k in path)), 'varianza',float(v),'sigma',math.sqrt(v))

# Tablas completas: la entrada de archivo queda fuera de la alineación.
for filename,header,footer in [
 ('pert-estimaciones.tex', r"\begin{tabular}{lP{2.2cm}rrrrr}\toprule ID & Predecesoras & $a$ & $m$ & $b$ & $t_e$ & $\sigma^2$ \\ \midrule", r"\midrule \multicolumn{5}{l}{Suma de las 23 actividades} & 107,83 & 15,92 \\ \bottomrule\end{tabular}"),
 ('pert-calculos.tex',r"\begin{tabular}{lrrrrrl}\toprule ID & ES & EF & LS & LF & Holgura & Crítica \\ \midrule",r"\bottomrule\end{tabular}")]:
 p=ROOT/filename
 p.write_text(header+'\n'+p.read_text()+footer+'\n')
