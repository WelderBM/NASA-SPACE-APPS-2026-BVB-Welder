// O CERNE, em JavaScript. Mesmas regras do motor/cerne.py, para a pagina
// CALCULAR em vez de consultar tabela pre-cozinhada.
//
// A tabela era o "if n==1 impar, if n==2 par": funcionava para o que estava
// enumerado e nao tinha nada para o resto. Aqui esta o %2: a regra geral, que
// responde combinacao que ninguem enumerou, inclusive mes que nao existia na
// tabela.
//
// motor/conformidade.py garante que este arquivo e o Python dao a MESMA
// resposta. Se divergirem, o teste quebra.
(function(global){
const DIAS=[31,28,31,30,31,30,31,31,30,31,30,31];
const CONF_MIN=0.5, MARGEM_SEM_CICLO=0.25;
const MES=['janeiro','fevereiro','março','abril','maio','junho','julho','agosto',
           'setembro','outubro','novembro','dezembro'];
const MOLDES_NEUTROS={
 indicacao:"Depois {de_colheu}, a melhor opção é {cultura}. {porque}. Quer saber os riscos?",
 indicacao_com_aviso:"Pelo que você quer, {cultura} seria a melhor, porque {porque}. Mas pode faltar água para ela. Quer ver uma de menor risco?",
 indicacao_com_aviso_sem_porque:"Pelo que você quer, {cultura} seria a melhor, mas pode faltar água para ela. Quer ver uma de menor risco?",
 hipotese_boa:"{cultura} pode ser plantada. A chuva do período atende o que ela precisa. Quer comparar com as outras?",
 hipotese_ruim:"{cultura} pode ser plantada, mas pode faltar água. A chuva do período fica abaixo do que ela precisa. Quer ver outra?",
 hipotese_parente:"{cultura} é da mesma família {de_colheu}. Plantar em seguida multiplica as pragas de solo. Não recomendo.",
 hipotese_mesma:"Essa é a mesma cultura que acabou de ser colhida. Repetir multiplica as pragas de solo. Não recomendo.",
 hipotese_parente_sem_ciclo:"{cultura} é da mesma família {de_colheu}, então não recomendo. Do resto eu não sei: falta a duração do ciclo.",
 hipotese_sem_ciclo:"{cultura} não é da mesma família {de_colheu}, o que já ajuda, e {mes} costuma ter {chuva}. Falta a duração do ciclo.",
 sem_dado:"Das culturas da região eu sei a família de {n}, mas não sei a duração de nenhuma. Sem isso eu não indico.",
 estado_da_terra:"O solo está {estado}. {mes} costuma ter {chuva}.",
 nao_sei_prever:"Previsão de chuva eu não tenho. {mes} costuma ter {chuva}, com estiagem máxima de {estiagem} dias, e o solo está {estado}.",
 hipotese_sem_agua:"{cultura} não é da mesma família {de_colheu}. A exigência de água dela não está registrada; a janela acumula {chuva_mm} mm e a estiagem máxima {base} é de {estiagem} dias.",
 indicacao_pouca_confianca:"Depois {de_colheu}, a melhor opção é {cultura}, mas só {pct}% dos critérios dessa prioridade puderam ser avaliados nela.",
 lacuna_falada:"A leitura deste ano vai até {ate}; para {mes} há apenas a média de {anos} anos, sem ajuste pelo ano corrente.",
 melhor_sem_ciclo:"Para esse objetivo a cultura indicada seria {cultura}, porque {porque}. Falta a duração do ciclo dela. Entre as avaliáveis, {alternativa} é a mais próxima.",
 melhor_sem_ciclo_sem_porque:"Para esse objetivo a cultura indicada seria {cultura}, mas falta a duração do ciclo dela. Entre as avaliáveis, {alternativa} é a mais próxima.",
 solo_fundo:"Camada superficial {sup}; camada profunda {fundo}. A reserva profunda é a que sustenta no veranico.",
 aviso_calor:"A máxima de {mes} chega a {pico} °C, acima do limite de {limite} °C dessa cultura.",
 agua_sem_numero:"A exigência de água dela não está registrada. A janela acumula {chuva_mm} mm e a estiagem máxima {base} é de {estiagem} dias.",
 porques:{familia:"é de outra família {de_colheu}, então as pragas de solo não se mantêm",
   agua:"a chuva do período atende o que ela precisa", solo:"melhora o solo para o que vem depois",
   risco:"é de ciclo curto, {dias} dias", risco_seca:"tolera estiagem melhor que as outras",
   comida:"pode permanecer no campo, serve de reserva", pasto:"serve de pasto"},
 estado_terra:{acima:"mais úmido que o normal",abaixo:"mais seco que o normal",media:"dentro do normal"},
 aviso_ano_seco:"O ano acumulou {pct}% da chuva normal até aqui; considere menos água disponível.",
 aviso_ano_chuvoso:"O ano acumulou {pct}% da chuva normal até aqui, acima do costume.",
 chuva_qualitativa:{muita:"chuva alta",media:"chuva média",pouca:"chuva baixa"}};

const PLURAL={'dias seguidos':'dia seguido','meses seguidos':'mês seguido',
  'dias':'dia','milímetros':'milímetro','graus':'grau','meses':'mês','anos':'ano'};
// concordancia num lugar so: ver o comentario do _conc no cerne.py
function conc(t){for(const pl in PLURAL)t=t.split(' 1 '+pl).join(' 1 '+PLURAL[pl]);return t}
function fmt(t,kw){return conc(String(t).replace(/\{(\w+)\}/g,(m,k)=>k in kw?kw[k]:m))}
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
  ateOndeEnxergo(place){
    const ch=this.NASA[place].ano2026.chuva_mm,idx=[];
    ch.forEach((v,i)=>{if(v!=null)idx.push(i)});
    return idx.length?Math.max(...idx):null;
  }
  lacunasDoLugar(place,m0){
    // UM lugar so que sabe o que falta e POR QUE
    const an=this.NASA[place].ano2026,out=[],ate=this.ateOndeEnxergo(place);
    if(ate==null)return out;
    const faltaChuva=[1,2,3].some(k=>an.chuva_mm[((m0-k)%12+12)%12]==null);
    if(faltaChuva)out.push({o_que:'como o ano está indo',ate:MES[ate],falar:true,
      por_que:`a leitura deste ano vai até ${MES[ate]}`,
      efeito:'uso só a média da série, sem ajustar pelo ano corrente'});
    if(an.solo_raiz[m0]==null)out.push({o_que:'umidade do solo deste mês',ate:MES[ate],
      falar:!faltaChuva,por_que:`a leitura deste ano vai até ${MES[ate]}`,
      efeito:'uso só a média da série'});
    return out;
  }
  estadoObservado(place,m0){
    const cl=this.NASA[place].clim,an=this.NASA[place].ano2026,[f,det]=this.fatorDoAno(place,m0);
    const e={mes:MES[m0],anos_de_serie:(this.NASA[place].abr_set||{}).anos_base||null,
             chuva_normal_do_mes_mm:cl.chuva_mm[m0],
             chuva_qualitativa:this.qualificaChuva(place,m0),
             veranico_normal_do_mes_dias:cl.veranico[m0]};
    if(an.solo_raiz[m0]!=null){const o=an.solo_raiz[m0],n=cl.solo_raiz[m0];
      const dif=n?(o-n)/n:0;
      e.solo_raiz={observado:o,normal:n,diferenca:Math.floor(dif*1000+0.5)/1000,
        situacao:Math.abs(dif)<0.03?'media':(dif>0?'acima':'abaixo')};}
    for(const[chave,campo]of[['solo_superficie','solo_sup'],['solo_profundo','solo_perfil']]){
      const ob=an[campo][m0],no=cl[campo][m0];
      if(ob==null)continue;
      const d=no?(ob-no)/no:0;
      e[chave]={observado:ob,normal:no,diferenca:Math.floor(d*1000+0.5)/1000,
        situacao:Math.abs(d)<0.03?'media':(d>0?'acima':'abaixo')};
    }
    const sp=e.solo_superficie,fu=e.solo_profundo;
    if(sp&&fu&&fu.situacao==='abaixo'&&sp.situacao!=='abaixo'&&(sp.diferenca-fu.diferenca)>=0.08)
      e.superficie_engana=true;
    e.tsolo_c=cl.tsolo[m0];
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
    const tl=c.tmax_sofre_c;
    if(tl){let pico=-1e9,mp=m0;
      for(const[m]of this.janela(m0,cmin))if(cl.tmax[m]>pico){pico=cl.tmax[m];mp=m}
      if(pico>tl)r.calor={limite:tl,pico:Math.floor(pico+0.5),mes:MES[mp]};
    }else nao_sei.push('a partir de que temperatura essa cultura sofre');
    r.avaliavel=true;return [r,nao_sei];
  }
  cobertura(c){
    if(((c.ciclo_nota||'')+'').toLowerCase().includes('perene'))return 1;
    const ci=c.ciclo_dias; if(!ci)return null;
    return Math.min(1,(ci[0]/30)/6);
  }
  cabeNaJanela(nome,loc,m0){
    const j=((loc.janelas_zarc||{})[nome])||{};
    const ini=j.inicio_mes,fim=j.fim_mes;
    if(ini==null||fim==null)return null;
    const dentro=(ini<=fim)?(ini<=m0&&m0<=fim):(m0>=ini||m0<=fim);
    return dentro?1:0;
  }
  encaixe(c,prioridade,nome,loc,m0){
    const p=this.PRIO[prioridade];
    if(!p.servivel)return [null,0,[],p.resposta_honesta];
    const ci=c.ciclo_dias,res={alto:1,medio:.5,baixo:0},sec={alta:1,media:.6,baixa:.2};
    const mapa={familia_diferente:1,fixa_n:c.fixa_n?1:0,
      residuo_alto:c.residuo in res?res[c.residuo]:null,
      forrageira:c.forrageira?1:0,
      tolera_seca:c.tolera_seca in sec?sec[c.tolera_seca]:null,
      espera_no_campo:c.espera_no_campo==null?null:(c.espera_no_campo?1:0),
      ciclo_curto:ci?(ci[0]<=90?1:ci[0]<=150?.6:.3):null,
      agua_baixa:null,
      cabe_na_janela:(nome&&loc&&m0!=null)?this.cabeNaJanela(nome,loc,m0):null,
      cobertura_meses:this.cobertura(c)};
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
  // evitar: chave de porque que nao deve ser usada, porque a razao da PROPRIA
  // prioridade e tautologica no melhor_sem_ciclo. quantos: quantas juntar.
  // Espelho do render_porque do cerne.py, inclusive na ordem de varredura.
  renderPorque(pqs,prioridade,M,cn,dcn,evitar,quantos){
    quantos=quantos||1;
    const d={};for(const[k,pr]of pqs)if(!(k in d))d[k]=pr;
    if(evitar)delete d[evitar];
    const ordem=(prioridade==='risco'?[prioridade,prioridade+'_seca']:[prioridade]).concat(['agua','familia']);
    const resto=Object.keys(d).filter(k=>ordem.indexOf(k)<0);
    const saida=[];
    for(const k of ordem.concat(resto)){
      if(k in d&&saida.length<quantos){
        const t=fmt(lista(M.porques[k]||'')[0],Object.assign({colheu:cn,de_colheu:dcn},d[k]));
        if(t)saida.push([t,k]);
      }
    }
    if(!saida.length)return ['',null];
    if(quantos===1)return saida[0];
    return [saida.map(x=>x[0]).join(', e '),saida[0][1]];
  }
  avisos(r,M){const out=[],v=r.veranico;
    if(r.agua_indireta&&v)out.push(fmt(lista(M.agua_sem_numero||'')[0],
      {chuva_mm:r.chuva_ajustada_mm||r.chuva_normal_mm,estiagem:Math.floor(v.dias+0.5),base:v.base}));
    else if(v&&v.dias>=10)out.push(`a estiagem normal ${v.base} é de ${Math.floor(v.dias+0.5)} dias`);
    if(r.agua&&r.agua.nivel==='alto')out.push('a chuva do período não cobre o que essa cultura pede');
    if(r.calor)out.push(fmt(lista(M.aviso_calor||'')[0],r.calor));
    return out}

  atender(p){
    const place=p.lugar.id,m0=p.momento.mes_plantio,loc=this.LOCAL[p.lugar.config_local];
    const M=this.moldes(loc),intencao=p.intencao,est=this.estadoObservado(place,m0);
    const nc=n=>this.CULT[n].nome.split(' (')[0].toLowerCase();
    const de=n=>((this.CULT[n].artigo||'a')==='a'?'da ':'do ')+nc(n);
    const res={intencao,lugar:this.NASA[place].nome,mes_plantio:MES[m0],
      registro:loc.moldes?'local':'português neutro',estado_observado:est,
      lacunas:this.lacunasDoLugar(place,m0),
      opcoes:[],sei_pouco:[],limites:[],fala:null,falas:[],aviso_do_ano:null,destaque:null};
    const _fecha=()=>{
      const f=res.lacunas.filter(l=>l.falar);
      if(f.length&&!res.aviso_do_ano)res.aviso_do_ano=this.renderAll(M,'lacuna_falada',null,
        {ate:f[0].ate,mes:est.mes,anos:est.anos_de_serie||45})[0];
      res.lacunas.forEach(l=>res.limites.push(`${l.o_que}: ${l.por_que}, então ${l.efeito}`));
    };
    const sr=est.solo_raiz;
    if(intencao==='estado-do-solo'){
      res.falas=this.renderAll(M,'estado_da_terra','fechos_terra',{mes:est.mes,
        chuva:M.chuva_qualitativa[est.chuva_qualitativa],
        estado:sr?M.estado_terra[sr.situacao]:'sem leitura'});
      res.fala=res.falas[0];
      if(est.superficie_engana){const sp=est.solo_superficie,fu=est.solo_profundo;
        res.aviso_do_ano=fmt(lista(M.solo_fundo||'')[0],
          {sup:M.estado_terra[sp.situacao],fundo:M.estado_terra[fu.situacao]});}
      if(!sr)res.limites.push('sem leitura de umidade do solo para este mês');
      _fecha();return res;
    }
    if(intencao==='vai-chover'){
      res.limites.push('não existe previsão de chuva nestes dados; a série é histórica');
      res.falas=this.renderAll(M,'nao_sei_prever',null,{mes:est.mes,
        chuva:M.chuva_qualitativa[est.chuva_qualitativa],
        estiagem:Math.floor(est.veranico_normal_do_mes_dias+0.5),
        estado:sr?M.estado_terra[sr.situacao]:'sem leitura'});
      res.fala=res.falas[0];_fecha();return res;
    }
    const colheu=p.colheu,fam=colheu?this.CULT[colheu].familia:null;
    const cn=colheu?nc(colheu):'',dcn=colheu?de(colheu):'';
    const cands=(intencao==='e-se'&&p.hipotese)?[p.hipotese]:loc.culturas_disponiveis;
    for(const nome of cands){
      const c=this.CULT[nome];if(!c)continue;
      if(fam&&c.familia===fam&&intencao!=='e-se')continue;
      const [r,ns]=this.risco(c,place,m0);
      const [enc,conf]=this.encaixe(c,p.prioridade,nome,loc,m0);
      const pqs=fam?this.porques(c,r,fam):[];
      res.opcoes.push({cultura:c.nome,id:nome,familia:c.familia,ciclo_dias:c.ciclo_dias||null,
        mesma_familia_do_que_colheu:!!(fam&&c.familia===fam),risco:r,
        encaixe:enc==null?null:Math.round(enc*100)/100,
        confianca:Math.round(conf*100)/100,_pqs:pqs,
        porques:pqs.map(([k,pr])=>fmt(lista(M.porques[k]||'')[0],Object.assign({colheu:cn,de_colheu:dcn},pr))),
        avisos:this.avisos(r,M),nao_sei:ns,
        nao_sei_nao_dito:ns.filter(x=>!(r.agua_indireta&&x.indexOf('água')>=0)),
        qualidade_do_dado:c.qualidade,
        validar_com_tecnico:(c.validar_com_tecnico||[])
          .concat(['a janela de plantio oficial do ZARC para o município'])});
    }
    const semJanela=res.opcoes.filter(o=>!(((loc.janelas_zarc||{})[o.id])||{}).inicio_mes);
    if(semJanela.length)res.lacunas.push({o_que:'a janela oficial de plantio',
      por_que:`o ZARC não está carregado para ${semJanela.length} das culturas daqui`,
      efeito:'não dá para dizer se cabe na janela recomendada',falar:false});
    res.sei_pouco=res.opcoes.filter(o=>!o.risco.avaliavel)
      .map(o=>({cultura:o.cultura,id:o.id,familia:o.familia,encaixe:o.encaixe,
        confianca:o.confianca,_pqs:o._pqs||[],falta:o.nao_sei}))
      .sort((a,b)=>(a.encaixe==null)-(b.encaixe==null)||(b.encaixe||0)-(a.encaixe||0));
    const gate=o=>((o.confianca||0)>=CONF_MIN?0:1);
    // ver o comentario no cerne.py: em "arriscar pouco", o risco de agua da NASA
    // (alto ou sem dado) desce a cultura abaixo das de risco baixo ou medio
    const aguaRuim=o=>(p.prioridade==='risco'&&['alto','sem dado'].includes((o.risco.agua||{}).nivel))?1:0;
    res.opcoes=res.opcoes.filter(o=>o.risco.avaliavel)
      .sort((a,b)=>(a.encaixe==null)-(b.encaixe==null)||gate(a)-gate(b)||aguaRuim(a)-aguaRuim(b)||(b.encaixe||0)-(a.encaixe||0));
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
      else if(res.opcoes[0].risco.agua&&res.opcoes[0].risco.agua.nivel==='sem dado'){
        const rk=res.opcoes[0].risco,v=rk.veranico||{};
        res.falas=this.renderAll(M,'hipotese_sem_agua',null,Object.assign({
          chuva_mm:rk.chuva_ajustada_mm||rk.chuva_normal_mm,
          estiagem:Math.floor((v.dias||0)+0.5),base:v.base||'no ciclo'},kw));
      }else res.falas=this.renderAll(M,'hipotese_boa','fechos_hipotese',kw);
    }else if(!res.opcoes.length&&res.sei_pouco.length){
      res.falas=this.renderAll(M,'sem_dado',null,{n:res.sei_pouco.length});
    }else if(res.opcoes.length){
      const o=res.opcoes[0];
      const sp=res.sei_pouco.length?res.sei_pouco[0]:null;
      if(sp&&(sp.confianca||0)>=CONF_MIN&&((sp.encaixe||0)-(o.encaixe||0))>=MARGEM_SEM_CICLO){
        res.destaque=sp.id;
        // diz o que sabe antes do que nao sabe: ver o comentario no cerne.py
        const [pqsp]=this.renderPorque(sp._pqs||[],p.prioridade,M,cn,dcn,p.prioridade,2);
        res.falas=this.renderAll(M,pqsp?'melhor_sem_ciclo':'melhor_sem_ciclo_sem_porque',null,
          {cultura:nc(sp.id),alternativa:nc(o.id),porque:pqsp});
        // o aviso dessa cultura NAO entra nos avisos da outra: a pagina junta os
        // avisos numa frase so e o "ela" trocava de dono no meio da mensagem
      }else if((o.confianca||0)<CONF_MIN){
        const pct=Math.floor((o.confianca||0)*100+0.5);
        res.falas=this.renderAll(M,'indicacao_pouca_confianca',null,
          {colheu:cn,de_colheu:dcn,cultura:nc(o.id),pct:pct});
        o.avisos.unshift(`só ${pct}% dos critérios dessa prioridade puderam ser avaliados`);
      }else if(o.risco.agua&&o.risco.agua.nivel==='alto'){
        // ver o comentario no cerne.py: dizia so a ma noticia
        const [pqa]=this.renderPorque(o._pqs,p.prioridade,M,cn,dcn,'agua');
        res.falas=this.renderAll(M,pqa?'indicacao_com_aviso':'indicacao_com_aviso_sem_porque',
          'fechos_aviso',{cultura:nc(o.id),porque:pqa});
        o.avisos.unshift('o encaixe é bom mas o lugar não dá a água que ela pede');
      }else{
        const [pq]=this.renderPorque(o._pqs,p.prioridade,M,cn,dcn);
        res.falas=this.renderAll(M,'indicacao','fechos',{colheu:cn,de_colheu:dcn,
          cultura:nc(o.id),porque:pq?pq.charAt(0).toUpperCase()+pq.slice(1):''});
      }
      // ver o comentario no cerne.py
      if(intencao!=='e-se'&&res.opcoes.every(aguaRuim))
        res.opcoes[0].avisos.unshift('nesse mês todas as opções daqui têm risco alto '+
          'de faltar água, ou água que eu não sei medir');
    }
    _fecha();
    const fa=est.fator_do_ano;
    if(fa&&(intencao==='proximo-plantio'||intencao==='e-se')&&res.falas.length){
      const rz=fa.razao;
      if(rz<=0.9||rz>=1.1)
        res.aviso_do_ano=this.renderAll(M,rz<=0.9?'aviso_ano_seco':'aviso_ano_chuvoso',
          null,{pct:Math.floor(rz*100+0.5)})[0];
    }
    if(res.falas.length)res.fala=res.falas[0];
    if(!res.destaque&&res.opcoes.length)res.destaque=res.opcoes[0].id;
    res.opcoes.forEach(o=>{delete o._pqs});
    res.sei_pouco.forEach(o=>{delete o._pqs});
    res.limites.push('de onde vem a semente ou a muda e quanto ela custa não entra aqui; '+
      'esta resposta diz o que plantar, não se dá para comprar');
    return res;
  }
}
global.Cerne=Cerne;global.MES_CERNE=MES;
})(typeof module!=='undefined'?module.exports:window);
