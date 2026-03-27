# PERSONALCANVAS — Memória do Projeto

> Este arquivo é lido automaticamente pelo Claude Code no início de cada sessão.
> Também é visualizado dentro do canvas no nó "memória".

---

## VISÃO DO PRODUTO

Personal Canvas é a central de comando e second brain do Daniel Lameira.
Concentra todos os seus fluxos — projetos pessoais, artísticos, profissionais e de estudo —
em um único lugar com fácil acesso e preparado para um futuro com IA mais presente.

**Filosofia:**
- Sem frameworks, sem dependências externas — tudo em `index.html`
- Persistência online via Directus (Railway) + GitHub Pages (sem servidor local)
- Escalável: cada projeto pode linkar a um repositório ou CMS próprio no futuro

---

## ARQUIVO PRINCIPAL
- Caminho: `E:/personalcanvas/index.html`
- localStorage key: `canvas_v7`
- Repositório: https://github.com/dlameira/personalcanvas
- GitHub Pages: https://dlameira.github.io/personalcanvas/

---

## PERSISTÊNCIA
- **Estado do canvas**: Directus `canvas_state` (id=1) → localStorage como cache
- **ArtCon items**: Directus collection `artcon_items`
- **Site Pessoal**: Directus collections `livros`, `obras`, `escritos`, `drops`
- Token Directus: `ynOx8xSSe-PVHMUBIlz0nG9YetXgAxU5`
- URL Directus: `https://directus-production-afdd.up.railway.app`
- Auto-save: a cada mudança (debounce 800ms → localStorage) + a cada 5 min → Directus

---

## ESTRUTURA DE NAVEGAÇÃO

### Nível 1 — Canvas Principal
Grafo de nós com pan/zoom. Clusters/hubs que agrupam projetos por área:

| Cluster | Cor | Hub | Descrição |
|---------|-----|-----|-----------|
| seiva | azul | SEIVA (id:1) | Empresa editorial e cultural |
| pessoal | verde | Projetos Pessoais (id:19) | Obras de autoria própria |
| colab | roxo | Colaborativos (id:20) | Projetos com outros criadores |
| editorial | âmbar | Outros Projetos (id:21) | Projetos editoriais e ficcionais |
| estudos | teal | Estudos (id:22) | Aprendizado contínuo |

### Nível 2 — Subcanvas (por nó)
Ao clicar em qualquer nó, entra no subcanvas daquele projeto.
Todos os nós têm subcanvas editável com:
- **Notas** arrastáveis com cores pastel (`state.subCanvases[id].notes[]`)
- **Vessel de referências** com links/arquivos (`state.subCanvases[id].refs[]`)
- Dados persistidos junto ao estado global no Directus

**Exceções com views customizadas:**
- `SP_NODE_ID = 8` — Site Pessoal → dashboard Directus (livros, obras, textos, drops)
- `ARTCON_NODE_ID = 12` — ArtCon → canvas Figma-like colaborativo com polling 5s
- Nó com label começando em "mem" → Memory view (renderiza este CLAUDE.md em cards)

---

## NÓS ESPECIAIS

### Nó "memória" (id: ~501)
- Abre a Memory View: CLAUDE.md renderizado em cards editáveis
- Detecção: `label.normalize('NFC').toLowerCase().startsWith('mem')`
- Encoding fix: `normalizeNodeTitles()` aplicado no loadState para corrigir acentos

### Site Pessoal (id: 8)
- Dashboard com vessels por tipo de conteúdo (livros, obras, textos, drops)
- Dados via Directus/Railway
- `SP_CARD_DIMS`: livros(w:82), obras(w:132), drops(w:96), textos(w:380)

### ArtCon (id: 12)
- Canvas colaborativo estilo Figma
- Tipos de item: `note`, `frame`, `image`, `file`, `vessel`
- Polling 5s, skip se dirty
- Pan: Space+drag ou middle-click | Zoom: scroll wheel

---

## PROJETOS ATIVOS

### ArtCon
Evento cultural de um dia em discussão como possibilidade.
- Data: 19 de setembro
- Local: Cidade das Artes, Rio de Janeiro
- Frentes: Teatro, Cinema, Talks, Expos, Música, Oficinas, Culinária
- Site: https://dlameira.github.io/artcon/
- Repo: https://github.com/dlameira/artcon
- Artistas: Emicida, Marcos Valle, Gregório Duvivier, Julia Portes, Clayton Nascimento,
  Kleber Mendonça, Camila Pitanga, Antônio Pitanga, Bráulio Amado, Mina Lima,
  Maxwell Alexandre, Paula Siebra, Noemi Jaffe, Helena Obersteiner,
  Angélica Freitas, Giovanna Cianelli, Erico Borgo, Laís Almeida
- Parceiros: Seiva, Janela Livraria, GL, Lei Rouanet

### Seiva
Empresa/coletivo de cultura, literatura e artes.
- Projetos internos: Seiva Brain, Ads Management, Aurora/Índice, Mapoteca, Base de Livros
- Parceiros recorrentes: Janela Livraria, GL

### Outros projetos relevantes
- Além das Árvores (conto de fantasia), Livrin (livro infantojuvenil), Cidade (obra digital)
- Telecosmo (universo ficcional infantojuvenil), Vida do Livro (curso → plataforma)
- Bookshop Brasil, Social Reading, Programação & IA, Design & UX, Leitura Técnica

---

## ARQUITETURA TÉCNICA

### Estado global
```js
state = {
  nodes: [],           // nós do canvas principal (= DN defaults se não carregado)
  connections: [],     // arestas entre nós
  nextId: 100,
  homeView: null,      // view salva ao entrar em subcanvas
  subCanvases: {       // por nodeId
    [id]: {
      nodes: [],       // nós do subcanvas (auto-populados ou editados)
      connections: [],
      notes: [],       // { id, text, x, y, color }
      refs: [],        // { id, title, url }
      view: {}         // pan/zoom restaurado ao voltar
    }
  },
  spConfig: {},        // config Directus do Site Pessoal
  spData: {}           // cache de dados do Site Pessoal
}
```

### Funções-chave
- `loadState()` → Directus → localStorage → DN defaults
- `normalizeNodeTitles(s)` → normaliza NFC em todos os títulos ao carregar
- `scheduleSave()` → debounce 800ms → localStorage + flag _dirty → Directus após 5min
- `enterSubCanvas(nodeId)` → detecta tipo → rota para view correta
- `showStdView(nodeId)` → subcanvas padrão (notas + refs) para todos os outros nós
- `autoPopulate(nodeId)` → gera nós filhos no subcanvas a partir das conexões do pai

### Clusters e cores
```js
CC = { seiva:'#4a9eff', pessoal:'#39d353', colab:'#b06fff', editorial:'#f0a500', estudos:'#00d4aa' }
```

---

## CONVENÇÕES DE CÓDIGO
- Sempre editar `E:/personalcanvas/index.html` (arquivo único)
- CSS inline em `<style>`, JS inline em `<script>`
- Padrão de modo: `body.xx-mode` ativa seção no panel e view correspondente
- Botão C (panel) sempre fecha a view atual e volta ao canvas
- Imagens do Directus: `${url}/assets/${id}?access_token=${token}`
- Novos nós: sempre incluir `{id, title, desc, cluster, status, hub, x, y}`

---

## ROADMAP / INTENÇÕES FUTURAS
- Linkar subcanvases de projetos a repositórios GitHub próprios
- Múltiplos projetos usando Directus como CMS compartilhado (coleções separadas)
- IA mais presente: contexto do canvas como prompt, agentes por projeto
- Nó "memória" como hub de contexto para o Claude em cada sessão
