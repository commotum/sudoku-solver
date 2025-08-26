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


## CSP-Rules-Generic

### CSP-Rules-Generic-Loader.clp
- Bootstrap script that batches all generic modules; no functions or rules defined.

---

## GENERAL

### 2-value.clp
- Introduces pattern for cells with two candidates.
- **Rules:** `activate-2-value`, `track-2-value`, `2-value`.

### 3-value.clp
- Manages three‑candidate cells.
- **Rules:** `activate-3-value`, `track-3-value`, `3-value`.

### Bivalue.clp
- Identifies bivalue cells for chain building.
- **Rules:** `activate-bivalue`, `track-bivalue`, `bivalue`.

### Typed-Bivalue.clp
- Same as above but typed by CSP variable.
- **Rules:** `activate-typed-bivalue`, `track-typed-bivalue`, `typed-bivalue`.

### gBivalue.clp
- Handles generalized bivalue cells via g-links.
- **Rules:** `activate-g-bivalue`, `track-g-bivalue`, `g-candidates-csp-glinked`, `g-bivalue`.

### Single.clp
- Naked/hidden single propagation.
- **Rules:** `activate-single`, `single`.

### SimulatedElim.clp
- Generic simulated‑elimination hook.
- **Rule:** `simulated-elimination-rule`.

### ECP.clp
- Elementary constraint propagation.
- **Rules:** `propagate-elementary-constraints`, `c-value-not-cand`.

### compute-RS.clp
- Extensive library for printing resolution states and configuring salience.
- **Functions:** `print-solution-in-context`, `compute-current-resolution-state`, `define-first-L1-salience`…`define-first-L36-salience`, `define-saliences-at-L1`…`define-saliences-at-L36`, `initialise-saliences`, and dozens of printing helpers for chains/whips/g-whips.

### glabels.clp
- Builds global labels and links.
- **Function:** `define-glabels-and-glinks`.

### globals.clp
- Defines and initialises solver-wide globals.
- **Functions:** `init-universal-globals`, `init-specific-globals`, `init-lists-for-files`, `redefine-all-generic-chains-max-length`, `enforce-generic-rules-dependencies`, `define-generic-rating-type`, `define-application-specific-rating-type`, `check-config-selection`, `mute-print-options`, `restore-print-options`, `initialise-biwhip-contrads`, `initialise-bibraid-contrads`.

### init-glinks.clp
- Creates initial g-links and g-candidates.
- **Rules:** `activate-init-g-labels`, `track-init-g-labels`, `init-g-labels`, `activate-init-g-candidates`, `track-init-g-candidates`, `init-g-candidates`, `init-effective-csp-glinks-1/2`, `init-effective-non-csp-glinks`, `init-effective-glinks-end`.

### init-links.clp
- Similar for standard links.
- **Rules:** `activate-init-links`, `track-init-links`, `init-effective-csp-links`, `init-effective-non-csp-links`.

### is-cspvar-for-cand.clp
- Asserts CSP variable membership for labels.
- **Rule:** `is-csp-variable-for-candidate`.

### is-cspvar-for-gcand.clp
- Same for generalized candidates.
- **Rule:** `is-csp-variable-for-g-candidate`.

### blocked-rules.clp
- Tracks when solver exits a blocked rule.
- **Rules:** `end-apply-a-blocked-rule-1`, `end-apply-a-blocked-rule-2`, `end-apply-a-pseudo-blocked-rule`.

### blocked-rules-fns.clp
- Utilities for blocked rules.
- **Functions:** `add-elimination-to-blocked-rule`, `print-blocked-rule`.

### focused-elims.clp
- Support for targeted eliminations.
- **Functions:** `try-to-eliminate-candidates-from-context`, `try-to-eliminate-candidates`, `try-to-eliminate`, `find-erasable-candidates`, `find-erasable-pairs`.

### generic-background.clp
- Fundamental label/glabel utilities.
- **Functions:** `csp-var-type`, `label-pair`, `labels-linked`, `add-link`, `glinked`, `g2-linked`, `biwhip-linked`, `contradictory-pair`, etc.

### generic-output.clp
- Low‑level printing helpers for cells, pairs, chains, typed chains, OR‑chains, etc.
- **Functions:** `print-starting-cell-symbol`, `print-label`, `print-chain`, `print-whip`, `print-gwhip`, `print-braid`, `print-ORk-whip`, `print-forcing-gbraid`, `print-biwhip-contrad`, and many other chain printers.

### nrc-output.clp
- Application‑neutral cell/number printers.
- **Functions:** `print-number`, `print-numeral`, `print-row`, `print-column`, `print-block`, `print-square`, `print-bivalue-cell`, `print-deleted-candidate`, `print-g2number-pair`, etc.

### parameters.clp
- Declares configuration parameters; no functions.

### play.clp
- Enables rules beyond basic resolution at startup.
- **Rule:** `enable-rules-beyond-BRT-in-initial-context`.

### saliences.clp
- Global salience schedule.
- **Functions:** `define-highest-salience`, `define-specific-init-saliences`, `define-generic-init-links-saliences`, `define-bivalue-saliences`, `define-2-value-saliences`, `define-generic-saliences-at-L1…L36`, plus placeholders for application‑specific saliences.

### solve.clp
- High‑level solver entry points.
- **Functions:** `print-start-banner`, `print-banner`, `seconds-to-hours`, `redefine-instance-globals`, `init-general-application-structures`, `init-instance-specific-structures`, `init-instance`, `init`, `solve`.

### templates.clp
- CLIPS template definitions; no functions.

### track-levels.clp
- Maintains solving level information.
- **Rules:** For each level L1–L36 (and L99), `enter-level-Ln` and `track-level-Ln` are provided.

---

## MODULES

### modules.clp
- Generic loader for named modules and preference solving.
- **Functions:** `load-modules`, `solve-w-preferences`.

### enter-module.clp
- Hook to register a module into current session.
- **Rule:** `enter-module`.

### BIVALUE-CHAINS-module.clp, BRT-module.clp, REVERSIBLE-CHAINS-module.clp, W1-module.clp
- Module metadata files; no functions or rules.

---

## UTIL

### CLIPS-utils.clp
- Set operations for CLIPS.
- **Functions:** `union$`, `complement$`, `intersection$`.

### JESS-utils.clp
- Compatibility shim for JESS.
- **Function:** `load` (delegates to batch).

### file-utils.clp
- File manipulation utilities.
- **Functions:** `file-exists`, `empty-file`, `file-length`, `extract-nth-data-from-each-line`, `compare-files`, `compare-levels-in-5-files`, etc.

### stats.clp
- Statistical helpers.
- **Functions:** `file-mean-and-sd`, `correlation-coefficient`, `X-distribution`, `diff-X-Y-distribution`, etc.

### utils.clp
- Assorted math/list helpers.
- **Functions:** `exor`, `first`, `create-list-of-0s`, `factorial`, `set-union`, `set-difference`, `p-different-numbers-out-of-n`, etc.

---

## T&E+DFS

### DFS.clp
- Depth‑first search context management.
- **Rules:** `DFS-init-non-first-context-c-values`, `DFS-init-non-first-context-candidates`, `DFS-detect-contradiction-in-non-first-context`, `DFS-detect-solution-in-context`, `DFS-generate-context`, etc.

### DFS-biv.clp
- DFS variant generating special contexts for bivalue exploration.
- **Rule:** `DFS-generate-special-context`.

### T&E1.clp, T&E2.clp, T&E3.clp
- Generic trial‑and‑error depth (1–3) engines.
- **Rules:** Each defines `TE*-init-non-first-context-c-values`, `TE*-generate-context-level*`, `TE*-iterate-phase-level*`, and clean‑up rules.

### T&E1-biv.clp, T&E2-biv.clp, T&E3-biv.clp
- Special T&E entry points for bivalue cells.
- **Rules:** `TE-generate-special-context` and `TE2/TE3-generate-special-context-level*`.

### Forcing2-TE.clp, Forcing3-TE.clp, Forcing4-TE.clp
- Forcing trial‑and‑error strategies on bivalue/trivalue/quadrivalue sets.
- **Functions:** `F2TE-compare-two-branches`, `F3TE-compare-three-branches`, `F4TE-compare-four-branches`, `apply-F*TE`, and numerous rules for branch generation, evaluation, and context fusion.

### ORk-Forcing-TE.clp
- Generic OR‑k forcing trial‑and‑error.
- **Rules:** `ORkF-activate-OR-k-Forcing`, `ORkF-start-OR-k-Forcing`, `ORkF-fuse-all-branches-*`, etc.

### backdoors.clp
- Backdoor detection using T&E.
- **Function:** `find-backdoors`.
- **Rules:** `activate-backdoors`, context generation and cleaning rules.

### anti-backdoors.clp
- Searches for anti-backdoors.
- **Function:** `find-anti-backdoors`.
- **Rules:** Corresponding activation, tracking, context and cleaning rules.

### anti-backdoor-pairs.clp
- Pair-based anti-backdoor search.
- **Functions:** `find-anti-backdoor-pairs`, `find-anti-backdoor-pairs-with-one-cand-in-list`.
- **Rules:** `activate-anti-backdoor-pairs`, context management, and clean-up.

---

## CHAIN-RULES-COMMON

_Generic chain families reusable across puzzles._

### BIVALUE-CHAINS/
- 19 files: `Bivalue-Chains[2–20].clp`
- **Rules:** `activate-bivalue-chain[n]`, `track-bivalue-chain[n]`, `partial-bivalue-chain[n]`, `bivalue-chain[n]`, `apply-bivalue-chain-to-more-targets[n]`.

### TYPED-BIVALUE-CHAINS/
- 19 files: `Typed-Bivalue-Chains[2–20].clp`
- **Rules:** Same as above but typed by CSP variable.

### FORCING-WHIPS/
- 36 files: `Forcing-Whips[1–36].clp`
- **Rules:** `activate-forcing-whip[n]`, `track-forcing-whip[n]`, `partial-forcing-whip[n]`, `forcing-whip[n]`, `apply-forcing-whip[n]-to-more-targets`.

### FORCING-G-WHIPS/
- 36 files: `Forcing-gWhips[1–36].clp`
- **Rules:** Analogous rules for generalized whips.

### FORCING-BRAIDS/
- 36 files: `Forcing-Braids[1–36].clp`
- **Rules:** Analogous rules for braids.

### FORCING-G-BRAIDS/
- 36 files: `Forcing-gBraids[1–36].clp`
- **Rules:** g-braid equivalents.

### ODDAGONS/
- 18 files: `Oddagons[11–45].clp` (odd lengths only)
- **Rules:** `activate-oddagon[n]`, `track-oddagon[n]`, `oddagon[n]`.

---

## CHAIN-RULES-MEMORY

_Memory‑optimised chain rules (one file per length)._

### WHIPS/
- `Whips[1–36].clp`
- **Rules:** `activate-whip[n]`, `track-whip[n]`, `whip[n]`, `apply-whip[n]-to-more-targets`.

### T-WHIPS/
- `T-Whips[1–36].clp`
- **Rules:** Whips with transversal links; same rule pattern.

### Z-CHAINS/
- `Z-Chains[1–36].clp`
- **Rules:** `activate-z-chain[n]`, `track-z-chain[n]`, `partial-z-chain[n]`, `z-chain[n]`, `apply-z-chain[n]-to-more-targets`.

### TYPED-WHIPS/
- `Typed-Whips[1–36].clp`
- **Rules:** Typed versions of whips with rules `activate-typed-whip[n]`, `track-typed-whip[n]`, etc.

### TYPED-T-WHIPS/
- `Typed-t-Whips[1–36].clp`
- **Rules:** Typed transversal whips with analogous rules.

### TYPED-Z-CHAINS/
- `Typed-z-chains[1–20].clp`
- **Rules:** Typed z-chains rules.

### G-WHIPS/
- `gWhips[1–36].clp`
- **Rules:** Generalized whips.

### G-BRAIDS/
- `gBraids[1–36].clp`
- **Rules:** Generalized braids.

### BRAIDS/
- `Braids[1–36].clp`
- **Rules:** Braid chains.

### G-BIVALUE-CHAINS/
- `gBivalue-Chains[2–20].clp`
- **Rules:** Parallel to bivalue chains but with g-links.

### PARTIAL-WHIPS/
- `partial-whip[n].clp` files for each length.
- **Rules:** Each contains rule `partial-whip[n]`.

### PARTIAL-G-WHIPS/
- `partial-gWhip[n].clp` files.
- **Rules:** Rule `partial-gWhip[n]`.

### TYPED-PARTIAL-WHIPS/
- Typed partial whip files: `typed-partial-whip[n].clp`.

### TYPED-WHIPS/
- Duplicate listing (same as above? present for clarity).

### TYPED-T-WHIPS/
- Typed transversal partial whips.

### TYPED-Z-CHAINS/
- Typed z-chain variants.

### Z-CHAINS/
- z-chain structures as above.

> _Directories may contain further numeric-suffixed files following the same rule pattern._

---

## CHAIN-RULES-SPEED

_Speed‑oriented chain rules mirroring the memory set; for each subfolder (WHIPS, T-WHIPS, Z-CHAINS, BRAIDS, G-WHIPS, G-BRAIDS, etc.) there are files `[1–36].clp` or `gBivalue-Chains[2–20].clp` using the same rule names as in the memory version but optimized for runtime._

---

## CHAIN-RULES-EXOTIC

_Specialised OR‑k and partial OR‑k chain families._

### OR2-WHIPS, OR2-G-WHIPS, OR2-FORCING-WHIPS, OR2-FORCING-G-WHIPS, OR2-CONTRAD-WHIPS, OR2-CONTRAD-G-WHIPS
- Each contains `OR2-Whips[k].clp` or similar for lengths 1–36.
- **Rules:** `activate-OR2-whip[k]`, `track-OR2-whip[k]`, `OR2-whip[k]`, plus forcing/contradiction variants.

> _Analogous subdirectories exist for OR3 through OR6 (Whips, gWhips, forcing, contradiction)._

### OR5-WHIPS, OR5-G-WHIPS, OR5-FORCING-WHIPS, OR5-FORCING-G-WHIPS, OR5-CONTRAD-WHIPS, OR5-CONTRAD-G-WHIPS
- And similarly for OR6.

### PARTIAL-ORk-WHIPS and PARTIAL-ORk-G-WHIPS
- For k=2…6, files `partial-ORk-Whips[n].clp` implementing `partial-ORk-whip[n]` rules.

### SPLIT-ORk/
- Numerous files: `split-ORm-ch[r].clp` (m=2…16, r=2,4,6,8,10) decomposing OR‑chains into components.

### SYMMETRIFY-ORk/
- Relation files: `symmetrify-ORx-relations.clp`, `partial-symmetrify-ORx-relations.clp` defining transformation functions to symmetrise OR‑k structures.

### update-ORk-relations.clp
- Procedural utilities for maintaining ORk relation tables.

---

### CHAIN-RULES-SPEED (G-BRAIDS, TYPED-G-WHIPS etc.)
- (Already summarised under speed; same rule sets exist for g-bivalue chains, typed variants, partial variants, each with `[1–36]` or `[2–20]` files defining corresponding activation/track/partial/final/apply rules.)

---

**Overall:**  
CSP-Rules-Generic provides the generic infrastructure (global variables, salience management, output, and solver core), utility modules, exhaustive trial‑and‑error mechanisms, and massive libraries of chain rules in multiple variants (basic, typed, g‑link, OR‑k, partial, memory‑optimized, and speed‑optimized), each implemented as families of numbered CLIPS files whose rules follow a consistent naming pattern (`activate‑…`, `track‑…`, `partial‑…`, …, `apply‑…`).