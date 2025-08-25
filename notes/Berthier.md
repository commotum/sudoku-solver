.
├── CHAIN-RULES-COMMON
│   ├── BIVALUE-CHAINS
│   ├── FORCING-BRAIDS
│   ├── FORCING-G-BRAIDS
│   ├── FORCING-G-WHIPS
│   ├── FORCING-WHIPS
│   ├── ODDAGONS
│   └── TYPED-BIVALUE-CHAINS
├── CHAIN-RULES-EXOTIC
│   ├── OR2-CONTRAD-G-WHIPS
│   ├── OR2-CONTRAD-WHIPS
│   ├── OR2-FORCING-G-WHIPS
│   ├── OR2-FORCING-WHIPS
│   ├── OR2-G-WHIPS
│   ├── OR2-WHIPS
│   ├── OR3-CONTRAD-G-WHIPS
│   ├── OR3-CONTRAD-WHIPS
│   ├── OR3-FORCING-G-WHIPS
│   ├── OR3-FORCING-WHIPS
│   ├── OR3-G-WHIPS
│   ├── OR3-WHIPS
│   ├── OR4-CONTRAD-G-WHIPS
│   ├── OR4-CONTRAD-WHIPS
│   ├── OR4-FORCING-G-WHIPS
│   ├── OR4-FORCING-WHIPS
│   ├── OR4-G-WHIPS
│   ├── OR4-WHIPS
│   ├── OR5-CONTRAD-G-WHIPS
│   ├── OR5-CONTRAD-WHIPS
│   ├── OR5-FORCING-G-WHIPS
│   ├── OR5-FORCING-WHIPS
│   ├── OR5-G-WHIPS
│   ├── OR5-WHIPS
│   ├── OR6-CONTRAD-G-WHIPS
│   ├── OR6-CONTRAD-WHIPS
│   ├── OR6-FORCING-G-WHIPS
│   ├── OR6-FORCING-WHIPS
│   ├── OR6-G-WHIPS
│   ├── OR6-WHIPS
│   ├── PARTIAL-OR2-G-WHIPS
│   ├── PARTIAL-OR2-WHIPS
│   ├── PARTIAL-OR3-G-WHIPS
│   ├── PARTIAL-OR3-WHIPS
│   ├── PARTIAL-OR4-G-WHIPS
│   ├── PARTIAL-OR4-WHIPS
│   ├── PARTIAL-OR5-G-WHIPS
│   ├── PARTIAL-OR5-WHIPS
│   ├── PARTIAL-OR6-G-WHIPS
│   ├── PARTIAL-OR6-WHIPS
│   ├── SPLIT-ORk
│   ├── SYMMETRIFY-ORk
│   └── update-ORk-relations.clp
├── CHAIN-RULES-MEMORY
│   ├── BRAIDS
│   ├── G2-WHIPS
│   ├── G-BIVALUE-CHAINS
│   ├── G-BRAIDS
│   ├── G-WHIPS
│   ├── PARTIAL-G-WHIPS
│   ├── PARTIAL-WHIPS
│   ├── T-WHIPS
│   ├── TYPED-PARTIAL-WHIPS
│   ├── TYPED-T-WHIPS
│   ├── TYPED-WHIPS
│   ├── TYPED-Z-CHAINS
│   ├── WHIPS
│   └── Z-CHAINS
├── CHAIN-RULES-SPEED
│   ├── BRAIDS
│   ├── G-BIVALUE-CHAINS
│   ├── G-BRAIDS
│   ├── G-WHIPS
│   ├── PARTIAL-G-WHIPS
│   ├── PARTIAL-WHIPS
│   ├── T-WHIPS
│   ├── TYPED-G-WHIPS
│   ├── TYPED-PARTIAL-WHIPS
│   ├── TYPED-T-WHIPS
│   ├── TYPED-WHIPS
│   ├── TYPED-Z-CHAINS
│   ├── WHIPS
│   └── Z-CHAINS
├── CSP-Rules-Generic-Loader.clp
├── GENERAL
│   ├── 2-value.clp
│   ├── 3-value.clp
│   ├── Bivalue.clp
│   ├── blocked-rules.clp
│   ├── blocked-rules-fns.clp
│   ├── compute-RS.clp
│   ├── ECP.clp
│   ├── focused-elims.clp
│   ├── gBivalue.clp
│   ├── generic-background.clp
│   ├── generic-output.clp
│   ├── glabels.clp
│   ├── globals.clp
│   ├── init-glinks.clp
│   ├── init-links.clp
│   ├── is-cspvar-for-cand.clp
│   ├── is-cspvar-for-gcand.clp
│   ├── manage.clp
│   ├── nrc-output.clp
│   ├── parameters.clp
│   ├── play.clp
│   ├── saliences.clp
│   ├── SimulatedElim.clp
│   ├── Single.clp
│   ├── solve.clp
│   ├── templates.clp
│   ├── track-levels.clp
│   └── Typed-Bivalue.clp
├── MODULES
│   ├── BIVALUE-CHAINS-module.clp
│   ├── BRT-module.clp
│   ├── enter-module.clp
│   ├── modules.clp
│   ├── REVERSIBLE-CHAINS-module.clp
│   └── W1-module.clp
├── T&E+DFS
│   ├── anti-backdoor-pairs.clp
│   ├── anti-backdoors.clp
│   ├── backdoors.clp
│   ├── DFS-biv.clp
│   ├── DFS.clp
│   ├── Forcing2-TE.clp
│   ├── Forcing3-TE.clp
│   ├── Forcing4-TE.clp
│   ├── ORk-Forcing-TE.clp
│   ├── T&E1-biv.clp
│   ├── T&E1.clp
│   ├── T&E2-biv.clp
│   ├── T&E2.clp
│   ├── T&E3-biv.clp
│   └── T&E3.clp
└── UTIL
    ├── CLIPS-utils.clp
    ├── file-utils.clp
    ├── JESS-utils.clp
    ├── stats.clp
    └── utils.clp

86 directories, 56 files


#### Repo-wide data model (shared terms)

* **Candidates:** Let $C$ be the finite set of candidate identifiers (e.g., integers or tuples).
* **Contexts:** Let $K$ be the set of solver contexts (problem instances), elements $k\in K$.
* **CSP types:** Let $P$ be the set of CSP “link” types (the particular constraint under which two candidates are mutually exclusive), elements $p\in P$.
* **Link relation:** A symmetric relation $L \subseteq K\times P\times C\times C$ where $(k,p,c_i,c_j)\in L$ encodes the CLIPS fact `(csp-linked k c_i c_j p)`. For each fixed $(k,p)$, define the boolean adjacency $L_{k,p}\in\{0,1\}^{|C|\times|C|}$ with zeros on the diagonal.
* **ORk record:** An emitted record `(ORk-relation …)` is an “OR-clause” over a small set $S\subseteq C$ with fields `(OR-name, OR-size, OR-candidates, OR-complexity, context)`.

> **NumPy view.** With candidate indexation, represent `csp-linked` as a tensor `L` of shape `( |K|, |P|, |C|, |C| )`, symmetric in the last two axes. Degrees are `deg = L.sum(axis=-1)`.

---

### Bivalue.clp

#### Purpose

Detect “bi-value” pairs: under a given CSP type $p$, a candidate that has exactly one neighbor (degree $=1$) in the `csp-linked` graph, and emit symmetric `(bivalue …)` facts for that pair. This characterizes domains of size 2 under the same CSP (e.g., a variable with exactly two remaining candidates).

#### Main rules (conceptual)

* **`activate-bivalue`, `track-bivalue`**: Gating/verbosity rules controlled by salience and printing flags.
* **`bivalue`**: If `(technique k bivalue)` is active and
  `(csp-linked k c_1 c_2 p)` holds with **no** other `csp-linked` neighbor for `c_1` under $(k,p)$, assert both `(bivalue k c_1 c_2 p)` and `(bivalue k c_2 c_1 p)`.

#### Set-notation definition

For fixed $k\in K, p\in P$, let $\mathrm{Nbr}_{k,p}(c)=\{c'\in C:\ (k,p,c,c')\in L\}$.
Define the bi-value edge set

$$
B_{k,p}=\bigl\{\{c_1,c_2\}\subseteq C:\ c_2\in \mathrm{Nbr}_{k,p}(c_1),\ |\mathrm{Nbr}_{k,p}(c_1)|=1\bigr\}.
$$

The rule asserts both orientations for each unordered $\{c_1,c_2\}\in B_{k,p}$.

#### NumPy/broadcasting sketch

* `deg = L[k,p].sum(-1)` → shape `(C,)`.
* `is_bi = (deg == 1)` → mask `(C,)`.
* `pairs_mask = np.triu(L[k,p] & is_bi[:,None] & is_bi[None,:], k=1)` → `(C,C)`.
* Extract candidate index pairs with `np.argwhere(pairs_mask)`.

#### Inputs/Outputs

* **Inputs (facts):** `(technique k bivalue)`, `(csp-linked k c_i c_j p)`.
* **Outputs (facts):** `(bivalue k c_i c_j p)` for both orientations of each pair.

#### Dependencies & side effects

* Depends on prior population of `csp-linked`.
* Produces `(bivalue …)` which downstream rules (e.g., 2-value) can consume.

---

### 2-value.clp

#### Purpose

Materialize a 2-candidate OR-clause from a detected bi-value pair and expose it uniformly via an `(ORk-relation …)` record with `OR-size = 2` and `OR-name = 2-value` (complexity = 1).

#### Main rules (conceptual)

* **`activate-2-value`, `track-2-value`**: Activation/verbosity.
* **`2-value`**: Under `(technique k 2-value)` (and ancillary/printing controls), collect a bi-value pair $\{c_1,c_2\}$ and assert:

  ```
  (ORk-relation
    (OR-name 2-value)
    (OR-complexity 1)
    (context k)
    (OR-size 2)
    (OR-candidates c1 c2))
  ```

#### Set-notation definition

For each $k$, define the set of size-2 ORs:

$$
\mathcal{O}^{(2)}_k=\bigl\{\ S\subseteq C:\ |S|=2\ \text{and}\ S\in B_{k,p}\ \text{for some }p\in P\bigr\}.
$$

Each $S=\{c_1,c_2\}\in\mathcal{O}^{(2)}_k$ yields one `ORk-relation`.

#### NumPy/broadcasting sketch

* Reuse `pairs_mask` from **Bivalue**; aggregate across $p$ with `any` on the `P` axis if needed.
* Vectorize to a `(N_pairs, 2)` array via `np.argwhere(pairs_mask).reshape(-1,2)`.

#### Inputs/Outputs

* **Inputs:** `(technique k 2-value)`, `(bivalue k c_1 c_2 p)` **or** directly the `csp-linked`/degree pattern (depending on rule body specifics).
* **Outputs:** One `(ORk-relation …)` per 2-set.

#### Dependencies & side effects

* Logically depends on the **Bivalue** detection (or equivalent degree-1 structure).
* Standardizes consumption by later reasoning stages that operate over generic `ORk-relation`s.

---

### 3-value.clp

#### Purpose

Emit size-3 OR-clauses (tri-value) as uniform `(ORk-relation …)` records with `OR-size = 3` and `OR-name = 3-value` (complexity = 1). Semantically, this corresponds to a variable/domain of size 3 under the same CSP type $p$.

#### Main rules (conceptual)

* **`activate-3-value`, `track-3-value`**: Activation/verbosity.
* **`3-value`**: Under `(technique k 3-value)`, identify a triple $\{c_1,c_2,c_3\}$ that forms a closed domain of size 3 under one CSP type (pairwise `csp-linked`, with no links from the triple to additional candidates under that same $(k,p)$), and assert:

  ```
  (ORk-relation
    (OR-name 3-value)
    (OR-complexity 1)
    (context k)
    (OR-size 3)
    (OR-candidates c1 c2 c3))
  ```

#### Set-notation definition

For fixed $(k,p)$, let $L_{k,p}$ be the adjacency. A tri-value set is

$$
T_{k,p}=\bigl\{S\subseteq C:\ |S|=3,\ \forall c_i\neq c_j\in S,\ (k,p,c_i,c_j)\in L,\ \text{and}\ \forall c\in S,\ \mathrm{Nbr}_{k,p}(c)\subseteq S\bigr\}.
$$

Then for each $k$, the 3-value ORs are $\mathcal{O}^{(3)}_k=\bigcup_{p\in P} T_{k,p}$.

> Equivalently, when `csp-linked` for a CSP type $p$ encodes “same variable” mutual exclusion, $|S|=3$ simply means that variable’s domain size is 3.

#### NumPy/broadcasting sketch

* `deg = L[k,p].sum(-1)`; tri-value nodes satisfy `deg == 2`.
* Compute connected components of `L[k,p]` restricted to nodes with `deg==2`; select those components of size 3 whose induced subgraph is complete (all off-diagonal ones).
* Vectorized test: for a candidate mask `m`, the triple $i<j<l$ is valid if

  ```
  L[k,p,i,j] & L[k,p,i,l] & L[k,p,j,l] &
  (deg[i]==2) & (deg[j]==2) & (deg[l]==2)
  ```

#### Inputs/Outputs

* **Inputs:** `(technique k 3-value)`, `(csp-linked …)`.
* **Outputs:** `(ORk-relation …)` with `OR-size 3`.

#### Dependencies & side effects

* Requires a consistent `csp-linked` graph for each $(k,p)$.
* Standardizes tri-value cases for later generic OR-reasoning.

---

#### Cross-file dependencies & portability notes

* **Technique gating:** All three files rely on `(technique k <name>)` facts and salience knobs (e.g., `?*bivalue-salience*`, `?*2-value-salience*`, `?*3-value-salience*`) plus optional printing flags (e.g., `?*print-levels*`). These are orthogonal to the core logic.
* **Data dependency chain:**
  `csp-linked` ⇒ **Bivalue** `(bivalue …)` ⇒ **2-value** `(ORk-relation …)`;
  **3-value** draws directly from `csp-linked` (or an equivalent domain-size-3 characterization).
* **Uniform output surface:** Both **2-value** and **3-value** emit `(ORk-relation …)` with a consistent schema, enabling downstream rules to consume OR-constraints without caring about their origin.

#### NumPy port: canonical shapes & broadcasting contracts

* `L`: `(K, P, C, C)` boolean, symmetric on the last two axes and zero diagonal.
* `deg`: `(K, P, C)` integer = `L.sum(-1)`.
* **Bivalue pairs:** boolean mask `pairs = np.triu((deg==1)[..., :, None] & L & (deg==1)[..., None, :], k=1)` → `(K, P, C, C)`.
* **2-value ORs:** reduce `pairs.any(axis=1)` over `P` if ORs don’t track `p`; otherwise keep `(K, P, C, C)` and index pairs.
* **3-value ORs:** enumerate triples `(i,j,l)` via vectorized broadcasting over `C` with upper-triangle constraints, testing all three edges in `L` and `deg==2` per node; result as indices array `(N_triples, 3)` per `(K,P)`.

These contracts give you a direct, fully-broadcastable path from the CLIPS facts to NumPy operations while preserving the exact set-theoretic intent of the rules.


---

### blocked-rules.clp

#### Purpose

Implements the “end of application” logic for **blocked** and **pseudo-blocked** rules: aggregate eliminations, print them once, then clear the aggregator.

#### Key facts / predicates

* `(apply-rule-as-a-block ?cont)`
* `(blocked ?cont …)` → collected eliminations for a block.
* `(apply-rule-as-a-pseudo-block ?cont)`
* `(pseudo-blocked ?cont …)` → collected eliminations for a pseudo-block.
* `(context (name ?cont))` (logical dependency)
* Globals used: `?*blocked-rule-description*`, `?*blocked-rule-eliminations*`, `?*implication-sign*`, `?*print-actions*`, `?*end-apply-a-blocked-rule-salience(-1|-2)*`.

#### Rules (set-notation view)

Let $\Lambda$ be all labels, and for each context $c$ let $B_c \subseteq \Lambda$ be the per-block accumulator of eliminations.

* **end-apply-a-blocked-rule-1**
  Trigger: `apply-rule-as-a-block(c)` ∧ `blocked(c, …)`
  Action: print $B_c$; clear $B_c$; end block.
  (Second variant `…-2` prints & ends even if no `blocked` fact remains.)
* **end-apply-a-pseudo-blocked-rule**
  Trigger: `apply-rule-as-a-pseudo-block(c)` ∧ `pseudo-blocked(c, …)`
  Action: clear pseudo-block accumulator (no formatted print of rule body).

#### NumPy mapping (shapes & ops)

* Represent $B_c$ as a boolean vector `B[c, :] ∈ {0,1}^{|Λ|}`.
  Printing resets: `B[c, :] = 0`.
* Salience just enforces evaluation order (no direct NumPy analogue).

#### Dependencies

Calls `print-blocked-rule` from **blocked-rules-fns.clp**. Assumes templates for `context`, `blocked`, `pseudo-blocked`, and globals above are defined elsewhere.

---

### blocked-rules-fns.clp

#### Purpose

Tiny helpers to build and flush the “blocked” elimination printout.

#### Functions (I/O & set-notation)

* `add-elimination-to-blocked-rule(?elim)`
  $B_c \leftarrow B_c \cup \{\texttt{elim}\}$.
  (In CLIPS this concatenates to a string; in NumPy: set `B[c, idx(elim)] = True`.)
* `print-blocked-rule()`
  If printing is enabled and $B_c \neq \varnothing$, emit description
  `blocked-rule-description ⇒ blocked-rule-eliminations`; then reset $B_c ← ∅$.

#### NumPy mapping

* Keep a vector `B[c, :]` and clear with `B[c, :] = False`.

#### Dependencies

Uses globals: `?*print-actions*`, `?*blocked-rule-description*`, `?*blocked-rule-eliminations*`, `?*implication-sign*`.

---

### ECP.clp

#### Purpose

**Elementary Constraints Propagation (ECP)**: whenever a value is decided, eliminate all candidates *linked* to it; and ensure a label cannot be both a value and a candidate.

#### Key facts / predicates

* `(technique ?cont BRT)` → gate for basic resolution techniques.
* `(candidate (context ?cont) (status c-value|cand) (label ?ℓ) (flag ?f))`
* `(labels-linked ?v ?c)` → symmetric incompatibility relation on labels.
* Globals: `?*nb-candidates*`, `?*print-all-details*`, `?*print-ECP-details*`.
* Printers: `print-deleted-candidate`.

#### Rules (set-notation view)

Let:

* $\Lambda$ = set of labels.
* For context $c$:
  $V_c \subseteq \Lambda$ = decided labels (status = `c-value`).
  $C_c \subseteq \Lambda$ = current candidates (status = `cand`).
* $L \subseteq \Lambda \times \Lambda$ = “linked” relation from `labels-linked`.

1. **propagate-elementary-constraints**
   If $v \in V_c$ (with `flag = 1`) and $ (v,x)\in L$, then remove $x$ from $C_c$:

   $$
   C_c \leftarrow C_c \setminus \{\,x \in C_c \mid \exists v\in V_c:\ (v,x)\in L\,\}.
   $$

2. **c-value-not-cand**
   Enforce exclusivity:

   $$
   C_c \leftarrow C_c \setminus V_c.
   $$

#### NumPy mapping (broadcast-friendly)

Index labels by `0..n-1`. For a single context:

* `V ∈ {0,1}^n` (decided), `C ∈ {0,1}^n` (candidates), `L ∈ {0,1}^{n×n}` (linked).
* Elimination mask from decided values:

  ```text
  elim = (V @ L) > 0        # shape (n,)
  C    = C & ~elim          # and also: C = C & ~V
  ```

For multiple contexts, stack along axis 0 and rely on broadcasting:

```text
elim = (V @ L) > 0          # (m,n) @ (n,n) → (m,n)
C    = C & ~elim & ~V
```

#### Dependencies

Requires a `candidate` template with slots `(context,status,label,flag)`, `labels-linked` predicate, `technique` fact. Uses counters/printers defined elsewhere.

---

### focused-elims.clp

#### Purpose

Utilities to **try targeted eliminations** and to **probe one-step eliminability** of single candidates and pairs, by running the rulebase on a *focus list* and inspecting the resulting state.

#### Key facts / predicates

* `(candidate-in-focus (context ?cont) (label ?ℓ))` → focus set $F_c$.
* `(candidate (context 0) (status cand) (label ?ℓ))` → current candidates.
* Uses time and printing helpers; global guards `?*t-Whips*`, `?*Typed-t-Whips*`.

#### Functions (set-notation & I/O)

* `try-to-eliminate-candidates-from-context(?cont, $?focus-list)`
  Assert $F_c = \{\texttt{labels in focus-list}\}$; run engine once.
  **Side-effect:** produces new resolution state $RS'_c$.
  **NumPy view:** treat as applying an elimination operator
  $ RS'_c = \mathcal{E}(RS_c;\,F_c)$ (implementation-dependent).

* `try-to-eliminate-candidates($?focus-list)`
  Abbrev for context 0; guards against incompatible techniques.

* `find-erasable-candidates($?cand-list) → list`
  If `cand-list` is empty, use all current candidates $C_0$. For each $x\in \texttt{cand-list}$:
  run $\mathcal{E}(RS_0;\{x\})$; if $x\notin C_0'$ afterwards, collect it.
  Returns $E_1 = \{\,x \mid x \text{ eliminable in one step}\,\}$.

* `find-erasable-pairs($?elim-list) → list-of-pairs` (**expensive**)
  Let $E_1$ be `elim-list` and $C_0$ the current candidates. For each $a\in E_1$:

  1. Temporarily remove $a$: $RS_1 = RS_0 \setminus \{a\}$.
  2. For each $b\in C_0\setminus\{a\}$: run $\mathcal{E}(RS_1;\{a,b\})$.
  3. If $b$ is gone, record pair $(a,b)$.
     Returns $E_2 \subseteq E_1 \times C_0$.

#### NumPy mapping (shapes & ops)

* Focus set as boolean vector `F ∈ {0,1}^n` (or indices).
* State snapshot/restore corresponds to copying arrays representing $C, V,\dots$.
* $\mathcal{E}$ is a placeholder for “run rulebase once with focus”; when porting, make it a vectorized function `E(C, V, F, …) -> (C', V', …)`.
* `find-erasable-candidates`: loop over indices of `cand-list` (can batch later).
* `find-erasable-pairs`: nested loop over `(a,b)`; possible batching by testing many `b` at once against a fixed `a`.

#### Dependencies

* Requires `compute-current-resolution-state`, `init-resolution-state` from **compute-RS.clp** (state capture/restore).
* Uses `candidate` and `candidate-in-focus` templates, printers, timers.

---

### compute-RS.clp

#### Purpose

**Placeholders** for capturing, printing, and restoring a **resolution state** (RS) in a given context. They currently return trivial values and must be implemented by the application.

#### Functions (intended contracts)

* `compute-current-resolution-state-in-context(?cont) → RS_c`
* `print-/pretty-print-current-resolution-state-in-context(?cont)`
* `init-context-with-resolution-state(?cont, $?RS)`
* Context-0 shorthands: `compute-current-resolution-state`, `print-current-resolution-state`, `init-resolution-state`, plus solution printers.

#### Set-notation for RS (for NumPy design)

Define the resolution state for context $c$ as a tuple

$$
RS_c = \big(C_c,\ V_c,\ \ldots\big),
$$

where:

* $C_c \in \{0,1\}^{|\Lambda|}$ (candidate mask),
* $V_c \in \{0,1\}^{|\Lambda|}$ (decided/value mask),
* optional arrays: givens, constraints, metadata.
  The “snapshot” functions should serialize/deserialize these arrays.

#### NumPy mapping

* Implement `compute-*` to **read** current masks from engine → NumPy arrays.
* Implement `init-*` to **write** arrays back into the engine (or the NumPy-only port) to restore a snapshot.

#### Dependencies

No hard dependencies inside this file; all functions are hooks to be overridden by the application layer.

---

#### Common objects & notation (for the NumPy port)

* **Labels:** $\Lambda = \{0,\dots,n-1\}$.
* **Contexts:** $c \in \{0,\dots,m-1\}$ (use $m=1$ with $c=0$ if single puzzle).
* **Candidates:** `C[m,n]` boolean.
* **Values (decided):** `V[m,n]` boolean (optionally `Vflag[m,n]` for the `flag` slot).
* **Linked relation:** `L[n,n]` symmetric boolean adjacency.
  ECP update (vectorized):

  ```text
  elim = (Vflag @ L) > 0         # (m,n) → (m,n)
  C    = C & ~elim & ~V
  ```
* **Focus set:** `F[m,n]` boolean (often sparse); used to restrict which labels are considered by elimination procedures.
* **Blocked aggregation:** per-context `B[m,n]` boolean; cleared after printing.

This overview should let us port these rule modules to NumPy by:

1. representing facts as boolean arrays and relations,
2. expressing propagation as masked matrix ops, and
3. re-implementing the probe utilities (`find-erasable-*`) as batched array transforms over `RS`.


---

### gBivalue.clp

#### Purpose

Derive the symmetric **g-bivalue** relation between two candidates within a CSP variable when enabled.

#### Core sets & notation

* $V$: set of CSP variables.
* $L$: set of labels (variable–value pairs).
* $C\subseteq L$: set of current candidates.
* $\mathrm{CONT}$: set of solving contexts.
* $E^{\mathrm{csp}}\subseteq C\times C\times V$: “csp-glinked” relation.
* $E^{\mathrm{gCSP}}\subseteq C\times C\times V$: “g-candidates-csp-glinked” relation.
* $I\subseteq L\times G$: label ∈ glabel (membership).

Define the **g-bivalue** relation:

$$
\mathrm{GBV}\;=\;\{(k,x,y,v)\in \mathrm{CONT}\times C\times C\times V:\; 
(x<y)\;\wedge\;[\,(k,x,y,v)\in B\;\;\vee\;\;(k,x,y,v)\in E^{\mathrm{csp}}\setminus\exists x'\neq x\;E^{\mathrm{csp}}(k,x',y,v)\;\;\vee
$$

$$
\qquad\qquad (k,x,y,v)\in E^{\mathrm{gCSP}}\setminus\exists x'\;(\neg I(x',x))\wedge E^{\mathrm{csp}}(k,x',y,v)\,]\}
$$

and the rule asserts both directions, so the effective relation is the symmetric closure:

$$
\mathrm{g\mbox{-}bivalue}\;=\;\mathrm{GBV}\;\cup\;\{(k,y,x,v):(k,x,y,v)\in \mathrm{GBV}\}.
$$

#### Key rule

* `defrule g-bivalue`: If `(technique k g-bivalue)` and any of the three bullets above hold, assert `(g-bivalue k x y v)` and `(g-bivalue k y x v)`.

#### Dependencies

* Facts/relations required: `bivalue`, `csp-glinked`, `g-candidates-csp-glinked`, `label-in-glabel`, `technique`.
* Uses salience `?*g-bivalue-salience-2*` (from globals).

#### Inputs/Outputs

* **In:** context $k$, candidates $x,y$, variable $v$; link/membership relations.
* **Out:** facts `(g-bivalue k x y v)` and `(g-bivalue k y x v)`.

#### NumPy/broadcasting sketch

* Represent $E^{\mathrm{csp}}$ as `E_csp[k, v, i, j]` (bool, symmetric in i,j).
* Represent $E^{\mathrm{gCSP}}$ similarly.
* `label-in-glabel` as `I[i, g]`.
* Compute GBV with vectorized masks over axes `(i,j)` per `(k,v)`, then OR the three conditions; symmetrize with `GBV |= GBV.swapaxes(-1,-2)`.

---

### generic-background.clp

#### Purpose

Provide generic, application-neutral helpers for links, glinks, g2-links, membership in glabels, and derived link notions (bi-whip/bi-braid), isolating rule logic from app-specific implementations.

#### Core sets & notation

* $V,L,C$ as above; $G$: set of glabels.
* **Label–label links:** $E\subseteq L\times L$ (symmetric, irreflexive).
* **Label–glabel glinks:** $E^{\mathrm{LG}}\subseteq L\times G$ (glinks).
* **Label ∈ glabel membership:** $I\subseteq L\times G$ (inclusion).
* **g2-link:** $E^{\mathrm{g2}}\subseteq L\times(L\times L)$ (a label linked to an OR of two labels).
* **Derived contradictory pairs:**

  * $B^{\mathrm{biwhip}}\subseteq L\times L$
  * $B^{\mathrm{bibraid}}\subseteq L\times L$
* **Convenience unions:**
  $\tilde E^{\mathrm{biwhip}}=E\;\cup\;B^{\mathrm{biwhip}}$,
  $\tilde E^{\mathrm{bibraid}}=E\;\cup\;B^{\mathrm{bibraid}}$.

#### Principal functions (signatures → set/logic meaning)

* `labels-linked(x,y)` / `linked(x,y)` → $(x,y)\in E$.
* `add-label-link(x,y)` / `add-link(x,y)` / `add-csp-link(x,y)` → insert into $E$ (possibly namespaced per CSP).
* `label-glabel-glinked(x,g)` / `glinked(x,g)` / `add-glink(x,g)` → $(x,g)\in E^{\mathrm{LG}}$.
* `label-in-glabel(x,g)` / `add-label-in-glabel(x,g)` → $(x,g)\in I$.
* `glabel-contains-none-of(g, S)` / `glabel-contains-some-of(g, S)` → set predicates over $I$.
* `g2-linked(x, a, b)` / `g2-linked-or(x, zzz, A, B)` → $(x,(a,b))\in E^{\mathrm{g2}}$.
* `biwhip-linked(x,y)` / `bibraid-linked(x,y)` → membership in $\tilde E^{\mathrm{biwhip}}$ / $\tilde E^{\mathrm{bibraid}}$.
* `contradictory-pair(x,y)` → pair belongs to some contradictory-pairs set.
* `same-sets-of-rlcs(rlc1, RL1, RL2)` → $\{rlc1\}\cup RL1 = RL2$ (as sets).

#### Invariants

* `label-pair` orders pairs with the smaller label first; $E$ is stored with canonical ordering.
* All membership checks are pure; mutators push into the corresponding global multisets/lists.

#### Dependencies

* Relies on global multisets like `?*label-links*`, `?*label-glabel-glinks*`, `?*label-in-glabel*`, `?*all-biwhip-contrads*` (see globals).

#### NumPy/broadcasting sketch

* $E$ → `A_LL[nL,nL]` (bool; maintain symmetry and zero diagonal).
* $E^{LG}$, $I$ → `A_LG[nL,nG]`, `I_LG[nL,nG]`.
* $E^{g2}$ → either a sparse 3-tensor `A_g2[nL,nL,nL]` or store as two boolean matrices per left label.
* `*_linked-or(x, S)` → vectorized `A_LL[x, S].any(-1)`.
* `glabel-contains-*` → reductions over `I_LG[:, g]`.
* `same-sets-of-rlcs` → set-equality via sorted unique or bitset rows; broadcast compare.

---

### generic-output.clp

#### Purpose

All text/console rendering utilities for variables, labels, cells, chains (z-chains, t-whips, whips/braids, g-chains, ORk variants), eliminations and assertions.

#### Conceptual I/O types (for porting)

* Label/variable/value naming:
  `label-name(ℓ)`, `csp-variable-name(v)`, `label-value-name(ℓ,v)`, `label-csp-variable(ℓ,v)` → `str`.
* Cells:

  * `print-pair-in-cell(x,y)` prints $\langle x\,|\,y\rangle$.
  * `print-final-pair-in-cell(x)` prints $\langle x\,|\,\cdot\rangle$.
* Chains (common signature):

  $$
  \texttt{print-<type>(p, z, LLCS, RLCS, CSPS, new\_llc, dot, new\_csp)}
  $$

  where
  $LLCS\in L^{p}$, $RLCS\in (L\cup\{\cdot\})^{p}$, $CSPS\in V^{p}$, `dot∈{·, label}`, `new_*` are terminal cell items.
  Specialized wrappers exist for `z-chain`, `t-chain`, `whip`, `braid`, `gwhip`, `gbraid`, and ORk variants (k=2..8), plus “forcing/contrad” flavors and partial chains.

#### Dependencies

* Delegates semantic info to helpers defined elsewhere (names, links, candidates).
* Controlled by many `?*print-*` and symbol globals (signs, separators).

#### NumPy/broadcasting sketch

* Treat sequences as integer arrays: `LLCS[p]`, `RLCS[p]` (with a sentinel index for `·`), `CSPS[p]`.
* Rendering can be done by vectorized gather → map to strings, then join.
* ORk tails: stack candidates as `(k,)` arrays and format with a small `vmap` over axis 0.

---

### glabels.clp

#### Purpose

Entry point to **define glabels and glinks** for a specific CSP application.

#### Core contracts

* `define-glabels-and-glinks()` must:

  * Instantiate $G$ (glabels).
  * Populate $I\subseteq L\times G$ (membership) and/or $E^{LG}\subseteq L\times G$ (glinks).
  * Be app-specific (e.g., Sudoku houses, Kakuro sums, etc.).

#### Dependencies

* Uses/sets the global containers consumed by `generic-background.clp`.

#### NumPy/broadcasting sketch

* Build `A_LG` / `I_LG` from app primitives (e.g., incidence matrices between labels and higher-level groups), ideally via sparse construction and then densify if needed.

---

### globals.clp

#### Purpose

Centralize configuration, feature toggles, limits, counters, symbol strings, and all global containers for links, glinks, memberships, and derived contradiction sets.

#### Core sets & containers (conceptual → globals)

* Version/engine info; CLIPS strategy.
* **Link stores** (as multisets/lists in CLIPS; model as matrices/sets in NumPy):

  * `?*label-links*` → $E\subseteq L\times L$.
  * `?*glinks*` → $E^{LG}\subseteq L\times G$.
  * `?*label-glabel-glinks*` → another store for $E^{LG}$.
  * `?*label-in-glabel*` → $I\subseteq L\times G$.
  * `?*biwhip-contrads[k]*`, `?*bibraid-contrads[k]*`, and `?*all-biwhip-contrads*` → $B^{\cdot}\subseteq L\times L$ partitioned by length $k$.
* **Context/runtime:** counters, timers, flags like `?*solution-found*`, instance timing.
* **Technique toggles:** booleans enabling Z-chains, t-whips, (g)whips, (g)braids, ORk variants (forcing/contrad), exotic patterns (oddagons), etc.
* **Length bounds:** `?*absolute-chains-max-length*`, per-technique max lengths; consistency rules propagate bounds across families.
* **Printing controls:** thousands of `?*print-…*` flags by technique and length (enable per-length tracing).

#### Dependencies

* Every other file reads/writes these; this file is foundational.

#### NumPy/broadcasting sketch

* Map each link store to a boolean ndarray:

  * `A_LL[nL,nL]`, `A_LG[nL,nG]`, `I_LG[nL,nG]`, plus per-k contradiction `A_biwhip[k,nL,nL]`, etc.
* Toggles/limits → simple scalars used to gate kernels.
* Symmetry/irreflexivity enforced by masking:

  * `A_LL = np.triu(A_LL,1); A_LL |= A_LL.T`.
* Accumulate “all-contrads” by OR-reducing across k: `A_biwhip_all = A_biwhip.any(axis=0)`.

---

#### Cross-file dependency snapshot

* **globals.clp** defines all state/toggles used elsewhere.
* **generic-background.clp** reads/writes link/membership sets from **globals**.
* **gBivalue.clp** consumes those relations to assert symmetric `g-bivalue` facts when `technique(..., g-bivalue)` is on.
* **generic-output.clp** formats results; it relies on naming and link/membership accessors but has no solving logic.
* **glabels.clp** is the app-specific constructor for $G$, $I$, and $E^{LG}$, feeding **generic-background**.

This structure should port cleanly to NumPy: represent each relation as a boolean array (or sparse), index labels/variables/glabels densely, and implement the predicates as vectorized logical expressions and reductions (any/all) with broadcasting across `(context, variable, i, j)` axes.


---

### Repository (cross-file overview)

#### Purpose

Formalize **candidates**, **links**, and **g-links** for CSP search and chain techniques, and orchestrate when they’re built and used.

#### Core sets & relations (for NumPy port)

* Contexts: $\mathcal{C}$.
* Labels (candidate ids): $\mathcal{L}$. Per-context active set $\mathcal{L}_c \subseteq \mathcal{L}$.
* CSP variables: $\mathcal{V}$ with a total function $v:\mathcal{L}\to\mathcal{V}$ (slot `is-csp-variable-for-label`).
* Application links: symmetric relation $E_{\text{app}} \subseteq \mathcal{L}\times\mathcal{L}$ (predicate `labels-linked`).
* CSP links: symmetric relation $E_{\text{csp}}=\{(\ell_i,\ell_j)\mid v(\ell_i)=v(\ell_j),\, i\neq j\}$.
* Effective links: $E=E_{\text{csp}}\cup E_{\text{app}}$.
* g-labels / g-candidates: $\mathcal{G}$ with membership/incidence $B\subseteq \mathcal{L}\times\mathcal{G}$ and map $v_g:\mathcal{G}\to\mathcal{V}$.
* g-links:

  * CSP g-links: $E^{g}_{\text{csp}}=\{(x,y)\in(\mathcal{L}\cup\mathcal{G})^2 \mid v^\star(x)=v^\star(y),\,x\neq y\}$ where $v^\star$ extends $v$ and $v_g$.
  * Non-CSP g-links: $E^{g}_{\text{app}}\subseteq (\mathcal{L}\cup\mathcal{G})^2$ (predicate `label-glabel-glinked` and similar).
  * Effective g-links: $E^g=E^{g}_{\text{csp}}\cup E^{g}_{\text{app}}$.

#### NumPy representation sketch

* Index labels and g-labels: arrays `L_idx` (|L|,), `G_idx` (|G|,).
* Map label→var: `var_of_L` (|L|,) ints; map g-label→var: `var_of_G` (|G|,).
* Candidate activity per context: `active[c, l] ∈ {0,1}`.
* CSP link adjacency (labels): `A_csp = (var_of_L[:,None] == var_of_L[None,:]) & ~np.eye(|L|,bool)`.
* App link adjacency (labels): sparse or boolean `A_app` from `labels-linked`.
* Effective links: `A = A_csp | A_app`.
* Incidence label↔g-label: `B` (|L|×|G|, bool) from glabel definitions.
* g-link adjacency as block matrix

  $$
  A^g=\begin{bmatrix}
  A_{LL} & A_{LG}\\
  A_{GL} & A_{GG}
  \end{bmatrix}
  $$

  with $A_{LL}=A$, $A_{LG}=B \lor A^{\text{app}}_{LG}$, $A_{GG}$ from g-structure (often sparse/zero unless defined).
* Use broadcasting to build CSP blocks:

  * `A_LL_csp = (var_of_L[:,None] == var_of_L[None,:]) & ~I`
  * `A_LG_csp = (var_of_L[:,None] == var_of_G[None,:])`
  * `A_GG_csp = (var_of_G[:,None] == var_of_G[None,:]) & ~I`

---

### init-links.clp

#### Purpose

Create **effective links** between existing candidates: (1) CSP-based links from `is-csp-variable-for-label`; (2) application links from `labels-linked`. Counts links and avoids duplicates via `exists-link` and `csp-linked`.

#### Key predicates & functions

* Input facts: `(candidate (context ?cont) (status cand) (label ?cand))`, `(is-csp-variable-for-label (csp-var ?csp) (label ?cand))`.
* External dependency (app-specific): `labels-linked(?cand1 ?cand2)`.
* Derived facts: `(csp-linked ?cont ?cand1 ?cand2 ?csp)`, `(exists-link ?cont ?cand1 ?cand2)`.
* Side effects / counters: updates `?*csp-links-count*`, `add-link`.

#### Set notation

* For context $c$: build $E_{\text{csp},c}=\{(\ell_i,\ell_j)\in\mathcal{L}_c^2\mid v(\ell_i)=v(\ell_j),\,i<j\}$.
* Build $E_{\text{app},c}=\{(\ell_i,\ell_j)\in\mathcal{L}_c^2\mid i<j \land \texttt{labels-linked}(\ell_i,\ell_j)\}$.
* Assert both orientations; track uniqueness with `exists-link`.

#### NumPy port notes

* Given `var_of_L` and `active[c]`:

  * `mask = np.ix_(active[c], active[c])`
  * `A_csp[c][mask] = (var_of_L[:,None]==var_of_L[None,:]) & ~I`
* Fill `A_app` from app callback; union to get `A`.
* Maintain counts as `A`’s upper-triangle `sum()`.

#### Notable rules (as implemented)

* `activate-init-links` (gates on `(technique ?cont BRT)` / `(context ...)`).
* `init-effective-csp-links` (asserts `csp-linked`).
* `init-effective-non-csp-links` (asserts `exists-link` including CSP pairs once; increments global link count via `add-link`).

---

### init-glinks.clp

#### Purpose

Initialize **g-candidates** and **effective g-links** once all glabels and physical g-links are defined. Activated only when G-chains (e.g., G-Bivalue-Chains, G-Whips, G-Braids) are in use.

#### Dependencies

* Precondition fact: `(glabels-and-glinks-defined)`.
* Stage facts: `(technique ?cont g-candidates)` (this file asserts it).
* Uses: `(g-candidate (context ?cont) (label ?glab) (csp-var ?csp))`, `(candidate ...)`.
* External function: `label-glabel-glinked(?lab ?glab)`.
* CSP mapping: `(is-csp-variable-for-label (csp-var ?csp) (label ?lab))`.

#### Set notation

* G-candidates: $\mathcal{G}_c \subseteq \mathcal{G}$ established from prebuilt glabels.
* Non-CSP g-links: $E^{g}_{\text{app},c}\supseteq\{(\ell,g)\mid \ell\in\mathcal{L}_c,\ g\in\mathcal{G}_c,\ \texttt{label-glabel-glinked}(\ell,g)\ \land\ v(\ell)\neq v_g(g)\}$.
* CSP g-links: $E^{g}_{\text{csp},c}=\{(x,y)\in(\mathcal{L}_c\cup\mathcal{G}_c)^2 \mid v^\star(x)=v^\star(y), x\neq y\}$.
* Effective g-links: $E^g_c=E^{g}_{\text{csp},c}\cup E^{g}_{\text{app},c}$.
* Duplicate prevention: `(exists-glink ?cont ?x ?y)`.

#### NumPy port notes

* Build `var_of_G` and `B` (label↔g-label incidence).
* Use broadcasting equalities (see repo overview) to create CSP blocks:

  * `A_LG_csp = var_of_L[:,None] == var_of_G[None,:]`
* Build `A_LG_app` from `label-glabel-glinked`; then `A^g` blockwise OR.
* Keep counters: totals of g-candidates and (CSP/non-CSP) g-links.

#### Notable rules

* `activate-init-g-labels` / `track-init-g-labels` (progress logging).
* `init-g-candidates` (asserts g-candidates; gated by `glabels-and-glinks-defined`).
* `init-effective-non-csp-glinks` (asserts label↔g-label g-links when not CSP).
* `init-effective-glinks-end` (prints counts).

---

### is-cspvar-for-cand.clp

#### Purpose

Utility (currently noted “not used”) that materializes the mapping **candidate → CSP variable** at the *candidate* granularity.

#### Predicate produced

* `(is-csp-variable-for-candidate (csp-var ?csp-var) (label ?cand) (csp-var-type ?type))`.

#### Set notation

* Function $v_{\text{cand}}:\mathcal{L}\to\mathcal{V}\times\mathcal{T}$ where $\mathcal{T}$ are variable types.

#### NumPy port notes

* Redundant if `var_of_L` already exists; keep loader to build `var_of_L` and optional `type_of_L`.

---

### is-cspvar-for-gcand.clp

#### Purpose

Utility (currently noted “not used”) that materializes the mapping **g-candidate → CSP variable** at the *g-candidate* granularity.

#### Predicate produced

* `(is-csp-variable-for-g-candidate (csp-var ?csp-var) (glabel ?gcand) (csp-var-type ?type))`.

#### Set notation

* Function $v_g:\mathcal{G}\to\mathcal{V}\times\mathcal{T}$.

#### NumPy port notes

* Produces `var_of_G` (and optional `type_of_G`) used in g-link broadcasting.

---

### manage.clp

#### Purpose

Drive the resolution lifecycle: when to build links (BRT completion), when to assert `(play)`, when to switch to chain rules / T\&E / DFS, and when to print solution or final state.

#### Orchestration facts & flow

* Presence of typed chains toggles whether to build links before deeper rules.
* When no more BRT rules apply:

  * If solution found: assert `(print-solution-in-context ?cont)` or halt.
  * Else if whips\[1] enabled: compute links then `(play)` to start advanced rules.
  * Else if T\&E/DFS enabled: `(play)` to start them.
* End condition: print final state or solution based on flags.

#### Set/array view for NumPy port

* Treat as **pipeline stages** rather than data:

  1. Build `active[c]` from candidates.
  2. Build `A_csp`, `A_app`, `A`, optionally `A^g`.
  3. Hand off to higher-level solvers (chains / DFS) that consume these arrays.

---

## Inputs / Outputs by file (quick matrix)

#### Inputs (facts/functions)

* `candidate(context, status, label)` → init-links, init-glinks, manage.
* `is-csp-variable-for-label(csp-var, label)` → init-links, init-glinks.
* `labels-linked(l1,l2)` (app function) → init-links.
* `label-glabel-glinked(l,g)` (app function) → init-glinks.
* `glabels-and-glinks-defined` → init-glinks.
* Stage/flow: `context(name)`, `technique(ctx, ...)`, `play`, `solution-found`.

#### Outputs (facts/counters)

* `csp-linked(ctx, l1, l2, v)`, `exists-link(ctx, l1, l2)`; global counts.
* `g-candidate(ctx, g, v)`, `glink(...)` / `exists-glink(...)`; global g-counts.
* Printing/termination triggers in manage: `print-solution-in-context`, final state.

---

## What to precompute for the NumPy port

#### Indices & mappings

* `label_index: dict[label_id→i]`, `glabel_index: dict[g_id→j]`.
* `var_index: dict[var_id→k]`.
* Arrays: `var_of_L[i]=k`, `var_of_G[j]=k`, `active[c,i]∈{0,1}`.

#### Broadcast builds (all boolean; cast to sparse as needed)

* Labels:

  * `A_csp = (var_of_L[:,None]==var_of_L[None,:]) & ~I`
  * `A_app` from callbacks; ensure symmetry & zero diag
  * `A = A_csp | A_app`
* g-structure:

  * `B_LG` from glabel membership
  * `A_LG_csp = (var_of_L[:,None]==var_of_G[None,:])`
  * `A_GG_csp = (var_of_G[:,None]==var_of_G[None,:]) & ~I`
  * `A^g` blockwise OR with any app-level g-links

#### Counts (to match CLIPS logs)

* `num_links = np.triu(A,1).sum()`
* `num_csp_links = np.triu(A_csp,1).sum()`
* `num_g_links` analogously from `A^g`.

---

If you want, I can sketch a tiny adapter that ingests your current facts (candidates, var mapping, app link callbacks) and emits these NumPy arrays so we can start porting chain rules next.


---


Nice drop! I skimmed the CLIPS files you uploaded and mapped out what you’ve got:

### What each file is for (quick map)

* **`parameters.clp`** — global symbols & name helpers
  • 23 `defglobal`s for things like the equal sign, link separator, and naming symbols (row/col/block/etc.)
  • 10 small `deffunction`s such as `row-name`, `column-name`, `block-name`, … (helpers to form pretty labels).

* **`saliences.clp`** — salience “catalog”
  • A *lot* of rule-priority globals (≈ **7,833** `defglobal`s) plus \~**215** helper `deffunction`s to assign/organize saliences.
  • Includes `?*simulated-eliminations-salience*` (default `0`) and functions like `define-simulated-eliminations-saliences`.

* **`SimulatedElim.clp`** — one focused rule
  • A single rule: **`simulated-elimination-rule`**.
  • When a **`candidate`** fact is in **context 0** *and* its `label` is a member of `?*simulated-eliminations*`, the rule:

  1. retracts that fact,
  2. decrements `?*nb-candidates*`,
  3. prints `Simulated elimination of <label>`.

* **`nrc-output.clp`** — printing/pretty output utilities
  • Many formatters like `print-bivalue-cell`, triplet printers, row/column/number renderers, etc.
  • These expect core functions such as `label-number`, `label-cell`, `cell-row`, `cell-column`, `csp-var-type`, `print-row`, `print-column`, etc., which are defined in other (not uploaded) core files.

* **`play.clp`** — “start play” entrypoint
  • Prints a post-Singles resolution state (if `?*print-actions*` and `?*print-RS-after-Singles*` are true), then asserts `(play)` and `(play-already-asserted)` to kick the main solver.
  • References globals/counters you haven’t included here (e.g., `?*nb-candidates*`, `?*csp-links-count*`, `?*links-count*`, `?*density*`, `?*print-actions*`, `?*print-RS-after-Singles*`).

### What’s missing to run the full solver

The uploaded set looks like a **subset** of the CSP-Rules library. To actually run “play” you’ll still need the core pieces that define:

* the **`candidate`** template and initial facts
* core counters/globals: `?*nb-candidates*`, `?*csp-links-count*`, `?*links-count*`, `?*density*`, `?*print-actions*`, …
* utility functions used by `nrc-output.clp`: `label-number`, `label-cell`, `cell-row/column`, `print-row/col/number`, `csp-var-type`, etc.

### A tiny runnable demo I made for you

To prove out **`SimulatedElim`**, I built a **minimal harness** that defines the needed globals/template and seeds a few candidates so you can see the rule fire in a clean CLIPS session.

[Download `demo_simulated_elim.clp`](sandbox:/mnt/data/demo_simulated_elim.clp)

**How to run the demo in CLIPS:**

```
CLIPS> (clear)
CLIPS> (load "demo_simulated_elim.clp")
CLIPS> (reset)
CLIPS> (run)
```

You should see:

```
Simulated elimination of a2
Simulated elimination of r3c4
Remaining candidates in context 0:
 - x9
nb-candidates = 1
```

(Feel free to edit the `?*simulated-eliminations*` list in that file to try other labels.)

### Suggested next steps (pick any)

* **Wire up a full run:** If you share the remaining CSP-Rules core files, I’ll assemble a `load-all.clp` in the correct order and add a one-command `(solve ...)` entrypoint.
* **Tune saliences:** If you want, I can extract and show just the salience globals relevant to your workflow (e.g., everything around simulated eliminations and early-game rules) so you can tweak priorities without wading through the 1.4MB file.
* **Custom logging:** I can integrate a slimmer `nrc-output` that only prints the formats you care about (e.g., bivalue cells and eliminations).

If you tell me your end goal (benchmarking a rule, porting to Jess, running a specific puzzle, etc.), I’ll tailor the setup right away.


---


Nice—looks like you dropped in a handful of CLIPS rulebase files from Denis Berthier’s **CSP-Rules (generic)** core. I took a look and set you up with a tiny starter pack so you can load and run them quickly.

# What’s in your upload (short + sweet)

* **templates.clp** — core `deftemplate`s for candidates, CSP variables, contexts (for T\&E), chains, etc.
* **solve.clp** — driver functions (`init-instance`, `solve`, timing + banners). `solve` does `(reset)`, calls `init-instance`, then `(run)`.
* **track-levels.clp** — rules to enter/track difficulty **levels L1…L36, L99** (controlled by globals like `?*max-level*`).
* **Single.clp** — the **single** technique: when a CSP variable has one remaining candidate, assert it as a `c-value`.
* **Typed-Bivalue.clp** — **typed-bivalue** activation/tracking; derives `typed-bivalue` facts from `csp-linked`.

# Handy loader + README

I generated two helper files you can download:

* [README-CLIPS-CSP-Rules.md](sandbox:/mnt/data/README-CLIPS-CSP-Rules.md) — quickstart, load order, expected app hooks, minimal session snippet.
* [load-generic.clp](sandbox:/mnt/data/load-generic.clp) — loads your five files in a sensible order.

# Quick load order (inline)

```clips
(load "templates.clp")
(load "solve.clp")
(load "track-levels.clp")
(load "Single.clp")
(load "Typed-Bivalue.clp")
```

# What you’ll still need (app layer)

This generic core expects an **application-specific** layer to provide:

* `redefine-instance-globals`, `init-general-application-structures`, `init-instance-specific-structures`
* Problem relations like `csp-linked` and mappings such as `is-csp-variable-for-label` (or the *\_glabel*/*\_candidate* variants)
* (Optionally) app-specific slots on `candidate` / `g-candidate` (e.g., Sudoku: `row/column/block`) and faster, specialized versions of generic techniques

If you tell me your target CSP (Sudoku? Kakuro? something else), I can draft the minimal app layer that plugs into these files so `solve` actually runs a puzzle end-to-end.
