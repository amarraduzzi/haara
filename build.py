import os,json,random,html
from content import *

BRAND="Haara"
PAL=["241,217,168","232,181,149","217,160,127","196,120,92","185,105,74","207,222,220","134,209,187"]

def L(l,place,label=None,cls="xl"):
    return f'<a class="{cls}" href="{MAIN}/?utm_source=haara&amp;utm_medium={l}&amp;utm_content={place}" rel="noopener">{label or MORE[l]}</a>'

for _l in T:
    T[_l]["arts"]=[dict(a,done=T[_l]["done"],rel=T[_l]["rel"],fine=T[_l]["fine"]) for a in T[_l]["arts"]]

AK=["waschen","wachstum","styling","haartyp"]

# ---------- generated artwork (SVG strands) ----------
def art(seed,w=1600,h=900,n=64):
    r=random.Random(seed)
    o=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid slice"><defs><radialGradient id="g" cx="72%" cy="18%" r="95%"><stop offset="0" stop-color="#1f5256"/><stop offset=".5" stop-color="#0e2326"/><stop offset="1" stop-color="#0a1416"/></radialGradient></defs><rect width="{w}" height="{h}" fill="url(#g)"/><g fill="none" stroke-linecap="round">']
    for i in range(n):
        y0=h*(.04+.92*i/n)+r.uniform(-14,14);amp=r.uniform(40,170);ph=r.uniform(0,6.28);col=r.choice(PAL)
        xs=list(range(-100,w+201,200));pts=[(x,y0+__import__("math").sin(x/300+ph)*amp+__import__("math").sin(x/140+ph*2)*amp*.28) for x in xs]
        d=f"M{pts[0][0]} {pts[0][1]:.0f}"
        for (xa,ya),(xb,yb) in zip(pts,pts[1:]): d+=f"C{xa+80} {ya:.0f} {xb-80} {yb:.0f} {xb} {yb:.0f}"
        o.append(f'<path d="{d}" stroke="rgb({col})" stroke-opacity="{r.uniform(.14,.55):.2f}" stroke-width="{r.uniform(.6,2.4):.1f}"/>')
    o.append('</g></svg>')
    return "".join(o)

def make_assets():
    os.makedirs("assets/img",exist_ok=True)
    for i,nm in enumerate(["pano"]+AK):
        if not os.path.exists(f"assets/img/{nm}.jpg"): open(f"assets/img/{nm}.svg","w").write(art(11+i*7))
    open("assets/haara.svg","w").write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#0a1416"/><g fill="none" stroke-linecap="round" stroke-width="3.4"><path d="M20 12c-9 14 9 26 0 40" stroke="#f1d9a8"/><path d="M32 12c-9 14 9 26 0 40" stroke="#e8b595"/><path d="M44 12c-9 14 9 26 0 40" stroke="#c4785c"/></g></svg>')

def imgfile(n):
    for e in ("jpg","svg"):
        if os.path.exists(f"assets/img/{n}.{e}"): return f"/assets/img/{n}.{e}"
    return None
def bg(n):
    f=imgfile(n)
    return f' style="background-image:linear-gradient(180deg,rgba(10,20,22,.55),rgba(10,20,22,.92)),url({f});background-size:cover;background-position:center"' if f else ""

# ---------- shared parts ----------
def head(l,title,desc,path_by_lang,self_path):
    alts="".join(f'<link rel="alternate" hreflang="{x}" href="{B}{p}">' for x,p in path_by_lang.items())+f'<link rel="alternate" hreflang="x-default" href="{B}{path_by_lang["de"]}">'
    return f'<!doctype html><html lang="{l}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="{B}{self_path}">{alts}<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:type" content="website"><meta name="theme-color" content="#0a1416"><link rel="icon" href="/assets/haara.svg"><link rel="stylesheet" href="/assets/style.css"><link rel="stylesheet" href="/assets/wow.css"><script>if(!matchMedia("(prefers-reduced-motion:reduce)").matches)document.documentElement.classList.add("wj")</script></head><body>'
LOGO='<svg class="lgo" viewBox="0 0 32 32" aria-hidden="true"><g fill="none" stroke-linecap="round" stroke-width="2.6"><path d="M9 4c-7 9 7 15 0 24" stroke="#f1d9a8"/><path d="M16 4c-7 9 7 15 0 24" stroke="#e8b595"/><path d="M23 4c-7 9 7 15 0 24" stroke="#c4785c"/></g></svg>'
def header(l,paths,home=True):
    t=T[l]
    if home:
        links="".join(f'<a href="#{a}">{n}</a>' for a,n in zip(["rechner","check","pflege","mythen","laenge"],t["nav"]))+L(l,"nav",NV[l])
        nvl=f'<nav class="nvl">{links}</nav>'
    else:
        nvl=f'<nav class="nvl"><a href="/{l}/">← {t["home"]}</a>{L(l,"nav",NV[l])}</nav>'
    lg="".join(f'<a href="{paths[x]}"{" class=on" if x==l else ""} hreflang="{x}">{x.upper()}</a>' for x in LANGS)
    return f'<header class="nv"><div class="nvi"><a class="logo" href="/{l}/">{LOGO}{BRAND}</a>{nvl}<div class="lg">{lg}</div></div></header>'
def flinks(l):
    return "".join('<a href="/%s/%s/">%s</a>'%(l,x["slug"],x["title"].split(":")[0]) for x in T[l]["arts"])
def rlinks(l,cur):
    return "".join(' &nbsp; <a class="xl" href="/%s/%s/">%s →</a>'%(l,x["slug"],x["title"]) for x in T[l]["arts"] if x is not cur)
def footer(l):
    t=T[l]
    return f'<footer><div class="wrap fi"><div>{t["foot"]}</div><div><a href="/{l}/">{t["home"]}</a>{flinks(l)}{L(l,"footer")}</div><div class="dis">{t["dis"]}</div></div></footer><script src="/assets/app.js" defer></script><script src="/assets/wow.js" defer></script><script src="/assets/wow2.js" defer></script></body></html>'
def paths_home(): return {x:f"/{x}/" for x in LANGS}
def paths_art(i=0): return {x:f'/{x}/{T[x]["arts"][i]["slug"]}/' for x in LANGS}
def js(o): return html.escape(json.dumps(o,ensure_ascii=False),quote=True)

def lock_svg():
    cols=["#f1d9a8","#e8b595","#d9a07f","#c4785c","#cfdedc","#86d1bb","#b9694a","#f8e1cf"]
    g="";v=""
    for i,c in enumerate(cols):
        x=26+i*21;d=f"M{x} 8C{x+34} 80 {x-36} 170 {x+8} 272"
        g+=f'<path d="{d}" stroke="#fff" stroke-opacity=".1"/>'
        v+=f'<path class="on" d="{d}" pathLength="100" stroke="{c}"/>'
    return f'<svg class="lk" viewBox="0 0 220 280" fill="none" stroke-linecap="round" stroke-width="3" aria-hidden="true">{g}{v}</svg>'

# ---------- home ----------
def home(l):
    t=T[l];w=t["wash"];k=t["ck"];r=t["rt"];m=t["my"];f=t["fq"];n=t["ln"]
    o=head(l,t["title"],t["desc"],paths_home(),f"/{l}/")+header(l,paths_home())
    o+=f'<section class="hero"><canvas id="strands" aria-hidden="true"></canvas><div class="wrap"><span class="eyebrow">{t["eb"]}</span><h1>{t["h"]}</h1><p>{t["p"]}</p><div class="btns"><a class="btn g" href="#rechner">{t["b1"]}</a>{L(l,"hero",GO[l],"btn o")}</div></div></section>'
    # wash
    grp="".join(f'<div class="grp"><span class="gl">{gl}</span><div class="seg" role="group" aria-label="{gl}">'+"".join(f'<button type="button" aria-pressed="{"true" if i==d else "false"}">{x}</button>' for i,x in enumerate(opts))+'</div></div>' for (gl,opts),d in zip(w["g"],[1,0,0]))
    o+=f'<section id="rechner" class="calc"><div class="wrap"><span class="eyebrow">{w["k"]}</span><h2>{w["h"]}</h2><p class="sub">{w["p"]}</p><div class="card rv" id="calc" data-cfg="{js(dict(l=w["l"],u=w["u"],s=w["s"],t=w["t"]))}"><div class="grps">{grp}</div><div class="cres" aria-live="polite"></div><p class="note">{w["note"]} {L(l,"rechner")}</p></div></div></section>'
    o+=f'<section class="pano"{bg("pano")}><p>{t["pano"]}</p>{L(l,"pano",GO[l])}</section>'
    # check
    qs="".join(f'<div class="cq"{"" if i==0 else " hidden"}><small>{k["of"]} {i+1} / 3</small><b>{q}</b><div class="co">'+"".join(f'<button type="button" data-v="{v}">{x}</button>' for v,x in enumerate(os_))+'</div></div>' for i,(q,os_) in enumerate(k["q"]))
    res="".join(f'<div class="cr" data-k="{kk}" hidden><span class="eyebrow">{k["k"]}</span><h3>{ti}</h3><p>{d}</p></div>' for kk,(ti,d) in k["r"].items())
    a=t["arts"][3];aurl=f'/{l}/{a["slug"]}/'
    o+=f'<section id="check" class="ck"><div class="wrap"><span class="eyebrow">{k["k"]}</span><h2>{k["h"]}</h2><p class="sub">{k["p"]}</p><div class="card ckb rv"><div class="cdots"><i></i><i></i><i></i></div>{qs}{res}<div class="cf2" hidden><span class="cs">{k["art"]}</span><a class="cl" href="{aurl}">{a["title"]}</a>{L(l,"check",GO[l],"cta2")}<button type="button" class="cagain">{k["again"]}</button></div></div></div></section>'
    # ritual
    tiles="".join(f'<button type="button" class="tile" aria-pressed="false">{x}</button>' for x in r["i"])
    o+=f'<section id="pflege" class="rt"><div class="wrap"><span class="eyebrow">{r["k"]}</span><h2>{r["h"]}</h2><p class="sub">{r["p"]}</p><div class="grid"><div class="lock rv">{lock_svg()}</div><div class="rv"><div class="tiles">{tiles}</div><p class="rmsg" data-m="{"|".join(r["m"])}">{r["m"][0]}</p><span class="rcount" data-u="{r["u"]}">0 / {len(r["i"])} {r["u"]}</span> {L(l,"ritual")}</div></div></div></section>'
    # myths
    cards="".join(f'<button class="mc rv" aria-pressed="false"><span class="mi"><span class="mf"><small>{i+1} / {len(m["c"])}</small><b>{q}</b><em>{m["tap"]} ↻</em></span><span class="mb"><small class="v{v}">{m["v"][v]}</small><p>{e}</p></span></span></button>' for i,(q,v,e) in enumerate(m["c"]))
    o+=f'<section id="mythen" class="my"><div class="wrap"><span class="eyebrow">{m["k"]}</span><h2>{m["h"]}</h2><p class="sub">{m["p"]}</p><div class="myths">{cards}</div><p class="mlink">{L(l,"myth")}</p></div></section>'
    # length calc
    spec=[(1,100,1,15),(1,120,1,30),(1,36,1,12),(0,15,.5,2)]
    sls="".join(f'<div class="sl" data-k="{kk}" data-u="{n["su"][i]}"><label><span>{n["sl"][i]}</span><output></output></label><input type="range" min="{a}" max="{b}" step="{s}" value="{v}" aria-label="{n["sl"][i]}"></div>' for i,(kk,(a,b,s,v)) in enumerate(zip(["cur","tar","mon","trim"],spec)))
    cfg=dict(lang=l,r=n["r"],pm=n["pm"],mon=n["mon"],m1=n["m1"],ca=n["ca"],aft=n["aft"],aft1=n["aft1"],err=n["err"])
    o+=f'<section id="laenge" class="ln"><div class="wrap"><span class="eyebrow">{n["k"]}</span><h2>{n["h"]}</h2><p class="sub">{n["p"]}</p><div class="card rv" id="lcalc" data-cfg="{js(cfg)}"><div class="tabs" role="tablist"><button role="tab" aria-selected="true">{n["t"][0]}</button><button role="tab" aria-selected="false">{n["t"][1]}</button></div><div class="sls">{sls}</div><div class="cres" aria-live="polite"></div><p class="note">{n["note"]} {L(l,"laenge")}</p></div></div></section>'
    fq="".join(f'<details class="rv"><summary>{q}</summary><p>{x}</p></details>' for q,x in f["c"])
    arts="".join(f'<a class="art rv" href="/{l}/{x["slug"]}/"><i class="ac" style="background-image:url({imgfile(AK[j])})"></i><h3>{x["title"]}</h3><p>{x["lede"]}</p><span class="go">{t["tz"]["go"]}</span></a>' for j,x in enumerate(t["arts"]))
    o+=f'<section id="artikel"><div class="wrap"><span class="eyebrow">{t["tz"]["k"]}</span><div class="arts">{arts}</div></div></section><section id="faq"><div class="wrap" style="max-width:780px"><span class="eyebrow">{f["k"]}</span><h2>{f["h"]}</h2>{fq}<p class="mlink">{L(l,"faq")}</p></div></section>'
    return o+footer(l)

def article(l,i0=0):
    t=T[l];a=t["arts"][i0];ps=paths_art(i0)
    o=head(l,a["title"]+" – "+BRAND,a["lede"],ps,ps[l])+header(l,ps,False)
    o+=f'<div class="ah"{bg(AK[i0])}><div class="wrap"><span class="eyebrow">{BRAND}</span><h1>{a["title"]}</h1><p>{a["lede"]}</p></div></div><article class="body">'
    for i,(h,p) in enumerate(a["s"]):
        o+=f'<h2>{h}</h2><p>{p}</p>'
        if i==0: o+=f'<div class="cb"><p>{MORE[l]}:</p>{L(l,"art-mid",GO[l])}</div>'
        if i==1 and imgfile(AK[i0]): o+=f'<figure class="pic"><img src="{imgfile(AK[i0])}" alt="" width="1600" height="900" loading="lazy"></figure>'
        if i<2: o+='<div class="sep">· · ·</div>'
    o+=f'<h2>{a["ch"]}</h2><div class="chk">'+"".join(f'<label><input type="checkbox"><span>{x}</span></label>' for x in a["ci"])+f'</div><p class="done" hidden>{a["done"]} {L(l,"art-end",GO[l])}</p>'
    o+=f'<p class="fine">{a["fine"]}</p><div class="rel"><span class="eyebrow">{a["rel"]}</span><p><a class="xl" href="/{l}/#check">{t["ck"]["k"]} →</a> &nbsp; <a class="xl" href="/{l}/#rechner">{t["wash"]["k"]} →</a> {rlinks(l,a)}</p></div></article>'
    return o+footer(l)

make_assets()
for l in LANGS:
    os.makedirs(l,exist_ok=True)
    open(f"{l}/index.html","w",encoding="utf-8").write(home(l))
    for i0,ar in enumerate(T[l]["arts"]):
        os.makedirs(f"{l}/{ar['slug']}",exist_ok=True)
        open(f"{l}/{ar['slug']}/index.html","w",encoding="utf-8").write(article(l,i0))
open("index.html","w").write('<!doctype html><meta charset="utf-8"><title>Haara</title><meta name="viewport" content="width=device-width,initial-scale=1"><script>var n=(navigator.language||"de").slice(0,2);location.replace("/"+(n=="fr"||n=="it"?n:"de")+"/")</script><noscript><a href="/de/">Haara</a></noscript>')
open("robots.txt","w").write(f"User-agent: *\nAllow: /\nSitemap: {B}/sitemap.xml\n")
u=[f"/{l}/" for l in LANGS]+[f'/{l}/{ar["slug"]}/' for l in LANGS for ar in T[l]["arts"]]
open("sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+"".join(f"<url><loc>{B}{x}</loc></url>\n" for x in u)+"</urlset>\n")
print("built",len(u),"pages")
