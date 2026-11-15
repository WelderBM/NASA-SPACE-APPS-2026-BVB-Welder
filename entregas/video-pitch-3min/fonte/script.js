const $=id=>document.getElementById(id);
const cl=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const ease=x=>{x=cl(x);return 1-Math.pow(1-x,3)};
const eio=x=>{x=cl(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2};
const fin=(t,a,d=.5)=>ease((t-a)/d);
const fio=(t,a,b,d=.4)=>Math.min(fin(t,a,d),ease((b-t)/d));
const lerp=(a,b,x)=>a+(b-a)*x;
const NS='http://www.w3.org/2000/svg';
const mk=(tag,attrs,parent)=>{const e=document.createElementNS(NS,tag);for(const k in attrs)e.setAttribute(k,attrs[k]);parent.appendChild(e);return e;};
let SUBS=[],T={},P=[];
function setSubs(s,timing){SUBS=s;T=timing;P=s.map(x=>x[1]);}

// ---------- builders ----------
// dry spell squares
for(let i=0;i<9;i++) mk('rect',{x:i*36,y:130,width:30,height:30,rx:5,fill:'#9AB8A6'},$('dryN'));
const D26=[];for(let i=0;i<24;i++) D26.push(mk('rect',{x:i*36,y:250,width:30,height:30,rx:5,fill:'#B5442E',opacity:0},$('dry26')));
// soil line (2026 root zone, Jan..Sep)
const SOIL=[0.5,0.51,0.5,0.58,0.67,0.83,0.76,0.58,0.51];const MON=['J','F','M','A','M','J','J','A','S'];
const sx=i=>40+i*75, sy=v=>250-(v-0.45)*400;
SOIL.forEach((v,i)=>{mk('text',{x:sx(i),y:285,'text-anchor':'middle'},$('soilMonths')).textContent=MON[i];});
const SD=SOIL.map((v,i)=>mk('circle',{cx:sx(i),cy:sy(v),r:(i==0||i==8)?16:9,fill:(i==0||i==8)?'#B5442E':'#6E4527',opacity:0},$('soilDots')));
// El Nino dots
const EN=[[1982,-33],[1986,14],[1987,-5],[1991,17],[1997,-21],[2002,16],[2009,-5],[2015,-48],[2023,-27]];
const ex=i=>300+i*160, ey=v=>560-v*6;
const END=EN.map(([y,v],i)=>{const g=mk('g',{opacity:0},$('enDots'));
  mk('line',{x1:ex(i),y1:560,x2:ex(i),y2:ey(v),stroke:v>0?'#2E6A4C':'#B5442E','stroke-width':10,'stroke-linecap':'round'},g);
  mk('circle',{cx:ex(i),cy:ey(v),r:18,fill:v>0?'#2E6A4C':'#B5442E'},g);
  const lab=mk('text',{x:ex(i),y:v>0?ey(v)-34:ey(v)+56,'text-anchor':'middle','font-size':30,'font-weight':800,fill:v>0?'#2E6A4C':'#B5442E'},g);lab.textContent=(v>0?'+':'−')+Math.abs(v)+'%';
  const yr=mk('text',{x:ex(i),y:v>0?600:530,'text-anchor':'middle','font-size':26,fill:'#4A5148'},g);yr.textContent=y;return g;});
// waffle 87%
const WF=[];for(let i=0;i<100;i++){const r=Math.floor(i/10),c=i%10;WF.push(mk('rect',{x:c*48,y:r*48,width:40,height:40,rx:8,fill:'#9AB8A6',opacity:0},$('waffle')));}
// houses along road
const HP=[[960,600],[1060,760],[1180,620],[1290,790],[1400,640],[1520,780],[1620,600],[1720,760],[1840,610]];
const HS=HP.map(([x,y],i)=>{const g=mk('g',{transform:`translate(${x},${y})`},$('houses'));mk('rect',{x:-30,y:-34,width:60,height:40,fill:'#E9D6B3'},g);mk('path',{d:'M-38,-30 L0,-60 L38,-30Z',fill:'#8C4A2F'},g);const glow=mk('circle',{cx:0,cy:-20,r:52,fill:'none',stroke:'#2E6A4C','stroke-width':6,opacity:0},g);return glow;});
// sprouts scene 7 & 11
const SP7=[];[[826,1080,1900],[906,1060,1900]].forEach(([y,x0,x1])=>{for(let x=x0;x<x1;x+=80){SP7.push(mk('use',{href:'#sprout'},$('sp7')));SP7[SP7.length-1]._p=[x,y];}});
const SP11=[];for(let x=60;x<1920;x+=90){const u=mk('use',{href:'#sprout'},$('sp11'));u._p=[x,1060];SP11.push(u);}
// months strip ZARC
const MS=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
const MR=MS.map((m,i)=>{const g=mk('g',{},$('months'));const r=mk('rect',{x:40+i*77,y:95,width:70,height:60,rx:10,fill:(i>=5&&i<=7)?'#9BE3B8':'#EAE3D3'},g);const tx=mk('text',{x:75+i*77,y:134,'text-anchor':'middle'},g);tx.textContent=m;return r;});
// rosa clones
function cloneRosa(holder,prefix){const r=$('rosa').cloneNode(true);r.removeAttribute('id');r.setAttribute('transform','');r.querySelectorAll('[id]').forEach(e=>e.setAttribute('id',prefix+e.id));$(holder).appendChild(r);}
cloneRosa('rosa7','r7_');
$('r7_basket').setAttribute('opacity',0);
// selection chips in phone
const CH=[['Better soil','#2E6A4C','#F5F0E6'],['Low risk','#D9902F','#1C2620'],['July','#3A8DC1','#F5F0E6'],['Pasture','#8C4A2F','#F5F0E6'],['Income','#4A5148','#F5F0E6']];
const CHG=CH.map(([txt,bg,fg],i)=>{const g=mk('g',{opacity:0},$('selChips'));mk('rect',{x:-90,y:-26,width:180,height:52,rx:26,fill:bg},g);const t=mk('text',{'text-anchor':'middle',y:9,fill:fg},g);t.textContent=txt;return g;});

function sub(t){
  let cur=null;
  for(let i=0;i<SUBS.length;i++){const [txt,a,b]=SUBS[i];const nx=i+1<SUBS.length?SUBS[i+1][1]:1e9;
    if(t>=a-0.08&&t<Math.min(b+0.25,nx-0.08))cur=txt;}
  const box=$('subBox');if(t>=T.lines[10][0]-0.1)cur=null;
  if(!cur){box.setAttribute('opacity',0);return;}
  cur=cur.replace(/\.\.\.$/,'…');
  const el=$('sub'),el2=$('sub2'),FS=44,MAXW=1680;
  el.setAttribute('font-size',FS);el2.setAttribute('font-size',FS);
  el.textContent=cur;el2.textContent='';
  let w=el.getComputedTextLength(),lines=1;
  if(w>MAXW){ // break into two balanced lines at the space nearest the middle
    const words=cur.split(' ');let best=1,bd=1e9;
    for(let k=1;k<words.length;k++){const l=words.slice(0,k).join(' ').length,r=cur.length-l;if(Math.abs(l-r)<bd){bd=Math.abs(l-r);best=k;}}
    el.textContent=words.slice(0,best).join(' ');el2.textContent=words.slice(best).join(' ');
    w=Math.max(el.getComputedTextLength(),el2.getComputedTextLength());lines=2;}
  const W=w+80,H=lines===1?80:136,Y=1046-H;
  $('subBg').setAttribute('x',960-W/2);$('subBg').setAttribute('width',W);
  $('subBg').setAttribute('y',Y);$('subBg').setAttribute('height',H);
  el.setAttribute('y',lines===1?1020:Y+56);el2.setAttribute('y',Y+112);
  box.setAttribute('opacity',1);
}
function vis(id,t,a,b){const o=fio(t,a,b,0.4);$(id).setAttribute('opacity',o);return o;}

function render(t){
  const L=T.lines;const S=i=>L[i][0];const E=i=>L[i][1];
  // ---- scene 1: world ----
  const w=vis('world',t,-1,E(0)+0.2);
  if(w>0){
    const k=eio(t/E(0)); const sc=lerp(1,1.25,k);
    $('world').setAttribute('transform',`translate(${lerp(0,-300,k)},${lerp(0,-120,k)}) scale(${sc})`);
    $('heat').setAttribute('transform',`translate(0,${-10*Math.sin(t*3)})`);
    $('rosa').setAttribute('transform',`translate(1180,${715+3*Math.sin(t*2.2)})`);
    const blink=((t%3.1)<0.12)?0.15:1;$('eyeL').setAttribute('ry',9*blink);$('eyeR').setAttribute('ry',9*blink);
    const worry=fin(t,P[2],0.4);
    $('brows').setAttribute('d',`M-34,${-18-worry*4} l22,${-3+worry*8} M12,${-21+worry*4} l22,${3-worry*8}`);
    $('mouth').setAttribute('d',worry>0.5?'M-14,34 Q0,26 14,34':'M-16,30 Q0,40 16,30');
    $('armR').setAttribute('transform',`translate(62,-10) rotate(${-150*fio(t,P[3]-0.3,E(0)+1,0.4)+8*Math.sin(t*14)*fin(t,P[3],0.3)})`);
    $('thought').setAttribute('opacity',fin(t,P[2]+0.4,0.4));
    $('thought').setAttribute('transform',`translate(860,450) scale(${0.85+0.15*fin(t,P[2]+0.4,0.5)})`);
    $('qmark').setAttribute('transform',`translate(0,${6*Math.sin(t*6)})`);
  }
  $('tag').setAttribute('opacity',fio(t,0.3,P[2],0.4));
  // ---- scene 2: title ----
  if(vis('sc2',t,S(1)-0.2,E(1)+0.2)>0){
    $('t2sprout').setAttribute('transform',`translate(960,330) scale(${2.6*fin(t,S(1),0.6)})`);
    $('t2a').setAttribute('opacity',fin(t,S(1)+0.1,0.4));$('t2b').setAttribute('opacity',fin(t,S(1)+0.6,0.4));
    $('t2cart').setAttribute('opacity',fio(t,P[5],P[6]+0.2,0.3));
    [['k1',0],['k2',1],['k3',2],['k4',3]].forEach(([id,i])=>{const k=fin(t,P[6]+i*0.25,0.4);
      $(id).setAttribute('transform',`translate(${330+i*420},${720+(1-k)*40})`);$(id).setAttribute('opacity',k);});
  }
  // ---- scene 3: data ----
  if(vis('sc3',t,S(2)-0.2,E(2)+0.2)>0){
    const ha=430*eio((t-P[8]+0.3)/1.0), hb=430*330/859*eio((t-P[8]-0.6)/1.0);
    $('barAvg').setAttribute('y',800-ha);$('barAvg').setAttribute('height',ha);
    $('bar26').setAttribute('y',800-hb);$('bar26').setAttribute('height',hb);
    $('lblAvg').setAttribute('y',800-ha-20);$('lblAvg').setAttribute('opacity',fin(t,P[9],0.3));
    $('lbl26').setAttribute('y',800-hb-20);$('lbl26').setAttribute('opacity',fin(t,P[8]+1.4,0.3));
    $('lowest').setAttribute('opacity',fin(t,P[9]+2.4,0.3));
    $('dry').setAttribute('opacity',fin(t,P[10],0.4));
    D26.forEach((r,i)=>r.setAttribute('opacity',fin(t,P[10]+0.6+i*0.07,0.15)));
    $('dryNum').setAttribute('opacity',fin(t,P[10]+2.6,0.3));
    $('soil').setAttribute('opacity',fin(t,P[11],0.4));
    const n=cl((t-P[11]-0.2)/1.8)*8; let pts=[];
    for(let i=0;i<=Math.floor(n);i++)pts.push(`${sx(i)},${sy(SOIL[i])}`);
    const fi=Math.floor(n),fr=n-fi; if(fi<8){pts.push(`${lerp(sx(fi),sx(fi+1),fr)},${lerp(sy(SOIL[fi]),sy(SOIL[fi+1]),fr)}`);}
    $('soilLine').setAttribute('points',pts.join(' ')); $('soilLine').setAttribute('transform','');
    SD.forEach((d,i)=>d.setAttribute('opacity',(i<=n)?1:0));
    $('soilNote').setAttribute('opacity',fin(t,P[11]+2.4,0.3));
  }
  // ---- scene 4: El Nino ----
  if(vis('sc4',t,S(3)-0.2,E(3)+0.2)>0){
    END.forEach((g,i)=>g.setAttribute('opacity',fin(t,P[13]+i*0.35,0.25)));
    $('noRule').setAttribute('opacity',fin(t,P[14],0.4));
  }
  // ---- scene 5: people ----
  if(vis('sc5',t,S(4)-0.2,E(4)+0.2)>0){
    WF.forEach((r,i)=>{r.setAttribute('opacity',fin(t,P[16]+i*0.02,0.2));r.setAttribute('fill',(t>P[16]+2.4&&i<87)?'#C9B9A6':'#2E6A4C');});
    ['w87','w87b','w87c'].forEach((id,i)=>$(id).setAttribute('opacity',fin(t,P[16]+2.6+i*0.2,0.3)));
    $('road').setAttribute('opacity',fin(t,P[17],0.4));
    const k=cl((t-P[17]-0.3)/7.5); const px=lerp(900,1500,k), py=700+20*Math.sin(k*9)-30;
    $('truck').setAttribute('transform',`translate(${px},${py})`);
    HS.forEach((g,i)=>{const hx=HP[i][0];g.setAttribute('opacity',(hx<px+40&&hx<1460)?0.9:0);});
    $('agentNote').setAttribute('opacity',fio(t,P[17]+0.3,P[19],0.4));
    $('survey').setAttribute('opacity',fin(t,P[19],0.4));
  }
  // ---- scene 6: gap ----
  if(vis('sc6',t,S(5)-0.2,E(5)+0.2)>0){
    [['g1',P[22]],['g2',P[23]],['g3',P[24]]].forEach(([id,a])=>{const k=fin(t,a,0.5);$(id).setAttribute('opacity',k);});
  }
  // ---- scene 7: demo ----
  if(vis('sc7',t,S(6)-0.2,E(6)+0.2)>0){
    $('r7_eyeL').setAttribute('ry',((t%3.1)<0.12)?1.4:9);$('r7_eyeR').setAttribute('ry',((t%3.1)<0.12)?1.4:9);
    $('r7_mouth').setAttribute('d','M-20,26 Q0,48 20,26');
    $('rosa7').setAttribute('transform',`translate(1260,${700+3*Math.sin(t*2.2)}) scale(.85)`);
    SP7.forEach((u,i)=>{const g=fin(t,P[26]+i*0.05,0.5);u.setAttribute('transform',`translate(${u._p[0]},${u._p[1]}) scale(${g})`);});
    // steps: 0 soil, 1 risk+july, 2 window, 3 pasture, 4 income
    const step = t<P[27]?0 : t<P[28]?1 : t<P[29]?2 : t<P[30]?3 : 4;
    const sel = step===0?[0]: (step<=2?[1,2]: step===3?[3]:[4]);
    CHG.forEach((g,i)=>{const on=sel.includes(i);const j=sel.indexOf(i);g.setAttribute('opacity',on?1:0);g.setAttribute('transform',`translate(${-110+j*200},-190)`);});
    const msgs=[['Cowpea','Not related to cassava:','the pest left in the','ground won’t take it.'],
                ['Cowpea','It’s quick. Out of','the ground in 70 days.',''],
                ['Cowpea','July is inside the','official window.',''],
                ['Brachiaria','I don’t know how long','it takes in the ground,','so I can’t promise it fits.'],
                ['Income','I could measure 0%','of what matters','for this goal.']];
    const st=[P[26],P[27],P[28],P[29],P[30]][step];
    const m=msgs[step];['botT1','botT2','botT3','botT4'].forEach((id,i)=>$(id).textContent=m[i]);
    $('botMsg').setAttribute('opacity',fin(t,st+0.8,0.3));
    $('botMsg').setAttribute('transform',`translate(0,${(1-fin(t,st+0.8,0.3))*20})`);
    const conf=[null,null,null,'cycle unknown, said out loud','0% measured, said out loud'][step];
    $('confBadge').setAttribute('opacity',conf?fin(t,st+1.6,0.3):0); if(conf)$('confT').textContent=conf;
    // ZARC panel
    $('zarc').setAttribute('opacity',fio(t,P[28],P[29],0.4));
    const fk=eio((t-P[28]-2.2)/1.4); const fit=lerp(53,87,fk);
    $('fitBar').setAttribute('width',920*fit/100);
    $('fitT').textContent=`Fit, low-risk goal: ${Math.round(fit)}% ${fk<0.05?'(April)':fk>0.95?'(July)':''}`;
    MR.forEach((r,i)=>r.setAttribute('stroke',(i===3&&fk<0.5)||(i===6&&fk>=0.5)?'#1C2620':'none'));
    MR.forEach((r,i)=>r.setAttribute('stroke-width',4));
  }
  // ---- scene 8: three numbers ----
  if(vis('sc8',t,S(7)-0.2,E(7)+0.2)>0){
    [['n1',P[32]],['n2',P[33]],['n3',P[34]]].forEach(([id,a],i)=>{const k=fin(t,i===0?P[31]+0.3:a,0.5);$(id).setAttribute('opacity',0.25+0.75*fin(t,a,0.5));$(id).setAttribute('transform',`translate(${120+i*580},${290+(1-k)*30})`);});
    const c=0.82*fin(t,P[34]+0.3,1.0);$('confArc').setAttribute('stroke-dasharray',`${c*389.6} 400`);$('confPct').textContent=Math.round(c*100)+'%';
    $('arith').setAttribute('opacity',fin(t,P[35],0.4));
  }
  // ---- scene 9: same code ----
  if(vis('sc9',t,S(8)-0.2,E(8)+0.2)>0){
    const a=eio((t-P[37])/1.2), b=eio((t-P[38])/1.2);
    $('barA').setAttribute('width',700*Math.min(686/800,1)*a);
    $('barB').setAttribute('width',700*386/800*b);
    $('pA').setAttribute('opacity',fin(t,S(8),0.4)); $('pB').setAttribute('opacity',fin(t,S(8)+0.6,0.4));
    $('vA').setAttribute('opacity',fin(t,P[37]+3.5,0.3)); $('vB').setAttribute('opacity',fin(t,P[38]+2.6,0.3));
    $('needA').setAttribute('x1',-350+700*500/800);$('needA').setAttribute('x2',-350+700*500/800);$('needAt').setAttribute('x',-350+700*500/800);
    document.querySelectorAll('#pB line').forEach(l=>{l.setAttribute('x1',-350+700*500/800);l.setAttribute('x2',-350+700*500/800);});
    document.querySelectorAll('#pB text')[3].setAttribute('x',-350+700*500/800);
  }
  // ---- scene 10 ----
  if(vis('sc10',t,S(9)-0.2,E(9)+0.2)>0){
    ['l1','l2','l3'].forEach((id,i)=>$(id).setAttribute('opacity',fin(t,P[39]+1.4+i*1.0,0.3)));
    ['nx1','nx2','nx3'].forEach((id,i)=>$(id).setAttribute('opacity',fin(t,P[40]+0.6+i*0.9,0.3)));
  }
  // ---- scene 11 ----
  if(vis('sc11',t,S(10)-0.2,999)>0){
    $('f1').setAttribute('opacity',fin(t,P[41],0.4));$('f2').setAttribute('opacity',fin(t,P[42],0.4));
    $('f3').setAttribute('opacity',fin(t,P[43],0.4));$('f4').setAttribute('opacity',fin(t,P[43]+0.4,0.4));
    $('f5').setAttribute('opacity',fin(t,P[44],0.4));$('f6').setAttribute('opacity',fin(t,P[44],0.4));
    SP11.forEach((u,i)=>{const g=fin(t,P[41]+i*0.06,0.5);u.setAttribute('transform',`translate(${u._p[0]},${u._p[1]}) scale(${g*1.3})`);});
  }
  sub(t);
}
window.render=render;window.setSubs=setSubs;
