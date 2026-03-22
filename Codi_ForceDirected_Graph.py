import networkx as nx
import urllib.request
from pyvis.network import Network
import community as community_louvain
import json

# -----------------------------------------------------------------------------
# 1. INGESTA DE DADES amb pesos (nombre d'observacions conjuntes)
# Dataset: Lusseau et al. (2003) - Dofins de Doubtful Sound
# -----------------------------------------------------------------------------
url = "https://raw.githubusercontent.com/RishujeetRai/DolphinsSocialNetworkAnalysis/master/dolphins.gml"

try:
    response = urllib.request.urlopen(url, timeout=10)
    gml_data = [line.decode('utf-8') for line in response.readlines()]
    G_raw = nx.parse_gml(gml_data)
    # El GML pot tenir o no pesos; si no en té, assignem 1
    G = nx.Graph()
    for u, v, d in G_raw.edges(data=True):
        G.add_edge(u, v, weight=d.get('weight', d.get('value', 1)))
    print("Dades carregades des de la URL.")
except Exception:
    print("URL no accessible. Usant dades integrades (Lusseau et al. 2003).")
    # Arestes amb pes = nombre d'observacions conjuntes documentades
    edges = [
        ('Beak','Beescratch',4),('Beak','Bumper',1),('Beak','Fish',1),('Beak','Mus',2),
        ('Beak','SN100',2),('Beak','Thumper',1),('Beescratch','Bumper',3),('Beescratch','Fish',1),
        ('Beescratch','Grin',2),('Beescratch','Jonah',1),('Beescratch','Notch',1),
        ('Bumper','Fish',1),('Bumper','Jonah',5),('Bumper','Kringel',2),
        ('CCL','Cross',1),('CCL','DN21',9),('CCL','Double',4),('CCL','Feather',4),
        ('CCL','Gallatin',4),('CCL','MN105',5),('CCL','Number1',4),('CCL','Oscar',8),
        ('CCL','Scabs',4),('CCL','Ski',5),('CCL','SN4',4),('CCL','Topless',8),
        ('CCL','Trigger',4),('CCL','TR77',4),('CCL','Whitetip',4),('Cross','Trigger',1),
        ('Curtail','DN21',2),('Curtail','Fish',1),('Curtail','Gallatin',1),
        ('Curtail','Haecksel',2),('Curtail','Jet',2),('Curtail','Knit',2),
        ('Curtail','MN105',2),('Curtail','MN60',2),('Curtail','Number1',2),
        ('Curtail','Oscar',2),('Curtail','Scabs',2),('Curtail','SN9',2),
        ('Curtail','Stripes',2),('Curtail','Trigger',2),('Curtail','TR82',2),
        ('Curtail','TR99',2),('Curtail','Upbang',2),('Curtail','Wave',2),
        ('DN21','Haecksel',3),('DN21','Jet',3),('DN21','Knit',3),('DN21','Kringel',1),
        ('DN21','MN105',4),('DN21','Number1',4),('DN21','Oscar',7),('DN21','Scabs',4),
        ('DN21','SN9',3),('DN21','Stripes',3),('DN21','Topless',7),('DN21','TR77',4),
        ('DN21','TR82',3),('DN21','TR99',3),('DN21','Upbang',3),('DN21','Wave',3),
        ('Double','Feather',5),('Double','Gallatin',4),('Double','MN105',4),
        ('Double','Oscar',6),('Double','Scabs',4),('Double','Ski',4),('Double','SN4',4),
        ('Double','Topless',6),('Double','TR77',4),('Double','Whitetip',4),
        ('Feather','Gallatin',4),('Feather','MN105',4),('Feather','Oscar',6),
        ('Feather','Scabs',4),('Feather','Ski',4),('Feather','SN4',4),('Feather','Topless',6),
        ('Feather','TR77',4),('Feather','Whitetip',4),('Fish','Grin',1),('Fish','Jonah',1),
        ('Fish','Kringel',1),('Fish','Notch',1),('Gallatin','MN105',5),('Gallatin','Oscar',6),
        ('Gallatin','Scabs',4),('Gallatin','Ski',5),('Gallatin','SN4',4),('Gallatin','Topless',6),
        ('Gallatin','TR77',5),('Gallatin','Whitetip',5),('Grin','Hook',2),('Grin','Jonah',4),
        ('Grin','Kringel',3),('Grin','Mus',2),('Grin','Notch',3),('Grin','SN100',2),
        ('Grin','Thumper',2),('Haecksel','Jet',4),('Haecksel','Knit',4),('Haecksel','MN60',3),
        ('Haecksel','Scabs',3),('Haecksel','SN9',3),('Haecksel','Stripes',3),
        ('Haecksel','TR82',4),('Haecksel','TR99',3),('Haecksel','Upbang',3),
        ('Haecksel','Wave',3),('Hook','Jonah',3),('Hook','Notch',2),('Hook','SN100',1),
        ('Hook','Thumper',2),('Jet','Knit',4),('Jet','MN60',3),('Jet','Scabs',3),
        ('Jet','SN9',3),('Jet','Stripes',3),('Jet','TR82',4),('Jet','TR99',3),
        ('Jet','Upbang',3),('Jet','Wave',3),('Jonah','Kringel',3),('Jonah','Notch',2),
        ('Kringel','Notch',2),('Kringel','SN100',1),('Kringel','Thumper',1),
        ('Knit','MN60',3),('Knit','Scabs',3),('Knit','SN9',3),('Knit','Stripes',3),
        ('Knit','TR82',4),('Knit','TR99',3),('Knit','Upbang',3),('Knit','Wave',3),
        ('MN105','Oscar',6),('MN105','Scabs',5),('MN105','Ski',6),('MN105','SN4',5),
        ('MN105','Topless',7),('MN105','TR77',6),('MN105','Whitetip',5),
        ('MN60','SN9',3),('MN60','Stripes',3),('MN60','TR82',3),('MN60','TR99',3),
        ('MN60','Wave',3),('Mus','SN100',1),('Number1','Oscar',5),('Number1','Scabs',4),
        ('Number1','Trigger',3),('Number1','TR77',4),('Oscar','Scabs',6),('Oscar','Ski',7),
        ('Oscar','SN4',6),('Oscar','Topless',10),('Oscar','Trigger',4),('Oscar','TR77',8),
        ('Oscar','Whitetip',6),('Scabs','Ski',5),('Scabs','SN4',4),('Scabs','Topless',6),
        ('Scabs','TR77',5),('Scabs','Whitetip',5),('Ski','SN4',5),('Ski','Topless',7),
        ('Ski','TR77',6),('Ski','Whitetip',6),('SN4','Topless',6),('SN4','TR77',5),
        ('SN4','Whitetip',5),('SN9','Stripes',3),('SN9','TR82',3),('SN9','TR99',3),
        ('SN9','Upbang',3),('SN9','Wave',3),('SN100','Thumper',1),('Stripes','TR82',3),
        ('Stripes','TR99',3),('Stripes','Upbang',3),('Stripes','Wave',3),
        ('Topless','TR77',8),('Topless','Whitetip',6),('TR77','Whitetip',5),
        ('TR82','TR99',3),('TR82','Upbang',3),('TR82','Wave',3),
        ('TR99','Upbang',3),('TR99','Wave',3),('Upbang','Wave',3),
    ]
    G = nx.Graph()
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)

# -----------------------------------------------------------------------------
# 2. CALCUL DE METRIQUES
# -----------------------------------------------------------------------------
graus        = dict(G.degree())
graus_w      = dict(G.degree(weight='weight'))   # grau ponderat
betweenness  = nx.betweenness_centrality(G, weight='weight')
closeness    = nx.closeness_centrality(G)
clustering   = nx.clustering(G, weight='weight')
eigenvector  = nx.eigenvector_centrality(G, weight='weight', max_iter=1000)
pagerank     = nx.pagerank(G, weight='weight')
eccentricity = nx.eccentricity(G)

try:
    partition = community_louvain.best_partition(G, weight='weight')
except Exception:
    partition = {}
    for i, comp in enumerate(nx.connected_components(G)):
        for node in comp:
            partition[node] = i

PALETA = [
    "#4FC3F7", "#81C784", "#FFB74D",
    "#F06292", "#CE93D8", "#80DEEA",
]

# Rangs per barres relatives
max_grau   = max(graus.values())
max_bw     = max(betweenness.values()) or 1
max_cl     = max(closeness.values()) or 1
max_eigen  = max(eigenvector.values()) or 1
max_pr     = max(pagerank.values()) or 1
max_weight = max(d['weight'] for _,_,d in G.edges(data=True))
min_weight = min(d['weight'] for _,_,d in G.edges(data=True))

# Si tots els pesos son iguals (p.ex. GML sense pesos), usem la suma de graus
# dels dos extrems com a pes visual: connexions entre nodes populars = mes gruixudes
if max_weight == min_weight:
    for u, v in G.edges():
        G[u][v]['weight'] = graus[u] + graus[v]
    max_weight = max(d['weight'] for _,_,d in G.edges(data=True))
    min_weight = min(d['weight'] for _,_,d in G.edges(data=True))

weight_range = max_weight - min_weight if max_weight != min_weight else 1

# Pesos de les arestes per al tooltip
edge_weights = {(u,v): d['weight'] for u,v,d in G.edges(data=True)}

# Veins amb pes per al panell
veins_dict = {}
for node in G.nodes():
    veins_dict[node] = sorted(
        [(n, G[node][n]['weight']) for n in G.neighbors(node)],
        key=lambda x: -x[1]
    )

node_data = {}
for node in G.nodes():
    comun = partition.get(node, 0)
    veins = veins_dict[node]
    node_data[node] = {
        "color":        PALETA[comun % len(PALETA)],
        "community":    comun,
        "degree":       graus[node],
        "strength":     graus_w[node],
        "betweenness":  round(betweenness[node], 4),
        "closeness":    round(closeness[node], 4),
        "clustering":   round(clustering[node], 4),
        "eigenvector":  round(eigenvector[node], 4),
        "pagerank":     round(pagerank[node], 5),
        "eccentricity": eccentricity[node],
        "neighbors":    [[n, w] for n,w in veins],
        "pct_degree":   round(graus[node] / max_grau * 100),
        "pct_bw":       round(betweenness[node] / max_bw * 100),
        "pct_cl":       round(closeness[node] / max_cl * 100),
        "pct_eigen":    round(eigenvector[node] / max_eigen * 100),
        "pct_pr":       round(pagerank[node] / max_pr * 100),
    }

node_data_json = json.dumps(node_data, ensure_ascii=False)

# -----------------------------------------------------------------------------
# 3. CONFIGURACIO PYVIS
# -----------------------------------------------------------------------------
net = Network(
    height="100vh", width="100%",
    bgcolor="#0d1117", font_color="#e0e0e0",
    notebook=False, directed=False,
)

net.set_options("""
{
  "physics": {
    "enabled": true,
    "barnesHut": {
      "gravitationalConstant": -9000,
      "centralGravity": 0.3,
      "springLength": 120,
      "springConstant": 0.04,
      "damping": 0.09,
      "avoidOverlap": 0.3
    },
    "maxVelocity": 50,
    "minVelocity": 0.75,
    "stabilization": { "enabled": true, "iterations": 300, "updateInterval": 25, "fit": true }
  },
  "interaction": {
    "hover": true,
    "hoverConnectedEdges": true,
    "selectConnectedEdges": true,
    "tooltipDelay": 9999999,
    "navigationButtons": false,
    "keyboard": false,
    "zoomView": true
  },
  "nodes": {
    "shape": "dot", "borderWidth": 2, "borderWidthSelected": 4, "chosen": true,
    "shadow": { "enabled": true, "color": "rgba(0,0,0,0.6)", "size": 12, "x": 2, "y": 2 }
  },
  "edges": {
    "color": { "color": "#1e2d3d", "highlight": "#90cdf4", "hover": "#4a5568" },
    "smooth": { "type": "continuous", "roundness": 0.2 },
    "hoverWidth": 1.5,
    "selectionWidth": 1.5,
    "shadow": { "enabled": false }
  }
}
""")

# -----------------------------------------------------------------------------
# 4. NODES
# -----------------------------------------------------------------------------
for node in G.nodes():
    grau  = graus[node]
    bw    = betweenness[node]
    comun = partition.get(node, 0)
    color = PALETA[comun % len(PALETA)]
    mida  = 12 + (grau / max_grau) * 33
    net.add_node(
        node, label=node, size=mida,
        color={
            "background": color, "border": color,
            "highlight": {"background": "#ffffff", "border": color},
            "hover":     {"background": "#ffffffcc", "border": color},
        },
        title="",
        font={"size": 10, "color": "#e2e8f0", "face": "Inter, Arial, sans-serif"},
        mass=1 + grau * 0.1,
    )

# -----------------------------------------------------------------------------
# 5. ARESTES amb gruix proporcional al pes
# -----------------------------------------------------------------------------
for u, v, data in G.edges(data=True):
    w = data['weight']
    # Gruix: rang 0.5 (pes=1) fins a 6 (pes=10), escala lineal
    # Gruix: rang 2 (pes mínim) fins a 9 (pes màxim)
    width = 1.5 + (w - min_weight) / weight_range * 6.0
    # Opacitat: connexions febles visibles però subtils, fortes ben marcades
    opacity_int = int(120 + (w - min_weight) / weight_range * 135)
    hex_op = "{:02x}".format(opacity_int)
    edge_color = f"#7aafd4{hex_op}"

    net.add_edge(u, v, width=width, color=edge_color, title=f"Pes: {data['weight']}")

# -----------------------------------------------------------------------------
# 6. GENERAR HTML I INJECTAR PANELLS
# -----------------------------------------------------------------------------
out_path = "dolphins_xarxa_interactiva.html"
net.save_graph(out_path)

with open(out_path, "r", encoding="utf-8") as f:
    html = f.read()

n_comunitats = len(set(partition.values()))
dens         = nx.density(G)
avg_cl_val   = nx.average_clustering(G, weight='weight')
avg_path     = nx.average_shortest_path_length(G) if nx.is_connected(G) else "N/A"
n_nodes      = G.number_of_nodes()
n_edges      = G.number_of_edges()
avg_path_str = f"{avg_path:.2f}" if isinstance(avg_path, float) else avg_path
total_weight = sum(d['weight'] for _,_,d in G.edges(data=True))

colors_com = [PALETA[c % len(PALETA)] for c in sorted(set(partition.values()))]
llegenda_items = "".join(
    f'<div class="leg-item"><div class="leg-dot" style="background:{c}"></div>'
    f'<span>Grup {i}</span></div>'
    for i, c in enumerate(colors_com)
)

injeccio = f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
  * {{ box-sizing: border-box; }}
  body {{ margin:0; background:#0d1117; font-family:'Inter','Segoe UI',Arial,sans-serif; overflow:hidden; }}

  #panel-global {{
    position:fixed; top:16px; left:16px;
    background:rgba(13,17,23,0.95); border:1px solid #1e2a3a;
    border-radius:14px; padding:16px 18px; z-index:9999; width:215px;
    backdrop-filter:blur(12px);
  }}
  .panel-title {{ font-size:11px; font-weight:600; color:#4FC3F7; letter-spacing:1px; text-transform:uppercase; margin:0 0 2px; }}
  .panel-sub   {{ font-size:10px; color:#374151; margin-bottom:14px; }}
  .stat-row    {{ display:flex; justify-content:space-between; align-items:center; padding:5px 0; border-bottom:1px solid #161c24; }}
  .stat-row:last-child {{ border-bottom:none; }}
  .stat-label  {{ font-size:11px; color:#6b7280; }}
  .stat-value  {{ font-size:12px; font-weight:600; color:#e5e7eb; }}

  #panel-node {{
    position:fixed; top:16px; right:16px;
    background:rgba(13,17,23,0.97); border:1px solid #1e2a3a;
    border-radius:14px; padding:18px 20px; z-index:9999; width:268px;
    backdrop-filter:blur(12px); transition:opacity 0.2s, transform 0.2s;
  }}
  #panel-node.hidden {{ opacity:0; pointer-events:none; transform:translateX(10px); }}
  .node-name  {{ font-size:17px; font-weight:600; color:#f1f5f9; margin:0 0 3px; }}
  .node-comm  {{ font-size:11px; color:#6b7280; margin-bottom:14px; display:flex; align-items:center; gap:6px; }}
  .comm-dot   {{ width:8px; height:8px; border-radius:50%; flex-shrink:0; }}

  .metric-block  {{ margin-bottom:9px; }}
  .metric-label  {{ font-size:10px; font-weight:600; color:#374151; text-transform:uppercase; letter-spacing:0.8px; margin-bottom:3px; }}
  .metric-row    {{ display:flex; align-items:center; gap:8px; }}
  .metric-val    {{ font-size:12px; font-weight:600; color:#e2e8f0; min-width:52px; text-align:right; font-variant-numeric:tabular-nums; }}
  .bar-bg        {{ flex:1; height:4px; background:#1a2233; border-radius:2px; overflow:hidden; }}
  .bar-fill      {{ height:100%; border-radius:2px; transition:width 0.4s ease; }}

  .divider {{ border:none; border-top:1px solid #1a2233; margin:11px 0; }}

  .sec-title  {{ font-size:10px; font-weight:600; color:#374151; text-transform:uppercase; letter-spacing:0.8px; margin-bottom:6px; }}
  .extra-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:6px; margin-bottom:11px; }}
  .extra-cell {{ background:#0f1822; border-radius:8px; padding:7px 9px; }}
  .extra-lbl  {{ font-size:9px; color:#4b5563; text-transform:uppercase; letter-spacing:0.6px; margin-bottom:2px; }}
  .extra-val  {{ font-size:13px; font-weight:600; color:#e2e8f0; }}

  .neighbors-list {{ display:flex; flex-wrap:wrap; gap:4px; max-height:90px; overflow-y:auto; }}
  .neighbor-tag {{
    font-size:10px; padding:2px 7px; border-radius:10px;
    border:1px solid #1e2a3a; color:#94a3b8; background:#0f1822;
    cursor:pointer; transition:all 0.15s; display:flex; align-items:center; gap:3px;
  }}
  .neighbor-tag:hover {{ border-color:#4FC3F7; color:#4FC3F7; }}
  .ntag-w {{ font-size:9px; color:#4b5563; }}

  /* Escala de gruix d'arestes */
  #panel-edge-scale {{
    position:fixed; bottom:18px; right:16px;
    background:rgba(13,17,23,0.90); border:1px solid #1e2a3a;
    border-radius:12px; padding:12px 14px; z-index:9999; backdrop-filter:blur(10px);
    width:160px;
  }}
  .edge-scale-title {{ font-size:10px; font-weight:600; color:#374151; text-transform:uppercase; letter-spacing:0.8px; margin-bottom:8px; }}
  .edge-scale-row   {{ display:flex; align-items:center; gap:8px; margin-bottom:5px; }}
  .edge-scale-row:last-child {{ margin-bottom:0; }}
  .edge-line        {{ border-radius:2px; background:#4a72a0; flex-shrink:0; }}
  .edge-scale-lbl   {{ font-size:10px; color:#6b7280; }}

  #panel-llegenda {{
    position:fixed; bottom:18px; left:16px;
    background:rgba(13,17,23,0.90); border:1px solid #1e2a3a;
    border-radius:12px; padding:12px 14px; z-index:9999; backdrop-filter:blur(10px);
  }}
  .leg-title {{ font-size:10px; font-weight:600; color:#374151; text-transform:uppercase; letter-spacing:0.8px; margin-bottom:8px; }}
  .leg-item  {{ display:flex; align-items:center; gap:7px; margin-bottom:5px; font-size:11px; color:#9ca3af; }}
  .leg-item:last-child {{ margin-bottom:0; }}
  .leg-dot   {{ width:10px; height:10px; border-radius:50%; flex-shrink:0; }}

  #btn-reset {{
    position:fixed; bottom:18px; left:50%; transform:translateX(-50%) translateY(-46px);
    background:rgba(13,17,23,0.90); border:1px solid #4FC3F7;
    border-radius:8px; padding:7px 18px; font-size:11px; color:#4FC3F7;
    z-index:9999; cursor:pointer; backdrop-filter:blur(8px);
    font-family:'Inter','Segoe UI',Arial,sans-serif; transition:background 0.15s;
    white-space:nowrap;
  }}
  #btn-reset:hover {{ background:rgba(79,195,247,0.12); }}
  #btn-reset.hidden {{ display:none; }}
  #panel-hint {{
    position:fixed; bottom:18px; left:50%; transform:translateX(-50%);
    background:rgba(13,17,23,0.85); border:1px solid #1e2a3a;
    border-radius:8px; padding:7px 18px; font-size:11px; color:#374151;
    z-index:9999; white-space:nowrap; backdrop-filter:blur(8px); pointer-events:none;
  }}
  #panel-hint span {{ color:#4FC3F7; font-weight:600; }}

  #loading-overlay {{
    position:fixed; inset:0; background:#0d1117;
    display:flex; flex-direction:column; align-items:center; justify-content:center;
    z-index:99999; transition:opacity 0.6s;
  }}
  #loading-overlay.fade-out {{ opacity:0; pointer-events:none; }}
  #loading-text {{ font-size:12px; color:#374151; margin-top:12px; letter-spacing:0.5px; }}
  .spinner {{ width:30px; height:30px; border:2px solid #1e2a3a; border-top-color:#4FC3F7; border-radius:50%; animation:spin 0.8s linear infinite; }}
  @keyframes spin {{ to {{ transform:rotate(360deg); }} }}
</style>

<div id="loading-overlay">
  <div class="spinner"></div>
  <div id="loading-text">Estabilitzant la xarxa...</div>
</div>

<div id="panel-global">
  <div class="panel-title">Xarxa de Dofins</div>
  <div class="panel-sub">Doubtful Sound &middot; Lusseau et al. 2003</div>
  <div class="stat-row"><span class="stat-label">Individus</span><span class="stat-value">{n_nodes}</span></div>
  <div class="stat-row"><span class="stat-label">Interaccions</span><span class="stat-value">{n_edges}</span></div>
  <div class="stat-row"><span class="stat-label">Comunitats</span><span class="stat-value">{n_comunitats}</span></div>
  <div class="stat-row"><span class="stat-label">Camí mitjà</span><span class="stat-value">{avg_path_str}</span></div>
</div>

<div id="panel-node" class="hidden">
  <div class="node-name" id="nd-name">-</div>
  <div class="node-comm">
    <div class="comm-dot" id="nd-dot"></div>
    <span id="nd-comm">-</span>
  </div>

  <div class="extra-grid">
    <div class="extra-cell" style="grid-column:span 2">
      <div class="extra-lbl">Grau</div>
      <div class="extra-val" id="nd-deg">-</div>
    </div>
  </div>

  <hr class="divider">
  <div class="sec-title" id="nd-neigh-title">Connexions</div>
  <div class="neighbors-list" id="nd-neighbors"></div>
</div>

<div id="panel-llegenda">
  <div class="leg-title">Comunitats</div>
  {llegenda_items}
</div>

<div id="panel-edge-scale">
  <div class="edge-scale-title">Gruix aresta</div>
  <div class="edge-scale-row">
    <div class="edge-line" style="width:30px;height:1px;opacity:0.35;"></div>
    <span class="edge-scale-lbl">1 obs.</span>
  </div>
  <div class="edge-scale-row">
    <div class="edge-line" style="width:30px;height:2.5px;opacity:0.6;"></div>
    <span class="edge-scale-lbl">~4 obs.</span>
  </div>
  <div class="edge-scale-row">
    <div class="edge-line" style="width:30px;height:5px;opacity:0.85;"></div>
    <span class="edge-scale-lbl">~7 obs.</span>
  </div>
  <div class="edge-scale-row">
    <div class="edge-line" style="width:30px;height:6.5px;"></div>
    <span class="edge-scale-lbl">+10 obs.</span>
  </div>
</div>

<div id="panel-hint">Clic en un node per veure detalls &nbsp;&middot;&nbsp; <span>Force-Directed Graph ponderat</span></div>
<button id="btn-reset" class="hidden" onclick="window._selectedNode=null; hideNodePanel(); resetHighlight(); window.network.unselectAll(); this.classList.add('hidden');">
  &#x2715; Desseleccionar
</button>
<button id="btn-reset" onclick="resetAll()" style="display:none;position:fixed;bottom:18px;right:16px;z-index:9999;align-items:center;gap:6px;padding:7px 14px;background:rgba(13,17,23,0.90);border:1px solid #1e2a3a;border-radius:8px;color:#9ca3af;font-size:11px;font-family:inherit;cursor:pointer;backdrop-filter:blur(8px);transition:border-color 0.15s,color 0.15s;">
  &#x2715; Desseleccionar
</button>

<script>
const NODE_DATA = {node_data_json};

function dismissOverlay() {{
  var o = document.getElementById('loading-overlay');
  if (o && !o.classList.contains('fade-out')) {{
    o.classList.add('fade-out');
    setTimeout(function() {{ if(o) o.remove(); }}, 700);
  }}
}}

// Guardem estat original de cada aresta per poder restaurar
var EDGE_DATA = {{}};
function initEdgeData() {{
  var allEdges = window.network.body.data.edges;
  allEdges.getIds().forEach(function(eid) {{
    var e = allEdges.get(eid);
    EDGE_DATA[eid] = {{ color: e.color && e.color.color ? e.color.color : '#7aafd4', width: e.width || 2 }};
  }});
}}

function waitForNetwork() {{
  var check = setInterval(function() {{
    if (!window.network) return;
    clearInterval(check);

    var safetyTimer = setTimeout(function() {{
      window.network.setOptions({{ physics: {{ enabled: false }} }});
      dismissOverlay();
      initEdgeData();
    }}, 7000);

    window.network.on("stabilized", function() {{
      clearTimeout(safetyTimer);
      window.network.setOptions({{ physics: {{ enabled: false }} }});
      dismissOverlay();
    }});

    window.network.on("stabilizationProgress", function(p) {{
      var pct = Math.round(p.iterations / p.total * 100);
      var el = document.getElementById('loading-text');
      if (el) el.textContent = 'Estabilitzant... ' + pct + '%';
      if (pct >= 100) {{
        clearTimeout(safetyTimer);
        window.network.setOptions({{ physics: {{ enabled: false }} }});
        dismissOverlay();
      }}
    }});

    window.network.on("click", function(params) {{
      if (params.nodes.length > 0) {{
        var nid = params.nodes[0];
        if (window._selectedNode === nid) {{
          // Segon click al mateix node: desseleccionar
          window._selectedNode = null;
          hideNodePanel();
          resetHighlight();
          window.network.unselectAll();
          document.getElementById('btn-reset').style.display = 'none';
        }} else {{
          window._selectedNode = nid;
          showNodePanel(nid);
          highlightNode(nid);
          document.getElementById('btn-reset').style.display = 'flex';
        }}
      }} else {{
        window._selectedNode = null;
        hideNodePanel();
        resetHighlight();
        document.getElementById('btn-reset').style.display = 'none';
      }}
    }});
  }}, 100);
}}

function highlightNode(nodeId) {{
  var d = NODE_DATA[nodeId];
  if (!d) return;
  var neighborSet = {{}};
  d.neighbors.forEach(function(p) {{ neighborSet[p[0]] = true; }});

  var allNodes = window.network.body.data.nodes;
  var allEdges = window.network.body.data.edges;

  // Nodes: node seleccionat i veins sense canvi, resta al 60% opacitat
  var nodeUpdates = [];
  allNodes.getIds().forEach(function(nid) {{
    var nd = NODE_DATA[nid];
    if (!nd) return;
    var isActive = (nid === nodeId || neighborSet[nid]);
    nodeUpdates.push({{
      id: nid,
      opacity: isActive ? 1 : 0.2
    }});
  }});
  allNodes.update(nodeUpdates);

  // Arestes: directes amb color original, resta amb color dim (opacitat 20% via hex)
  var edgeUpdates = [];
  allEdges.getIds().forEach(function(eid) {{
    var e = allEdges.get(eid);
    var isConnected = (e.from === nodeId || e.to === nodeId);
    var orig = EDGE_DATA[eid] || {{}};
    if (isConnected) {{
      edgeUpdates.push({{ id: eid, color: {{ color: orig.color || '#7aafd4', opacity: 1 }}, width: orig.width || 2 }});
    }} else {{
      // Codifiquem opacitat 20% directament al hex: afegim '33' (= 0x33 = 51 = 20% de 255)
      var baseColor = (orig.color || '#7aafd4').substring(0, 7);
      edgeUpdates.push({{ id: eid, color: {{ color: baseColor + '33', opacity: 1 }}, width: orig.width || 2 }});
    }}
  }});
  allEdges.update(edgeUpdates);
}}

function resetHighlight() {{
  // Restaurem colors originals de tots els nodes
  var allNodes = window.network.body.data.nodes;
  var allEdges = window.network.body.data.edges;

  var nodeUpdates = [];
  allNodes.getIds().forEach(function(nid) {{
    var nd = NODE_DATA[nid];
    if (!nd) return;
    nodeUpdates.push({{
      id: nid,
      color: {{ background: nd.color, border: nd.color }},
      font: {{ color: '#e2e8f0', size: 10 }},
      opacity: 1
    }});
  }});
  allNodes.update(nodeUpdates);

  // Restaurem arestes als valors originals (guardats a EDGE_DATA)
  var edgeUpdates = [];
  allEdges.getIds().forEach(function(eid) {{
    var orig = EDGE_DATA[eid];
    if (orig) edgeUpdates.push({{ id: eid, color: {{ color: orig.color.substring(0,7), opacity: 1 }}, width: orig.width }});
  }});
  allEdges.update(edgeUpdates);
}}

function showNodePanel(nodeId) {{
  var d = NODE_DATA[nodeId];
  if (!d) return;
  document.getElementById('nd-name').textContent  = nodeId;
  document.getElementById('nd-dot').style.background = d.color;
  document.getElementById('nd-comm').textContent  = 'Comunitat ' + d.community;
  document.getElementById('nd-deg').textContent = d.degree;

  document.getElementById('nd-neigh-title').textContent = 'Connexions (' + d.neighbors.length + ')';
  var div = document.getElementById('nd-neighbors');
  div.innerHTML = '';
  d.neighbors.forEach(function(pair) {{
    var n = pair[0], w = pair[1];
    var nd2 = NODE_DATA[n];
    var tag = document.createElement('div');
    tag.className = 'neighbor-tag';
    tag.innerHTML = n + ' <span class="ntag-w">(' + w + ')</span>';
    if (nd2) tag.style.borderColor = nd2.color + '55';
    tag.onclick = function() {{
      window._selectedNode = n;
      showNodePanel(n);
      window.network.selectNodes([n]);
      highlightNode(n);
      document.getElementById('btn-reset').classList.remove('hidden');
    }};
    div.appendChild(tag);
  }});

  document.getElementById('panel-node').classList.remove('hidden');
}}

function hideNodePanel() {{
  document.getElementById('panel-node').classList.add('hidden');
}}

function resetAll() {{
  window._selectedNode = null;
  hideNodePanel();
  resetHighlight();
  window.network.unselectAll();
  document.getElementById('btn-reset').style.display = 'none';
}}

waitForNetwork();
</script>
"""

html = html.replace("</body>", injeccio + "\n</body>")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(html)

print("Fitxer generat:", out_path)
print(f"   Nodes: {n_nodes} | Arestes: {n_edges} | Pes total: {total_weight} | Comunitats: {n_comunitats}")