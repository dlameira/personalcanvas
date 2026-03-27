# PERSONALCANVAS — Memória do Projeto

> Este arquivo é lido automaticamente pelo Claude Code no início de cada sessão.
> Também é visualizado dentro do canvas no nó "memória".

---

## VISÃO GERAL
Canvas interativo de segunda memória e mapa mental de projetos pessoais e profissionais.
Single-file HTML/JS/CSS app, estado em localStorage. Projetos integrados ao Directus CMS (Railway).
Filosofia: sem frameworks, sem dependências externas, tudo em `index.html`.

## ARQUIVO PRINCIPAL
- Caminho: `E:/personalcanvas/index.html`
- localStorage key: `canvas_v7`
- Servidor local: Python http.server porta 3000
- Repositório: a criar em github.com/dlameira/personalcanvas

## DIRECTUS (CMS)
- URL: `https://directus-production-afdd.up.railway.app`
- Token: `ynOx8xSSe-PVHMUBIlz0nG9YetXgAxU5`
- Collections: `livros`, `obras`, `escritos`, `drops`, `artcon_items`

## NÓS ESPECIAIS
- `SP_NODE_ID = 8` — Site Pessoal (dashboard Directus com livros, obras, textos, drops)
- `ARTCON_NODE_ID = 12` — ArtCon (canvas Figma-like colaborativo, dados online no Directus)
- Nó "memória" — abre esta view (CLAUDE.md renderizado)

## MODOS / VIEWS
- **Canvas principal** — grafo de nós, pan/zoom, clusters, minimap
- **body.sp-mode** — site pessoal dashboard (vessels por tipo de conteúdo)
- **body.ac-mode** — ArtCon canvas (pan/zoom, elementos livres, polling 5s)
- **body.memory-mode** — memory view (renderiza CLAUDE.md em cards)
- **Panel flutuante** — sempre visível z-index 300, arrastável, seção muda por modo

## PROJETOS ATIVOS

### ArtCon
Evento cultural de um dia em discussão como possibilidade.
- Data: 19 de setembro
- Local: Cidade das Artes, Rio de Janeiro
- Frentes: Teatro, Cinema, Talks, Expos, Música, Oficinas, Culinária
- Site apresentação: https://dlameira.github.io/artcon/
- Repositório: https://github.com/dlameira/artcon
- Canvas interno: nó 12, collection `artcon_items` no Directus
- Artistas confirmados/em discussão: Emicida, Marcos Valle, Gregório Duvivier, Julia Portes,
  Clayton Nascimento, Kleber Mendonça, Camila Pitanga, Antônio Pitanga, Bráulio Amado,
  Mina Lima, Maxwell Alexandre, Paula Siebra, Noemi Jaffe, Helena Obersteiner,
  Angélica Freitas, Giovanna Cianelli, Erico Borgo, Laís Almeida
- Parceiros em discussão: Seiva, Janela Livraria, GL, Lei Rouanet

### personalcanvas
- O próprio canvas (este projeto)
- Stack: HTML/CSS/JS vanilla, localStorage, Python http.server
- Repositório: a criar

## ARQUITETURA TÉCNICA

### Estado
- `state` object salvo em localStorage (`canvas_v7`)
- `scheduleSave()` → debounce 800ms → `localStorage.setItem`
- `undoPush()` / Ctrl+Z para desfazer

### Canvas principal
- Nós: `state.canvases[id].nodes[]` com `{id, x, y, label, cluster, hub, subcanvas}`
- Pan/zoom: `view = {x, y, scale}` → `applyView()`
- Conexões: SVG paths entre nós
- Clusters: cores por categoria em `CC{}` object

### SP Canvas (body.sp-mode)
- `spVesselEls{}` — map de vessels por tipo
- `spIsInsideVessel(card, vessel)` — geometry check pelo centro do card
- `spReflowVesselCards(vessel, type)` — grid reflow
- `SP_CARD_DIMS` — dimensões por tipo: livros(w:82), obras(w:132), drops(w:96), textos(w:380)
- Drag: hold mousedown → mousemove → mouseup to drop
- `-webkit-user-drag:none` nas imagens para evitar drag nativo

### ArtCon Canvas (body.ac-mode)
- `acItems[]` — itens carregados do Directus
- Tipos: `note`, `frame`, `image`, `file`, `vessel`
- `acScheduleSave(id)` → debounce 800ms → PATCH Directus
- Polling colaborativo: `setInterval` 5s, skip se dirty
- Vessel de refs: item tipo "vessel", links em JSON no campo `content`
- Pan: Space+drag ou middle-click
- Zoom: scroll wheel

## CONVENÇÕES DE CÓDIGO
- Sempre editar `E:/personalcanvas/index.html` (arquivo único)
- CSS inline em `<style>`, JS inline em `<script>`
- Padrão de modo: `body.xx-mode` ativa seção no panel e view correspondente
- Botão C (panel) sempre fecha a view atual e volta ao canvas
- Imagens do Directus: `${url}/assets/${id}?access_token=${token}`

## SEIVA (contexto)
Empresa/coletivo de cultura, literatura e artes.
Projetos: personalcanvas, ArtCon.
Parceiros recorrentes: Janela Livraria, GL.
