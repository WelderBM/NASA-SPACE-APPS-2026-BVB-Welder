const fs=require('fs'),{Cerne}=require('./cerne.js');
const D='dados/';const j=f=>JSON.parse(fs.readFileSync(D+f,'utf8'));
const cerne=new Cerne({nasa:j('nasa-power.json'),culturas:j('culturas.json'),
  prioridades:j('prioridades.json'),
  locais:{roraima:j('local-roraima.json'),'centro-oeste':j('local-centro-oeste.json')}});
const {casos,esperado}=JSON.parse(fs.readFileSync(process.argv[2]||'/tmp/conf.json','utf8'));
// compara a resposta INTEIRA, com chaves ordenadas: falas e resumo das opcoes
// deixavam de fora o veranico e o resto do risco
const canon=v=>Array.isArray(v)?v.map(canon):(v&&typeof v==='object')?
  Object.keys(v).sort().reduce((o,k)=>(o[k]=canon(v[k]),o),{}):v;
let erros=0, inteira=0;
casos.forEach((c,i)=>{
  const got=cerne.atender(c),exp=esperado[i];
  const a=JSON.stringify(got.falas), b=JSON.stringify(exp.falas);
  const ao=JSON.stringify((got.opcoes||[]).map(o=>[o.id,o.encaixe,o.confianca,o.risco.chuva_ajustada_mm,(o.risco.agua||{}).nivel]));
  const bo=JSON.stringify((exp.opcoes||[]).map(o=>[o.id,o.encaixe,o.confianca,o.risco.chuva_ajustada_mm,(o.risco.agua||{}).nivel]));
  const ia=JSON.stringify(canon(got)), ib=JSON.stringify(canon(exp));
  if(ia!==ib && a===b && ao===bo){ if(inteira<3){console.log('DIVERGE fora das falas, caso',i,JSON.stringify(c));
      console.log('  py:',ib.slice(0,300));console.log('  js:',ia.slice(0,300));} inteira++; }
  if(a!==b||ao!==bo){
    if(erros<3){console.log('DIVERGE no caso',i,JSON.stringify(c));
      console.log('  py falas:',b.slice(0,160));console.log('  js falas:',a.slice(0,160));
      if(ao!==bo){console.log('  py opcoes:',bo.slice(0,200));console.log('  js opcoes:',ao.slice(0,200));}}
    erros++;
  }
});
erros+=inteira;
console.log(erros?`${erros} de ${casos.length} casos divergem`:`OK: ${casos.length} casos, Python e JavaScript respondem igual`);
process.exit(erros?1:0);
