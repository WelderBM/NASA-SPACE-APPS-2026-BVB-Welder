// O CERNE, em JavaScript. Mesmas regras do motor/cerne.py, para a pagina
// CALCULAR em vez de consultar tabela pre-cozinhada.
//
// A tabela era o "if n==1 impar, if n==2 par": funcionava para o que eu tinha
// enumerado e nao tinha nada para o resto. Aqui esta o %2: a regra geral, que
// responde combinacao que ninguem enumerou, inclusive mes que nao existia na
// tabela.
//
// motor/conformidade.py garante que este arquivo e o Python dao a MESMA
// resposta. Se divergirem, o teste quebra.
(function(global){
const DIAS=[31,28,31,30,31,30,31,31,30,31,30,31];
const MES=['janeiro','fevereiro','março','abril','maio','junho','julho','agosto',
           'setembro','outubro','novembro','dezembro'];
const MOLDES_NEUTROS={
 indicacao:"Depois {de_colheu}, a melhor opção é {cultura}. {porque}. Quer saber os riscos?",
 indicacao_com_aviso:"Pelo que você quer, {cultura} seria a melhor, mas pode faltar água para ela. Quer ver uma de menor risco?",
 hipotese_boa:"{cultura} pode ser plantada. A chuva do período atende o que ela precisa. Quer comparar com as outras?",
 hipotese_ruim:"{cultura} pode ser plantada, mas pode faltar água. A chuva do período fica abaixo do que ela precisa. Quer ver outra?",
 hipotese_parente:"{cultura} é da mesma família {de_colheu}. Plantar em seguida multiplica as pragas de solo. Não recomendo.",
 hipotese_mesma:"Essa é a mesma cultura que acabou de ser colhida. Repetir multiplica as pragas de solo. Não recomendo.",
 hipotese_parente_sem_ciclo:"{cultura} é da mesma família {de_colheu}, então não recomendo. Do resto eu não sei: falta a duração do ciclo.",
 hipotese_sem_ciclo:"{cultura} não é da mesma família {de_colheu}, o que já ajuda, e {mes} costuma ter {chuva}. Falta a duração do ciclo.",
 sem_dado:"Das culturas da região eu sei a família de {n}, mas não sei a duração de nenhuma. Sem isso eu não indico.",
 estado_da_terra:"O solo está {estado}. {mes} costuma ter {chuva}.",
 nao_sei_prever:"Previsão de chuva eu não tenho. {mes} costuma ter {chuva}, com estiagem máxima de {estiagem} dias, e o solo está {estado}.",
 agua_sem_numero:"A exigência de água dela não está registrada. A janela acumula {chuva_mm} mm e a estiagem máxima {base} é de {estiagem} dias.",
 porques:{familia:"é de outra família {de_colheu}, então as pragas de solo não se mantêm",
   agua:"a chuva do período atende o que ela precisa", solo:"melhora o solo para o que vem depois",
   risco:"é de ciclo curto, {dias} dias", risco_seca:"tolera estiagem melhor que as outras",
   comida:"pode permanecer no campo, serve de reserva", pasto:"serve de pasto"},
 estado_terra:{acima:"mais úmido que o normal",abaixo:"mais seco que o normal",media:"dentro do normal"},
 aviso_ano_seco:"O ano acumulou {pct}% da chuva normal até aqui; considere menos água disponível.",
 aviso_ano_chuvoso:"O ano acumulou {pct}% da chuva normal até aqui, acima do costume.",
 chuva_qualitativa:{muita:"chuva alta",media:"chuva média",pouca:"chuva baixa"}};

function fmt(t,kw){return String(t).replace(/\{(\w+)\}/g,(m,k)=>k in kw?kw[k]:m)}
const lista=v=>Array.isArray(v)?v:[v];

class Cerne{
  constructor(d){this.NASA=d.nasa.lugares;this.CULT=d.culturas.culturas;
    this.PRIO=d.prioridades.prioridades;this.LOCAL=d.locais;}
  moldes(loc){return Object.assign({},MOLDES_NEUTROS,loc.moldes||{})}
  renderAll(M,chave,fechos,kw){
    const corpos=lista(M[chave]||''), fs=fechos?lista(M[fechos]||['']):[''];
    const out=[];
    for(const b of corpos)for(const f of fs){
      let t=fmt(b,kw); if(/\{\w+\}/.test(t))continue;
      t=f?(t+' '+f).trim():t.trim();
      if(t)t=t[0].toUpperCase()+t.slice(1);
      if(t&&!out.includes(t))out.push(t);
    }
    return out.slice(0,8);
  }
  janela(m0,dias){const o=[];let r=dias,m=m0;
    while(r>0&&o.length<15){o.push([m%12,Math.min(1,r/DIAS[m%12])]);r-=DIAS[m%12];m++}return o}
  fatorDoAno(place,m0,n=3){
    const c=this.NASA[place].clim.chuva_mm,o=this.NASA[place].ano2026.chuva_mm,ms=[];
    for(let k=1;k<=n;k++)ms.push((m0-k+12*9)%12);
    if(ms.some(m=>o[m]==null))return [null,null];
    const obs=ms.reduce((a,m)=>a+o[m],0),nor=ms.reduce((a,m)=>a+c[m],0);
    return [obs/nor,{observado_mm:Math.round(obs*10)/10,normal_mm:nor,
                     meses:ms.slice().reverse().map(m=>MES[m])}];
  }
  qualificaChuva(place,m){const a=this.NASA[place].clim.chuva_mm,c=a.slice().sort((x,y)=>x-y);
    return a[m]<=c[3]?'pouca':a[m]>=c[8]?'muita':'media'}
  estadoObservado(place,m0){
    const cl=this.NASA[place].clim,an=this.NASA[place].ano2026,[f,det]=this.fatorDoAno(place,m0);
    const e={mes:MES[m0],chuva_normal_do_mes_mm:cl.chuva_mm[m0],
             chuva_qualitativa:this.qualificaChuva(place,m0),
             veranico_normal_do_mes_dias:cl.veranico[m0]};
    if(an.solo_raiz[m0]!=null){const o=an.solo_raiz[m0],n=cl.solo_raiz[m0];
      const dif=n?(o-n)/n:0;
      e.solo_raiz={observado:o,normal:n,diferenca:Math.floor(dif*1000+0.5)/1000,
        situacao:Math.abs(dif)<0.03?'media':(dif>0?'acima':'abaixo')};}
    if(f)e.fator_do_ano=Object.assign({razao:Math.round(f*100)/100},det);
    return e;
  }
  risco(c,place,m0){
    const r={},nao_sei=[],ciclo=c.ciclo_dias,cmin=ciclo?ciclo[0]:null;
    const [f]=this.fatorDoAno(place,m0),cl=this.NASA[place].clim;
    if(cmin==null){nao_sei.push('quanto tempo essa cultura leva até a colheita');
      return [{avaliavel:false},nao_sei]}
    const ch=this.janela(m0,cmin).reduce((a,[m,fr])=>a+cl.chuva_mm[m]*fr,0);
    r.chuva_normal_mm=Math.round(ch);
    r.chuva_ajustada_mm=f?Math.round(ch*f):null;
    const ag=c.agua_ciclo_mm;
    if(ag&&ag[0]!=null){const razao=(ch*(f||1))/ag[0];
      r.agua={exige_mm:ag[0],razao:Math.round(razao*100)/100,
              nivel:razao>=1.2?'baixo':razao>=0.9?'médio':'alto'};
    }else{r.agua={nivel:'sem dado'};nao_sei.push('quanta água essa cultura precisa');r.agua_indireta=true}
    const fc=c.fase_critica_dias,ini=fc?fc[0]:0,fim=fc?fc[1]:cmin,set=new Set();
    for(let d=ini;d<=fim;d+=10)set.add((m0+Math.floor(d/30))%12);
    const ms=[...set].sort((a,b)=>a-b);
    r.veranico={dias:Math.max(...ms.map(m=>cl.veranico[m])),meses:ms.map(m=>MES[m]),
                base:fc?'na fase crítica':'no ciclo'};
    if(!fc)nao_sei.push('qual é a fase crítica dessa cultura, então usei o ciclo inteiro');
    r.avaliavel=true;return [r,nao_sei];
  }
  encaixe(c,prioridade){
    const p=this.PRIO[prioridade];
    if(!p.servivel)return [null,0,[],p.resposta_honesta];
    const ci=c.ciclo_dias,res={alto:1,medio:.5,baixo:0},sec={alta:1,media:.6,baixa:.2};
    const mapa={familia_diferente:1,fixa_n:c.fixa_n?1:0,
      residuo_alto:c.residuo in res?res[c.residuo]:null,
      forrageira:c.forrageira?1:0,
      tolera_seca:c.tolera_seca in sec?sec[c.tolera_seca]:null,
      espera_no_campo:c.espera_no_campo==null?null:(c.espera_no_campo?1:0),
      ciclo_curto:ci?(ci[0]<=90?1:ci[0]<=150?.6:.3):null,
      agua_baixa:null,cabe_na_janela:null,cobertura_meses:null};
    let num=0,den=0,tot=0;const faltou=[];
    for(const[pn,pw]of Object.entries(p.pesos)){tot+=pw;const e=mapa[pn];
      if(e==null){faltou.push(pn);continue}num+=pw*e;den+=pw}
    return [den?num/den:null,tot?den/tot:0,faltou,null];
  }
  porques(c,r,fam){
    const out=[];
    if(c.familia!==fam)out.push(['familia',{}]);
    if(r.agua&&r.agua.razao!=null&&r.agua.nivel!=='alto')out.push(['agua',{}]);
    if(c.fixa_n||c.residuo==='alto')out.push(['solo',{}]);
    if(c.tolera_seca==='alta')out.push(['risco_seca',{}]);
    else if(c.ciclo_dias&&c.ciclo_dias[0]<=90)out.push(['risco',{dias:c.ciclo_dias[0]}]);
    if(c.espera_no_campo)out.push(['comida',{}]);
    if(c.forrageira)out.push(['pasto',{}]);
    return out;
  }
  renderPorque(pqs,prioridade,M,cn,dcn){
    const d={};for(const[k,pr]of pqs)if(!(k in d))d[k]=pr;
    const ordem=(prioridade==='risco'?[prioridade,prioridade+'_seca']:[prioridade]).concat(['agua','familia']);
    for(const k of ordem)if(k in d)return [fmt(lista(M.porques[k]||'')[0],Object.assign({colheu:cn,de_colheu:dcn},d[k])),k];
    for(const k in d)return [fmt(lista(M.porques[k]||'')[0],Object.assign({colheu:cn,de_colheu:dcn},d[k])),k];
    return ['',null];
  }
  avisos(r,M){const out=[],v=r.veranico;
    if(r.agua_indireta&&v)out.push(fmt(lista(M.agua_sem_numero||'')[0],
      {chuva_mm:r.chuva_ajustada_mm||r.chuva_normal_mm,estiagem:Math.floor(v.dias+0.5),base:v.base}));
    else if(v&&v.dias>=10)out.push(`a estiagem normal ${v.base} é de ${Math.floor(v.dias+0.5)} dias`);
    if(r.agua&&r.agua.nivel==='alto')out.push('a chuva do período não cobre o que essa cultura pede');
    return out}

  atender(p){
    const place=p.lugar.id,m0=p.momento.mes_plantio,loc=this.LOCAL[p.lugar.config_local];
    const M=this.moldes(loc),intencao=p.intencao,est=this.estadoObservado(place,m0);
    const nc=n=>this.CULT[n].nome.split(' (')[0].toLowerCase();
    const de=n=>((this.CULT[n].artigo||'a')==='a'?'da ':'do ')+nc(n);
    const res={intencao,lugar:this.NASA[place].nome,mes_plantio:MES[m0],
      registro:loc.moldes?'local':'português neutro',estado_observado:est,
      opcoes:[],sei_pouco:[],limites:[],fala:null,falas:[],aviso_do_ano:null};
    const sr=est.solo_raiz;
    if(intencao==='estado-do-solo'){
      res.falas=this.renderAll(M,'estado_da_terra','fechos_terra',{mes:est.mes,
        chuva:M.chuva_qualitativa[est.chuva_qualitativa],
        estado:sr?M.estado_terra[sr.situacao]:'sem leitura'});
      res.fala=res.falas[0];
      if(!sr)res.limites.push('sem leitura de umidade do solo para este mês');
      return res;
    }
    if(intencao==='vai-chover'){
      res.limites.push('não existe previsão de chuva nestes dados; a série é histórica');
      res.falas=this.renderAll(M,'nao_sei_prever',null,{mes:est.mes,
        chuva:M.chuva_qualitativa[est.chuva_qualitativa],
        estiagem:Math.floor(est.veranico_normal_do_mes_dias+0.5),
        estado:sr?M.estado_terra[sr.situacao]:'sem leitura'});
      res.fala=res.falas[0];return res;
    }
    const colheu=p.colheu,fam=colheu?this.CULT[colheu].familia:null;
    const cn=colheu?nc(colheu):'',dcn=colheu?de(colheu):'';
    const cands=(intencao==='e-se'&&p.hipotese)?[p.hipotese]:loc.culturas_disponiveis;
    for(const nome of cands){
      const c=this.CULT[nome];if(!c)continue;
      if(fam&&c.familia===fam&&intencao!=='e-se')continue;
      const [r,ns]=this.risco(c,place,m0);
      const [enc,conf]=this.encaixe(c,p.prioridade);
      const pqs=fam?this.porques(c,r,fam):[];
      res.opcoes.push({cultura:c.nome,id:nome,familia:c.familia,
        mesma_familia_do_que_colheu:!!(fam&&c.familia===fam),risco:r,
        encaixe:enc==null?null:Math.round(enc*100)/100,
        confianca:Math.round(conf*100)/100,_pqs:pqs,
        porques:pqs.map(([k,pr])=>fmt(lista(M.porques[k]||'')[0],Object.assign({colheu:cn,de_colheu:dcn},pr))),
        avisos:this.avisos(r,M),nao_sei:ns,qualidade_do_dado:c.qualidade,
        validar_com_tecnico:['a janela de plantio oficial do ZARC para o município']});
    }
    res.sei_pouco=res.opcoes.filter(o=>!o.risco.avaliavel)
      .map(o=>({cultura:o.cultura,familia:o.familia,falta:o.nao_sei}));
    res.opcoes=res.opcoes.filter(o=>o.risco.avaliavel)
      .sort((a,b)=>(a.encaixe==null)-(b.encaixe==null)||(b.encaixe||0)-(a.encaixe||0));
    if(intencao==='e-se'&&p.hipotese){
      const h=p.hipotese,alvo=nc(h);
      const parente=this.CULT[h].familia===fam,av=res.opcoes.length>0;
      const kw={cultura:alvo,colheu:cn,de_colheu:dcn};
      if(h===colheu)res.falas=this.renderAll(M,'hipotese_mesma',null,kw);
      else if(parente&&!av)res.falas=this.renderAll(M,'hipotese_parente_sem_ciclo',null,kw);
      else if(parente)res.falas=this.renderAll(M,'hipotese_parente',null,kw);
      else if(!av)res.falas=this.renderAll(M,'hipotese_sem_ciclo',null,
        Object.assign({mes:est.mes,chuva:M.chuva_qualitativa[est.chuva_qualitativa]},kw));
      else if(res.opcoes[0].risco.agua&&res.opcoes[0].risco.agua.nivel==='alto')
        res.falas=this.renderAll(M,'hipotese_ruim','fechos_hipotese',kw);
      else res.falas=this.renderAll(M,'hipotese_boa','fechos_hipotese',kw);
    }else if(!res.opcoes.length&&res.sei_pouco.length){
      res.falas=this.renderAll(M,'sem_dado',null,{n:res.sei_pouco.length});
    }else if(res.opcoes.length){
      const o=res.opcoes[0];
      if(o.risco.agua&&o.risco.agua.nivel==='alto'){
        res.falas=this.renderAll(M,'indicacao_com_aviso','fechos_aviso',{cultura:nc(o.id)});
        o.avisos.unshift('o encaixe é bom mas o lugar não dá a água que ela pede');
      }else{
        const [pq]=this.renderPorque(o._pqs,p.prioridade,M,cn,dcn);
        res.falas=this.renderAll(M,'indicacao','fechos',{colheu:cn,de_colheu:dcn,
          cultura:nc(o.id),porque:pq?pq.charAt(0).toUpperCase()+pq.slice(1):''});
      }
    }
    const fa=est.fator_do_ano;
    if(fa&&(intencao==='proximo-plantio'||intencao==='e-se')&&res.falas.length){
      const rz=fa.razao;
      if(rz<=0.9||rz>=1.1)
        res.aviso_do_ano=this.renderAll(M,rz<=0.9?'aviso_ano_seco':'aviso_ano_chuvoso',
          null,{pct:Math.floor(rz*100+0.5)})[0];
    }
    if(res.falas.length)res.fala=res.falas[0];
    res.opcoes.forEach(o=>{delete o._pqs});
    res.limites.push('a janela de plantio oficial do ZARC não está carregada; confirme com técnico');
    return res;
  }
}
global.Cerne=Cerne;global.MES_CERNE=MES;
})(typeof module!=='undefined'?module.exports:window);
