import {route, effectiveCost, defaultPolicies, retrieveNearby, shortlist,
  rankCandidates, decision, lexicalScore, normalize} from './method-engine.mjs';

// Synthetic teaching data. All calculations use the snapshotted application core.
export const routeBranches = [
  {id:'stairs',name:'Stairs',label:'Short outdoor connection',mode:'stairs',lengths:[20,25,15],exposed:[false,true,true],y:95},
  {id:'lift-a',name:'Lift A',label:'A shorter lift connection',mode:'lift',lengths:[30,10,50],exposed:[true,false,false],y:225},
  {id:'lift-b',name:'Lift B',label:'A longer indoor connection',mode:'lift',lengths:[60,10,70],exposed:[false,false,false],y:355},
];
const baseNode=(id,levelId)=>({id,sceneId:'teaching-graph',kind:'junction',levelId,lon:0,lat:0,z:levelId==='F1'?0:4});
export function routingModel({profile='walking',rain=false,objective='balanced',closedA=false,closedB=false}={}) {
  const nodes=[baseNode('s','F1'),baseNode('t','F2')];
  const edges=[];
  for(const b of routeBranches){
    nodes.push(baseNode(`${b.id}-in`,'F1'),baseNode(`${b.id}-out`,'F2'));
    const ids=['s',`${b.id}-in`,`${b.id}-out`,'t'];
    b.lengths.forEach((distanceM,i)=>edges.push({id:`${b.id}-${i}`,from:ids[i],to:ids[i+1],
      distanceM,kind:i===1?b.mode:'corridor',bidirectional:true,indoor:!b.exposed[i],
      sheltered:!b.exposed[i],wheelchair:'verified_accessible',provenance:'manual/demo augmentation',
      ...(i===1?{facilityId:b.id}:{}),...(i===1&&b.mode==='stairs'?{stepCount:12}:{})}));
  }
  const graph={schemaVersion:'1.0',sceneId:'teaching-graph',nodes,edges,
    facilities:routeBranches.map(b=>({id:b.id,label:b.name,kind:b.mode,sourceRefs:[]}))};
  const events=[...(closedA?['lift-a']:[]),...(closedB?['lift-b']:[])].map(id=>({id:`closed-${id}`,
    type:'facility_closed',target:{facilityId:id},status:'active',validFrom:'2026-01-01T00:00:00Z',source:'demo'}));
  const context={profile,rain,objective,now:'2026-10-23T00:00:00Z',events,strictAccessibility:false};
  const result=route(graph,'s','t',context);
  const primary=objective==='balanced'&&rain?'sheltered':objective;
  const branches=routeBranches.map(b=>{
    const parts=edges.filter(e=>e.id.startsWith(`${b.id}-`));
    const costs=parts.map(e=>effectiveCost(e,context,defaultPolicies));
    return {...b,available:costs.every(c=>Number.isFinite(c.cost)),
      reasons:[...new Set(costs.flatMap(c=>c.reasons))],
      distance:parts.reduce((n,e)=>n+e.distanceM,0),
      exposure:parts.reduce((n,e)=>n+(!e.indoor&&!e.sheltered?e.distanceM:0),0),
      cost:costs.reduce((n,c)=>n+c.cost,0),
      selected:result.status==='ok'&&result.edgeIds.includes(`${b.id}-1`)};
  });
  return {graph,context,result,branches,primary};
}

const lonAt=metres=>metres/6371000*180/Math.PI;
export const landmarkRecords=[
  {id:'record-a1',node_id:'v_A',names:['Landmark Alpha'],level_id:'F1',metres:25,category:'landmark'},
  {id:'record-a2',node_id:'v_A2',names:['Landmark Alpha'],level_id:'F2',metres:20,category:'landmark'},
  {id:'record-b',node_id:'v_B',names:['Landmark Beta'],level_id:'F1',metres:45,category:'landmark'},
  {id:'record-c',node_id:'v_C',names:['Landmark Gamma'],level_id:'F1',metres:160,category:'landmark'},
  {id:'record-l',node_id:'v_L',names:['Public lift'],level_id:'F1',metres:18,category:'lift'},
];
export function localizationModel({clarity='clear',floor='seen',accuracy=60,approximate=false}={}) {
  const records=landmarkRecords.map(k=>({...k,lon:lonAt(k.metres),lat:0,descriptions:[],
    source:'synthetic teaching record',distance_m:0,route_distance_m:0,
    ...(approximate&&k.id==='record-a1'?{association:'approximate'}:{})}));
  const observation=clarity==='clear'?{names:['Landmark Alpha'],text:[],objects:[],confidence:.95}:
    clarity==='partial'?{names:[],text:['Landmark'],objects:[],confidence:.72}:
    {names:[],text:[],objects:[],confidence:.25};
  const graph={nodes:[baseNode('current','F1'),{...baseNode('route','F1'),lon:lonAt(25)},
    ...records.map(k=>({...baseNode(k.node_id,k.level_id),lon:k.lon}))]};
  const photo={position:{lon:0,lat:0,accuracy_m:Number(accuracy)},...(floor==='seen'?{level_id:'F1'}:{})};
  const nearby=retrieveNearby({graph},records,{input:{current_node_id:'current'},segments:[{nodeIds:['route']}]},photo,'landmark');
  const candidates=shortlist(observation,nearby);
  // Prepared model outputs, never a live image or model API call.
  const matches=candidates.filter(k=>clarity==='partial'?k.names[0].startsWith('Landmark'):
    k.names[0]==='Landmark Alpha').map(k=>({candidate_id:k.id,evidence:[{
      source:'photo',observed:clarity==='partial'?'Landmark':'Landmark Alpha',mapped:k.names[0]}]}));
  const ranked=rankCandidates(observation,candidates,matches);
  const status=decision(ranked,'localization');
  return {records,observation,nearby,ranked,matches,status,radius:Math.max(60,Number(accuracy)*2),
    floor:floor==='seen'?'F1':null,
    breakdown:ranked.map(k=>({id:k.id,lexical:.7*lexicalScore(observation,k),
      evidence:k.evidence.length ? 0.15 : 0,spatial:.1*Math.max(0,1-k.distance_m/120),
      route:.05*Math.max(0,1-k.route_distance_m/50),cap:Math.min(observation.confidence,k.association==='approximate' ? 0.79 : 1)})),
    evidence:matches.flatMap(m=>m.evidence.map(pair=>({id:m.candidate_id,...pair,
      valid:ranked.find(k=>k.id===m.candidate_id)?.evidence.length>0,
      observedPresent:[...observation.names,...observation.text].some(x=>normalize(x).includes(normalize(pair.observed)))})))};
}
