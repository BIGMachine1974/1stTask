// TCMG motion v2 shared kit: brand tokens, springs, drawing helpers, captions, fine print, end card.
// A video page sets window.DUR, window.CAPS, window.END ({t0, typeAt, typeDur, phoneAt, tag:[white line, brass line]}) and window.scenes(t).
const W=1080,H=1920;
const C={carbon:'#121411',carbonSoft:'#1c1f1b',ink:'#171915',parch:'#f1efe8',paper:'#e7e3d8',white:'#fffdf8',line:'#cfc9ba',
  brass:'#c2a56a',brassL:'#d8c08f',brassD:'#725b2f',moss:'#59644d',mute:'#5a5b54'};
const HEAD='MS',BODY='MR',R=4;
const BROKER='The Campbell-Maric Group · eXp Realty, Brokerage';
const cv=document.getElementById('c'),x=cv.getContext('2d');
const LOGO=new Image();LOGO.src='../common/lockup-light.png'; // TCMG lockup, light version for the carbon end card

// ---------- motion helpers ----------
const clamp=(v,a=0,b=1)=>Math.min(b,Math.max(a,v));
const lerp=(a,b,p)=>a+(b-a)*p;
const smooth=p=>{p=clamp(p);return p*p*(3-2*p)};
function spring(dt,{w,z}){ if(dt<=0)return 0;
  if(z<1){const wd=w*Math.sqrt(1-z*z);return 1-Math.exp(-z*w*dt)*(Math.cos(wd*dt)+z*w/wd*Math.sin(wd*dt));}
  return 1-Math.exp(-w*dt)*(1+w*dt);}
const SNAP={w:26,z:.85}, PANEL={w:15,z:.72}, LAND={w:17,z:.48};
const fadeWin=(t,a,b,f=.25)=>clamp(Math.min((t-a)/f,(b-t)/f));

// ---------- drawing helpers ----------
function rr(X,Y,w,h,r=R){x.beginPath();x.roundRect(X,Y,w,h,r);}
function text(s,X,Y,{size=40,weight=600,fam=BODY,color=C.ink,align='center',ls=0,alpha=1}={}){
  x.save();x.globalAlpha*=alpha;x.font=`${weight} ${size}px ${fam}`;x.fillStyle=color;x.textAlign=align;x.textBaseline='alphabetic';
  x.letterSpacing=ls+'px';x.fillText(s,X,Y);x.restore();}
function runs(parts,X,Y,o){x.save();x.font=`${o.weight} ${o.size}px ${o.fam}`;x.letterSpacing=(o.ls||0)+'px';
  const tw=parts.reduce((a,[s])=>a+x.measureText(s).width,0);let cx=X-tw/2;
  for(const[s,c]of parts){x.globalAlpha=o.alpha??1;x.fillStyle=c;x.textAlign='left';x.fillText(s,cx,Y);cx+=x.measureText(s).width;}x.restore();}
function withT(tx,ty,sc,fn,alpha=1,rot=0){if(alpha<=0.001)return;x.save();x.globalAlpha*=alpha;x.translate(tx,ty);x.rotate(rot);x.scale(sc,sc);fn();x.restore();}
// matches the TCMG reels: one line of fine print, left-aligned, just above the caption bar
const LX=84;
function finePrint(lines,a,dark=false){const s=lines.join('  ·  ');let size=22;x.save();x.letterSpacing='0px';x.font=`600 ${size}px ${BODY}`;
  while(x.measureText(s).width>W-2*LX&&size>16){size--;x.font=`600 ${size}px ${BODY}`;}x.restore();
  text(s,LX,1392,{size,weight:600,color:dark?'#9a9a8f':C.mute,align:'left',alpha:a});}
// "*word*" marks the accent word; returns [[text,color],...]
function accent(s,base=C.ink,acc=C.brassD){return s.split('*').map((p,i)=>[p,i%2?acc:base]).filter(([p])=>p);}
function runsL(parts,X,Y,o){x.save();x.font=`${o.weight} ${o.size}px ${o.fam}`;x.letterSpacing=(o.ls||0)+'px';let cx=X;
  for(const[s,c]of parts){x.globalAlpha=o.alpha??1;x.fillStyle=c;x.textAlign='left';x.fillText(s,cx,Y);cx+=x.measureText(s).width;}x.restore();}
function fitSize(parts,size,fam=HEAD,max=W-2*LX){x.save();x.letterSpacing='0px';let s=size;const wid=()=>{x.font=`800 ${s}px ${fam}`;return parts.reduce((a,[p])=>a+x.measureText(p).width,0);};
  while(wid()>max&&s>30)s-=2;x.restore();return s;}
// a sentence-case headline line, left-aligned, that lands with a spring
function landLine(s,y,t0,t,{size=92,color=C.ink,a=1,from=1.3}={}){const l=spring(t-t0,LAND);const parts=accent(s,color);const sz=fitSize(parts,size);
  withT(LX,y,lerp(from,1,clamp(l,0,1.25)),()=>runsL(parts,0,0,{size:sz,weight:800,fam:HEAD}),a*clamp(l*2));}
// the scene title at the top, like the reels' headline
function head(s,t0,t,a=1,{y=360,size=80}={}){landLine(s,y,t0,t,{size,a,from:1.15});}
function kicker(s,t0,t,a=1,y=420){text(s,LX,y,{size:26,weight:800,color:C.brassD,ls:4,align:'left',alpha:a*clamp((t-t0)/.3)});}
// soft ground shadow under objects
function shadow(X,Y,w,al=.13){x.save();x.fillStyle=`rgba(23,25,21,${al})`;x.beginPath();x.ellipse(X,Y,w/2,w*.09,0,0,7);x.fill();x.restore();}
function pin(sc=1){x.save();x.scale(sc,sc);shadow(0,6,70,.18);x.fillStyle=C.brass;x.strokeStyle=C.ink;x.lineWidth=5;x.beginPath();x.arc(0,-62,34,Math.PI*.82,Math.PI*2.18);x.lineTo(0,0);x.closePath();x.fill();x.stroke();
  x.fillStyle=C.white;x.beginPath();x.arc(0,-64,14,0,7);x.fill();x.stroke();x.restore();}
function check(t0,t,X,Y){if(t<t0)return;const ck=spring(t-t0,LAND);withT(X,Y,clamp(ck,0,1.2),()=>{x.fillStyle=C.moss;x.beginPath();x.arc(0,0,30,0,7);x.fill();
  x.strokeStyle=C.white;x.lineWidth=7;x.lineCap='round';x.beginPath();x.moveTo(-12,1);x.lineTo(-3,11);x.lineTo(13,-9);x.stroke();});}
function house(sc=1,col=C.moss){x.save();x.scale(sc,sc);shadow(0,58,130);x.fillStyle=col;x.strokeStyle=C.ink;x.lineWidth=4;x.lineJoin='round';
  x.beginPath();x.moveTo(-46,-14);x.lineTo(-60,-12);x.lineTo(0,-66);x.lineTo(60,-12);x.lineTo(46,-14);x.lineTo(46,56);x.lineTo(-46,56);x.closePath();x.fill();x.stroke();
  x.fillStyle=C.parch;x.fillRect(-14,18,28,38);x.restore();}

// ---------- captions: dark bar, left-aligned, fits its text, max 2 lines, "*word*" in brass ----------
function captions(t){for(const[a,b,s,,dark]of window.CAPS){const al=fadeWin(t,a,b,.12);if(al<=0)continue;
  const lines=s.split('|').map(l=>accent(l,C.white,C.brassL));x.save();x.letterSpacing='0px';x.font=`700 38px ${BODY}`;
  const tw=Math.max(...lines.map(p=>p.reduce((q,[z])=>q+x.measureText(z).width,0)));x.restore();
  const h=lines.length>1?134:84;
  if(dark){const y=1508-h/2+(1-spring(t-a,SNAP))*12;x.save();x.globalAlpha=al;x.fillStyle=C.carbonSoft;x.strokeStyle='#33372f';x.lineWidth=2;rr(540-(tw+64)/2,y,tw+64,h);x.fill();x.stroke();x.restore();
    lines.forEach((p,i)=>runs(p,540,y+(lines.length>1?55+i*48:55),{size:38,weight:700,fam:BODY,alpha:al}));continue;}
  const bw=tw+56,y=1440+(1-spring(t-a,SNAP))*12;
  x.save();x.globalAlpha=al;x.fillStyle=C.ink;rr(LX-24,y,bw,h);x.fill();x.restore();
  lines.forEach((p,i)=>runsL(p,LX+4,y+(lines.length>1?55+i*48:55),{size:38,weight:700,fam:BODY,alpha:al}));}}

// ---------- end card on carbon: matches the current TCMG reels ----------
const PHONE='613-799-9022';
function endCard(t){const E=window.END;if(t<E.t0-0.25)return;
  if(t<E.t0+0.2){const p=smooth((t-(E.t0-0.25))/.45);x.fillStyle=C.carbon;x.fillRect(0,H*(1-p),W,H*p);}else{x.fillStyle=C.carbon;x.fillRect(0,0,W,H);}
  if(t<E.t0)return;
  const s1=spring(t-(E.t0+.05),PANEL),s2=spring(t-(E.t0+.25),PANEL),s3=spring(t-(E.t0+.2),PANEL),s4=spring(t-E.phoneAt,PANEL);
  withT(540,575+(1-s1)*40,1,()=>{const lw=720,lh=lw*LOGO.naturalHeight/LOGO.naturalWidth;x.drawImage(LOGO,-lw/2,-lh/2,lw,lh);},clamp(s1*1.3));
  // two-line headline: white, then light brass
  const hs=Math.min(fitSize([[E.tag[0],0]],96,HEAD,900),fitSize([[E.tag[1],0]],96,HEAD,900));
  withT(540,(1-s2)*40,1,()=>{text(E.tag[0],0,860,{size:hs,weight:800,fam:HEAD,color:C.white});text(E.tag[1],0,860+hs*1.1,{size:hs,weight:800,fam:HEAD,color:C.brassL});},clamp(s2*1.3));
  withT(540,1158+(1-s3)*30,1,()=>{x.fillStyle=C.carbonSoft;x.strokeStyle=C.brass;x.lineWidth=3;rr(-406,-72,812,144,8);x.fill();x.stroke();
    const url='yourhomeinottawa.ca',n=Math.floor(clamp((t-E.typeAt)/E.typeDur)*url.length),sub=url.slice(0,n);
    x.font=`800 62px ${BODY}`;x.letterSpacing='0px';const full=x.measureText(url).width,sw=x.measureText(sub).width;
    text(sub,-full/2,22,{size:62,weight:800,color:C.white,align:'left'});
    if(n<url.length||Math.floor(t*2)%2===0){x.fillStyle=C.brassL;x.fillRect(-full/2+sw+6,-30,5,62);}
    const sh=E.typeAt+E.typeDur+.2;if(t>sh){const ph=((t-sh)%2.4)/2.4;const sx=lerp(-520,520,smooth(ph*1.4));x.save();rr(-406,-72,812,144,8);x.clip();
      const g=x.createLinearGradient(sx-90,0,sx+90,0);g.addColorStop(0,'rgba(255,253,248,0)');g.addColorStop(.5,'rgba(255,253,248,.14)');g.addColorStop(1,'rgba(255,253,248,0)');x.fillStyle=g;x.fillRect(-406,-72,812,144);x.restore();}},clamp(s3*1.3));
  withT(540,1326+(1-s4)*20,1,()=>text('Talk to us first. '+PHONE,0,0,{size:36,weight:700,color:'#a9a79f'}),clamp(s4*1.3));
  withT(540,1392+(1-s4)*20,1,()=>text('eXp Realty, Brokerage',0,0,{size:30,weight:700,color:'#8f8d86',ls:1}),clamp((s4-.1)*1.3));}

// static warm vignette like the reels (no animation: an animated glow caused keyframe flashes)
function bg(){x.fillStyle=C.parch;x.fillRect(0,0,W,H);const g=x.createRadialGradient(540,860,80,540,860,1150);
  g.addColorStop(0,'rgba(255,253,248,.55)');g.addColorStop(.55,'rgba(241,239,232,0)');g.addColorStop(1,'rgba(214,206,188,.45)');x.fillStyle=g;x.fillRect(0,0,W,H);}
function seek(t){x._t=t;bg();window.scenes(t);endCard(t);captions(t);}
window.seek=seek;
window.ready=Promise.all([new Promise(r=>LOGO.complete?r():LOGO.onload=r)].concat(['800 40px MR','600 40px MR','500 40px MR','700 40px MR','800 40px MS','600 40px MS'].map(f=>document.fonts.load(f)))).then(()=>{seek(0);return true});
