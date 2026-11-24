(()=>{
const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)];
const rm=matchMedia('(prefers-reduced-motion:reduce)').matches;
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.12});
$$('.rv').forEach(e=>io.observe(e));
const nv=$('header.nv');const onS=()=>nv.classList.toggle('sc',scrollY>20);
addEventListener('scroll',onS,{passive:true});onS();

/* hero: fliessende Strähnen, weichen der Maus aus */
const cv=$('#strands');
if(cv){const c=cv.getContext('2d'),hero=cv.parentElement;let W,H,S=[],mx=-999,my=-999,t=0;
 const cols=['241,217,168','232,181,149','217,160,127','196,120,92','207,222,220','134,209,187'];
 const size=()=>{const r=hero.getBoundingClientRect(),d=Math.min(devicePixelRatio||1,1.5);W=r.width;H=r.height;cv.width=W*d;cv.height=H*d;c.setTransform(d,0,0,d,0,0);
  const n=Math.round(Math.max(22,Math.min(58,W/22)));
  S=Array.from({length:n},(_,i)=>({y:H*(.06+.9*i/n)+(Math.random()-.5)*26,a:16+Math.random()*52,f:.0015+Math.random()*.002,g:.004+Math.random()*.005,p:Math.random()*6.28,s:.5+Math.random()*.9,c:cols[Math.floor(Math.random()*cols.length)],w:.6+Math.random()*1.4,o:.2+Math.random()*.42}))};
 size();addEventListener('resize',()=>{size();if(rm)draw()});
 const draw=()=>{c.clearRect(0,0,W,H);const sy=scrollY*.16;
  for(const s of S){c.beginPath();c.strokeStyle='rgba('+s.c+','+s.o+')';c.lineWidth=s.w;
   for(let x=-12;x<=W+12;x+=12){let y=s.y-sy*s.w+Math.sin(x*s.f+t*s.s+s.p)*s.a+Math.sin(x*s.g-t*.7*s.s+s.p*2)*s.a*.45;
    const dx=x-mx,dy=y-my,d2=dx*dx+dy*dy;if(d2<48400){const d=Math.sqrt(d2)||1,f=1-d/220;y+=dy/d*f*f*70}
    x===-12?c.moveTo(x,y):c.lineTo(x,y)}
   c.stroke()}};
 hero.addEventListener('pointermove',e=>{if(e.pointerType!=='mouse')return;const r=hero.getBoundingClientRect();mx=e.clientX-r.left;my=e.clientY-r.top});
 hero.addEventListener('pointerleave',()=>{mx=my=-999});
 const loop=()=>{if(scrollY<H&&!document.hidden){t+=.0045;draw()}requestAnimationFrame(loop)};
 if(rm)draw();else loop()}

const fmt=(n,L,d=1)=>n.toLocaleString(L||document.documentElement.lang,{maximumFractionDigits:d});
const seg=(root,cb)=>$$('.seg',root).forEach((sg,gi)=>$$('button',sg).forEach((b,i)=>b.onclick=()=>{$$('button',sg).forEach((x,j)=>x.setAttribute('aria-pressed',j==i));cb(gi,i)}));

/* Waschrhythmus */
const calc=$('#calc');
if(calc){const cfg=JSON.parse(calc.dataset.cfg),st=[1,0,0],out=$('.cres',calc),base=[[1,2],[2,3],[3,5]];
 const run=()=>{let [lo,hi]=base[st[0]];if(st[1]==2){lo++;hi++}if(st[2]==2)hi=Math.max(lo,hi-1);
  const d=lo==hi?String(lo):lo+'–'+hi,s=cfg.s[st[0]],t=cfg.t[st[1]];
  out.innerHTML=`<div class="cc"><small>${cfg.l[0]}</small><b>${d}</b><span>${cfg.u}</span></div><div class="cc"><small>${cfg.l[1]}</small><b class="w">${s[0]}</b><span>${s[1]}</span></div><div class="cc"><small>${cfg.l[2]}</small><b class="w">${t[0]}</b><span>${t[1]}</span></div>`};
 seg(calc,(g,i)=>{st[g]=i;run()});run()}

/* Haarlänge */
const lc=$('#lcalc');
if(lc){const cfg=JSON.parse(lc.dataset.cfg),L=cfg.lang,out=$('.cres',lc),rates=[.8,1,1.25];let mode=0;
 const sl={};$$('.sl',lc).forEach(s=>sl[s.dataset.k]={el:s,i:$('input',s),o:$('output',s),u:s.dataset.u});
 const v=k=>+sl[k].i.value;
 const vis=()=>{[['cur',1,1],['tar',1,0],['mon',0,1],['trim',0,1]].forEach(([k,a,b])=>sl[k].el.hidden=!(mode?b:a))};
 const run=()=>{for(const k in sl)sl[k].o.textContent=fmt(v(k),L)+' '+sl[k].u;
  if(!mode){const need=v('tar')-v('cur');if(need<=0){out.innerHTML=`<p class="warn">${cfg.err}</p>`;return}
   out.innerHTML=rates.map((r,i)=>{const m=Math.ceil(need/r),d=new Date();d.setMonth(d.getMonth()+m);
    return `<div class="cc"><small>${cfg.r[i]} · ${fmt(r,L,2)} cm/${cfg.pm}</small><b>${m}</b><span>${m==1?cfg.m1:cfg.mon} · ${cfg.ca} ${d.toLocaleDateString(L,{month:'long',year:'numeric'})}</span></div>`}).join('')}
  else{out.innerHTML=rates.map((r,i)=>{const len=Math.max(0,v('cur')+r*v('mon')-v('trim'));
    return `<div class="cc"><small>${cfg.r[i]} · ${fmt(r,L,2)} cm/${cfg.pm}</small><b>${fmt(len,L)} cm</b><span>${v('mon')==1?cfg.aft1:cfg.aft.replace('{n}',v('mon'))}</span></div>`}).join('')}};
 $$('.tabs button',lc).forEach((b,i)=>b.onclick=()=>{mode=i;$$('.tabs button',lc).forEach((x,j)=>x.setAttribute('aria-selected',j==i));vis();run()});
 for(const k in sl)sl[k].i.oninput=run;vis();run()}

/* Haartyp-Check */
const ck=$('#check .ckb');
if(ck){let i=0,sum=0;const qs=$$('.cq',ck),dots=$$('.cdots i',ck);dots[0].classList.add('on');
 $$('.co button',ck).forEach(b=>b.onclick=()=>{sum+=+b.dataset.v;qs[i].hidden=true;i++;
  if(i<3){qs[i].hidden=false;dots[i].classList.add('on')}else{dots.forEach(d=>d.classList.add('on'));const k=sum<=1?'light':sum<=4?'mid':'rich';$('.cr[data-k='+k+']',ck).hidden=false;$('.cf2',ck).hidden=false}});
 $('.cagain',ck).onclick=()=>{i=0;sum=0;qs.forEach((q,j)=>q.hidden=j>0);$$('.cr',ck).forEach(r=>r.hidden=true);$('.cf2',ck).hidden=true;dots.forEach((d,j)=>d.classList.toggle('on',j==0))}}

/* Pflegeritual: Strähnen wachsen mit jeder Gewohnheit */
const rt=$('#pflege');
if(rt){const t=$$('.tile',rt),lock=$('.lock',rt),st=$$('.lk .on',rt),msg=$('.rmsg',rt),cnt=$('.rcount',rt),ms=msg.dataset.m.split('|');
 t.forEach(b=>b.onclick=()=>{b.setAttribute('aria-pressed',b.getAttribute('aria-pressed')!='true');const n=t.filter(x=>x.getAttribute('aria-pressed')=='true').length;
  lock.style.setProperty('--p',n/t.length);st.forEach((p,i)=>{p.style.transitionDelay=(i*.07)+'s';p.style.strokeDashoffset=i<n?0:100});
  msg.textContent=ms[n==0?0:n<=2?1:n<=5?2:n<8?3:4];cnt.textContent=n+' / '+t.length+' '+cnt.dataset.u})}

/* Mythen */
$$('.mc').forEach(b=>b.onclick=()=>b.setAttribute('aria-pressed',b.getAttribute('aria-pressed')!='true'));
/* Artikel-Checkliste */
const cl=$('.chk');
if(cl){const bx=$$('input',cl),d=$('.done');bx.forEach(x=>x.onchange=()=>{d.hidden=!bx.every(y=>y.checked)})}
})();
