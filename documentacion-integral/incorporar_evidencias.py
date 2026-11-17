"""Copia evidencias autorizadas y prepara tablas y CSV para el informe."""
import collections
import contextlib
import csv
import hashlib
import io
import json
from pathlib import Path
import runpy
import shutil
import statistics
import sys
import types

ROOT=Path(__file__).resolve().parent
EXT=Path('/home/kedap/Documentos/escuela/facial/reconocimiento_facial')
DEST=ROOT/'evidencias-2026-11-13'
DEST.mkdir(exist_ok=True)
shutil.copy2(EXT/'resultados/pruebas.csv',DEST/'pruebas-2026-11-13.csv')
shutil.copy2(ROOT.parent/'evidencias/avances-2026-10-13/resultados/pruebas.csv',DEST/'pruebas-2026-10-13.csv')
shutil.copy2(EXT/'analizar.py',DEST/'analizar-fuente.py')
images=sorted((EXT/'Imagenes').glob('*.png'))
manifest=[]
for i,p in enumerate(images,1):
 target=DEST/'imagenes'/f'{i:02d}.png'
 shutil.copy2(p,target)
 manifest.append(dict(origen=str(p),copia=str(target.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))

def read(p):
 with p.open(newline='',encoding='utf-8') as f:return list(csv.DictReader(f))

def summarize(rows):
 groups=collections.defaultdict(list)
 for r in rows:groups[r['tecnologia'],r['condicion'],r['resultado_esperado']].append(r)
 result=[]
 for (tec,cond,esp),g in sorted(groups.items()):
  correct=sum(int(r['correcto']) for r in g)
  # Mismas reglas de analizar.py; comprobación adicional de etiquetas.
  assert all(int(r['correcto'])==int((r['resultado_obtenido']=='acepta' and r['identidad_detectada']==r['sujeto']) if esp=='acepta' else r['resultado_obtenido']!='acepta') for r in g)
  fr=sum(r['resultado_obtenido']!='acepta' for r in g) if esp=='acepta' else 0
  fa=sum(r['resultado_obtenido']=='acepta' and (esp=='rechaza' or r['identidad_detectada']!=r['sujeto']) for r in g)
  times=[float(r['tiempo_ms']) for r in g]
  result.append(dict(tecnologia=tec,condicion=cond,resultado_esperado=esp,intentos=len(g),aciertos=correct,porcentaje_correcto=100*correct/len(g),falsos_rechazos=fr,falsas_aceptaciones=fa,media_ms=statistics.mean(times),mediana_ms=statistics.median(times),maximo_ms=max(times)))
 return result

allgroups={}
for date in ['2026-10-13','2026-11-13']:
 p=DEST/f'pruebas-{date}.csv'
 groups=summarize(read(p));allgroups[date]=groups
 with (DEST/f'analisis-{date}.csv').open('w',newline='',encoding='utf-8-sig') as f:
  writer=csv.DictWriter(f,fieldnames=list(groups[0]));writer.writeheader()
  for row in groups:
   writer.writerow({k:round(v,4) if isinstance(v,float) else v for k,v in row.items()})
 # Ejecuta analizar.py original con solo la ruta de CSV_RESULTADOS aislada.
 # Evita importar cámara/modelos: analizar.py no usa ningún otro atributo de comun.
 stub=types.ModuleType('comun');stub.CSV_RESULTADOS=p
 previous=sys.modules.get('comun');sys.modules['comun']=stub
 oldargv=sys.argv;sys.argv=['analizar.py','--csv',str(p)]
 capture=io.StringIO()
 try:
  with contextlib.redirect_stdout(capture):runpy.run_path(str(DEST/'analizar-fuente.py'),run_name='__main__')
 finally:
  sys.argv=oldargv
  if previous is None:sys.modules.pop('comun',None)
  else:sys.modules['comun']=previous
 (DEST/f'analizar-salida-{date}.txt').write_text(capture.getvalue())

def d(v):return f'{v:.1f}'.replace('.',',')
# Tablas completas para evitar insertar input dentro de una alineación.
new=allgroups['2026-11-13']
text=r'\begin{tabular}{P{2.7cm}rrrrrrrr}\toprule Condición & $n$ & Aciertos & \% & FR & FA & Media & Mediana & Máx. \\ \midrule'+'\n'
for g in new:
 name='Foto en celular' if g['condicion']=='foto_celular' else 'Luz normal'
 text+=' & '.join([name,str(g['intentos']),str(g['aciertos']),d(g['porcentaje_correcto']),str(g['falsos_rechazos']),str(g['falsas_aceptaciones']),d(g['media_ms']),d(g['mediana_ms']),d(g['maximo_ms'])])+r' \\'+'\n'
text+=r'\bottomrule\end{tabular}'
(DEST/'tabla-resumen.tex').write_text(text)
rows=read(DEST/'pruebas-2026-11-13.csv')
text=r'\begin{tabular}{rlclllrr}\toprule N.º & Hora & Sujeto & Condición & Resultado & Identidad & ms & OK \\ \midrule'+'\n'
for i,r in enumerate(rows,1):
 label={'rechaza_vida':'Rechazo vida','rechaza':'Rechazo','acepta':'Acepta'}[r['resultado_obtenido']]
 text+=' & '.join([str(i),r['fecha_hora'][11:],r['sujeto'],'Foto' if r['condicion']=='foto_celular' else 'Luz normal',label,r['identidad_detectada'] or '--',d(float(r['tiempo_ms'])),r['correcto']])+r' \\'+'\n'
text+=r'\bottomrule\end{tabular}'
(DEST/'tabla-intentos.tex').write_text(text)
for p in sorted(DEST.glob('*.csv')):
 manifest.append(dict(copia=str(p.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),filas=len(read(p))))
(DEST/'procedencia.json').write_text(json.dumps(dict(fecha_revision='2026-11-13',nota='Series de octubre y noviembre separadas. Analizar original ejecutado aislando únicamente la constante de ruta de comun.',archivos=manifest,resumenes=allgroups),ensure_ascii=False,indent=2)+'\n')
print('Noviembre:',len(rows),'intentos;',sum(int(r['correcto']) for r in rows),'aciertos;',len(images),'imágenes')
assert len(rows)==24 and sum(int(r['correcto']) for r in rows)==11
assert sum(g['falsos_rechazos'] for g in new)==11 and sum(g['falsas_aceptaciones'] for g in new)==2
