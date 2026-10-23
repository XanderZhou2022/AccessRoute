import assert from 'node:assert/strict';
import {routingModel,localizationModel} from '../dist/assets/method-model.mjs';

const chosen=m=>m.branches.find(b=>b.selected)?.id;
assert.equal(chosen(routingModel()),'stairs');
assert.equal(chosen(routingModel({profile:'wheelchair'})),'lift-a');
assert.equal(chosen(routingModel({profile:'wheelchair',rain:true})),'lift-b');
assert.equal(chosen(routingModel({profile:'wheelchair',closedA:true})),'lift-b');
assert.equal(routingModel({profile:'wheelchair',closedA:true,closedB:true}).result.status,'no_route');
assert.equal(chosen(routingModel({profile:'walking',closedA:true,closedB:true})),'stairs');
assert.equal(chosen(routingModel({profile:'wheelchair',rain:true,objective:'shortest'})),'lift-a');
assert.equal(chosen(routingModel({profile:'wheelchair',closedA:false,closedB:false})),'lift-a');

let routingCases=0;
for(const profile of ['walking','wheelchair','stroller'])for(const rain of [false,true])
for(const objective of ['balanced','shortest','sheltered'])for(const closedA of [false,true])for(const closedB of [false,true]){
  const m=routingModel({profile,rain,objective,closedA,closedB});
  assert.equal(m.result.status==='no_route',profile!=='walking'&&closedA&&closedB);
  if(m.result.status==='ok'){
    const picked=m.branches.find(b=>b.selected);
    assert(picked.available);
    assert(!closedA||picked.id!=='lift-a');
    assert(!closedB||picked.id!=='lift-b');
    assert(profile==='walking'||picked.id!=='stairs');
    if(objective==='shortest')assert.equal(picked.distance,Math.min(...m.branches.filter(b=>b.available).map(b=>b.distance)));
    if(m.primary==='sheltered')assert.equal(picked.exposure,Math.min(...m.branches.filter(b=>b.available).map(b=>b.exposure)));
  }
  routingCases++;
}
const clear=localizationModel();
assert.equal(clear.status,'ready');
assert.equal(clear.ranked[0].node_id,'v_A');
assert.equal(localizationModel({floor:'unknown'}).status,'needs_confirmation');
assert.equal(localizationModel({clarity:'partial'}).status,'needs_confirmation');
const unreadable=localizationModel({clarity:'unreadable'});
assert.equal(unreadable.status,'no_match');
assert(unreadable.evidence.length>0);
assert(unreadable.evidence.every(e=>!e.valid&&!e.observedPresent));
const approximate=localizationModel({approximate:true});
assert.equal(approximate.status,'needs_confirmation');
assert.equal(approximate.ranked[0].score,.79);
assert(!localizationModel({accuracy:15}).nearby.some(k=>k.id==='record-c'));
assert(localizationModel({accuracy:100}).nearby.some(k=>k.id==='record-c'));
let localizationCases=0;
for(const clarity of ['clear','partial','unreadable'])for(const floor of ['seen','unknown'])
for(const accuracy of [15,60,100])for(const approximate of [false,true]){
  const m=localizationModel({clarity,floor,accuracy,approximate});
  assert(m.nearby.every(k=>k.distance_m<=m.radius));
  assert(floor!=='seen'||m.nearby.every(k=>k.level_id==='F1'));
  assert(m.ranked.every(k=>Number.isFinite(k.score)&&k.score>=0&&k.score<=m.observation.confidence));
  assert(!approximate||m.ranked.filter(k=>k.association==='approximate').every(k=>k.score<=.79));
  localizationCases++;
}
console.log(`PASS: ${routingCases} route settings and ${localizationCases} retrieval settings; closures, rain preference, ambiguity, evidence rejection and score caps.`);
