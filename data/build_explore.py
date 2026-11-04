import json, pickle, math, re, unicodedata, os
from shapely.geometry import Point, LineString, box
from shapely.strtree import STRtree
from shapely.ops import unary_union
from shapely.prepared import prep

A=pickle.load(open('/home/claude/geo/areas.pkl','rb')); areas=A['areas']
pois=json.load(open('/home/claude/geo/pois_raw.json'))
streets=json.load(open('/home/claude/geo/streets_raw.json'))
BB=(17.62,58.95,18.98,59.56); LAT0=59.3; KX=math.cos(math.radians(LAT0)); U=1e4
def P(lon,lat): return (round((lon-BB[0])*KX*U), round((BB[3]-lat)*U))
def slug(a): return re.sub(r'[^a-z0-9]+','-',unicodedata.normalize('NFKD',a).encode('ascii','ignore').decode().lower()).strip('-')

prepd={k:prep(v.buffer(0.0006)) for k,v in areas.items()}
by={k:[] for k in areas}
seen=set()
for cat,lon,lat,name,sub in pois:
    key=(cat,round(lon,4),round(lat,4),name)
    if key in seen: continue
    seen.add(key)
    pt=Point(lon,lat)
    for k,pp in prepd.items():
        if pp.contains(pt):
            x,y=P(lon,lat); by[k].append([cat,x,y,name,sub]); break

lines=[(c,LineString(l)) for c,l in streets if len(l)>=2]
tree=STRtree([g for c,g in lines])
def line_d(g):
    parts=[g] if g.geom_type=='LineString' else list(getattr(g,'geoms',[]))
    s=''
    for ln in parts:
        if ln.geom_type!='LineString': continue
        pts=[P(x,y) for x,y in ln.coords]
        if len(pts)<2: continue
        s+='M%d %d'%pts[0]; px,py=pts[0]
        for x,y in pts[1:]:
            if (x,y)!=(px,py): s+='l%d %d'%(x-px,y-py); px,py=x,y
    return s
os.makedirs('/home/claude/stockholm-property-signals/explore',exist_ok=True)
index={}; tot=0
for k,g in areas.items():
    x0,y0,x1,y1=g.bounds; mx=(x1-x0)*0.18; my=(y1-y0)*0.18
    B=box(x0-mx,y0-my,x1+mx,y1+my)
    idx=tree.query(B)
    S={'s':[],'n':[]}
    for i in idx:
        c,ln=lines[i]; cl=ln.intersection(B)
        if not cl.is_empty: S[c].append(cl.simplify(0.00003))
    out={'pois':by[k],'s':line_d(unary_union(S['s'])) if S['s'] else '','n':line_d(unary_union(S['n'])) if S['n'] else ''}
    s=json.dumps(out,ensure_ascii=False,separators=(',',':'))
    open(f'/home/claude/stockholm-property-signals/explore/{slug(k)}.json','w').write(s)
    from collections import Counter
    index[k]={'slug':slug(k),'counts':dict(Counter(p[0] for p in by[k])),'km2':round(g.area*111.32*111.32*KX,1)}
    tot+=len(s); print(k,len(by[k]),len(s))
json.dump(index,open('/home/claude/geo/explore_index.json','w'),ensure_ascii=False)
print('total',tot)
