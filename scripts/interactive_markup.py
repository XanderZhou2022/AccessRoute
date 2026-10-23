"""Accessible markup for the two browser-based method explanations."""

def routing_explainer():
    return '''<section class="method-lab" id="try-it" data-explainer="routing" aria-labelledby="routing-lab-title">
    <div class="lab-heading"><div><span class="lab-kicker">EXPLORE THE IDEA</span>
    <h2 id="routing-lab-title">Change a setting. Watch the route change.</h2>
    <p>The planner first removes connections you cannot use, then compares the remaining paths.</p></div>
    <a class="lab-jump" href="#overview">Read the technical method ↓</a></div>
    <noscript><p>Enable JavaScript to use this interactive explanation. The method figures and algorithms below remain readable.</p></noscript>
    <div class="lab-layout"><form class="demo-controls" aria-label="Route planning controls">
    <fieldset><legend>Getting around</legend><div class="choice-row">
    <label><input type="radio" name="profile" value="walking" checked> Walking</label>
    <label><input type="radio" name="profile" value="wheelchair"> Wheelchair</label>
    <label><input type="radio" name="profile" value="stroller"> Stroller</label></div></fieldset>
    <fieldset><legend>Weather</legend><div class="choice-row">
    <label><input type="radio" name="weather" value="dry" checked> Dry</label>
    <label><input type="radio" name="weather" value="rain"> Rain</label></div></fieldset>
    <label class="select-label" for="route-goal">What matters most?</label>
    <select id="route-goal" name="objective"><option value="balanced">Balance my needs</option>
    <option value="shortest">Shortest distance</option><option value="sheltered">Least rain exposure</option></select>
    <fieldset><legend>Try a facility closure</legend>
    <label class="check-row"><input type="checkbox" name="closedA"> Close Lift A</label>
    <label class="check-row"><input type="checkbox" name="closedB"> Close Lift B</label></fieldset>
    <button class="lab-secondary" type="button" data-reset>Reset settings</button>
    <p class="lab-footnote">An abstract teaching graph. Routes use the same policy and search code as the application.</p>
    </form><div class="lab-workspace">
    <div class="lab-status" aria-live="polite" aria-atomic="true" data-route-summary>Calculating the route…</div>
    <div class="route-canvas" data-route-map></div>
    <div class="map-legend"><span><i class="legend-line selected"></i> Selected</span><span><i class="legend-line"></i> Available</span><span><i class="legend-line blocked"></i> Unavailable</span></div>
    <div class="route-comparison" data-route-comparison></div></div></div>
    <div class="logic-walkthrough"><div class="lab-step-buttons" role="group" aria-label="Routing explanation steps">
    <button type="button" data-route-step="0" aria-pressed="false"><span>1</span> Filter</button>
    <button type="button" data-route-step="1" aria-pressed="false"><span>2</span> Compare</button>
    <button type="button" data-route-step="2" aria-pressed="true"><span>3</span> Choose</button></div>
    <p data-route-explanation></p></div>
    <details class="lab-glossary"><summary>What does “best route” mean?</summary>
    <p>A hard rule removes a connection entirely. A preference changes how the planner compares usable connections.
    In rain-aware balanced mode, less uncovered distance wins first; cost breaks ties. Shortest mode keeps the
    hard rules and compares distance. If every connection between floors is blocked, the planner returns no route.</p></details>
    </section>'''


def localization_explainer():
    return '''<section class="method-lab" id="try-it" data-explainer="localization" aria-labelledby="localization-lab-title">
    <div class="lab-heading"><div><span class="lab-kicker">EXPLORE THE IDEA</span>
    <h2 id="localization-lab-title">Follow the clues from a sign to a map point.</h2>
    <p>Read the visible clues, look up nearby map records, then choose a supported location.</p></div>
    <a class="lab-jump" href="#rag-detail">See the detailed RAG figure ↓</a></div>
    <p class="prepared-note">Prepared visual observations and model evidence; map retrieval and scoring run in your browser.</p>
    <noscript><p>Enable JavaScript to use this interactive explanation. The method figures and algorithms below remain readable.</p></noscript>
    <div class="lab-layout"><form class="demo-controls" aria-label="Localization controls">
    <label class="select-label" for="photo-detail">What is readable in the photo?</label>
    <select id="photo-detail" name="clarity"><option value="clear">A clear landmark name</option>
    <option value="partial">Only part of the name</option><option value="unreadable">No readable name</option></select>
    <label class="select-label" for="photo-floor">Is the floor visible?</label>
    <select id="photo-floor" name="floor"><option value="seen">Yes: F1</option><option value="unknown">No floor sign</option></select>
    <label class="range-label" for="position-accuracy">Position uncertainty <output data-accuracy-value>60 m</output></label>
    <input id="position-accuracy" type="range" name="accuracy" min="15" max="100" step="5" value="60">
    <p class="control-help">More uncertainty means a wider search area.</p>
    <label class="check-row"><input type="checkbox" name="approximate"> F1 Landmark Alpha has an approximate map association</label>
    <button class="lab-secondary" type="button" data-reset>Reset walkthrough</button>
    <p class="lab-footnote">Synthetic landmarks and map nodes explain the mechanism. This walkthrough makes no live model calls.</p>
    </form><div class="lab-workspace">
    <div class="rag-stepper" role="group" aria-label="Photo-to-map explanation steps">
    <button type="button" data-rag-step="0" aria-pressed="true"><span>1</span> Read</button>
    <button type="button" data-rag-step="1" aria-pressed="false"><span>2</span> Retrieve</button>
    <button type="button" data-rag-step="2" aria-pressed="false"><span>3</span> Match</button>
    <button type="button" data-rag-step="3" aria-pressed="false"><span>4</span> Rank</button>
    <button type="button" data-rag-step="4" aria-pressed="false"><span>5</span> Locate</button></div>
    <p class="lab-screen-reader" role="status" aria-live="polite" aria-atomic="true" data-rag-announcement></p>
    <div class="rag-stage" data-rag-panel="0"></div><div class="rag-stage" data-rag-panel="1" hidden></div>
    <div class="rag-stage" data-rag-panel="2" hidden></div><div class="rag-stage" data-rag-panel="3" hidden></div>
    <div class="rag-stage" data-rag-panel="4" hidden></div>
    <div class="rag-navigation"><button class="lab-secondary" type="button" data-rag-back disabled>← Previous</button>
    <p aria-live="polite" aria-atomic="true" data-rag-progress>Step 1 of 5 · Read the visible clues</p>
    <button class="lab-primary" type="button" data-rag-next>Next step →</button></div></div></div>
    <details class="lab-glossary"><summary>RAG, in plain language</summary>
    <p>Retrieval-augmented generation gives the model relevant records before it responds. Here, the records
    come from a map. The model compares visible clues with those records; the program checks the evidence
    and looks up the selected node’s stored coordinates. A nearby point alone provides too little evidence to identify a landmark.</p></details>
    </section>'''
