"""Paper-style method pages. Equations and pseudocode remain selectable HTML."""
from html import escape
from interactive_markup import routing_explainer, localization_explainer

CODE = 'https://github.com/XanderZhou2022/AccessRoute_small_demo/blob/main/'


def equation(body, label, number):
    return (f'<div class="equation"><div role="math" aria-label="{escape(label)}">'
            f'{body}</div><span class="equation-number">({number})</span></div>')


def algorithm(number, title, inputs, outputs, lines):
    rows = ''.join(f'<li><span style="--indent:{indent}">{line}</span></li>' for indent, line in lines)
    return f'''<section class="algorithm" aria-label="Algorithm {number}: {title}">
    <h3><strong>Algorithm {number}</strong> {title}</h3>
    <div class="algorithm-contract"><p><b>Input:</b> {inputs}</p><p><b>Output:</b> {outputs}</p></div>
    <ol class="algorithm-lines">{rows}</ol></section>'''


def source_links(files):
    return '<ul class="source-files">' + ''.join(
        f'<li><a href="{CODE}{path}" target="_blank" rel="noopener">{label} ↗</a><code>{path}</code></li>'
        for path, label in files) + '</ul>'


def figure(name, caption, description, number=None, anchor='overview', height=600):
    number = number or (1 if name == 'route-planning' else 2)
    return f'''<figure class="method-figure" id="{anchor}"><p class="figure-mobile-hint">Scroll the figure horizontally to read all panels ↔</p>
    <div class="figure-scroll" tabindex="0" role="region" aria-label="Method figure; scroll horizontally on narrow screens">
    <img src="assets/methods/{name}.svg" alt="{escape(description)}" width="1050" height="{height}"></div>
    <figcaption><b>Figure {number}.</b> {caption}</figcaption>
    <div class="figure-downloads"><a href="assets/methods/{name}.svg" target="_blank" rel="noopener">Open vector figure ↗</a>
    <a href="assets/methods/{name}.pdf" download>Download PDF ↓</a>
    <a href="downloads/method-figures-source.zip" download>TikZ sources ↓</a></div></figure>'''


def shell(kind, title, subtitle, content):
    return f'''<div class="method-page"><div class="wrap">
    <nav class="method-nav" aria-label="Technical methods"><a href="technology.html">Technology</a>
    <a href="routing.html"{' aria-current="page"' if kind == 'routing' else ''}>Route planning</a>
    <a href="localization.html"{' aria-current="page"' if kind == 'localization' else ''}>Visual localization</a><a href="service-budget.html">API cost &amp; timing</a></nav>
    <header class="method-header"><span class="method-kicker">ACCESSROUTE HK / METHOD {'01' if kind == 'routing' else '02'}</span>
    <h1>{title}</h1><p>{subtitle}</p>
    <div class="method-contents"><a href="#try-it">Try it yourself</a><a href="#overview">Method overview</a>{('<a href="#rag-detail">RAG data flow</a>' if kind == 'localization' else '')}<a href="#formulation">Formulation</a>
    <a href="#algorithm">Algorithm</a><a href="#implementation">Implementation</a></div></header>
    {content}</div></div>'''


def routing_page():
    body = routing_explainer() + figure('route-planning',
        'Policies construct a feasible graph before lexicographic Dijkstra selects a path. '
        '(a) Cross-floor graph representation. (b) Hard constraints and objective costs. '
        '(c) Search, reconstruction and replanning.',
        'Three panels show a cross-floor mobility graph, edge filtering and objective costs, '
        'then lexicographic Dijkstra with a priority queue and current-anchor replanning.')
    body += '''<article class="method-body"><section class="method-section" id="formulation">
    <div class="section-marker">01 / FORMULATION</div><h2>Constraints define the feasible graph</h2>
    <p>A mobility graph <i>G</i> = (<i>V</i>, <i>E</i>) stores public-path nodes and directed connections across floors.
    Each node carries a map ID, longitude, latitude and optional floor. Each edge carries length, travel mode,
    indoor and shelter flags, accessibility attributes and an optional facility ID.
    A bidirectional edge contributes one arc in each direction.</p>
    <p>The query context contains endpoints <i>s</i>, <i>t</i>, user constraints <i>u</i>, objective <i>o</i>,
    weather <i>w</i> and the events active at time <i>τ</i>. A blocking policy excludes an edge;
    each remaining policy contributes a finite, nonnegative penalty.</p>'''
    body += equation('<i>A</i><sub>τ</sub> = {<i>a</i> : active(<i>a</i>) ∧ start(<i>a</i>) ≤ <i>τ</i> &lt; end(<i>a</i>)}',
                     'Active events have active status and contain the query time in their validity interval.', 1)
    body += '<p class="equation-note">An event without an expiry has end(<i>a</i>) = ∞.</p>'
    body += equation('<i>E</i><sub>τ</sub> = {<i>e</i> ∈ <i>E</i> : allowed(<i>e</i>, <i>u</i>, <i>A</i><sub>τ</sub>)}',
                     'The feasible edge set contains edges allowed by all hard constraints and active events.', 2)
    body += '''<div class="method-columns"><div><h3>Hard constraints</h3><p>Policies check step-free access,
    slope and width limits, opening times, facility closures and explicit exclusions. Strict accessibility mode
    also rejects unknown accessibility attributes and missing dimensions required by the query.</p></div>
    <div><h3>Event overlays</h3><p>Events target facility IDs or edge IDs. The planner constructs a fresh adjacency
    list for each query, so closures and restorations leave the stored base graph intact.</p></div></div>
    <h2 class="subsection-title">Exposure takes priority when the objective requires it</h2>
    <p>For sheltered routing, the primary weight counts outdoor distance without shelter.
    For indoor routing, it counts all outdoor distance. Other objectives use a zero primary weight.
    The secondary weight combines an objective-dependent base cost with policy penalties.</p>'''
    body += '''<div class="definition-table"><table><caption>Primary edge weight q<sub>o</sub>(e)</caption>
    <thead><tr><th>Objective</th><th>Primary weight</th></tr></thead><tbody>
    <tr><td>Sheltered</td><td>Edge length if outdoor and uncovered; zero otherwise.</td></tr>
    <tr><td>Indoor</td><td>Edge length if outdoor; zero otherwise.</td></tr>
    <tr><td>Balanced, shortest, least effort, fastest</td><td>Zero.</td></tr></tbody></table></div>'''
    body += equation('<i>c</i><sub>o</sub>(<i>e</i>) = <i>b</i><sub>o</sub>(<i>e</i>) + ∑<sub>p ∈ policies</sub> π<sub>p</sub>(<i>e</i>), &nbsp; π<sub>p</sub>(<i>e</i>) ≥ 0',
                     'Secondary cost is the objective base cost plus nonnegative policy penalties.', 3)
    body += '''<p>The base cost <i>b</i><sub>o</sub> is edge length, except that fastest mode uses estimated
    traversal and waiting time. Policy penalties depend on the objective: shortest mode suppresses soft penalties;
    least-effort mode increases stair, escalator and slope penalties. The fastest score combines time with policy
    penalties. It therefore expresses a routing preference score. Balanced mode switches to sheltered ordering
    when rain or a covered-route preference applies.</p>'''
    body += equation('<i>P</i><sup>*</sup> = arg min<sub>P : s ↝ t, P ⊆ E<sub>τ</sub></sub><sup>lex</sup> '
                     '〈 ∑<sub>e ∈ P</sub> <i>q</i><sub>o</sub>(<i>e</i>), ∑<sub>e ∈ P</sub> <i>c</i><sub>o</sub>(<i>e</i>) 〉',
                     'Choose a feasible path by minimizing its primary total first, then its secondary total.', 4)
    body += '''<p class="equation-note">Lexicographic order compares the first component, then breaks ties with the second.
    Every edge weight has nonnegative components.</p></section>
    <section class="method-section" id="algorithm"><div class="section-marker">02 / ALGORITHM</div>
    <h2>A priority queue orders two-component path labels</h2>'''
    body += algorithm(1, 'Policy-Constrained Lexicographic Dijkstra',
        'Graph <i>G</i>, endpoints <i>s</i>, <i>t</i>, context (<i>u</i>, <i>o</i>, <i>w</i>, <i>A</i><sub>τ</sub>).',
        'A feasible node / edge sequence, or <code>no_route</code> with policy reason codes.', [
        (0, 'Build adjacency over <i>E</i><sub>τ</sub>; attach weights (<i>q</i><sub>o</sub>, <i>c</i><sub>o</sub>) to each arc.'),
        (0, 'Set <i>D</i>[<i>v</i>] ← (∞, ∞) and pred[<i>v</i>] ← ∅ for every node.'),
        (0, 'Set <i>D</i>[<i>s</i>] ← (0, 0); push (<i>D</i>[<i>s</i>], <i>s</i>) into min-heap <i>Q</i>; settled ← ∅.'),
        (0, '<b>while</b> <i>Q</i> is nonempty <b>do</b>'),
        (1, '(<i>d</i>, <i>v</i>) ← extract-min<sub>lex</sub>(<i>Q</i>).'),
        (1, '<b>if</b> <i>v</i> ∈ settled or <i>d</i> ≠ <i>D</i>[<i>v</i>] <b>then continue</b>.'),
        (1, '<b>if</b> <i>v</i> = <i>t</i> <b>then break</b>; otherwise add <i>v</i> to settled.'),
        (1, '<b>for each</b> feasible outgoing arc <i>e</i> = (<i>v</i>, <i>z</i>) <b>do</b>'),
        (2, '<i>d</i>′ ← <i>D</i>[<i>v</i>] + (<i>q</i><sub>o</sub>(<i>e</i>), <i>c</i><sub>o</sub>(<i>e</i>)).'),
        (2, '<b>if</b> <i>d</i>′ &lt;<sub>lex</sub> <i>D</i>[<i>z</i>] <b>then</b>'),
        (3, '<i>D</i>[<i>z</i>] ← <i>d</i>′; pred[<i>z</i>] ← (<i>v</i>, <i>e</i>); push (<i>d</i>′, <i>z</i>) into <i>Q</i>.'),
        (0, '<b>if</b> <i>D</i>[<i>t</i>] = (∞, ∞) <b>then return</b> <code>no_route</code>.'),
        (0, 'Backtrack pred from <i>t</i> to <i>s</i>; aggregate distance, metrics, reasons and warnings.'),
        (0, '<b>return</b> the reconstructed route.')])
    body += '''<p>The binary heap avoids a linear scan of unsettled nodes. On the stored mobility graphs,
    search takes <i>O</i>((|<i>V</i>| + |<i>E</i>|) log |<i>V</i>|).
    Context changes trigger a fresh search from the current anchor; the session retains completed journey stages.</p>
    </section><section class="method-section" id="implementation"><div class="section-marker">03 / IMPLEMENTATION</div>
    <h2>Route outputs retain policy decisions</h2><p>The route returns node IDs, edge IDs, distance,
    preference cost, exposure and time metrics, policy reasons and data-quality warnings.
    A segmentation pass converts its edge sequence into floor, transition, bridge and outdoor instructions.</p>
    <div class="method-note"><b>Engine boundary.</b> This formulation describes the general graph engine.
    The field-route wrapper also evaluates stored, ordered route sequences to preserve their exit
    identities. It applies the same edge policies and uses graph search when connecting an anchor to a branch.</div>'''
    body += source_links([
        ('shared/routing/route.ts', 'Search and multi-objective route generation'),
        ('shared/routing/policies.ts', 'Accessibility, event and weather policies'),
        ('shared/routing/metrics.ts', 'Travel-time estimates and route metrics'),
        ('shared/journey/segment.ts', 'Path segmentation')])
    body += '''</section><a class="next-method" href="localization.html"><span>METHOD 02</span>
    Retrieval-augmented visual localization <span aria-hidden="true">→</span></a></article>'''
    return shell('routing', 'Policy-Constrained Route Planning',
                 'See how travel needs, rain and facility closures change a route. Then explore the algorithm behind the choice.', body)


def localization_page():
    body = localization_explainer() + figure('visual-localization',
        'Retrieved map records ground landmark matching and coordinate lookup. '
        '(a) Map index construction. (b) Visual observation, bounded retrieval and evidence matching. '
        '(c) Evidence validation, candidate ranking and map-node resolution.',
        'Three panels show a structured map index, image-to-candidate retrieval and evidence matching, '
        'then validation, score-based decisions and graph-node coordinate lookup.')
    body += '''<section class="rag-detail" id="rag-detail"><div class="section-marker">RETRIEVAL / EVIDENCE / MAP ANCHORS</div>
    <h2>From retrieved records to a map-grounded location</h2>
    <p>The expanded data flow exposes the records, model context and evidence that connect an image observation to a stored graph node.</p>'''
    body += figure('rag-retrieval',
        'Retrieved records supply the matching context; validated evidence ranks the candidate anchors. '
        '(a) Structured photo query. (b) Map records and their graph associations. (c) Bounded Top-20 retrieval. '
        '(d) Model input and evidence matching. (e) Span validation, scoring and candidate decisions. '
        '(f) Stored coordinate lookup for a ready or confirmed anchor. Solid graph lines denote mobility edges; '
        'dashed record links denote stored associations. Retrieval uses floor, spatial and lexical filters. '
        'L, M, D and R denote lexical, validated-evidence, spatial and route scores; γ is observation reliability '
        'and κ is the association cap.',
        'Six panels show a symbolic photo query, node-linked map records with a mobility graph, a retrieved-candidate table, '
        'a structured evidence-matching prompt, observed-to-mapped text pairs with ranked candidates, and coordinate lookup on the stored graph.',
        number=3, anchor='rag-figure', height=705)
    body += '</section>'
    body += '''<article class="method-body"><section class="method-section" id="formulation">
    <div class="section-marker">01 / FORMULATION</div><h2>Map records bind visual identity to graph nodes</h2>
    <p>The index <i>K</i> combines named map units, amenities, facility anchors and landmark-directory records.
    A record <i>k</i> stores names and aliases <i>N</i><sub>k</sub>, descriptions <i>T</i><sub>k</sub>,
    a category, source, graph node <i>v</i><sub>k</sub>, optional floor <i>ℓ</i><sub>k</sub> and association type.
    The graph supplies the output coordinate <i>x</i>(<i>v</i><sub>k</sub>).</p>
    <p>For named unit and amenity geometry, indexing selects a junction, entrance or point-of-interest node on
    the same floor within 20 metres of the feature centre. Landmark-directory entries supply their own node
    associations. Facility records attach to graph endpoints associated with that facility.</p>
    <h2 class="subsection-title">Spatial filtering bounds the candidate set</h2>
    <p>The vision model maps image <i>I</i> to an observation <i>O</i>: visible names, text, objects,
    floor label, direction hint and reliability <i>γ</i>. The workflow resolves a visible floor label against
    the scene manifest. An unknown label or a conflict with the supplied floor produces an empty match set.</p>'''
    body += equation('<i>r</i> = max(60, 2<i>a</i>) m with photo position; &nbsp; <i>r</i> = 120 m otherwise',
                     'The retrieval radius is the larger of 60 metres and twice position accuracy, or 120 metres without photo position.', 1)
    body += equation('<i>C</i> = {<i>k</i> ∈ <i>K</i> : landmark(<i>k</i>) ∧ floor-compatible(<i>k</i>) ∧ dist(<i>k</i>, <i>x</i><sub>0</sub>) ≤ <i>r</i>}',
                     'Candidates are nearby landmark records compatible with the resolved floor.', 2)
    body += '''<p>The centre <i>x</i><sub>0</sub> is the supplied photo position, or the current graph node.
    The uncertainty radius <i>a</i> comes from the supplied position accuracy. With no floor constraint,
    retrieval includes nearby records on all floors. Localization excludes path-edge records.</p>
    <h2 class="subsection-title">Text retrieval supplies evidence to the matching model</h2>
    <p>Normalization applies Unicode NFKC, lowercasing and removal of punctuation and spaces.
    The lexical matcher compares character-bigram sets with Dice similarity, retaining exact-name matches.
    Generic facility names receive a 0.35 multiplier; description matches receive a 0.85 multiplier.
    The shortlist keeps the 20 highest lexical scores, with distance breaking ties.</p>'''
    body += equation('Dice(<i>A</i>, <i>B</i>) = 2|<i>A</i> ∩ <i>B</i>| / (|<i>A</i>| + |<i>B</i>|)',
                     'Dice similarity is twice the number of shared character bigrams divided by the total set sizes.', 3)
    body += '''<p>The matching model receives the observation and retrieved records, then returns candidate IDs
    with paired observed and mapped text spans. Programmatic validation keeps a pair only when both normalized
    spans contain at least two characters and occur in their declared sources. Optional user clues remain a
    separate evidence source. In the live workflow that accepts these clues, the lexical score takes the maximum
    of photo-based and user-description similarity.</p>
    <div class="method-note"><b>Retrieval representation.</b> This implementation uses spatial filters,
    lexical retrieval and model-assisted evidence matching. Its map index stores structured records and text.
    The evidence indicator below records valid text-span pairs.</div>
    <h2 class="subsection-title">Ranking combines identity evidence with spatial context</h2>'''
    body += equation('<i>S</i><sub>k</sub> = round<sub>3</sub>(min{<i>γ</i>, <i>κ</i><sub>k</sub>, '
                     '0.70<i>L</i><sub>k</sub> + 0.15<i>M</i><sub>k</sub> + 0.10<i>D</i><sub>k</sub> + 0.05<i>R</i><sub>k</sub>})',
                     'The candidate score is a capped weighted sum of lexical, evidence, spatial and route terms, rounded to three decimal places.', 4)
    body += '''<div class="definition-table"><table><caption>Candidate score terms</caption>
    <thead><tr><th>Symbol</th><th>Definition</th></tr></thead><tbody>
    <tr><td><i>L</i><sub>k</sub></td><td>Maximum supported lexical similarity for the candidate.</td></tr>
    <tr><td><i>M</i><sub>k</sub></td><td>1 if at least one evidence pair survives validation; 0 otherwise.</td></tr>
    <tr><td><i>D</i><sub>k</sub></td><td>max(0, 1 − dist(<i>k</i>, <i>x</i><sub>0</sub>) / 120 m).</td></tr>
    <tr><td><i>R</i><sub>k</sub></td><td>max(0, 1 − distance to the nearest same-floor route node / 50 m); zero if none exists.</td></tr>
    <tr><td><i>γ</i></td><td>Reliability of the visual observation.</td></tr>
    <tr><td><i>κ</i><sub>k</sub></td><td>0.79 for an approximate association; 1 for other associations.</td></tr>
    </tbody></table></div><p class="equation-note">The fixed spatial-score scale is 120 m even when the retrieval
    radius differs. Scores express retrieval support; the implementation has no probability calibration.</p>
    </section><section class="method-section" id="algorithm"><div class="section-marker">02 / ALGORITHM</div>
    <h2>Evidence gates the selection of a map anchor</h2>'''
    body += algorithm(2, 'Retrieval-Augmented Landmark Localization',
        'Image <i>I</i>, map index <i>K</i>, graph <i>G</i>, position / floor / route context, optional user clues.',
        '<code>ready</code> with a node reference, <code>needs_confirmation</code> with candidates, or <code>no_match</code>.', [
        (0, '<i>O</i> ← visual observation of <i>I</i>; resolve its floor against the scene manifest.'),
        (0, '<b>if</b> a visible floor label is present but unrecognized, or its resolved floor conflicts with the supplied floor, <b>then return</b> <code>no_match</code>.'),
        (0, '<i>C</i> ← nearby, floor-compatible landmark records from <i>K</i>.'),
        (0, '<i>C</i><sub>20</sub> ← top 20 records by lexical score, breaking ties by distance.'),
        (0, '<b>if</b> <i>C</i><sub>20</sub> = ∅ <b>then return</b> <code>no_match</code>.'),
        (0, '<i>H</i> ← model evidence matches between <i>O</i> and <i>C</i><sub>20</sub>.'),
        (0, 'Validate observed and mapped spans in <i>H</i> against their declared sources.'),
        (0, 'Compute <i>S</i><sub>k</sub> for each candidate; sort by score, then distance.'),
        (0, 'Let <i>k</i><sub>1</sub> be the top record; let <i>k</i><sub>2</sub> be the highest-ranked record on a different node.'),
        (0, '<b>if</b> <i>S</i><sub>1</sub> &lt; 0.20 <b>then return</b> <code>no_match</code>.'),
        (0, '<b>if</b> <i>S</i><sub>1</sub> ≥ 0.80 and <i>S</i><sub>1</sub> − <i>S</i><sub>2</sub> ≥ 0.12 <b>then</b>'),
        (1, '<b>return</b> <code>ready</code> with node <i>v</i><sub>1</sub> and its floor reference.'),
        (0, '<b>return</b> <code>needs_confirmation</code> with the ranked candidates.')])
    body += '''<p class="equation-note">Use <i>S</i><sub>2</sub> = 0 when no candidate refers to a different node.
    Records that share one node represent the same approximate location. Approximate associations remain below
    the 0.80 ready threshold.</p></section>
    <section class="method-section" id="implementation"><div class="section-marker">03 / IMPLEMENTATION</div>
    <h2>Coordinate lookup connects localization to routing</h2>'''
    body += equation('<i>k</i><sup>*</sup> → <i>v</i><sub>k*</sub> → '
                     '(<i>lon</i>(<i>v</i><sub>k*</sub>), <i>lat</i>(<i>v</i><sub>k*</sub>), <i>ℓ</i><sub>k*</sub>)',
                     'The selected landmark resolves to a graph node, whose stored longitude, latitude and floor define the output anchor.', 5)
    body += '''<p>The workflow validates node and floor references against the scene. Pending workflow confirmations
    expire after five minutes and bind to their originating journey context. In the phone session flow, the user
    confirms the selected anchor before the session updates its current position and replans the remaining journey.
    The returned coordinate denotes the associated map anchor near the landmark.</p>
    <div class="method-note"><b>Execution boundary.</b> This pipeline describes live backend inference.
    The static showcase uses prepared observations and anchor associations. Its preset scores belong to those
    demonstrations; live matching scores come from the evidence-ranking workflow.</div>'''
    body += source_links([
        ('backend/agents/vision.ts', 'Structured visual observation'),
        ('backend/retrieval/map-index.ts', 'Map index and spatial retrieval'),
        ('backend/agents/map-matcher.ts', 'Retrieved-evidence matching'),
        ('backend/retrieval/rank.ts', 'Lexical scoring, evidence validation and decisions'),
        ('backend/workflows/localization.ts', 'Localization output and pending confirmation')])
    body += '''</section><a class="next-method" href="routing.html"><span>METHOD 01</span>
    Policy-constrained route planning <span aria-hidden="true">→</span></a></article>'''
    return shell('localization', 'Retrieval-Augmented Visual Localization',
                 'A photo supplies clues. Map records supply coordinates. Follow how the system connects the two.', body)
