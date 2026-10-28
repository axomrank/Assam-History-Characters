/* Assam history character sheets. Offline-first, no build step; data comes from data/site.js. */
(() => {
const S = window.SITE, $ = id => document.getElementById(id);
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const url = p => p.split('/').map(encodeURIComponent).join('/');
const eraById = Object.fromEntries(S.eras.map(e => [e.id, e]));
const charById = Object.fromEntries(S.characters.map(c => [c.id, c]));
const sceneById = Object.fromEntries(S.scenes.map(s => [s.id, s]));
const realms = S.realms || [], places = S.places || [], placeById = Object.fromEntries(places.map(p => [p.id, p]));
const chars = [...S.characters].sort((a, b) => a.sort_year - b.sort_year);
for (const c of S.characters) { c.sheets = c.sheets || []; c.scenes = []; c.mainScenes = []; }
for (const s of S.scenes) for (const id of s.chars) { const c = charById[id]; if (c) { c.scenes.push(s.id); if (s.main.includes(id)) c.mainScenes.push(s.id); } }
/* Image availability comes from the build: c.av = [level, full sheets, portraits, main scenes, background scenes]
   level 3 sheet, 2 portrait, 1 scenes only, 0 none */
const lvl = c => (c.av ? c.av[0] : 0);
const withSheets = c => lvl(c) >= 2;
const hasSheet = c => lvl(c) === 3;
const srcOf = idx => (idx || []).map(i => S.src[i]);
const coverRank = k => ({ turnaround: 0, sheet: 1, face: 2, portrait: 3 }[k] ?? 4);
/* One colour per dynasty or house, used everywhere a person appears. Colours live in app.css (.h-<key>). */
const HOUSES = [
  ['varman', 'Varman dynasty', ['Barman dynasty']],
  ['salastambha', 'Mlechchha (Salastambha) dynasty', ['Salastambha dynasty']],
  ['pala', 'Pala dynasty of Kamarupa and its successors', ['Pala dynasty', 'Kamarupa after the Palas']],
  ['kamata', 'Kamata and Khen', ['Kamata and Khen kingdoms']],
  ['bhuyan', 'Baro-Bhuyans', ['Baro-Bhuyans']],
  ['koch', 'Koch, all branches', ['Koch kingdom (undivided)', 'Koch Hajo kings', 'Darrang kings', 'Beltola kings', 'Bijni kings', 'Khaspur kings']],
  ['ahom', 'Ahom', ['Ahom kings', 'Ahom queens and royal family', 'Ahom officers and generals', 'Moamoria rebels']],
  ['chutia', 'Chutia', ['Chutia kingdom']],
  ['dimasa', 'Dimasa (Kachari)', ['Dimasa (Kachari) kingdom']],
  ['hill', 'Jaintia and Manipur', ['Jaintia and Manipur']],
  ['foreign', 'Outside powers: Bengal, Delhi, Mughal, Burmese, British', ['Pala Empire of Bengal', 'Bengal and Delhi rulers', 'Mughal and Bengal commanders', 'Burmese and British figures', 'Contemporaries and visitors']],
  ['culture', 'Saints, poets and legends', ['Poets and writers', 'Saints of the bhakti movement', 'Legends']],
  ['colonial', 'Colonial Assam', []],
  ['modern', 'Assam since independence', []],
];
const houseOfGroup = Object.fromEntries(HOUSES.flatMap(([k, , gs]) => gs.map(g => [g, k])));
const house = c => houseOfGroup[c.group || c.dynasty] || (c.era === 'colonial' || c.era === 'modern' ? c.era : '');
const houseLabel = Object.fromEntries(HOUSES.map(([k, l]) => [k, l]));
const hc = k => k ? `hh h-${k}` : '';
const houseKey = () => `<ul class="hkey" aria-label="Dynasty colours">${HOUSES.map(([k, l]) => `<li class="${hc(k)}"><i class="sw"></i>${esc(l)}</li>`).join('')}</ul>`;

/* ---------- language ---------- */
const STR = {
  en: {
    brand:'Assam history sheets', home:'Home', characters:'Characters', kings:'Kings', timeline:'Timeline', scenes:'Scenes', coverage:'Coverage', about:'About',
    h1:'The people of Assam’s history', h1sub:'Character sheets from Pushyavarman to Tarun Gogoi',
    lede:'Use them as reference images when you make AI art, video and books, so the same person looks the same in every scene.',
    span:(e, n)=>`${e} periods, ${n} people`,
    browse:'Browse characters', seeScenes:'See historical scenes',
    haveSheets:'characters have a portrait or sheet', ofTotal:'of', scenesOnlyMore:n=>`${n} more appear only in scenes`, inScenes:n=>`In ${n} ${n === 1 ? 'scene' : 'scenes'}`, backgroundScenes:n=>`Background in ${n} ${n === 1 ? 'scene' : 'scenes'}`, noImages:'No images yet', scenesLegend:'In scenes only', onlySheet:'Sheet', onlyPortrait:'Portrait', onlyScenes:'In scenes', onlyNone:'None', imagesCol:'Images', mainScenesH:n=>`Scenes where ${n} is the main figure`, alsoIn:'Also appears in', noPortraitBody:'There is no sheet or portrait yet. Use the scenes below as reference.',
    withSheet:'Has a sheet', portraitsOnly:'Portraits only', noSheet:'Sheet needed', hasLegend:'Full sheet', partLegend:'Portraits only', needLegend:'No images yet',
    recent:'Recently added sheets', recentEmpty:'No sheets added yet', recentEmptyBody:'The timeline starts with Pushyavarman. Add his sheet first and it will appear here.',
    sceneTeaser:'Historical scenes', allScenes:'All scenes',
    search:'Search by name, role or era', allEras:'All eras', all:'All', onlyWith:'Has images', onlyNeed:'No images',
    results:n=>`${n} ${n===1?'character':'characters'}`, none:'No characters match. Clear the search or choose another era.',
    back:'All characters', prev:'Earlier', next:'Later', dates:'Dates', era:'Era', role:'Role',
    approx:'Dates approximate', approxNote:'This entry is from the starting roster. Dates and descriptions are approximate and need checking against sources.',
    inEra:'in', allGroups:'All groups', conf:'Confidence', confHigh:'High', confMedium:'Medium', confLow:'Low', sources:'Sources', alsoKnown:'Also known as',
    confHighNote:'Several sources agree on the main facts.', confMediumNote:'One good source, or dates that vary between sources.', confLowNote:'A single source, a legend, or disputed. Check before relying on it.', showAll:'Show all eras', approxCsv:'Reign dates follow the source timeline, which uses evenly spaced periods for the early dynasties. Treat them as approximate.',
    dynasty:'Dynasty', consort:'Consort', marital:'Marital status', events:'Events and notes', source:'Source', noEvents:'The source timeline lists no events for this ruler.',
    sheetsH:'Character sheets', noSheetTitle:'No sheet yet', noSheetBody:'This character’s sheet has not been added.',
    download:'Download', zoom:'Open large', refNotes:'Reference notes', notesEmpty:'No reference notes have been written for this character yet.',
    appearance:'Appearance', costume:'Costume', props:'Props and weapons', avoid:'Avoid',
    copyBrief:'Copy reference brief', copied:'Reference brief copied', copyFail:'Could not copy. Select the text and copy it yourself.',
    scenesWith:'Scenes with this character', scenesWithNone:'No catalogued scene features this character yet.',
    about1:'Interpretation, not evidence',
    scenesTitle:'Historical scenes', scenesLede:'Illustrated scenes from the Ahom chronology and the Assamese AI gallery, linked to the characters in them. Researched scenes that are not painted yet are shown as placeholders.',
    allCollections:'All collections', allChars:'All characters', sceneCount:n=>`${n} scenes`, allStates:'Painted and not yet painted', painted:'Painted', planned:'Not painted yet', plannedTag:'Not painted yet', plannedBody:'This scene is researched but not painted yet. Use the description and sources as the brief.', plannedCount:n=>`, ${n} not painted yet`, confWord:'Confidence', sourcesWord:'Sources',
    close:'Close', fit:'Fit', openChar:'Character page',
    foot:'Illustrations are interpretations, not photographs or evidence of how anyone looked. Dates and names come from the project catalogue and starting roster and are not independently verified.',
    covTitle:'Coverage', covLede:'Which characters still need a sheet. Use the folder name when you add images.',
    folder:'Folder name', status:'Sheets', copyMissing:'Copy missing ids', missingCopied:'Missing ids copied',
    kinds:{portrait:'Portrait',sheet:'Sheet',turnaround:'Turnaround',face:'Face',costume:'Costume',props:'Props',palette:'Palette',pose:'Pose',other:'Other'},
    searchLabel:'Search', searchPh:'Search a character, scene or place',
    srHint:'Type a name to see that character’s sheet and the scenes they are in. Type an event, a place or a date to see matching scenes, each with the sheets of the people in it.',
    srNone:'Nothing matches. Try a shorter name or another spelling.', srPick:'Several characters match. Choose one to see their sheet and scenes.',
    srCharacter:'Character', srScenesWith:n=>`Scenes with ${n}`, srScenes:'Scenes', srPeople:'People mentioned', srOpen:'Open full page', srSheetCount:n=>`${n} ${n === 1 ? 'sheet' : 'sheets'}`,
    srExtent:'Extent through time', srBoundaryOf:'Marks the boundary of', srBoundsAt:'Bounded by', srPlace:'Place', srPlaceScenes:n=>`Scenes at ${n}`, srAlso:'Also called', srToday:'Today', srIdent:'Identification', srPlacePick:'Several places match. Choose one.', srPlaceCount:n=>`${n} ${n === 1 ? 'place' : 'places'}`, srTimeline:'On the timeline', srMapPoint:'Map point', srApprox:'approximate', srOpenMap:'Open map', srNoSceneHere:'No catalogued scene is set here yet.', placesWord:'Places', todayWord:'today',
    srSceneCount:n=>`${n} ${n === 1 ? 'scene' : 'scenes'}`, srCharCount:n=>`${n} ${n === 1 ? 'character' : 'characters'}`, srNoSheet:'No sheet yet', srMore:n=>`+${n}`,
  },
  as: {
    brand:'অসম ইতিহাস চৰিত্ৰ-পত্ৰ', home:'ঘৰ', characters:'চৰিত্ৰ', kings:'ৰজাসকল', timeline:'সময়ৰেখা', scenes:'দৃশ্য', coverage:'অগ্ৰগতি', about:'আমাৰ বিষয়ে',
    h1:'অসমৰ ইতিহাসৰ মানুহ', h1sub:'পুষ্যবৰ্মাৰ পৰা তৰুণ গগৈলৈ চৰিত্ৰ-পত্ৰ', span:(e, n)=>`${e}টা যুগ, ${n} জন মানুহ`,
    lede:'অসমৰ ইতিহাসৰ মানুহবোৰৰ চৰিত্ৰ-পত্ৰ। এআই চিত্ৰ, ভিডিঅ’ আৰু কিতাপ বনাওঁতে ৰেফাৰেন্স হিচাপে ব্যৱহাৰ কৰক।',
    browse:'চৰিত্ৰবোৰ চাওক', seeScenes:'ঐতিহাসিক দৃশ্য চাওক',
    haveSheets:'জন চৰিত্ৰৰ চিত্ৰ আছে', ofTotal:'ৰ ভিতৰত',
    withSheet:'পত্ৰ আছে', noSheet:'পত্ৰ লাগে', hasLegend:'পত্ৰ আছে', needLegend:'পত্ৰ যোগ কৰা হোৱা নাই',
    search:'নাম, ভূমিকা বা যুগ অনুসৰি বিচাৰক', allEras:'সকলো যুগ', all:'সকলো',
    results:n=>`${n} জন চৰিত্ৰ`, back:'সকলো চৰিত্ৰ', download:'ডাউনলোড', close:'বন্ধ কৰক', fit:'খাপ খুৱাওক',
    sceneTeaser:'ঐতিহাসিক দৃশ্য', allScenes:'সকলো দৃশ্য', sceneCount:n=>`${n}টা দৃশ্য`, painted:'অঁকা', planned:'এতিয়াও অঁকা হোৱা নাই', plannedTag:'এতিয়াও অঁকা হোৱা নাই', plannedCount:n=>`, ${n}টা এতিয়াও অঁকা হোৱা নাই`,
    scenesTitle:'ঐতিহাসিক দৃশ্য', refNotes:'ৰেফাৰেন্স টোকা', copyBrief:'ৰেফাৰেন্স ব্ৰিফ কপি কৰক',
    searchLabel:'বিচাৰক', searchPh:'চৰিত্ৰ, দৃশ্য বা ঠাই বিচাৰক', srHint:'নাম লিখিলে সেই চৰিত্ৰৰ পত্ৰ আৰু তেওঁ থকা দৃশ্য দেখুৱাব। ঘটনা বা ঠাইৰ নাম লিখিলে মিল থকা দৃশ্য দেখুৱাব।',
    srNone:'একো পোৱা নগ’ল। চুটি নাম বা আন বানান চেষ্টা কৰক।', srPick:'কেইবাজনো চৰিত্ৰ মিলিছে। এজনক বাছক।', srCharacter:'চৰিত্ৰ', srScenesWith:n=>`${n} থকা দৃশ্য`, srScenes:'দৃশ্য', srPeople:'উল্লেখ থকা মানুহ', srOpen:'সম্পূৰ্ণ পৃষ্ঠা খোলক',
    srExtent:'সময়ৰ লগে লগে সীমা', srBoundaryOf:'ইয়াৰ সীমা চিহ্নিত কৰে', srBoundsAt:'সীমা', srPlace:'ঠাই', srPlaceScenes:n=>`${n}ৰ দৃশ্য`, srAlso:'আন নাম', srToday:'এতিয়া', srIdent:'চিনাক্তকৰণ', srPlacePick:'কেইবাটাও ঠাই মিলিছে। এটা বাছক।', srPlaceCount:n=>`${n}টা ঠাই`, srTimeline:'সময়ৰেখাত', srMapPoint:'মানচিত্ৰৰ বিন্দু', srApprox:'আনুমানিক', srOpenMap:'মানচিত্ৰ চাওক', srNoSceneHere:'ইয়াত এতিয়াও কোনো দৃশ্য নাই।', placesWord:'ঠাই', todayWord:'এতিয়া',
    srSheetCount:n=>`${n}খন পত্ৰ`, srSceneCount:n=>`${n}টা দৃশ্য`, srCharCount:n=>`${n} জন চৰিত্ৰ`, srNoSheet:'এতিয়াও পত্ৰ নাই', srMore:n=>`+${n}`,
  },
};
let lang = 'en';
try { lang = localStorage.getItem('lang') === 'as' ? 'as' : 'en'; } catch {}
const t = (k, ...a) => { const v = STR[lang][k] ?? STR.en[k]; return typeof v === 'function' ? v(...a) : v; };
const nm = c => (lang === 'as' && c.name_as) ? c.name_as : c.name;
const nm2 = c => c.name_as ? (lang === 'as' ? c.name : c.name_as) : '';
const eraName = e => (lang === 'as' && e.name_as) ? e.name_as : e.name;
const kindName = k => (t('kinds') || {})[k] || STR.en.kinds[k] || k;

/* ---------- helpers ---------- */
function toast(msg) {
  const el = $('toast'); el.textContent = msg; el.classList.add('show');
  clearTimeout(toast.t); toast.t = setTimeout(() => el.classList.remove('show'), 2400);
}
async function copy(text, ok, fail) {
  try { await navigator.clipboard.writeText(text); toast(ok); }
  catch {
    const ta = document.createElement('textarea'); ta.value = text; document.body.append(ta); ta.select();
    try { document.execCommand('copy'); toast(ok); } catch { toast(fail); } ta.remove();
  }
}
function parseHash() {
  const raw = location.hash.replace(/^#/, '') || '/';
  const [path, qs = ''] = raw.split('?');
  return { parts: path.split('/').filter(Boolean).map(decodeURIComponent), q: new URLSearchParams(qs) };
}
function setQuery(path, params) {
  const q = new URLSearchParams(); for (const [k, v] of Object.entries(params)) if (v) q.set(k, v);
  history.replaceState(null, '', '#' + path + (q.toString() ? '?' + q : ''));
}
function availTag(c) {
  const [l, full, port, m, a] = c.av || [0, 0, 0, 0, 0];
  if (l === 3) return [t('withSheet') + (full + port > 1 ? ` (${full + port})` : ''), 'ok'];
  if (l === 2) return [t('portraitsOnly') + (port > 1 ? ` (${port})` : ''), 'ok'];
  if (l === 1) return [m ? t('inScenes', m) : t('backgroundScenes', a), 'scene'];
  return [t('noImages'), ''];
}
const availText = c => { const [, f, p, m, a] = c.av || [0, 0, 0, 0, 0]; return [f ? `${f} sheet${f > 1 ? 's' : ''}` : '', p ? `${p} portrait${p > 1 ? 's' : ''}` : '', m || a ? `${m} main, ${a} background scenes` : ''].filter(Boolean).join(', ') || 'none'; };
const dotCls = c => ['', 'scene', 'part', 'has'][lvl(c)];
const dotTip = c => `${nm(c)}, ${availTag(c)[0]}`;

/* ---------- components ---------- */
function charCard(c) {
  const s = [...c.sheets].sort((a, b) => coverRank(a.kind) - coverRank(b.kind))[0];
  const sc = !s ? c.mainScenes.map(x => sceneById[x]).find(x => !x.planned) || null : null;
  const [tag, tone] = availTag(c);
  return `<li><a class="card ${hc(house(c))}" href="#/c/${esc(c.id)}">
    <div class="media ${sc ? 'photo' : ''}">${s ? `<img src="${url(s.thumb)}" alt="Character sheet of ${esc(c.name)}" loading="lazy" decoding="async">` : sc ? `<img src="${url(sc.thumbnail)}" alt="Scene: ${esc(sc.event)}" loading="lazy" decoding="async">` : `<span class="ph" aria-hidden="true">${esc([...nm(c)][0])}</span>`}</div>
    <div class="body"><h3>${esc(nm(c))}</h3>${nm2(c) ? `<span class="as">${esc(nm2(c))}</span>` : ''}
    <span class="meta">${esc(c.label)}</span>${c.ahom_no ? `<span class="meta">Ahom king no. ${c.ahom_no.join(' and ')}${c.tai_name && c.tai_name !== c.name ? `, Tai name ${esc(c.tai_name)}` : ''}</span>` : c.koch_no ? `<span class="meta">${esc(c.koch_branch)} no. ${c.koch_no}</span>` : ''}
    <span class="tag ${tone}">${esc(tag)}</span></div></a></li>`;
}
function sceneBtn(s) {
  const sc = s.main[0] || s.chars[0], hk = sc && charById[sc] ? house(charById[sc]) : '';
  const pic = s.planned ? `<span class="ph-scene" aria-hidden="true"><em>${esc(t('plannedTag'))}</em></span>` : `<img src="${url(s.thumbnail)}" alt="${esc(s.event)}" loading="lazy" decoding="async">`;
  return `<li><button type="button" class="scene ${hc(hk)} ${s.planned ? 'planned' : ''}" data-scene="${esc(s.id)}">${pic}<span><b>${esc(s.event)}</b><small>${esc(s.date_label)}</small></span></button></li>`;
}

/* ---------- views ---------- */
function viewHome() {
  const total = chars.length, have = chars.filter(withSheets).length, sceneOnly = chars.filter(c => lvl(c) === 1).length, nFull = chars.filter(hasSheet).length;
  const ribbon = S.eras.map(e => {
    const cs = chars.filter(c => c.era === e.id), h = cs.filter(withSheets).length;
    return `<li class="seg"><h3><a href="#/characters?era=${e.id}">${esc(eraName(e))}</a></h3><span class="yrs">${esc(e.label)}</span>
      <ul class="dots" aria-label="${esc(eraName(e))}: ${h} of ${cs.length} with a sheet">${cs.map(c => `<li><a class="dot ${dotCls(c)} ${hc(house(c))}" href="#/c/${esc(c.id)}" data-tip="${esc(dotTip(c))}" aria-label="${esc(dotTip(c))}"></a></li>`).join('')}</ul></li>`;
  }).join('');
  const recent = chars.filter(withSheets).sort((a, b) => b.sheets.at(-1).added.localeCompare(a.sheets.at(-1).added)).slice(0, 8);
  const painted = S.scenes.filter(s => !s.planned), step = Math.max(1, Math.floor(painted.length / 8)), teaser = painted.filter((_, i) => i % step === 0).slice(0, 8);
  return `<section class="folio hero"><h1>${esc(t('h1'))}<span>${esc(t('h1sub'))}</span></h1><p class="lede">${esc(t('lede'))}</p>
    <div class="cta"><a class="btn primary" href="#/characters">${esc(t('browse'))}</a><a class="btn" href="#/scenes">${esc(t('seeScenes'))}</a></div>
    <p class="span-yrs" aria-label="c. 350 to 2020"><b>c. 350</b><i></i><span>${esc(t('span', S.eras.length, total))}</span><i></i><b>2020</b></p></section>
    <div class="progress"><strong>${have} ${esc(t('ofTotal'))} ${total}</strong><span>${esc(t('haveSheets'))}, ${esc(t('scenesOnlyMore', sceneOnly))}</span><div class="bar" role="img" aria-label="${have} of ${total}"><i style="width:${total ? 100 * have / total : 0}%"></i></div></div>
    <ol class="ribbon" style="--n:${S.eras.length}">${ribbon}</ol>
    <div class="legend"><span><span class="dot has"></span>${esc(t('hasLegend'))} (${nFull})</span><span><span class="dot part"></span>${esc(t('partLegend'))} (${have - nFull})</span><span><span class="dot scene"></span>${esc(t('scenesLegend'))} (${sceneOnly})</span><span><span class="dot"></span>${esc(t('needLegend'))} (${total - have - sceneOnly})</span></div>
    ${houseKey()}
    <section class="section"><div class="row"><h2>${esc(t('recent'))}</h2></div>
      ${recent.length ? `<ul class="grid">${recent.map(charCard).join('')}</ul>` : `<div class="empty"><strong>${esc(t('recentEmpty'))}</strong>${esc(t('recentEmptyBody'))}</div>`}</section>
    <section class="section"><div class="row"><h2>${esc(t('sceneTeaser'))}</h2><a href="#/scenes">${esc(t('allScenes'))}</a></div><ul class="grid">${teaser.map(sceneBtn).join('')}</ul></section>`;
}

function viewCharacters(q) {
  const st = { q: q.get('q') || '', era: q.get('era') || '', grp: q.get('grp') || '', av: q.get('av') || '' };
  const groups = [...new Set(chars.map(c => c.group || c.dynasty).filter(Boolean))].sort((a, b) => a.localeCompare(b));
  const html = `<div class="page-head"><h1>${esc(t('characters'))}</h1></div>${houseKey()}
    <div class="filters" role="search">
      <input type="search" id="fq" placeholder="${esc(t('search'))}" aria-label="${esc(t('search'))}" value="${esc(st.q)}">
      <select id="fe" aria-label="${esc(t('era') || 'Era')}"><option value="">${esc(t('allEras'))}</option>${S.eras.map(e => `<option value="${e.id}" ${st.era === e.id ? 'selected' : ''}>${esc(eraName(e))}</option>`).join('')}</select>
      <select id="fg" aria-label="${esc(t('allGroups'))}"><option value="">${esc(t('allGroups'))}</option>${groups.map(g => `<option ${st.grp === g ? 'selected' : ''}>${esc(g)}</option>`).join('')}</select>
      <span class="seg-btns" role="group" aria-label="Sheet status">${[['', t('all')], ['3', t('onlySheet')], ['2', t('onlyPortrait')], ['1', t('onlyScenes')], ['0', t('onlyNone')]].map(([v, l]) => `<button type="button" data-av="${v}" aria-pressed="${st.av === v}">${esc(l)}</button>`).join('')}</span>
    </div><p class="count" id="fcount" aria-live="polite"></p><div id="flist"></div>`;
  setTimeout(() => {
    if (!$('fq')) return;
    const draw = () => {
      const needle = st.q.trim().toLowerCase();
      const list = chars.filter(c => (!st.era || c.era === st.era) && (!st.grp || (c.group || c.dynasty) === st.grp) && (!st.av || String(lvl(c)) === st.av) &&
        (!needle || [c.name, c.name_as, c.alt_names, c.role, c.label, c.summary, c.group, c.dynasty, c.consort, c.notes, eraById[c.era].name].join(' ').toLowerCase().includes(needle)));
      $('fcount').innerHTML = esc(t('results', list.length)) + (st.era ? ` ${esc(t('inEra'))} <b>${esc(eraName(eraById[st.era]))}</b>. <a href="#/characters" id="showAll">${esc(t('showAll'))}</a>` : '');
      $('flist').innerHTML = list.length ? S.eras.map(e => {
        const cs = list.filter(c => c.era === e.id); if (!cs.length) return '';
        const h = cs.filter(withSheets).length;
        return `<section class="era-block"><div class="weave" aria-hidden="true"></div><header><h2>${esc(eraName(e))}</h2><span class="yrs">${esc(e.label)}, ${h} / ${cs.length} ${esc(t('withSheet').toLowerCase())}</span></header>${e.blurb ? `<p class="blurb">${esc(e.blurb)}</p>` : ''}${dynGroups(cs, e)}</section>`;
      }).join('') : `<div class="empty">${esc(t('none'))}</div>`;
      document.querySelectorAll('[data-av]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.av === st.av)));
      setQuery('/characters', st);
    };
    $('fq').oninput = e => { st.q = e.target.value; draw(); };
    $('fe').onchange = e => { st.era = e.target.value; draw(); };
    $('fg').onchange = e => { st.grp = e.target.value; draw(); };
    document.querySelectorAll('[data-av]').forEach(b => b.onclick = () => { st.av = b.dataset.av; draw(); });
    draw();
  });
  return html;
}

const cap = x => (x || 'medium').charAt(0).toUpperCase() + (x || 'medium').slice(1);
function srcList(c) {
  const list = c.src && c.src.length ? srcOf(c.src) : c.source ? [c.source] : [];
  if (!list.length) return '';
  const short = u => decodeURIComponent(u.replace(/^https?:\/\/(en\.)?wikipedia\.org\/wiki\//, 'Wikipedia: ')).replace(/_/g, ' ').slice(0, 48);
  return `<p class="srcline">${esc(t('sources'))}: ${list.map(u => /^https?:/.test(u) ? `<a href="${esc(u)}" target="_blank" rel="noopener">${esc(short(u))}</a>` : esc(u)).join(', ')}</p>`;
}
function dynGroups(cs, e) {
  const order = (e && e.groups) || [];
  const names = [...new Set(cs.map(c => c.group || c.dynasty).filter(Boolean))].sort((a, b) => (order.indexOf(a) + 1 || 99) - (order.indexOf(b) + 1 || 99));
  if (names.length < 2) return `<ul class="grid">${cs.map(charCard).join('')}</ul>`;
  return names.map(n => {
    const g = cs.filter(c => (c.group || c.dynasty) === n), ys = g.flatMap(c => [c.reign_start, c.reign_end]).filter(Number.isFinite);
    return `<div class="dyn"><h3 class="${hc(houseOfGroup[n])}"><i class="sw"></i>${esc(n)}${ys.length ? ` <span class="yrs">${Math.min(...ys)}\u2013${Math.max(...ys)} CE</span>` : ''}</h3><ul class="grid">${g.map(charCard).join('')}</ul></div>`;
  }).join('') + (() => { const o = cs.filter(c => !(c.group || c.dynasty)); return o.length ? `<div class="dyn"><ul class="grid">${o.map(charCard).join('')}</ul></div>` : ''; })();
}

function briefText(c) {
  const b = c.brief || {}, e = eraById[c.era];
  const lines = [`${c.name}${c.name_as ? ' (' + c.name_as + ')' : ''}, ${c.role}. ${c.label}. Era: ${e.name}.`, c.summary];
  if (c.consort) lines.push(`Consort: ${c.consort}.`);
  for (const [k, l] of [['appearance', 'Appearance'], ['costume', 'Costume'], ['props', 'Props and weapons'], ['avoid', 'Avoid']]) if (b[k]) lines.push(`${l}: ${b[k]}`);
  lines.push('Use the attached character sheet as the visual reference. This is an illustrated interpretation; do not present it as documentary evidence of how the person looked.');
  return lines.join('\n');
}

let sheetIdx = 0;
function viewCharacter(id, q) {
  const c = charById[id];
  if (!c) return `<div class="page-head"><h1>Character not found</h1><p><a href="#/characters">Back to all characters</a></p></div>`;
  sheetIdx = Math.min(Math.max(0, Number(q.get('s')) || 0), Math.max(0, c.sheets.length - 1));
  const sib = chars.filter(x => x.era === c.era && (x.group || x.dynasty) === (c.group || c.dynasty)), i = sib.indexOf(c), prev = sib[i - 1], next = sib[i + 1], e = eraById[c.era];
  const b = c.brief || {}, notes = [['appearance', t('appearance')], ['costume', t('costume')], ['props', t('props')], ['avoid', t('avoid')]].filter(([k]) => b[k]);
  const mainSc = c.mainScenes.map(x => sceneById[x]), otherSc = c.scenes.filter(x => !c.mainScenes.includes(x)).map(x => sceneById[x]);
  return `<nav class="crumb" aria-label="Breadcrumb"><a href="#/characters">${esc(t('back'))}</a>
      <span>${prev ? `<a href="#/c/${prev.id}">‹ ${esc(nm(prev))}</a>` : ''}${prev && next ? '&nbsp;&nbsp;&nbsp;' : ''}${next ? `<a href="#/c/${next.id}">${esc(nm(next))} ›</a>` : ''}</span></nav>
    <header class="chead ${hc(house(c))}"><h1>${esc(nm(c))}</h1>${nm2(c) ? `<div class="as">${esc(nm2(c))}</div>` : ''}
      <div class="facts"><span><b>${esc(c.label)}</b></span><span>${esc(c.role)}</span><span><a href="#/characters?era=${c.era}">${esc(eraName(e))}</a></span>${house(c) ? `<span class="hchip"><i class="sw"></i>${esc(c.group || c.dynasty || houseLabel[house(c)])}</span>` : ''}
      ${c.consort || c.marital ? `<span>${esc(t(c.consort ? 'consort' : 'marital'))}: ${esc(c.consort || c.marital)}</span>` : ''}
      ${c.status === 'researched' ? `<span class="badge ${c.confidence === 'high' ? '' : 'warn'}" title="${esc(t('conf' + cap(c.confidence) + 'Note'))}">${esc(t('conf'))}: ${esc(t('conf' + cap(c.confidence)))}</span>` : c.status === 'seed' || c.approx ? `<span class="badge warn" title="${esc(t(c.status === 'csv' ? 'approxCsv' : 'approxNote'))}">${esc(t('approx'))}</span>` : ''}</div>${(c.tai_name || c.hindu_name || c.nicknames || c.relation) ? `<dl class="names">${c.ahom_no ? `<div><dt>Ahom king</dt><dd>No. ${c.ahom_no.join(' and ')} of 41 reigns</dd></div>` : ''}${c.koch_no ? `<div><dt>${esc(c.koch_branch)}</dt><dd>No. ${c.koch_no}</dd></div>` : ''}${c.tai_name ? `<div><dt>Tai name</dt><dd>${esc(c.tai_name)}</dd></div>` : ''}${c.hindu_name ? `<div><dt>Hindu name</dt><dd>${esc(c.hindu_name)}</dd></div>` : ''}${c.nicknames ? `<div><dt>Also called</dt><dd>${esc(c.nicknames)}</dd></div>` : ''}${c.relation ? `<div><dt>Relation</dt><dd>${esc(c.relation)}</dd></div>` : ''}${c.fate ? `<div><dt>How it ended</dt><dd>${esc(c.fate)}</dd></div>` : ''}</dl>` : ''}${c.alt_names ? `<p class="alt">${esc(t('alsoKnown'))}: ${esc(c.alt_names)}</p>` : ''}</header>
    <div class="stage"><div>
      <div class="sheetview ${hc(house(c))}" id="sheetview">${sheetViewHTML(c)}</div>
    </div>
    <aside class="side"><section><p>${esc(c.summary)}</p>${c.status === 'csv' || c.status === 'researched' ? `<h2>${esc(t('events'))}</h2><p>${c.notes ? esc(c.notes) : `<span class="none">${esc(t('noEvents'))}</span>`}</p>${srcList(c)}` : ''}<h2>${esc(t('refNotes'))}</h2>
      ${notes.length ? `<dl class="notes">${notes.map(([k, l]) => `<dt>${esc(l)}</dt><dd>${esc(b[k])}</dd>`).join('')}</dl>` : `<p class="notes"><span class="none">${esc(t('notesEmpty'))}</span></p>`}
      <p><button type="button" class="primary" id="copyBrief">${esc(t('copyBrief'))}</button></p></section></aside></div>
    ${mainSc.length ? `<section class="section"><div class="row"><h2>${esc(t('mainScenesH', nm(c)))}</h2></div><ul class="grid">${mainSc.map(sceneBtn).join('')}</ul></section>` : ''}
    ${otherSc.length ? `<section class="section"><div class="row"><h2>${esc(t('alsoIn'))}</h2></div><ul class="grid">${otherSc.map(sceneBtn).join('')}</ul></section>` : ''}
    ${!mainSc.length && !otherSc.length ? `<section class="section"><div class="empty">${esc(t('scenesWithNone'))}</div></section>` : ''}`;
}
function sheetViewHTML(c) {
  if (!c.sheets.length) return `<div class="sheetmain none"><div><strong style="font-family:var(--serif);font-size:1.3rem;color:var(--text)">${esc(t('noSheetTitle'))}</strong><br>${esc(c.mainScenes.length ? t('noPortraitBody') : t('noSheetBody'))}</div></div>`;
  const s = c.sheets[sheetIdx];
  return `<button type="button" class="sheetmain" id="sheetOpen" aria-label="${esc(t('zoom'))}"><img src="${url(s.file)}" alt="${esc(kindName(s.kind))} character sheet of ${esc(c.name)}" width="${s.width}" height="${s.height}"></button>
    <div class="sheetbar"><span>${esc(kindName(s.kind))}${s.caption ? ', ' + esc(s.caption) : ''}</span><span><a class="btn" href="${url(s.file)}" download>${esc(t('download'))}</a> <button type="button" id="sheetOpen2">${esc(t('zoom'))}</button></span></div>
    ${c.sheets.length > 1 ? `<div class="thumbs">${c.sheets.map((x, n) => `<button type="button" data-sheet="${n}" aria-label="${esc(kindName(x.kind))} ${n + 1}" ${n === sheetIdx ? 'aria-current="true"' : ''}><img src="${url(x.thumb)}" alt=""></button>`).join('')}</div>` : ''}`;
}

function viewScenes(q) {
  const st = { q: q.get('q') || '', col: q.get('col') || '', c: q.get('c') || '', st: q.get('st') || '' };
  const html = `<div class="page-head"><h1>${esc(t('scenesTitle'))}</h1><p>${esc(t('scenesLede'))}</p></div>
    <div class="filters" role="search"><input type="search" id="sq" placeholder="${esc(t('search'))}" aria-label="${esc(t('search'))}" value="${esc(st.q)}">
    <select id="sc" aria-label="Collection"><option value="">${esc(t('allCollections'))}</option>${[...new Set(S.scenes.map(s => s.collection))].map(v => `<option ${st.col === v ? 'selected' : ''}>${esc(v)}</option>`).join('')}</select>
    <select id="sp" aria-label="Character"><option value="">${esc(t('allChars'))}</option>${chars.filter(c => c.scenes.length).map(c => `<option value="${c.id}" ${st.c === c.id ? 'selected' : ''}>${esc(nm(c))} (${c.scenes.length})</option>`).join('')}</select>
    <select id="sst" aria-label="Painted"><option value="">${esc(t('allStates'))}</option>${[['painted', t('painted')], ['planned', t('planned')]].map(([v, l]) => `<option value="${v}" ${st.st === v ? 'selected' : ''}>${esc(l)}</option>`).join('')}</select></div>
    <p class="count" id="scount" aria-live="polite"></p><ul class="grid" id="sgrid"></ul>`;
  setTimeout(() => {
    if (!$('sq')) return;
    const draw = () => {
      const n = st.q.trim().toLowerCase();
      const list = S.scenes.filter(s => (!st.col || s.collection === st.col) && (!st.c || s.chars.includes(st.c)) && (!st.st || (st.st === 'planned') === !!s.planned) && (!n || (s.event + ' ' + s.description + ' ' + s.date_label).toLowerCase().includes(n)));
      const np = list.filter(s => s.planned).length; $('scount').textContent = t('sceneCount', list.length) + (np && np < list.length ? t('plannedCount', np) : '');
      $('sgrid').innerHTML = list.map(sceneBtn).join('');
      window.__sceneList = list; setQuery('/scenes', st);
    };
    $('sq').oninput = e => { st.q = e.target.value; draw(); };
    $('sc').onchange = e => { st.col = e.target.value; draw(); };
    $('sp').onchange = e => { st.c = e.target.value; draw(); };
    $('sst').onchange = e => { st.st = e.target.value; draw(); };
    draw();
  });
  return html;
}

function viewCoverage() {
  const missing = chars.filter(c => !withSheets(c));
  const rows = S.eras.map(e => `<tr><th colspan="5" scope="colgroup">${esc(eraName(e))} <span class="badge">${esc(e.label)}</span></th></tr>` +
    chars.filter(c => c.era === e.id).map(c => `<tr><td class="${hc(house(c))}"><i class="sw"></i><a href="#/c/${c.id}">${esc(c.name)}</a></td><td><code>${esc(c.id)}</code></td><td>${lvl(c) >= 2 ? esc(availText(c)) : `<span style="color:${lvl(c) ? 'var(--river)' : 'var(--warn)'}">${esc(availText(c))}</span>`}</td><td>${esc(c.label)}</td><td>${esc(c.confidence || '')}</td></tr>`).join('')).join('');
  return `<div class="page-head"><h1>${esc(t('covTitle'))}</h1><p>${esc(t('covLede'))} ${chars.length - missing.length} of ${chars.length} characters have a portrait or sheet, and ${chars.filter(c => lvl(c) === 1).length} more appear only in scenes. The Images column reads: sheets, portraits, then scenes where the person is the main figure and scenes where they only appear.</p></div>
    <p><button type="button" id="copyMissing">${esc(t('copyMissing'))}</button></p>
    <div style="overflow-x:auto"><table class="cov"><thead><tr><th>${esc(t('characters'))}</th><th>${esc(t('folder'))}</th><th>${esc(t('imagesCol'))}</th><th>Dates</th><th>${esc(t('conf'))}</th></tr></thead><tbody>${rows}</tbody></table></div>`;
}

function viewAbout() {
  return `<div class="page-head"><h1>${esc(t('about'))}</h1></div><div class="prose">
    <p>This library collects character sheets for the people of Assam’s history, from the Varman king Pushyavarman in the fourth century to Tarun Gogoi, Chief Minister until 2016. Anyone making AI images, video, comics or books about Assam can use a sheet as a visual reference so the same person looks the same across scenes.</p>
    <h2>Using a sheet</h2><ol><li>Find a character and open their page.</li><li>Download the sheet and attach it as the reference image in your generator.</li><li>Copy the reference brief and paste it into your prompt.</li><li>Check dress, weapons and buildings against the period before you publish.</li></ol>
    <h2>${esc(t('about1'))}</h2><p>Sheets are illustrations. Nobody alive has seen most of these people, and for early figures nothing records how they looked. Most entries before 1826 were researched from published references (mainly Wikipedia articles on the Ahom, Koch, Kamata, Chutia and Dimasa kingdoms and on individual rulers), each with its sources and a confidence level. Confidence is High when several sources agree, Medium for one good source or dates that vary, and Low for single-source, legendary or disputed entries. Early dates are approximate, and where sources conflict the notes say so.</p>
    <h2>Licence</h2><p>A licence for the images has not been chosen yet. Until one is added here, ask the maintainer before using them in anything you sell.</p>
    <h2>For maintainers</h2><p>Add images to the <code>incoming</code> folder (<code>incoming/lachit-borphukan/turnaround.png</code>), then run <code>python3 tools/add_sheets.py</code>. See <a href="#/coverage">Coverage</a> for every character’s folder name. Everything on this site comes from one spreadsheet, <a href="data/assam_history.csv" download>data/assam_history.csv</a>: periods, people, images, events and scenes, one row each. Edit it, then run <code>python3 tools/build.py</code>.</p></div>`;
}

/* ---------- viewer ---------- */
const V = { items: [], i: 0, z: 1, x: 0, y: 0, drag: null };
const dlg = $('viewer'), vimg = $('vImg');
function vApply() { vimg.style.transform = `translate(${V.x}px,${V.y}px) scale(${V.z})`; }
function vFit() { V.z = 1; V.x = V.y = 0; vApply(); }
function vShow() {
  const it = V.items[V.i], none = !it.src; dlg.classList.toggle('noimg', none);
  if (none) vimg.removeAttribute('src'); else vimg.src = it.src; vimg.hidden = none; $('vPh').hidden = !none; vimg.alt = it.title; $('vTitle').textContent = it.title; $('vSub').textContent = it.sub || '';
  const d = $('vDownload'); d.href = it.src; d.setAttribute('download', it.name || ''); $('vFoot').innerHTML = it.foot || '';
  $('vPrev').hidden = $('vNext').hidden = V.items.length < 2; vFit();
}
function openViewer(items, i) { V.items = items; V.i = i; vShow(); if (!dlg.open) dlg.showModal(); }
function vStep(n) { if (V.items.length > 1) { V.i = (V.i + n + V.items.length) % V.items.length; vShow(); } }
function vZoom(f) { V.z = Math.min(6, Math.max(1, V.z * f)); if (V.z === 1) V.x = V.y = 0; vApply(); }
$('vClose').onclick = () => dlg.close(); $('vPrev').onclick = () => vStep(-1); $('vNext').onclick = () => vStep(1);
$('vZoomIn').onclick = () => vZoom(1.4); $('vZoomOut').onclick = () => vZoom(1 / 1.4); $('vFit').onclick = vFit;
dlg.addEventListener('keydown', e => { if (e.key === 'ArrowLeft') vStep(-1); else if (e.key === 'ArrowRight') vStep(1); else if (e.key === '+' || e.key === '=') vZoom(1.4); else if (e.key === '-') vZoom(1 / 1.4); });
$('vStage').addEventListener('wheel', e => { e.preventDefault(); vZoom(e.deltaY < 0 ? 1.15 : 1 / 1.15); }, { passive: false });
$('vStage').addEventListener('dblclick', () => { V.z > 1 ? vFit() : vZoom(2.5); });
$('vStage').addEventListener('pointerdown', e => { V.drag = { x: e.clientX - V.x, y: e.clientY - V.y }; $('vStage').setPointerCapture(e.pointerId); });
$('vStage').addEventListener('pointermove', e => { if (V.drag && V.z > 1) { V.x = e.clientX - V.drag.x; V.y = e.clientY - V.drag.y; vApply(); } });
for (const ev of ['pointerup', 'pointercancel']) $('vStage').addEventListener(ev, () => V.drag = null);
dlg.addEventListener('click', e => { if (e.target === dlg) dlg.close(); });

function sceneItem(s) {
  const links = s.chars.map(id => `<a href="#/c/${id}" data-closeviewer>${esc(nm(charById[id]))}</a>`).join('');
  const srcs = srcOf(s.src).map(u => /^https?:/.test(u) ? `<a href="${esc(u)}" target="_blank" rel="noopener">${esc(decodeURIComponent(u.replace(/^https?:\/\/(www\.)?/, '').replace(/^en\.wikipedia\.org\/wiki\//, 'Wikipedia: ')).replace(/_/g, ' ').slice(0, 60))}</a>` : esc(u)).join('');
  const meta = s.conf || srcs ? `<p class="vmeta">${s.conf ? `${esc(t('confWord'))}: ${esc(s.conf)}. ` : ''}${srcs ? `${esc(t('sourcesWord'))}: ${srcs}` : ''}</p>` : '';
  const pls = (s.places || []).map(id => placeById[id]).filter(Boolean);
  const where = pls.length ? `<p class="vmeta vplaces">${esc(t('placesWord'))}: ${pls.map(p => placeLink(p) + (p.present && norm(p.present) !== norm(p.name) ? ` <small>(${esc(t('todayWord'))}: ${esc(p.present)})</small>` : '')).join('; ')}</p>` : '';
  return { src: s.planned ? '' : url(s.file), title: s.event, sub: s.date_label, name: s.filename,
    foot: `${s.planned ? `<p><em>${esc(t('plannedBody'))}</em></p>` : ''}<p>${esc(s.description)}</p>${s.notes ? `<p class="vnote">${esc(s.notes)}</p>` : ''}${where}${meta}${links}` };
}
function sheetItems(c) {
  return c.sheets.map(s => ({ src: url(s.file), title: nm(c), sub: kindName(s.kind), name: `${c.id}-${s.kind}.webp`, foot: s.caption ? esc(s.caption) : '' }));
}
dlg.addEventListener('click', e => { if (e.target.closest('[data-closeviewer]')) dlg.close(); });


/* ---------- kings tables ---------- */
const AHOM_REIGN = { 37: '1811–1818', 38: '1818–1819', 39: '1819–1821', 41: '1833–1838' };
const GAPS = { 5: ['Interregnum', '1364–1369'], 6: ['Interregnum', '1376–1380'], 7: ['Interregnum', '1389–1397'], 40: ['No Ahom king: Burmese rule, then the East India Company', '1822–1833'] };
const kcell = c => `<a href="#/c/${esc(c.id)}">${esc(c.name.replace(/ \(.*\)$/, ''))}</a>`;
function viewKings(which) {
  const tab = which === 'west' || which === 'koch' ? 'west' : which === 'neighbours' ? 'neighbours' : 'ahom';
  const tabs = `<nav class="tabs" aria-label="Kings">${[['', 'ahom', 'Ahom kings'], ['west', 'west', 'Western Assam kings'], ['neighbours', 'neighbours', 'Neighbouring kingdoms']].map(([h, k, l]) => `<a href="#/kings${h ? '/' + h : ''}" ${tab === k ? 'aria-current="page"' : ''}>${l}</a>`).join('')}</nav>`;
  if (tab === 'ahom') {
    const rows = [];
    for (const c of chars.filter(x => x.ahom_no)) for (const n of c.ahom_no) rows.push([n, c]);
    rows.sort((a, b) => a[0] - b[0]);
    const body = rows.map(([n, c]) => `<tr><td>${n}</td><td>${c.tai_name ? esc(c.tai_name) : '<span class="none">not recorded</span>'}</td><td>${kcell(c)}</td><td>${esc(c.nicknames || '')}</td><td>${esc(AHOM_REIGN[n] || c.label.replace(/ CE$/, ''))}</td><td>${esc(c.relation || '')}</td><td>${esc(c.fate || '')}</td></tr>${GAPS[n] ? `<tr class="gap"><td></td><td colspan="6">${esc(GAPS[n][0])}, ${esc(GAPS[n][1])}</td></tr>` : ''}`).join('');
    return `<div class="page-head"><h1>${esc(t('kings'))}</h1><p>The Ahom period is kept on its own. All 41 Ahom reigns from 1228 to 1838, by 39 kings: Chandrakanta Singha and Purandar Singha each reigned twice. Tai names come first; most kings after 1603 also took a Hindu name ending in Singha.</p></div>${tabs}
      <div class="tablewrap"><table class="cov kings hh h-ahom"><thead><tr><th>No.</th><th>Tai name</th><th>Name used here</th><th>Also called</th><th>Reign</th><th>Relation</th><th>How the reign ended</th></tr></thead><tbody>${body}</tbody></table></div>
      <p class="srcline">Source: Wikipedia, Ahom dynasty (king list), cross-checked against Ahom kingdom and the individual king articles. Spellings of Tai names vary between sources.</p>`;
  }
  const note = { 'Kamarupa after the Palas': 'The successors of the Pala kings, c. 1100–1228, in several regions: the west under Bengal’s Palas, a lunar dynasty on the north bank, and Prithu.', 'Kamata and Khen kingdoms': 'The Kamata kingdom founded by Sandhya after 1228 and the Khen dynasty (1440–1498). Dates are later reconstructions and sources differ.', 'Baro-Bhuyans': 'The Bhuyan chiefs who held power between the Khen and the Koch, and ended Sultanate rule around 1510.',
    'Koch kingdom (undivided)': 'The undivided kingdom (1515–1587) and the family around it.', 'Koch Hajo kings': 'The eastern Koch branch, in lower Assam, to 1613–14.', 'Darrang kings': 'Tributary kings of the Ahoms between the Barnadi and Bharali, from 1616. The Darrang line was annexed by the British in 1826.', 'Beltola kings': 'A small kingdom near Guwahati, set up in 1615 under the Ahom Borphukan.', 'Bijni kings': 'Descendants of Parikshit Narayan between the Sankosh and Manas. The sources give no reign years, so only the order is known.', 'Khaspur kings': 'A Koch outpost in the Barak valley that merged into the Kachari kingdom in 1745.',
    'Chutia kingdom': 'The kingdom of Sadiya in the north-east, attested by inscriptions from the late 14th century and annexed by the Ahoms in 1523–24.', 'Dimasa (Kachari) kingdom': 'The Dimasa and Barahi kings of the Kapili, Dhansiri and Barak valleys. Early king lists are late constructions.', 'Jaintia and Manipur': 'The hill kingdoms on the edge of the valley.' };
  const groups = tab === 'west' ? ['Kamarupa after the Palas', 'Kamata and Khen kingdoms', 'Baro-Bhuyans', 'Koch kingdom (undivided)', 'Koch Hajo kings', 'Darrang kings', 'Beltola kings', 'Bijni kings', 'Khaspur kings'] : ['Chutia kingdom', 'Dimasa (Kachari) kingdom', 'Jaintia and Manipur'];
  const lead = tab === 'west' ? 'Western (Namoni) Assam after 1100 is kept on its own: the successors of Kamarupa, Kamata and the Khen, the Bhuyans, and every Koch branch. Where the sources give no reign years the label says so and the order is the only claim.' : 'Kingdoms beside the Ahoms that were neither Ahom nor part of the western Assam lines.';
  const sect = groups.map(b => {
    const list = chars.filter(c => (c.group || c.dynasty) === b).sort((a, c) => (a.koch_no || 0) - (c.koch_no || 0) || a.sort_year - c.sort_year);
    if (!list.length) return '';
    return `<section class="section"><div class="row"><h2 class="${hc(houseOfGroup[b])}"><i class="sw"></i>${esc(b)}</h2></div><p class="muted">${esc(note[b] || '')}</p><div class="tablewrap"><table class="cov ${hc(houseOfGroup[b])}"><thead><tr><th>No.</th><th>Name</th><th>Reign</th><th>Role or relation</th><th>${esc(t('conf'))}</th></tr></thead><tbody>${list.map(c => `<tr><td>${c.koch_no || ''}</td><td>${kcell(c)}</td><td>${esc(c.label.replace(/ CE$/, ''))}</td><td>${esc(c.relation || c.role || '')}</td><td>${esc(c.confidence || '')}</td></tr>`).join('')}</tbody></table></div></section>`;
  }).join('');
  return `<div class="page-head"><h1>${esc(t('kings'))}</h1><p>${esc(lead)}</p></div>${tabs}${sect}`;
}

/* ---------- timeline: who ruled where, 1100 to 1545 ---------- */
const TL = { from: 1100, to: 1545 };
const LANES = [
  ['West: Kamarupa after the Palas', ['Pala dynasty', 'Kamarupa after the Palas'], 'pala'],
  ['West: Kamata and Khen', ['Kamata and Khen kingdoms'], 'kamata'],
  ['West: Baro-Bhuyans', ['Baro-Bhuyans'], 'bhuyan'],
  ['West: Koch', ['Koch kingdom (undivided)'], 'koch'],
  ['Bengal and Delhi', ['Pala Empire of Bengal', 'Bengal and Delhi rulers'], 'foreign'],
  ['Chutia', ['Chutia kingdom'], 'chutia'],
  ['Dimasa and Barahi', ['Dimasa (Kachari) kingdom'], 'dimasa'],
  ['Ahom', ['Ahom kings'], 'ahom'],
];
function viewTimeline() {
  const span = TL.to - TL.from, pct = y => 100 * (Math.min(Math.max(y, TL.from), TL.to) - TL.from) / span;
  const ticks = []; for (let y = 1100; y <= 1500; y += 50) ticks.push(y);
  const lanes = LANES.map(([name, groups, cls]) => {
    const items = chars.filter(c => groups.includes(c.group || c.dynasty) && Number.isFinite(c.reign_start) && Number.isFinite(c.reign_end) && c.reign_end > TL.from && c.reign_start < TL.to)
      .sort((a, b) => a.reign_start - b.reign_start);
    const rows = [];
    const placed = items.map(c => {
      const end = Math.max(c.reign_end, c.reign_start + 10); let r = rows.findIndex(last => c.reign_start >= last + 1);
      if (r < 0) { r = rows.length; rows.push(0); } rows[r] = end; return [c, r, end];
    });
    const bars = placed.map(([c, r, end]) => `<a class="tbar ${c.confidence === 'low' ? 'low' : ''}" href="#/c/${esc(c.id)}" style="left:${pct(c.reign_start)}%;width:${Math.max(0.5, pct(end) - pct(c.reign_start))}%;top:${r * 28 + 4}px" title="${esc(c.name)}, ${esc(c.label)}"><span>${esc(c.name.replace(/ \(.*\)$/, ''))}</span></a>`).join('');
    return `<div class="lane ${hc(cls)}"><div class="lname">${esc(name)}</div><div class="lbars" style="height:${Math.max(1, rows.length) * 28 + 8}px">${bars}</div></div>`;
  }).join('');
  const grid = ticks.map(y => `<i style="left:${pct(y)}%"><b>${y % 100 === 0 ? y : ''}</b></i>`).join('');
  const yr = e => e.end && e.end !== e.year ? `${e.year}–${String(e.end).length === 4 && String(e.end).slice(0, 2) === String(e.year).slice(0, 2) ? String(e.end).slice(2) : e.end}` : String(e.year);
  const evs = [...(S.events || [])].sort((a, b) => a.year - b.year || (a.end || 0) - (b.end || 0)).map(e => `<li><div class="ey">${esc(yr(e))}</div><div>${e.image ? `<button type="button" class="evimg" data-evimg="${esc(e.image)}" data-evtitle="${esc(e.title)}" aria-label="Open the scene image for ${esc(e.title)}"><img src="${url(e.thumb)}" alt="" loading="lazy"></button>` : ''}<h3>${esc(e.title)}</h3><p>${esc(e.body)}</p>${e.ids.length ? `<p class="chips">${e.ids.filter(i => charById[i]).map(i => `<a href="#/c/${esc(i)}">${esc(charById[i].name.replace(/ \(.*\)$/, ''))}</a>`).join('')}</p>` : ''}${e.src && e.src.length ? `<p class="srcline">${srcOf(e.src).map(u => /^https?:/.test(u) ? `<a href="${esc(u)}" target="_blank" rel="noopener">${esc(decodeURIComponent(u.replace(/^https?:\/\/(en\.)?wikipedia\.org\/wiki\//, 'Wikipedia: ')).replace(/_/g, ' ').slice(0, 44))}</a>` : esc(u)).join(', ')}</p>` : ''}</div></li>`).join('');
  return `<div class="page-head"><h1>${esc(t('timeline'))}</h1><p>After the Pala line ended around 1100, no single kingdom ruled Assam. Several states stood side by side, sometimes allied, often at war, while Sultans from Bengal raided the valley. This chart puts them on one time axis, western Assam first, then the neighbours, with the Ahoms at the bottom. Dashed bars are less certain, and the dates of the Kamata kings are later reconstructions.</p></div>
    <div class="tl" role="group" aria-label="Rulers by kingdom, 1100 to 1545"><div class="tlinner"><div class="axis"><div class="lname"></div><div class="lbars axisbars">${grid}</div></div>${lanes}</div></div>
    <p class="count">Click any bar to open that ruler. The chart scrolls sideways on small screens.</p>
    <section class="section"><div class="row"><h2>What happened</h2></div><ol class="events">${evs}</ol></section>`;
}


/* ---------- search ---------- */
const norm = x => String(x ?? '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^\p{L}\p{M}\p{N}\s]/gu, ' ').replace(/\s+/g, ' ').trim();
const nameKeys = c => c._nk || (c._nk = [c.name, c.name_as, c.tai_name, c.hindu_name, c.nicknames, c.alt_names, c.id.replace(/-/g, ' ')].map(norm).filter(Boolean));
const charText = c => c._tx || (c._tx = norm([c.role, c.label, c.summary, c.notes, c.group, c.dynasty, c.consort, c.relation, c.fate].join(' ')));
const sceneText = s => s._tx || (s._tx = norm([s.event, s.description, s.notes, s.date_label, s.collection, ...s.chars.map(id => (charById[id] || {}).name), ...(s.places || []).map(id => placeById[id] ? placeWords(placeById[id]) : '')].join(' ')));
function scoreKeys(keys, n, toks, cap = 100) {
  let best = 0;
  for (const k of keys) {
    if (k === n) best = Math.max(best, 100);
    else if (k.startsWith(n)) best = Math.max(best, 70);
    else if (k.includes(' ' + n)) best = Math.max(best, 55);
    else if (k.includes(n)) best = Math.max(best, 40);
    else if (toks.length > 1 && toks.every(w => k.includes(w))) best = Math.max(best, 30);
  }
  return Math.min(best, cap);
}
const nameScore = (c, n, toks) => scoreKeys(nameKeys(c), n, toks);
/* Places: names and historic names count in full; the present-day name counts less, so the historic place wins an exact match. */
const placeNameKeys = p => p._nk || (p._nk = [p.name, p.name_as, ...(p.alt || '').split(';')].map(norm).filter(Boolean));
const placeNowKeys = p => p._pk || (p._pk = [p.present].map(norm).filter(Boolean));
const placeScore = (p, n, toks) => Math.max(scoreKeys(placeNameKeys(p), n, toks), scoreKeys(placeNowKeys(p), n, toks, 60));
const placeWords = p => p._pw || (p._pw = norm([p.name, p.name_as, p.alt, p.present].join(' ')));
/* The catalogue records who a scene is about, not who is visible in the painted image, and a scene's people list also holds
   the reigning king and other context figures. For the tiny sheets use only the scene's main figures; when a scene has
   none, use the people its own text names, or its single linked person. */
const GENERIC = new Set(['singha', 'singh', 'borphukan', 'burhagohain', 'borgohain', 'borbarua', 'phukan', 'gohain', 'khan', 'shah', 'narayan', 'varman', 'deva', 'raja', 'rani', 'bhuyan', 'kumar', 'chandra', 'baruah', 'ahom', 'king', 'queen', 'prince', 'princess']);
const nameWords = c => c._nw || (c._nw = [...new Set(nameKeys(c).flatMap(k => k.split(' ')).filter(w => w.length >= 4 && !GENERIC.has(w)))]);
function namedIn(s, c) {
  const tx = s._mt || (s._mt = ' ' + norm([s.event, s.description, s.notes].join(' ')) + ' ');
  const ws = nameWords(c);
  if (ws.length) return ws.some(w => tx.includes(w));
  return nameKeys(c).some(k => k.length >= 6 && tx.includes(k));
}
function sceneCast(s) {
  const all = s.chars.map(id => charById[id]).filter(Boolean);
  const main = all.filter(c => s.main.includes(c.id));
  if (main.length) return main;
  const named = all.filter(c => namedIn(s, c));
  return named.length ? named : all.length === 1 ? all : [];
}
const tinyChars = s => {
  const withSheet = sceneCast(s).filter(c => c.sheets.length);
  const shown = withSheet.slice(0, 10), more = withSheet.length - shown.length;
  if (!withSheet.length) return '';
  return `<ul class="tiny" aria-label="${esc(t('srCharacters') || 'Characters')}">${shown.map(c => {
    const sh = [...c.sheets].sort((a, b) => coverRank(a.kind) - coverRank(b.kind))[0];
    return `<li><a class="hh ${hc(house(c)).replace('hh ', '')}" href="#/c/${esc(c.id)}" title="${esc(nm(c))}" aria-label="${esc(nm(c))}"><img src="${url(sh.thumb)}" alt="" loading="lazy" decoding="async"></a></li>`;
  }).join('')}${more > 0 ? `<li class="more">${esc(t('srMore', more))}</li>` : ''}</ul>`;
};
const sceneResult = s => sceneBtn(s).replace(/^<li>/, '<li class="sres">').replace(/<\/li>$/, tinyChars(s) + '</li>');
function charHit(c) {
  const sh = [...c.sheets].sort((a, b) => coverRank(a.kind) - coverRank(b.kind))[0];
  return { c, sh };
}
const placeLink = (p, label) => `<a href="#/search?q=${encodeURIComponent(p.name)}" data-closeviewer>${esc(label || p.name)}</a>`;
function placeCard(p) {
  return `<li><a class="placecard" href="#/search?q=${encodeURIComponent(p.name)}"><b>${esc(p.name)}</b>${p.name_as ? `<span class="as">${esc(p.name_as)}</span>` : ''}<small>${esc(p.cat || '')}${p.present ? ` · ${esc(t('srToday'))}: ${esc(p.present)}` : ''}</small></a></li>`;
}
const placeHref = id => `#/search?q=${encodeURIComponent((placeById[id] || { name: id }).name)}`;
function realmView(r, withKingdom) {
  const rows = (r.bounds || '').split('|').map(x => x.trim()).filter(Boolean).map(x => { const i = x.indexOf(':'); return i > 0 ? [x.slice(0, i), x.slice(i + 1).trim()] : ['', x]; });
  const pols = placeById[r.polity];
  return `<li><h3>${esc(r.label)}${r.conf ? ` <span class="badge ${r.conf === 'high' ? '' : 'warn'}" title="${esc(t('srIdent'))}">${esc(cap(r.conf))}</span>` : ''}</h3>
    <p class="rname">${esc(r.name)}${withKingdom && pols ? ` · <a href="${placeHref(pols.id)}">${esc(pols.name)}</a>` : ''}</p>
    ${rows.length ? `<dl class="bounds">${rows.map(([k, v]) => `<div><dt>${esc(k)}</dt><dd>${esc(v)}</dd></div>`).join('')}</dl>` : ''}
    <p>${esc(r.desc || '')}</p>${r.note ? `<p class="pnote">${esc(r.note)}</p>` : ''}
    ${(r.places || []).length ? `<p class="rchips">${r.places.filter(id => placeById[id]).map(id => `<a href="${placeHref(id)}">${esc(placeById[id].name)}</a>`).join('')}</p>` : ''}</li>`;
}
function placeView(p) {
  const scs = S.scenes.filter(s => (s.places || []).includes(p.id)), evs = S.events.filter(e => (e.places || []).includes(p.id)).sort((a, b) => (a.year ?? 0) - (b.year ?? 0));
  const ext = realms.filter(r => r.polity === p.id).sort((a, b) => (a.start ?? 0) - (b.start ?? 0)), bnd = realms.filter(r => r.polity !== p.id && (r.places || []).includes(p.id)).sort((a, b) => (a.start ?? 0) - (b.start ?? 0));
  window.__sceneList = scs;
  const srcs = srcOf(p.src).map(u => /^https?:/.test(u) ? `<a href="${esc(u)}" target="_blank" rel="noopener">${esc(decodeURIComponent(u.replace(/^https?:\/\/(www\.)?/, '').replace(/^en\.wikipedia\.org\/wiki\//, 'Wikipedia: ')).replace(/_/g, ' ').slice(0, 56))}</a>` : esc(u)).join(', ');
  const alt = (p.alt || '').split(';').map(x => x.trim()).filter(x => x && x !== p.name);
  const now = [p.present, p.loc].filter(Boolean).join(', ');
  return `<section class="sr-place" aria-label="${esc(t('srPlace'))}"><p class="kind">${esc(p.cat || t('srPlace'))}</p><h2>${esc(p.name)}</h2>${p.name_as ? `<div class="as">${esc(p.name_as)}</div>` : ''}
    <dl class="pfacts">${alt.length ? `<div><dt>${esc(t('srAlso'))}</dt><dd>${esc(alt.join(', '))}</dd></div>` : ''}${now ? `<div><dt>${esc(t('srToday'))}</dt><dd>${esc(now)}</dd></div>` : ''}${p.conf ? `<div><dt>${esc(t('srIdent'))}</dt><dd>${esc(cap(p.conf))}</dd></div>` : ''}${p.geo ? `<div><dt>${esc(t('srMapPoint'))}</dt><dd>${p.geo[0].toFixed(3)}°N, ${p.geo[1].toFixed(3)}°E <small>(${esc(t('srApprox'))})</small> <a href="https://www.openstreetmap.org/?mlat=${p.geo[0]}&mlon=${p.geo[1]}#map=9/${p.geo[0]}/${p.geo[1]}" target="_blank" rel="noopener">${esc(t('srOpenMap'))}</a></dd></div>` : ''}</dl>
    <p>${esc(p.desc || '')}</p>${p.note ? `<p class="pnote">${esc(p.note)}</p>` : ''}${srcs ? `<p class="srcline">${esc(t('sources'))}: ${srcs}</p>` : ''}</section>
    ${ext.length ? `<section class="section"><div class="row"><h2>${esc(t('srExtent'))}</h2></div><ol class="rlist">${ext.map(r => realmView(r, false)).join('')}</ol></section>` : ''}
    <section class="section"><div class="row"><h2>${esc(t('srPlaceScenes', p.name))}</h2><span class="count">${esc(t('srSceneCount', scs.length))}</span></div>
      ${scs.length ? `<ul class="grid">${scs.map(sceneResult).join('')}</ul>` : `<div class="empty">${esc(t('srNoSceneHere'))}</div>`}</section>
    ${bnd.length ? `<section class="section"><div class="row"><h2>${esc(t('srBoundaryOf'))}</h2></div><ol class="rlist">${bnd.map(r => realmView(r, true)).join('')}</ol></section>` : ''}
    ${evs.length ? `<section class="section"><div class="row"><h2>${esc(t('srTimeline'))}</h2><a href="#/timeline">${esc(t('timeline'))}</a></div><ul class="evlist">${evs.map(e => `<li><b>${esc(e.year ?? '')}${e.end && e.end !== e.year ? '–' + esc(e.end) : ''}</b> ${esc(e.title)}<small>${esc(e.body || '')}</small></li>`).join('')}</ul></section>` : ''}`;
}
function viewSearch(raw) {
  const n = norm(raw), toks = n.split(' ').filter(Boolean);
  const head = `<div class="page-head sr-head"><h1>${esc(t('searchLabel'))}</h1>${raw.trim() ? `<p class="qshow">“${esc(raw.trim())}”</p>` : ''}</div>`;
  if (!n) return head + `<p class="sr-hint">${esc(t('srHint'))}</p>`;
  const byName = chars.map(c => [c, nameScore(c, n, toks)]).filter(x => x[1] > 0).sort((a, b) => b[1] - a[1] || withSheets(b[0]) - withSheets(a[0]) || a[0].sort_year - b[0].sort_year);
  const byPlace = places.map(p => [p, placeScore(p, n, toks)]).filter(x => x[1] > 0).sort((a, b) => b[1] - a[1] || a[0].name.localeCompare(b[0].name));
  const placeFirst = byPlace.length > 0 && byPlace[0][1] > (byName.length ? byName[0][1] : 0);   /* a person wins a tie */
  if (placeFirst) {
    const top = byPlace[0][1], one = byPlace.length === 1 || (top >= 100 && byPlace[1][1] < 100) || (top >= 55 && byPlace[1][1] < top);
    if (one) return head + placeView(byPlace[0][0]);
    return head + `<p class="count" aria-live="polite">${esc(t('srPlacePick'))} ${esc(t('srPlaceCount', byPlace.length))}</p><ul class="pcards">${byPlace.slice(0, 48).map(([pl]) => placeCard(pl)).join('')}</ul>`;
  }
  const single = byName.length === 1 || (byName.length > 1 && byName[0][1] >= 100 && byName[1][1] < 100);
  if (single) {
    const c = byName[0][0], sheets = c.sheets, scs = [...c.mainScenes, ...c.scenes.filter(x => !c.mainScenes.includes(x))].map(x => sceneById[x]);
    window.__sceneList = scs;
    const main = sheets[0], e = eraById[c.era];
    const sheetBlock = main ? `<button type="button" class="sheetmain" data-ssheet="${esc(c.id)}|0" aria-label="${esc(t('zoom'))}"><img src="${url(main.file)}" alt="${esc(kindName(main.kind))} character sheet of ${esc(c.name)}" width="${main.width}" height="${main.height}"></button>
        ${sheets.length > 1 ? `<div class="thumbs">${sheets.map((x, i) => `<button type="button" data-ssheet="${esc(c.id)}|${i}" aria-label="${esc(kindName(x.kind))} ${i + 1}"><img src="${url(x.thumb)}" alt=""></button>`).join('')}</div>` : ''}`
      : `<div class="sheetmain none"><div><strong style="font-family:var(--serif);font-size:1.3rem;color:var(--text)">${esc(t('noSheetTitle'))}</strong><br>${esc(t(scs.length ? 'noPortraitBody' : 'noSheetBody'))}</div></div>`;
    return head + `<section class="sr-char ${hc(house(c))}" aria-label="${esc(t('srCharacter'))}"><div class="sr-sheet">${sheetBlock}</div>
      <div class="sr-info"><h2>${esc(nm(c))}</h2>${nm2(c) ? `<div class="as">${esc(nm2(c))}</div>` : ''}
        <p class="facts"><span><b>${esc(c.label)}</b></span> <span>${esc(c.role)}</span> <span>${esc(eraName(e))}</span>${house(c) ? `<span class="hchip"><i class="sw"></i>${esc(c.group || c.dynasty || houseLabel[house(c)])}</span>` : ''}</p>
        <p>${esc(c.summary)}</p><p><a class="btn primary" href="#/c/${esc(c.id)}">${esc(t('srOpen'))}</a></p></div></section>
      <section class="section"><div class="row"><h2>${esc(t('srScenesWith', nm(c)))}</h2><span class="count">${esc(t('srSceneCount', scs.length))}</span></div>
        ${scs.length ? `<ul class="grid">${scs.map(sceneResult).join('')}</ul>` : `<div class="empty">${esc(t('scenesWithNone'))}</div>`}</section>`;
  }
  if (byName.length > 1) {
    return head + `<p class="count" aria-live="polite">${esc(t('srPick'))} ${esc(t('srCharCount', byName.length))}</p><ul class="grid sr-pick">${byName.slice(0, 48).map(([c]) => charCard(c)).join('')}</ul>`;
  }
  const scs = S.scenes.map((s, i) => {
    const hay = sceneText(s), ev = norm(s.event);
    if (!toks.every(w => hay.includes(w))) return null;
    return [s, (ev.includes(n) ? 6 : 0) + toks.filter(w => ev.includes(w)).length * 2 + (norm(s.description).includes(n) ? 2 : 0), i];
  }).filter(Boolean).sort((a, b) => b[1] - a[1] || a[2] - b[2]).map(x => x[0]);
  const ppl = chars.filter(c => toks.every(w => charText(c).includes(w))).slice(0, 12);
  window.__sceneList = scs;
  if (!scs.length && !ppl.length) return head + `<div class="empty"><strong>${esc(t('srNone'))}</strong></div>`;
  return head + (scs.length ? `<section class="section sr-first"><div class="row"><h2>${esc(t('srScenes'))}</h2><span class="count" aria-live="polite">${esc(t('srSceneCount', scs.length))}</span></div><ul class="grid">${scs.map(sceneResult).join('')}</ul></section>` : '')
    + (ppl.length ? `<section class="section"><div class="row"><h2>${esc(t('srPeople'))}</h2></div><ul class="grid">${ppl.map(charCard).join('')}</ul></section>` : '');
}
const sBtn = $('searchBtn'), sForm = $('searchForm'), sIn = $('hq');
function openSearch(focus) { sForm.hidden = false; sBtn.setAttribute('aria-expanded', 'true'); if (focus) { sIn.focus(); sIn.select(); } }
function closeSearch() { sForm.hidden = true; sBtn.setAttribute('aria-expanded', 'false'); }
function goSearch(v) {
  const q = v.trim(), h = '/search' + (q ? '?q=' + encodeURIComponent(q) : '');
  if (parseHash().parts[0] === 'search') { history.replaceState(null, '', '#' + h); route(true); } else location.hash = h;
}
sBtn.onclick = () => { if (sForm.hidden) openSearch(true); else { closeSearch(); } };
sForm.addEventListener('submit', e => { e.preventDefault(); goSearch(sIn.value); });
sIn.addEventListener('input', () => { clearTimeout(sIn._t); sIn._t = setTimeout(() => goSearch(sIn.value), 140); });
sIn.addEventListener('keydown', e => { if (e.key === 'Escape') { closeSearch(); sBtn.focus(); } });
document.addEventListener('keydown', e => {
  if (e.key === '/' && !e.ctrlKey && !e.metaKey && !e.altKey && !/^(input|textarea|select)$/i.test(document.activeElement.tagName) && !dlg.open) { e.preventDefault(); openSearch(true); }
});

/* ---------- router ---------- */
function setNav(active) {
  $('nav').innerHTML = [['', 'home'], ['characters', 'characters'], ['kings', 'kings'], ['timeline', 'timeline'], ['scenes', 'scenes'], ['coverage', 'coverage'], ['about', 'about']]
    .map(([p, k]) => `<a href="#/${p}" ${active === p ? 'aria-current="page"' : ''}>${esc(t(k))}</a>`).join('');
  $('brandName').textContent = t('brand'); $('langBtn').textContent = lang === 'as' ? 'English' : 'অসমীয়া';
  sIn.placeholder = t('searchPh'); sBtn.setAttribute('aria-label', t('searchLabel')); sIn.setAttribute('aria-label', t('searchLabel'));
  $('footNote').textContent = t('foot'); document.documentElement.lang = lang === 'as' ? 'as' : 'en';
}
function route(keepScroll) {
  const { parts, q } = parseHash(), main = $('main'), top = parts[0] || '';
  let html, active = top, title = t('brand');
  if (top === 'characters') { html = viewCharacters(q); title = t('characters'); }
  else if (top === 'c') { html = viewCharacter(parts[1], q); active = 'characters'; if (charById[parts[1]]) title = nm(charById[parts[1]]); }
  else if (top === 'kings') { html = viewKings(parts[1]); title = t('kings'); }
  else if (top === 'timeline') { html = viewTimeline(); title = t('timeline'); }
  else if (top === 'scenes') { html = viewScenes(q); title = t('scenesTitle'); }
  else if (top === 'coverage') { html = viewCoverage(); title = t('covTitle'); }
  else if (top === 'about') { html = viewAbout(); title = t('about'); }
  else if (top === 'search') { html = viewSearch(q.get('q') || ''); title = t('searchLabel'); active = 'search'; }
  else { html = viewHome(); active = ''; }
  setNav(active); main.innerHTML = html; document.title = title === t('brand') ? title : `${title}, ${t('brand')}`;
  if (top === 'search') { if (document.activeElement !== sIn) sIn.value = q.get('q') || ''; openSearch(false); } else closeSearch();
  if (!route.first && keepScroll !== true) window.scrollTo(0, 0); route.first = false;
}
route.first = true;
window.addEventListener('hashchange', route);

document.addEventListener('click', e => {
  const sc = e.target.closest('[data-scene]');
  if (sc) {
    const { parts } = parseHash(); const c = parts[0] === 'c' ? charById[parts[1]] : null;
    const list = (parts[0] === 'scenes' || parts[0] === 'search') ? (window.__sceneList || S.scenes) : c ? c.scenes.map(x => sceneById[x]) : [sceneById[sc.dataset.scene]];
    const i = Math.max(0, list.findIndex(s => s.id === sc.dataset.scene));
    return openViewer(list.length > 1 || parts[0] ? list.map(sceneItem) : [sceneItem(sceneById[sc.dataset.scene])], parts[0] ? i : 0);
  }
  const ss = e.target.closest('[data-ssheet]');
  if (ss) { const [id, i] = ss.dataset.ssheet.split('|'); return openViewer(sheetItems(charById[id]), Number(i)); }
  const th = e.target.closest('[data-sheet]');
  if (th) { sheetIdx = Number(th.dataset.sheet); const c = charById[parseHash().parts[1]]; $('sheetview').innerHTML = sheetViewHTML(c); return; }
  if (e.target.closest('#sheetOpen,#sheetOpen2')) { const c = charById[parseHash().parts[1]]; return openViewer(sheetItems(c), sheetIdx); }
  if (e.target.closest('#copyBrief')) return copy(briefText(charById[parseHash().parts[1]]), t('copied'), t('copyFail'));
  const ev = e.target.closest('[data-evimg]');
  if (ev) return openViewer([{ src: url(ev.dataset.evimg), title: ev.dataset.evtitle, name: ev.dataset.evimg.split('/').pop() }], 0);
  if (e.target.closest('#copyMissing')) return copy(chars.filter(c => !withSheets(c)).map(c => c.id).join('\n'), t('missingCopied'), t('copyFail'));
});
$('langBtn').onclick = () => { lang = lang === 'as' ? 'en' : 'as'; try { localStorage.setItem('lang', lang); } catch {} route(); };
route();
})();
