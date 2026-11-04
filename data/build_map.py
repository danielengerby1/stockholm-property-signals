import json, gzip, math
import shapely
from shapely.geometry import shape, Polygon, MultiPolygon, LineString, box, Point, mapping
from shapely.ops import unary_union, polygonize
from shapely.validation import make_valid

BB=(17.62,58.95,18.98,59.56)
FRAME=box(*BB)
d=json.load(gzip.open('/mnt/user-data/uploads/Downloads/stockholm_basemap.json.gz'))
B=json.load(open('/home/claude/geo/bnd.json'))
kom=json.load(open('/home/claude/geo/kommuner.geojson'))
regso=json.load(open('/home/claude/geo/regso_0180.json'))
rmap=json.load(open('/home/claude/stockholm-property-signals/data/regso_to_district_map.json'))

def poly(pg):
    try:
        p=Polygon(pg[0],[h for h in pg[1:] if len(h)>=4])
        if not p.is_valid: p=make_valid(p)
        return p
    except Exception: return None
def polys_of(g):
    if g.is_empty: return []
    if g.geom_type=='Polygon': return [g]
    if g.geom_type=='MultiPolygon': return list(g.geoms)
    if g.geom_type=='GeometryCollection': return [x for gg in g.geoms for x in polys_of(gg)]
    return []

water=unary_union([p for p in (poly(pg) for c,pg in d['water']) if p is not None and not p.is_empty]).buffer(0)
water=water.intersection(FRAME)
land=FRAME.difference(water)
# drop tiny islands (< ~0.5 ha) to save bytes
land=MultiPolygon([p for p in polys_of(land) if p.area>8e-8])
print('water/land ok', water.area, land.area)

green=unary_union([p for p in (poly(pg) for c,pg in d['green']) if p is not None and not p.is_empty]).buffer(0).intersection(land)
print('green ok')

# ---- municipality polygons from boundary lines
lines=[LineString(l) for lvl,mar,l in B if len(l)>=2]
strips=unary_union(lines).buffer(0.00012)
faces=polys_of(FRAME.difference(strips))
print('faces',len(faces))
KOMS={'Stockholm','Solna','Sundbyberg','Nacka','Lidingö','Danderyd','Täby','Sollentuna','Järfälla','Huddinge','Botkyrka','Haninge','Tyresö','Värmdö',
      'Södertälje','Norrtälje','Sigtuna','Nynäshamn','Vaxholm','Salem','Upplands Väsby','Upplands-Bro','Ekerö','Vallentuna','Österåker','Nykvarn'}
kpoly={f['properties']['kom_namn']:make_valid(shape(f['geometry'])) for f in kom['features'] if f['properties']['kom_namn'] in KOMS}
groups={k:[] for k in kpoly}
for fc in faces:
    if fc.area<1e-9: continue
    pt=fc.representative_point(); best=None
    for k,kp in kpoly.items():
        if kp.contains(pt): best=k; break
    if best is None:
        # nearest coarse polygon (for faces in the sea etc.)
        dist=min(((kp.distance(pt),k) for k,kp in kpoly.items()))
        if dist[0]<0.02: best=dist[1]
    if best: groups[best].append(fc)
mun={k:unary_union(v).buffer(0.00014).intersection(FRAME) for k,v in groups.items() if v}
seen=None
for k in sorted(mun,key=lambda k:-mun[k].area):
    if seen is not None: mun[k]=mun[k].difference(seen)
    seen=mun[k] if seen is None else unary_union([seen,mun[k]])
# check: coverage sanity
for k in ['Stockholm','Solna','Lidingö','Värmdö']:
    print(k, round(mun[k].area,4), round(kpoly[k].area,4))

# ---- Stockholm districts from RegSO, fitted to the OSM municipal polygon
rs={r[0]:make_valid(shape({'type':'MultiPolygon','coordinates':r[2]})) for r in regso}
dist={dn:unary_union([rs[c] for c in codes if c in rs]).buffer(0) for dn,codes in rmap.items()}
STO=mun['Stockholm']
dist={k:v.intersection(STO) for k,v in dist.items()}
gap=STO.difference(unary_union(list(dist.values())))
for gp in polys_of(gap):
    if gp.area<1e-10: continue
    # assign to district sharing the longest border, else nearest
    best=max(dist, key=lambda k: gp.buffer(1e-5).intersection(dist[k]).area)
    if gp.buffer(1e-5).intersection(dist[best]).area==0: best=min(dist, key=lambda k: dist[k].distance(gp))
    dist[best]=unary_union([dist[best],gp])
# remove overlaps (first come wins)
done=None
for k in list(dist):
    if done is not None: dist[k]=dist[k].difference(done)
    done=dist[k] if done is None else unary_union([done,dist[k]])

AREA_MUNI=['Solna','Sundbyberg','Nacka','Lidingö','Danderyd','Täby','Sollentuna','Järfälla','Huddinge','Botkyrka','Haninge','Tyresö','Värmdö']
areas={**dist, **{k:mun[k] for k in AREA_MUNI}}
others={k:mun[k] for k in mun if k not in AREA_MUNI and k!='Stockholm'}
areas={k:v.intersection(land).buffer(0) for k,v in areas.items()}
others={k:v.intersection(land).buffer(0) for k,v in others.items()}

# ---- projection to integer units: 1 unit = 1e-4 deg latitude
LAT0=59.3; KX=math.cos(math.radians(LAT0)); U=1e4
def P(lon,lat): return (round((lon-BB[0])*KX*U), round((BB[3]-lat)*U))
W,H=P(BB[2],BB[1])
def ring_d(coords):
    pts=[P(x,y) for x,y in coords]
    out=[]; prev=None
    for p in pts:
        if p!=prev: out.append(p); prev=p
    if len(out)<3: return ''
    s='M%d %d'%out[0]; px,py=out[0]
    for x,y in out[1:]:
        s+='l%d %d'%(x-px,y-py); px,py=x,y
    return s+'z'
CITY=box(17.84,59.22,18.27,59.44)
def split_d(g,t_in,t_out,min_out):
    a=g.intersection(CITY); o=g.difference(CITY)
    o=MultiPolygon([p for p in polys_of(o) if p.area>min_out]) if polys_of(o) else o
    return geom_d(a,t_in)+geom_d(o,t_out)
def geom_d(g,tol,minA=0):
    g=g.simplify(tol,preserve_topology=True)
    s=''
    for p in polys_of(g):
        if p.area<max(tol*tol*2,minA): continue
        s+=ring_d(p.exterior.coords)+''.join(ring_d(i.coords) for i in p.interiors)
    return s.replace('l0 0','')
def line_d(g,tol):
    g=g.simplify(tol)
    parts=[g] if g.geom_type=='LineString' else list(getattr(g,'geoms',[]))
    s=''
    for ln in parts:
        pts=[P(x,y) for x,y in ln.coords]
        if len(pts)<2: continue
        s+='M%d %d'%pts[0]; px,py=pts[0]
        for x,y in pts[1:]:
            if (x,y)!=(px,py): s+='l%d %d'%(x-px,y-py); px,py=x,y
    return s

T_AREA=0.00006; T_BASE=0.00008
out={'W':W,'H':H,'bb':BB,'lat0':LAT0,'u':U}
out['land']=split_d(land,0.00006,0.00022,4e-6)
out['green']=split_d(green,0.00014,0.0004,3e-5)
out['areas']={k:split_d(v,0.00006,0.00022,4e-6) for k,v in areas.items()}
out['others']={k:geom_d(v,0.0003,2e-5) for k,v in others.items()}
roads={'m':[],'t':[],'p':[]}
for c,l in d['roads']:
    if len(l)>=2: roads[c].append(LineString(l))
out['roads']={k:line_d(unary_union(v).intersection(FRAME),0.0001) for k,v in roads.items()}
rail=[LineString(l) for c,l in d['rail'] if len(l)>=2 and c.startswith('rail')]
lrail=[LineString(l) for c,l in d['rail'] if len(l)>=2 and c.startswith('transit')]
out['rail']=line_d(unary_union(rail).intersection(FRAME),0.0001)
out['lrail']=line_d(unary_union(lrail).intersection(FRAME),0.0001)
# label points: pole of inaccessibility-ish via representative point of largest polygon
def labpt(g):
    ps=sorted(polys_of(g),key=lambda p:-p.area)
    if not ps: return None
    try: c=shapely.polylabel(ps[0],0.0005)
    except Exception: c=ps[0].representative_point()
    return P(c.x,c.y)
out['lab']={k:labpt(v) for k,v in areas.items()}
out['olab']={k:labpt(v) for k,v in others.items()}
# bbox of each area for zoom-to
def bbp(g):
    x0,y0,x1,y1=g.bounds; a=P(x0,y1); b=P(x1,y0); return [a[0],a[1],b[0]-a[0],b[1]-a[1]]
out['abox']={k:bbp(v) for k,v in areas.items()}
pl=[]
for name,cls,rank,(x,y) in d['places']:
    if not (BB[0]<x<BB[2] and BB[1]<y<BB[3]): continue
    pl.append([name,{'town':1,'suburb':2,'quarter':3,'neighbourhood':3,'island':4}.get(cls,3),*P(x,y)])
out['places']=pl
s=json.dumps(out,ensure_ascii=False,separators=(',',':'))
open('/home/claude/geo/basemap_out.json','w').write(s)
print('size',len(s),{k:len(json.dumps(v)) for k,v in out.items()})
print('areas', {k:len(v) for k,v in out['areas'].items()})
