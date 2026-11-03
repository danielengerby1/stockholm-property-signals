// Fetch police events (polisen.se open API) for Stockholm County.
// 1. Open https://polisen.se/api/events in a browser.
// 2. Open the developer console (F12 / Cmd+Opt+J), paste this file and press Enter.
// 3. A JSON file downloads. Drop it into the app's Data & sources tab (file type: Polisen events).
// The API only keeps roughly the last 6 months, so run this every month or two to build up history.
// The app removes duplicates by event id, so overlapping downloads are fine.
(async () => {
  const locs = ['Stockholms län','Stockholm','Solna','Sundbyberg','Nacka','Lidingö','Huddinge','Danderyd','Täby','Järfälla','Sollentuna','Botkyrka','Haninge','Tyresö','Värmdö'];
  const months = []; const d = new Date(); for (let i = 0; i < 7; i++) { const x = new Date(d.getFullYear(), d.getMonth() - i, 1); months.push(x.getFullYear() + '-' + String(x.getMonth() + 1).padStart(2, '0')); }
  const all = new Map();
  for (const m of months) for (const l of locs) {
    const j = await fetch('/api/events?locationname=' + encodeURIComponent(l) + '&DateTime=' + m).then(r => r.json()).catch(() => []);
    for (const e of j) all.set(e.id, e); await new Promise(r => setTimeout(r, 250));
  }
  const ev = [...all.values()].sort((a, b) => a.datetime.localeCompare(b.datetime));
  const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([JSON.stringify(ev)], {type: 'application/json'}));
  a.download = 'polisen_events_' + months[0] + '.json'; a.click(); console.log('Done:', ev.length, 'events');
})();
