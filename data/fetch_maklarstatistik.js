// Refresh Svensk Mäklarstatistik data for Stockholm.
// 1. Open https://www.maklarstatistik.se/omrade/riket/stockholms-lan/stockholm/ in a browser.
// 2. Open the developer console (F12 / Cmd+Opt+J), paste this whole file and press Enter.
// 3. Two CSV files download: monthly (last 48 months) and yearly history.
// Drop the monthly file into the app's Data & sources tab (tick "Prices are already 3-month averages").
(async () => {
  const base = 'https://www.maklarstatistik.se/omrade/riket/stockholms-lan/';
  const urls = [...window.chart_obj.child_urls, ...['solna','sundbyberg','nacka','lidingo','huddinge','danderyd','taby','jarfalla','sollentuna','botkyrka','haninge','tyreso','varmdo'].map(s => base + s + '/')];
  const M = {jan:1,feb:2,mar:3,apr:4,maj:5,jun:6,jul:7,aug:8,sep:9,okt:10,nov:11,dec:12};
  const mon = l => { const [a, b] = l.split(' -'); return '20' + b + '-' + String(M[a]).padStart(2, '0'); };
  const monthly = ['month,area,price_per_sqm,n_sales'], yearly = ['year,area,price_per_sqm'];
  for (const u of urls) {
    const d = new DOMParser().parseFromString(await fetch(u).then(r => r.text()), 'text/html');
    const get = n => { const c = d.querySelector(`canvas[data-chart=${n}]`); return c ? {l: JSON.parse(c.dataset.labels || '[]'), s: JSON.parse(c.dataset.series || '[]')[0] || []} : null; };
    const name = d.querySelector('h1')?.textContent.trim(); const p = get('br-48m-prisutveckling'), n = get('br-48m-antal-salda'), y = get('br-arshistorik-prisutveckling');
    if (p) p.l.forEach((l, i) => monthly.push([mon(l), name, Math.round(+p.s[i]), n ? Math.round(+n.s[i]) : ''].join(',')));
    if (y) y.l.forEach((l, i) => { if (y.s[i]) yearly.push([l, name, Math.round(+y.s[i])].join(',')); });
    await new Promise(r => setTimeout(r, 400));
  }
  const dl = (name, text) => { const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([text + '\n'], {type: 'text/csv'})); a.download = name; a.click(); };
  dl('maklarstatistik_monthly_bostadsratter.csv', monthly.join('\n'));
  dl('maklarstatistik_yearly_bostadsratter.csv', yearly.join('\n'));
  console.log(`Done: ${monthly.length - 1} monthly rows, ${yearly.length - 1} yearly rows`);
})();
