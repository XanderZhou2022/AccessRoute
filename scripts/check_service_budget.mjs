import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { calculateBudget } from '../dist/assets/service-budget.mjs';
const data = JSON.parse(readFileSync(new URL('../dist/downloads/service-budget.json', import.meta.url)));
const near = (a, b) => assert.ok(Math.abs(a-b)<1e-10, `${a} differs from ${b}`);
for (const call of data.calls) {
  const model = data.models.find(m => m.id === call.model);
  near(call.usd, (call.input*model.input_per_million+call.output*model.output_per_million)/1e6);
}
for (const journey of data.journeys) {
  const result = calculateBudget(data, journey);
  for (const key of ['calls','input','output']) assert.equal(result[key], journey[key]);
  near(result.usd, journey.usd);
}
assert.deepEqual(calculateBudget(data,{preferences:0,guidance:0,localization:0,obstacle:0}), {calls:0,input:0,output:0,usd:0});
const photo = calculateBudget(data,{preferences:0,guidance:0,localization:1,obstacle:0});
assert.equal(photo.calls,2); near(photo.usd,0.006032);
for (const bad of [-1,0.5,101,NaN,Infinity]) assert.throws(()=>calculateBudget(data,{preferences:bad,guidance:0,localization:0,obstacle:0}),RangeError);
assert.equal(data.component_targets.length,14);
assert.equal(data.workflow_targets.length,6);
assert.equal(data.price_date,'2026-10-11');
const csv = readFileSync(new URL('../dist/downloads/service-budget.csv',import.meta.url),'utf8');
for (const row of [...data.calls,...data.journeys]) assert.ok(csv.includes(row.usd.toFixed(6)));
console.log('PASS: six model charges, three report workloads, two-call photo composition, zero/invalid inputs, 20 labelled targets and CSV consistency.');
