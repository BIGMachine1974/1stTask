// Motion Studio paper kit: the cut-paper style, shared by every paper video.
// Torn edges that re-tear every pose (the boil), drop shadows, paper grain, springs, text strips, pins,
// little houses and trees, captions, fine print and torn-paper wipes. Animated on twos: seekPaper() snaps time to 12 poses a second.
// A page sets window.BRAND (optional colour overrides), then window.DUR, window.scenes(t), optional window.CAPS and window.WIPES,
// and calls paperReady(extraPromises). render.js drives window.seek(t).
const W=1080,H=1920,cv=document.getElementById('c'),x=cv.getContext('2d');
const C=Object.assign({carbon:'#121411',ink:'#171915',parch:'#f1efe8',paper:'#e7e3d8',white:'#fffdf8',
  brass:'#c2a56a',brassL:'#d8c08f',brassD:'#725b2f',moss:'#59644d',mossL:'#7d8770',mute:'#5a5b54',
  brick:'#a8664a',slate:'#4d5560',river:'#7b8e9a',riverL:'#a4b4bd',sand:'#e4d3a8'},window.BRAND||{});
const HEAD='MS',BODY='MR';

// ---------- randomness, easing, springs ----------
function rng(seed){let s=seed>>>0||1;return()=>((s=Math.imul(s^s>>>15,s|1),s^=s+Math.imul(s^s>>>7,s|61),((s^s>>>14)>>>0)/4294967296));}
const clamp=(v,a=0,b=1)=>Math.min(b,Math.max(a,v));
const ease=p=>{p=clamp(p);return p<.5?4*p*p*p:1-Math.pow(-2*p+2,3)/2;};
function spring(dt,w=15,z=.42){if(dt<=0)return 0;const wd=w*Math.sqrt(1-z*z);return 1-Math.exp(-z*w*dt)*(Math.cos(wd*dt)+z*w/wd*Math.sin(wd*dt));}

// ---------- paper ----------
let BOIL=0; // the pose number; every torn edge re-rolls with it
function torn(pts,seed,amp=3,step=14){const r=rng(seed),out=[];
  for(let i=0;i<pts.length;i++){const[a,b]=[pts[i],pts[(i+1)%pts.length]];const L=Math.hypot(b[0]-a[0],b[1]-a[1])||1,n=Math.max(1,Math.round(L/step));
    const nx=-(b[1]-a[1])/L,ny=(b[0]-a[0])/L;
    for(let k=0;k<n;k++){const p=k/n,j=(r()-.5)*2*amp;out.push([a[0]+(b[0]-a[0])*p+nx*j,a[1]+(b[1]-a[1])*p+ny*j]);}}
  return out;}
const GRAIN=document.createElement('canvas');GRAIN.width=W;GRAIN.height=H;
{const g=GRAIN.getContext('2d'),r=rng(7);for(let i=0;i<26000;i++){g.fillStyle=r()<.5?'#000':'#fff';g.globalAlpha=r()*.6;
  g.fillRect(r()*W,r()*H,1+r()*2.5,1+r()*1.2);}}
function piece(pts,fill,id,{amp=3,shadow=true,grain=true,alpha=1}={}){const p=torn(pts,id*977+BOIL*13,amp);
  x.save();x.globalAlpha*=alpha;x.beginPath();p.forEach(([a,b],i)=>i?x.lineTo(a,b):x.moveTo(a,b));x.closePath();
  if(shadow){x.shadowColor='rgba(23,25,21,.28)';x.shadowBlur=14;x.shadowOffsetX=5;x.shadowOffsetY=8;}
  x.fillStyle=fill;x.fill();x.shadowColor='transparent';
  if(grain){x.clip();x.globalAlpha*=.10;x.drawImage(GRAIN,0,0);}x.restore();}
const rect=(X,Y,w,h)=>[[X,Y],[X+w,Y],[X+w,Y+h],[X,Y+h]];
const circle=(cx,cy,r,n=26)=>Array.from({length:n},(_,i)=>[cx+r*Math.cos(i/n*6.283),cy+r*Math.sin(i/n*6.283)]);
function ground(c){x.fillStyle=c;x.fillRect(0,0,W,H);x.globalAlpha=.07;x.drawImage(GRAIN,0,0);x.globalAlpha=1;}
// pop: springs a drawing in at t0. from 'scale' (grows from bx,by), 'slide' (up from below) or 'drop' (down from above)
function pop(t,t0,draw,{bx=540,by=960,from='scale'}={}){const p=spring(t-t0);if(p<=0)return;
  x.save();x.translate(bx,by);if(from==='scale')x.scale(p,p);else x.translate(0,(1-p)*(from==='drop'?-700:900));x.translate(-bx,-by);draw();x.restore();}

// ---------- text ----------
function textW(parts,font,ls=0){x.save();x.font=font;x.letterSpacing=ls+'px';const w=parts.reduce((a,[s])=>a+x.measureText(s).width,0);x.restore();return w;}
function runs(parts,cx,y,font,ls=0){x.save();x.font=font;x.letterSpacing=ls+'px';x.textAlign='left';let X=cx-textW(parts,font,ls)/2;
  for(const[s,c]of parts){x.fillStyle=c;x.fillText(s,X,y);X+=x.measureText(s).width;}x.restore();}
function parse(s,base=C.ink,hot=C.brassD){return s.split(/(\*[^*]+\*)/).filter(Boolean).map(p=>p[0]==='*'?[p.slice(1,-1),hot]:[p,base]);}
// a torn white strip holding one or two lines, centred; "*word*" in the accent colour
function strip(t,t0,lines,cy,{size=64,id=1,fill=C.white,font=HEAD}={}){const f=`800 ${size}px ${font}`,ls=lines.map(l=>parse(l));
  const w=Math.max(...ls.map(p=>textW(p,f)))+110,lh=size*1.18,h=lh*lines.length+size*.9;
  pop(t,t0,()=>{piece(rect(540-w/2,cy-h/2,w,h),fill,id,{amp:3});ls.forEach((p,i)=>runs(p,540,cy-h/2+size*.45+lh*(i+.82),f));},{bx:540,by:cy});}
function chip(t,t0,s,cy,{id=2,fill=C.carbon,col=C.parch,size=28,cx=540}={}){const f=`700 ${size}px ${BODY}`,w=textW([[s,col]],f,4)+70;
  pop(t,t0,()=>{piece(rect(cx-w/2,cy-34,w,68),fill,id,{amp:2});runs([[s,col]],cx,cy+size*.36,f,4);},{bx:cx,by:cy});}

// ---------- props ----------
function house(cx,base,w,h,wall,roof,door,id,{chimney=false}={}){const X=cx-w/2,Y=base-h;
  if(chimney)piece(rect(X+w*.62,Y-h*.42,w*.12,h*.3),C.brick,id+5,{amp:2});
  piece(rect(X,Y,w,h),wall,id,{amp:2.5});
  piece([[X-w*.1,Y+6],[cx,Y-h*.5],[X+w*1.1,Y+6]],roof,id+1,{amp:3});
  piece(rect(cx-w*.11,base-h*.46,w*.22,h*.46),door,id+2,{amp:2});
  const ww=w*.2;piece(rect(X+w*.12,Y+h*.18,ww,ww),C.brassL,id+3,{amp:1.5,shadow:false});
  piece(rect(X+w*.68,Y+h*.18,ww,ww),C.brassL,id+4,{amp:1.5,shadow:false});}
function tree(cx,base,s,id){piece(rect(cx-9*s,base-80*s,18*s,80*s),C.brassD,id,{amp:1.5});
  piece([[cx,base-260*s],[cx+85*s,base-70*s],[cx-85*s,base-70*s]],C.moss,id+1,{amp:4});
  piece([[cx,base-320*s],[cx+65*s,base-170*s],[cx-65*s,base-170*s]],C.mossL,id+2,{amp:4});}
function hill(y,c,id){piece([[-40,y+40],[260,y-30],[620,y+10],[1120,y-50],[1120,H+40],[-40,H+40]],c,id,{amp:6});}
// a map pin with a torn label; sub = optional small second line; side 1 = label right, -1 = left
function pin(cx,cy,label,id,{hot=false,side=1,sub=''}={}){
  piece(rect(cx-5,cy-70,10,70),C.ink,id,{amp:1,grain:false});
  piece(circle(cx,cy-86,hot?34:26),hot?C.brass:C.brick,id+1,{amp:2});
  piece(circle(cx,cy-86,hot?12:9,12),C.white,id+2,{amp:1,shadow:false});
  const f=`800 ${hot?44:34}px ${HEAD}`,fs=`600 24px ${BODY}`;
  const w=Math.max(textW([[label,C.ink]],f),sub?textW([[sub,C.mute]],fs):0)+44,h=(hot?64:54)+(sub?34:0),lx=side>0?cx+30:cx-30-w;
  piece(rect(lx,cy-58,w,h),C.white,id+3,{amp:2});
  runs([[label,hot?C.brassD:C.ink]],lx+w/2,cy-58+(hot?46:39),f);
  if(sub)runs([[sub,C.mute]],lx+w/2,cy-58+(hot?46:39)+32,fs);}
// a price tag like the TCMG explainers, centred on cx,cy
function priceTag(cx,cy,label,value,sub,id,{hi=false}={}){x.save();x.translate(cx,cy);
  piece([[-330,-130],[250,-130],[340,0],[250,130],[-330,130]],hi?C.brass:C.white,id,{amp:3});
  piece(circle(230,0,18,14),C.parch,id+1,{amp:1,shadow:false});
  runs([[label,hi?C.ink:C.brassD]],-40,-62,`800 26px ${BODY}`,4);
  runs([[value,C.ink]],-40,30,`800 92px ${HEAD}`);
  if(sub)runs([[sub,hi?C.ink:C.mute]],-40,86,`600 30px ${BODY}`);x.restore();}

// ---------- captions and fine print (Motion Studio rules: centred, dark bar, one line of fine print above) ----------
const CAP_Y=1650;
function captions(t){for(const[a,b,s]of (window.CAPS||[])){const al=clamp(Math.min((t-a)/.12,(b-t)/.12));if(al<=0)continue;
  const lines=s.split('|').map(l=>parse(l,C.white,C.brassL)),f=`700 38px ${BODY}`;
  const w=Math.max(...lines.map(p=>textW(p,f)))+64,h=lines.length>1?134:84,y=CAP_Y-h/2+(1-spring(t-a,26,.85))*12;
  x.save();x.globalAlpha=al;piece(rect(540-w/2,y,w,h),C.carbon,900+Math.round(a*10),{amp:2,grain:false});
  lines.forEach((p,i)=>runs(p,540,y+(lines.length>1?55+i*48:55),f));x.restore();}}
function finePrint(s,al=1,dark=false){x.save();x.globalAlpha=al;let size=22;x.font=`600 ${size}px ${BODY}`;
  while(x.measureText(s).width>W-120&&size>15){size--;x.font=`600 ${size}px ${BODY}`;}
  x.fillStyle=dark?'#9a9a8f':C.mute;x.textAlign='center';x.fillText(s,540,CAP_Y-96);x.restore();}

// ---------- wipes ----------
function wipe(t,{t:t0,c,d=.7},i){const p=(t-t0)/d;if(p<=0||p>=1)return;
  const y=p<.5?H*(1-ease(p*2)):-H*ease((p-.5)*2);
  piece([[-60,y-30],[1140,y+20],[1140,y+H+40],[-60,y+H+10]],c,500+i,{amp:14});}

window.seek=function(tIn){const t=Math.floor(tIn*12)/12;BOIL=Math.floor(tIn*12);
  window.scenes(t);captions(t);(window.WIPES||[]).forEach((w,i)=>wipe(t,w,i));};
function paperReady(extra=[]){window.ready=Promise.all([document.fonts.load(`800 84px ${HEAD}`),document.fonts.load(`700 30px ${BODY}`),...extra]).then(()=>window.seek(0));}
function imageReady(img){return new Promise(r=>{if(img.complete)r();else{img.onload=r;img.onerror=r;}});}
