import {routingModel,localizationModel} from './method-model.mjs';

const escape = value => String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const number = value => Math.round(value);
const score = value => value.toFixed(3);

function routeMap(model){
  return `<svg viewBox="0 0 690 445" role="img" aria-label="Three schematic connections between a start on floor F1 and a destination on floor F2. Selected paths are green; blocked paths are dashed and marked with a cross.">
    <text x="65" y="25" class="svg-meta" text-anchor="middle">FLOOR F1</text>
    <text x="625" y="25" class="svg-meta" text-anchor="middle">FLOOR F2</text>
    ${model.branches.map(b=>{
      const state=!b.available?'path-blocked':b.selected?'path-selected':'path-available';
      return `<g class="${state}"><path d="M65 225 L200 ${b.y} L490 ${b.y} L625 225" class="network-path"/>
        <circle cx="200" cy="${b.y}" r="8" class="network-node"/><circle cx="490" cy="${b.y}" r="8" class="network-node"/>
        <rect x="278" y="${b.y-39}" width="135" height="27" rx="7" class="network-label-bg"/>
        <text x="345" y="${b.y-20}" text-anchor="middle" class="network-label">${b.name}</text>
        <text x="345" y="${b.y+29}" text-anchor="middle" class="network-detail">${b.distance} m · ${b.exposure?`${b.exposure} m uncovered`:'fully covered'}</text>
        ${!b.available?`<path d="M337 ${b.y-8}l16 16m0-16l-16 16" class="blocked-cross"/>`:''}</g>`;
    }).join('')}
    <circle cx="65" cy="225" r="15" class="endpoint"/><circle cx="625" cy="225" r="15" class="endpoint"/>
    <text x="65" y="263" text-anchor="middle" class="endpoint-label">Start</text>
    <text x="625" y="263" text-anchor="middle" class="endpoint-label">Destination</text>
    <text x="345" y="428" class="svg-meta" text-anchor="middle">SCHEMATIC TEACHING GRAPH · LENGTHS COME FROM THE EDGE RECORDS</text></svg>`;
}

function mountRouting(root){
  const form=root.querySelector('form');
  let step=2;
  function render(){
    const data=new FormData(form);
    const state={profile:data.get('profile'),rain:data.get('weather')==='rain',objective:data.get('objective'),
      closedA:form.elements.closedA.checked,closedB:form.elements.closedB.checked};
    const model=routingModel(state);
    const chosen=model.branches.find(b=>b.selected);
    root.dataset.routeStage=String(step);
    root.querySelector('[data-route-summary]').innerHTML=chosen?
      `<div><span class="result-eyebrow">CURRENT BEST CONNECTION</span><h3>${chosen.name}</h3></div><div class="result-metrics"><span><strong>${chosen.distance}</strong> m total</span><span><strong>${chosen.exposure}</strong> m uncovered</span></div>`:
      '<div><span class="result-eyebrow">NO FEASIBLE ROUTE</span><h3>Every usable connection is closed.</h3><p>Reopen a lift or change the travel settings to explore alternatives.</p></div>';
    root.querySelector('[data-route-map]').innerHTML=routeMap(model);
    root.querySelector('[data-route-comparison]').innerHTML=model.branches.map(b=>
      `<div class="connection-card ${b.selected?'is-selected':''} ${!b.available?'is-blocked':''}"><div><strong>${b.name}</strong><span>${b.distance} m · ${b.exposure} m uncovered</span></div>
      <b class="connection-state">${!b.available?(b.reasons.includes('FACILITY_CLOSED')?'Closed':'Steps excluded'):b.selected?'Selected':'Available'}</b></div>`).join('');
    const unavailable=model.branches.filter(b=>!b.available).map(b=>b.name);
    const blockedSteps=model.branches.some(b=>!b.available&&b.reasons.includes('STEP_FREE_REQUIRED'));
    const closed=model.branches.filter(b=>b.reasons.includes('FACILITY_CLOSED')).map(b=>b.name);
    const filter=unavailable.length?`Remove ${unavailable.join(' and ')}. ${blockedSteps?'The travel settings require a step-free connection. ':''}${closed.length?`${closed.join(' and ')} ${closed.length===1?'is':'are'} closed.`:''}`:
      'All three connections are available. Hard rules remove a connection only when it cannot meet the travel settings.';
    const compare=model.primary==='sheltered'?'Compare uncovered distance first. A longer indoor path can win because it keeps more of the journey covered.':
      state.objective==='shortest'?'Compare distance among the usable paths. A shorter path still has to meet the hard travel rules.':
      'Compare distance plus the policy costs for stairs and lifts. The shortest usable connection is not always the lowest-cost one.';
    const choose=chosen?`Choose ${chosen.name}. ${model.primary==='sheltered'?`It has the least rain exposure among the usable connections (${chosen.exposure} m).`:state.objective==='shortest'?'It has the shortest distance among the usable connections.':'It has the lowest policy-adjusted cost among the usable connections.'}`:
      'Return “no route” because no usable connection reaches the destination. The planner keeps the travel constraints in place.';
    root.querySelector('[data-route-explanation]').textContent=[filter,compare,choose][step];
    root.querySelectorAll('[data-route-step]').forEach(b=>b.setAttribute('aria-pressed',String(Number(b.dataset.routeStep)===step)));
  }
  form.addEventListener('change',render);
  root.addEventListener('click',event=>{
    const button=event.target.closest('button');
    if(!button)return;
    if(button.hasAttribute('data-reset')){form.reset();step=2;render();}
    if(button.hasAttribute('data-route-step')){step=Number(button.dataset.routeStep);render();}
  });
  form.addEventListener('submit',event=>event.preventDefault());
  render();
}

function lookupMap(records,selected){
  const positions={v_A:[235,110],v_B:[420,110],v_C:[555,210],v_L:[75,210],v_A2:[235,300]};
  return `<svg viewBox="0 0 630 360" role="img" aria-label="Synthetic map anchors on floors F1 and F2. A confirmed anchor is highlighted in green.">
    <rect x="15" y="28" width="600" height="205" rx="13" class="lookup-floor"/>
    <rect x="15" y="250" width="600" height="95" rx="13" class="lookup-floor"/>
    <text x="35" y="56" class="svg-meta">F1</text><text x="35" y="278" class="svg-meta">F2</text>
    ${records.map(k=>{const [x,y]=positions[k.node_id];const active=selected===k.id;
      return `<g class="${active?'lookup-selected':''}"><circle cx="${x}" cy="${y}" r="${active?14:9}" class="lookup-point"/>
      <text x="${x}" y="${y-23}" text-anchor="middle" class="network-label">${escape(k.names[0])}</text>
      <text x="${x}" y="${y+29}" text-anchor="middle" class="network-detail">${k.node_id}</text></g>`;}).join('')}</svg>`;
}

function mountLocalization(root){
  const form=root.querySelector('form');
  let step=0,applied=null,model;
  const titles=['Read the visible clues','Retrieve nearby map records','Check the matching evidence','Compare candidate scores','Confirm a map anchor'];
  function render(){
    const data=new FormData(form);
    const state={clarity:data.get('clarity'),floor:data.get('floor'),accuracy:Number(data.get('accuracy')),
      approximate:form.elements.approximate.checked};
    model=localizationModel(state);
    const top=model.ranked[0];
    root.querySelector('[data-accuracy-value]').textContent=`${state.accuracy} m`;
    const sign=state.clarity==='clear'?'LANDMARK ALPHA':state.clarity==='partial'?'LANDMARK…':'···';
    root.querySelector('[data-rag-panel="0"]').innerHTML=`<div class="rag-stage-title"><span>01 / READ</span><h3>Keep what is visible.</h3><p>The photo supplies a clue. The map will supply the coordinate.</p></div>
      <div class="observation-layout"><div class="prepared-sign"><span>PREPARED SIGN OBSERVATION</span><strong>${sign}</strong><b>${state.floor==='seen'?'F1':'Floor not visible'}</b></div>
      <div class="clue-list"><div><span>Readable clue</span><strong>${state.clarity==='clear'?'Landmark Alpha':state.clarity==='partial'?'Landmark':'None'}</strong></div>
      <div><span>Floor clue</span><strong>${state.floor==='seen'?'F1':'Unknown'}</strong></div><div><span>Visual reliability</span><strong>${model.observation.confidence.toFixed(2)}</strong></div></div></div>
      <p class="stage-takeaway">${state.clarity==='clear'?'A specific name can distinguish similar nearby places.':state.clarity==='partial'?'A partial name can fit several records. Expect the system to ask for confirmation.':'With no readable name, being near a map point is too little evidence to identify it.'}</p>`;
    root.querySelector('[data-rag-panel="1"]').innerHTML=`<div class="rag-stage-title"><span>02 / RETRIEVE</span><h3>Search the relevant part of the map.</h3><p>A ${model.radius} m radius${model.floor?' and the F1 floor clue':''} leaves ${model.nearby.length} of ${model.records.length} map records.</p></div>
      <div class="record-table-wrap"><table class="record-table"><thead><tr><th>Map record</th><th>Floor</th><th>Distance</th><th>Retrieval</th></tr></thead><tbody>
      ${model.records.map(k=>{const kept=model.nearby.some(c=>c.id===k.id);const reason=model.floor&&k.level_id!==model.floor?'Different floor':k.metres>model.radius?'Outside radius':'Kept';
        return `<tr class="${kept?'record-kept':'record-excluded'}"><td>${escape(k.names[0])}</td><td>${k.level_id}</td><td>${k.metres} m</td><td><span class="record-tag">${reason}</span></td></tr>`;}).join('')}
      </tbody></table></div><p class="stage-takeaway">The remaining records are ordered by text similarity, with distance breaking ties. The model receives at most 20.</p>`;
    root.querySelector('[data-rag-panel="2"]').innerHTML=`<div class="rag-stage-title"><span>03 / MATCH</span><h3>Ask what supports each match.</h3><p>The model proposes evidence pairs. The program checks that both text spans exist in their declared sources.</p></div>
      <div class="evidence-list">${model.evidence.length?model.evidence.map(e=>`<div class="evidence-card ${e.valid?'supported':'unsupported'}"><div><span>Photo observation</span><strong>${escape(e.observed)}</strong></div><span aria-hidden="true">↔</span><div><span>Retrieved record</span><strong>${escape(e.mapped)}</strong></div>
      <b>${e.valid?'Supported':'Rejected: absent from observation'}</b></div>`).join(''):'<p class="empty-state">No supported identity evidence is available.</p>'}</div>
      <p class="stage-takeaway">${state.clarity==='unreadable'?'The prepared model output mentions “Landmark Alpha”, but the observation contains no such text. Validation rejects that evidence.':'A candidate needs support from the visible clue and the retrieved record. Location context contributes only a small part of its score.'}</p>`;
    root.querySelector('[data-rag-panel="3"]').innerHTML=`<div class="rag-stage-title"><span>04 / RANK</span><h3>Combine identity evidence with context.</h3><p>The matching score uses text, valid evidence, distance and route proximity.</p></div>
      <div class="candidate-ranking">${model.ranked.map(k=>`<div class="ranking-row"><div><strong>${escape(k.names[0])}</strong><span>${k.level_id} · ${k.node_id}${k.association==='approximate'?' · approximate association':''}</span></div><div class="score-track"><i style="width:${k.score*100}%"></i></div><b>${score(k.score)}</b></div>`).join('')}</div>
      <p class="stage-takeaway">${model.status==='ready'?'One candidate reaches 0.80 and leads the best candidate on another node by at least 0.12.':model.status==='needs_confirmation'?'The evidence supports possible locations, but does not meet both the score and separation thresholds.':'The best candidate scores below 0.20. The workflow reports no match.'}</p>
      ${top?`<details class="score-details"><summary>See the top candidate’s score</summary><dl>${(()=>{const b=model.breakdown.find(x=>x.id===top.id);return [['Text · 70%',b.lexical],['Valid evidence · 15%',b.evidence],['Distance · 10%',b.spatial],['Route context · 5%',b.route]].map(([label,value])=>`<div><dt>${label}</dt><dd>${score(value)}</dd></div>`).join('')+`<div><dt>Reliability / association cap</dt><dd>${score(b.cap)}</dd></div><div><dt>Final matching score</dt><dd>${score(top.score)}</dd></div>`;})()}</dl><p>Weights sum before the cap applies. This score measures retrieval support, not a probability of correct positioning.</p></details>`:''}`;
    const selected=model.ranked.find(k=>k.id===applied);
    const choices=model.ranked.filter(k=>k.score>=.2).slice(0,3);
    root.querySelector('[data-rag-panel="4"]').innerHTML=`<div class="rag-stage-title"><span>05 / LOCATE</span><h3>${selected?'Anchor confirmed.':model.status==='no_match'?'Ask for another clue.':'Confirm the map anchor.'}</h3><p>${selected?`${escape(selected.names[0])} on ${selected.level_id} becomes the new starting anchor.`:model.status==='no_match'?'The system keeps the current location. A clearer name or floor sign can supply new evidence.':'Choose a candidate to see where its stored map node places the anchor.'}</p></div>
      ${model.status==='no_match'?'<div class="no-match-note">No match: the current position stays unchanged.</div>':`<div class="confirm-choices">${choices.map(k=>`<button type="button" class="confirm-choice ${k.id===applied?'is-confirmed':''}" data-confirm="${k.id}"><strong>${escape(k.names[0])}</strong><span>${k.level_id} · ${k.node_id} · ${score(k.score)}</span><b>${k.id===applied?'Confirmed ✓':'Use this anchor →'}</b></button>`).join('')}</div>`}
      <div class="lookup-map">${lookupMap(model.records,applied)}</div>
      <div class="anchor-result" aria-live="polite" aria-atomic="true">${selected?`<strong>Stored node: ${selected.node_id} · ${selected.level_id}</strong><span>Longitude ${selected.lon.toFixed(6)}°, latitude ${selected.lat.toFixed(6)}°</span><p>The coordinate comes from this map record. The remaining journey can now be replanned from its node.</p>`:'<p>The map holds the coordinates. A confirmed record tells the planner which node to use.</p>'}</div>`;
    root.querySelectorAll('[data-rag-panel]').forEach(p=>p.hidden=Number(p.dataset.ragPanel)!==step);
    root.querySelectorAll('[data-rag-step]').forEach(b=>b.setAttribute('aria-pressed',String(Number(b.dataset.ragStep)===step)));
    root.querySelector('[data-rag-back]').disabled=step===0;
    root.querySelector('[data-rag-next]').disabled=step===4;
    root.querySelector('[data-rag-progress]').textContent=`Step ${step+1} of 5 · ${titles[step]}`;
  }
  form.addEventListener('input',()=>{
    const hadAnchor=applied!==null;
    applied=null;render();
    if(hadAnchor)root.querySelector('[data-rag-announcement]').textContent='The clues changed. Confirm a map anchor again.';
  });
  form.addEventListener('submit',event=>event.preventDefault());
  root.addEventListener('click',event=>{
    const b=event.target.closest('button');if(!b)return;
    if(b.hasAttribute('data-reset')){form.reset();applied=null;step=0;}
    if(b.hasAttribute('data-rag-next'))step=Math.min(4,step+1);
    if(b.hasAttribute('data-rag-back'))step=Math.max(0,step-1);
    if(b.hasAttribute('data-rag-step'))step=Number(b.dataset.ragStep);
    const confirmed=b.hasAttribute('data-confirm')&&model.status!=='no_match'&&model.ranked.some(k=>k.id===b.dataset.confirm);
    if(confirmed)applied=b.dataset.confirm;
    render();
    if(confirmed){
      root.querySelector(`[data-confirm="${applied}"]`)?.focus({preventScroll:true});
      const anchor=model.ranked.find(k=>k.id===applied);
      root.querySelector('[data-rag-announcement]').textContent=`Confirmed ${anchor.names[0]} on ${anchor.level_id}. Stored map node ${anchor.node_id}.`;
    }
    if(b.hasAttribute('data-reset'))root.querySelector('[data-rag-announcement]').textContent='Walkthrough reset.';
  });
  render();
}

for(const root of document.querySelectorAll('[data-explainer]')){
  if(root.dataset.explainer==='routing')mountRouting(root);
  if(root.dataset.explainer==='localization')mountLocalization(root);
}
