// TCMG motion v2 shared kit: brand tokens, springs, drawing helpers, captions, fine print, end card.
// A video page sets window.DUR, window.CAPS, window.END ({t0, typeAt, typeDur, phoneAt, tag:[l1,l2], note}) and window.scenes(t).
const W=1080,H=1920;
const C={carbon:'#121411',carbonSoft:'#1c1f1b',ink:'#171915',parch:'#f1efe8',paper:'#e7e3d8',white:'#fffdf8',line:'#cfc9ba',
  brass:'#c2a56a',brassL:'#d8c08f',brassD:'#725b2f',moss:'#59644d',mute:'#5a5b54'};
const HEAD='MS',BODY='MR',R=4;
const BROKER='The Campbell-Maric Group · eXp Realty, Brokerage';
const cv=document.getElementById('c'),x=cv.getContext('2d');

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
function finePrint(lines,a,dark=false){lines.forEach((l,i)=>text(l,540,1584+i*32,{size:24,weight:500,color:dark?'#9a9a8f':C.mute,alpha:a}));}
// a headline line that lands with a spring
function landLine(s,y,t0,t,{size=92,color=C.ink,a=1,from=1.3}={}){const l=spring(t-t0,LAND);
  withT(540,y,lerp(from,1,clamp(l,0,1.25)),()=>text(s,0,0,{size,weight:800,fam:HEAD,color}),a*clamp(l*2));}
function check(t0,t,X,Y){if(t<t0)return;const ck=spring(t-t0,LAND);withT(X,Y,clamp(ck,0,1.2),()=>{x.fillStyle=C.moss;x.beginPath();x.arc(0,0,30,0,7);x.fill();
  x.strokeStyle=C.white;x.lineWidth=7;x.lineCap='round';x.beginPath();x.moveTo(-12,1);x.lineTo(-3,11);x.lineTo(13,-9);x.stroke();});}
function house(sc=1,col=C.moss){x.save();x.scale(sc,sc);x.fillStyle=col;x.beginPath();x.moveTo(-60,-10);x.lineTo(0,-64);x.lineTo(60,-10);x.fill();
  rr(-46,-14,92,70);x.fill();x.fillStyle=C.parch;x.fillRect(-14,18,28,38);x.restore();}

// ---------- captions: bar fits its text, max 2 lines ----------
function captions(t){for(const[a,b,s,g,dark]of window.CAPS){const al=fadeWin(t,a,b,.12);if(al<=0)continue;
  const lines=s.split('|');x.save();x.font=`600 36px ${BODY}`;const tw=Math.max(...lines.map(l=>x.measureText(l).width));x.restore();
  const bw=tw+64,h=lines.length>1?132:84,y=1458-h/2+(1-spring(t-a,SNAP))*12;
  x.save();x.globalAlpha=al;x.fillStyle=dark?C.carbonSoft:C.white;x.strokeStyle=dark?'#33372f':C.line;x.lineWidth=2;rr(540-bw/2,y,bw,h);x.fill();x.stroke();x.restore();
  lines.forEach((l,i)=>text(l,540,y+(lines.length>1?54+i*46:55),{size:36,weight:g?800:600,color:dark?C.white:(g?C.brassD:C.ink),alpha:al}));}}

// ---------- end card on carbon ----------
function endCard(t){const E=window.END;if(t<E.t0-0.25)return;
  if(t<E.t0+0.2){const p=smooth((t-(E.t0-0.25))/.45);x.fillStyle=C.carbon;x.fillRect(0,H*(1-p),W,H*p);}else{x.fillStyle=C.carbon;x.fillRect(0,0,W,H);}
  if(t<E.t0)return;
  const s1=spring(t-(E.t0+.05),PANEL),s2=spring(t-(E.t0+.25),PANEL),s3=spring(t-(E.t0+.2),PANEL),s4=spring(t-E.phoneAt,PANEL);
  withT(540,470+(1-s1)*40,1,()=>{text('THE CAMPBELL-MARIC GROUP',0,0,{size:46,weight:800,fam:HEAD,color:C.white,ls:4});
    x.fillStyle=C.brassL;x.fillRect(-120,30,240,5);},clamp(s1*1.3));
  withT(540,(1-s2)*40,1,()=>{const ts=E.tagSize||80;runs([[E.tag[0],C.brassL]],0,680,{size:ts,weight:800,fam:HEAD});runs([[E.tag[1],C.white]],0,680+ts*1.2,{size:ts,weight:800,fam:HEAD});},clamp(s2*1.3));
  withT(540,960+(1-s3)*30,1,()=>{x.fillStyle=C.carbonSoft;x.strokeStyle=C.brassL;x.lineWidth=3;rr(-430,-70,860,140);x.fill();x.stroke();
    const url='yourhomeinottawa.ca',n=Math.floor(clamp((t-E.typeAt)/E.typeDur)*url.length),sub=url.slice(0,n);
    x.font=`800 60px ${BODY}`;x.letterSpacing='0px';const full=x.measureText(url).width,sw=x.measureText(sub).width;
    text(sub,-full/2,21,{size:60,weight:800,color:C.white,align:'left'});
    if(n<url.length||Math.floor(t*2)%2===0){x.fillStyle=C.brassL;x.fillRect(-full/2+sw+4,-26,5,60);}
    const sh=E.typeAt+E.typeDur+.2;if(t>sh){const ph=((t-sh)%2.4)/2.4;const sx=lerp(-520,520,smooth(ph*1.4));x.save();rr(-430,-70,860,140);x.clip();
      const g=x.createLinearGradient(sx-90,0,sx+90,0);g.addColorStop(0,'rgba(255,253,248,0)');g.addColorStop(.5,'rgba(255,253,248,.14)');g.addColorStop(1,'rgba(255,253,248,0)');x.fillStyle=g;x.fillRect(-430,-70,860,140);x.restore();}},clamp(s3*1.3));
  withT(540,1130+(1-s4)*20,1,()=>text('613-558-3294',0,0,{size:48,weight:800,color:C.brassL,ls:2}),clamp(s4*1.3));
  finePrint([BROKER].concat(E.note?[E.note]:[]),clamp((t-(E.t0+.55))/.4),true);}

function seek(t){x._t=t;x.fillStyle=C.parch;x.fillRect(0,0,W,H);window.scenes(t);endCard(t);captions(t);}
window.seek=seek;
window.ready=Promise.all(['800 40px MR','600 40px MR','500 40px MR','700 40px MR','800 40px MS','600 40px MS'].map(f=>document.fonts.load(f))).then(()=>{seek(0);return true});
