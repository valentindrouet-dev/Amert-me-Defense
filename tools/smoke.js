// Test de fumée : node tools/smoke.js [url]
// Lance une partie, enchaîne quelques jours et nuits en accéléré, sauvegarde/recharge, et signale toute erreur JS.
// Prérequis : serveur local (python3 -m http.server 8765) et Playwright.
const {chromium}=require('playwright');
(async()=>{const url=process.argv[2]||'http://localhost:8765/';const b=await chromium.launch();const p=await b.newPage({viewport:{width:1600,height:930}});
  const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
  await p.goto(url);await p.waitForTimeout(1200);await p.click('#bGo');await p.waitForTimeout(300);
  const r=await p.evaluate(()=>{const S=__S(),T=__test;T.setPaused(true);S.res.bois=S.res.pierre=S.res.vivres=3000;S.keep.max=S.keep.hp=1e6;
    for(const [t,i,j] of [['farm',3,-5],['tower',-5,3],['tower',5,0],['kennel',2,5],['armory',-3,6]])T.tryPlace(t,{i,j},true,true);
    for(const t of ['gardien','fusilier','chien','etendard','tambour','arbalet','mystique'])T.addUnit(t);
    const t0=performance.now();for(let d=0;d<6;d++){let g=0;while(S.phase!=='night'&&g++<5000)T.step(.05);while(S.phase==='night'&&g++<12000)T.step(.05);while(S.phase!=='day'&&g++<14000)T.step(.05)}
    T.saveGame('lamuline-smoke');const ok=T.loadGame(JSON.parse(localStorage.getItem('lamuline-smoke')));localStorage.removeItem('lamuline-smoke');
    return{day:S.day,reload:ok,ms:Math.round(performance.now()-t0)}});
  console.log(JSON.stringify(r));console.log(errs.length?'ERREURS :\n'+errs.join('\n'):'Aucune erreur.');await b.close();process.exit(errs.length?1:0)})();
