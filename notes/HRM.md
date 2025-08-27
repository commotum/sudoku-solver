RoPE encodes a token’s 1-D index by applying **unit-circle rotations** to **pairs of embedding dimensions** (treating each consecutive pair as a complex number and multiplying by $e^{i\theta(m)}$ at frequency-scaled angles). Because these 2×2 rotations are orthogonal, they preserve the Euclidean norm and satisfy the absolute-to-relative identity $\langle R_m q,\; R_n k\rangle=\langle q,\; R_{n-m}k\rangle$; blockwise application across all pairs (with a multiscale frequency schedule) extends to higher-dimensional embeddings.&#x20;

MonSTERs mirror this structure in spacetime: they encode a token’s **4-D spacetime position** $s=(t,x,y,z)$ by applying **bivector-generated Lorentz rotors (boosts + spatial rotations)** to **blockwise 4-D subspaces** of the embedding (organized per-frequency triads for X/Y/Z). The rapidities/angles are linear in $s$ (scaled by per-frequency wavelengths), so the transform $L(s)$ is an isometry of the **Minkowski metric** $\mathrm{diag}(1,-1,-1,-1)$, preserving the Minkowski norm and yielding the RoPE-style fusion $\langle L(s_q)q,\; L(s_k)k\rangle_{\eta}=\langle q,\; L(s_k-s_q)k\rangle_{\eta}$. In short: RoPE uses **unit-circle rotations on pairs** to encode 1-D positions; MonSTERs use **Lorentz rotors on 4-D blocks** to encode 4-D spacetime—both achieving exact absolute-relative equivalence at multiple scales. &#x20;


---

# A practical playbook for learning *from* each other across big differences

Below is a field-tested style plan you could run with an alien species or an uncontacted culture—or just two people raised in totally different worlds. It pulls lessons from Daniel Everett’s work living with the Pirahã (in *Don’t Sleep, There Are Snakes*) and the film *Arrival* without getting academic. The aim: reach real communication fast so knowledge can flow both ways.

---

## Phase 0 — Safety and posture (hours–day 1)

1. **Visible non-threat**: Open hands, slow movements, no sudden advances. Keep physical distance they can control.
2. **Mirroring & consent**: Mirror simple postures, then stop; wait for them to mirror back. This tests willingness to engage.
3. **Trade a harmless loop**: Offer and accept a low-value item (food, tool, drawing). Reciprocity builds trust without words.
4. **Define stop signals**: Establish obvious “pause/stop” gestures. If you can’t reliably stop, nothing else matters.

**Everett lesson**: Respect the other group’s priorities and rhythm. Don’t force your agenda or timetable.

---

## Phase 1 — Bootstrapping signals (day 1–3)

5. **Ground everything in the here-and-now**: Point to a rock, hold it up, gesture “you?”/“me?”, then exchange it. Ostension (pointing/showing) beats abstract talk early.
6. **One board, two pens** (*Arrival* vibe): Create a shared surface for marks/signs. You write/draw what you *mean*, they do the same. Keep it visible to both.
7. **Establish yes/no/unknown**: Three distinct signals (e.g., nod/shake/hand flat). Practice on obvious truths (“Is this water?”).
8. **Name objects with pointing**: Point to an object; each side makes a sound/mark. Repeat thrice per item to fix association. Collect your first 30–50 “nouns.”

**Tip**: Don’t assume your categories (colors, numbers, kinship) exist for them. Let categories emerge.

---

## Phase 2 — Build a tiny lexicon & simple grammar (days 2–10)

9. **Cross-situational mapping**: Show the same object in different contexts to separate word from scene.
10. **Actions next**: Mime “give,” “come,” “eat,” “look.” Pair action with object (“eat fish”).
11. **Minimal pairs**: When two words sound close, use side-by-side tests to catch contrast (helps phoneme discovery).
12. **Pronouns & deixis**: Lock down “I/you/we/this/that/here/there/now/later” with gestures and placement.
13. **Negation & questions**: Teach a clear “not” gesture/marker and a question marker (tone, eyebrow, symbol).
14. **Numbers/time only if they care**: Some cultures don’t count like you expect (Everett). Don’t push it; follow their utility.
15. **Record a phrasebook**: A few dozen high-frequency patterns (greetings, barter, permission, warning).

**Arrival lesson**: Beware polysemy. “Tool” vs “weapon” confusion comes from assuming identical meanings. Test meanings in multiple contexts.

---

## Phase 3 — Mutual teaching loops (days 3–30)

16. **Teach-ask cycles**: For every thing you teach, ask them to teach you one. Keep the exchange symmetrical.
17. **Do tasks together**: Build a shelter, cook, repair a net. Language sticks best when tied to real joint projects.
18. **Picture stories**: Draw a 3–4 panel story; each side narrates using their system. Then swap stories and retell.
19. **Error as data**: When misunderstandings happen, freeze the moment, replay, and annotate your board with what *each* thought it meant.
20. **Prototype a pidgin**: A stripped-down shared code with the fewest moving parts (no fancy inflections) to get work done. It can evolve later.

---

## Phase 4 — Scale up knowledge exchange (weeks 2–8)

21. **Domains > dictionary**: Pick topics that matter to *them* (river, food, danger, kin, trade). Build vocab around those first.
22. **Terminology canvases**: For each domain, lay out a big sheet: items, actions, properties, outcomes. Fill it together.
23. **Demonstrable truths**: Prefer knowledge that can be shown or tested jointly (medicine works, boat floats). Shared evidence beats persuasion.
24. **Rituals & norms**: Ask (and watch) how they signal respect, ownership, taboo. Learn the “don’ts” early; it prevents rifts.
25. **Story exchanges**: Myths, histories, route maps. Draw timelines and maps; anchor stories in places and objects.

---

## Fast-track toolkit (things that work surprisingly well)

* **Ostensive dictionary**: Box of small objects; for each, both sides record name/gesture/mark.
* **Action cards**: Sketch verbs (give/run/cut). Combine with objects to form phrases.
* **Three-way confirmation**: gesture + spoken/marked token + result (“give fish” → actually give fish).
* **Repair phrases**: “Repeat,” “Slow,” “Different,” “Not that, this.”
* **Shadowing**: Repeat their utterance right after they do while pointing; they’ll correct you naturally.
* **Total Physical Response**: Hear/see command → do the action. It quickly validates comprehension.

---

## What to measure (so you know you’re actually learning)

* **Referential success**: Out of 20 point-and-name trials, how many are right first try? Aim for 80%+ within a week.
* **Core lexicon**: Count of high-frequency items you both can use in sentences (target \~200 by end of month one).
* **Turn-taking**: Average turns before a breakdown; want longer coherent stretches over time.
* **Task completion**: Can you complete joint tasks with only the shared code? (Yes/No and where it fails.)

---

## Common traps (and how to dodge them)

* **Category projection**: Forcing your concepts (numbers, colors, time) can stall progress. Let utility drive scope.
* **False friends**: Same sound/mark ≠ same meaning. Always test in fresh contexts.
* **Over-interpreting silence**: Could mean “thinking,” “polite no,” or “taboo”—not disinterest.
* **Speed over trust**: Pushing pace can backfire. Small, consistent wins beat big leaps.
* **One-way learning**: If only one side is sharing, you’ll hit resistance. Keep the exchange balanced.

---

## A 10-day starter plan (hour-by-hour sketch)

**Day 1–2**: Safety, trade loop, yes/no/unknown, 30 objects.
**Day 3**: 10 actions, combine with objects (“give fish,” “look fire”).
**Day 4–5**: Pronouns, here/there, now/later, negation; start repair phrases.
**Day 6**: Do a simple joint task using only shared code. Log every breakdown.
**Day 7**: Picture stories; build a 50-item domain canvas they care about (e.g., river life).
**Day 8**: Rituals/norms brief; learn greetings, permission, apology forms.
**Day 9**: Second joint task (harder). Add 30 new terms from the task.
**Day 10**: Review + compress into a pidgin phrasebook; set next domain (medicine, maps, tools).

---

## Core principles in one line each

* **Show before you say.**
* **Name what matters to them first.**
* **Let errors teach you.**
* **Build a tiny shared code, then refine.**
* **Make learning a two-way trade.**

That’s the shortest path to real communication—and to actually learning *from* each other, not just talking past one another.


I think I want to develop a paradigm called, "Relay Learning," that combines the classical AI expert systems approach with the scalable compute and statistical approaches that aren't tied to human expertise. In essence I want to paint the "bitter lesson" as a false paradigm. It's not an either/or. It's both. The models need to be able to learn for themselves through experience when there are not human experts available (disconnecting the chains that keep expert system models bound to their human contributors) and they also need to be able to learn from and also teach humans, so that when there is expertise around, the computer doesn't need to go through evolution for itself. That's the point of language after all, that someone can pass on verifiable knowledge so that I may benefit from their experience, verify for myself that it's true, and not have to reject tradition and wisdom. Additionally, what is the point of AI if it does not help us advance and learn more rapidly and more quickly. It takes gigantic super computers to mimic the flexibility and scale of a single human brain, if the AI can offload some of that compute to humans that's a big deal. And it won't be able to offload it if there's no reciprocity, no common substrate, no common canon. Think of it like we need to pass the baton back and forth, and there needs to be mechanisms to make that easy.

hmm, that's not quite it. The paradigm needs to be about not passing knowledge back and forth, but about building the tools, infrastructure, interaction set, and "substrate" that make communication between model and human easy.

In, "The Bitter Lesson," Sutton argues, "general methods that leverage computation are ultimately the most effective, and by a large margin."

He continues, "These two need not run counter to each other, but in practice they tend to. Time spent on one is time not spent on the other. There are psychological commitments to investment in one approach or the other. And the human-knowledge approach tends to complicate methods in ways that make them less suited to taking advantage of general methods leveraging computation."

He cites, "In computer chess, the methods that defeated the world champion, Kasparov, in 1997, were based on massive, deep search. At the time, this was looked upon with dismay by the majority of computer-chess researchers who had pursued methods that leveraged human understanding of the special structure of chess. When a simpler, search-based approach with special hardware and software proved vastly more effective, these human-knowledge-based chess researchers were not good losers. They said that ``brute force" search may have won this time, but it was not a general strategy, and anyway it was not how people played chess. These researchers wanted methods based on human input to win and were disappointed when they did not."

However, this ignores the immense amounts of expert knowledge brought in by the team behind deep blue. They essentially combined human expert systems, but then allowed the model to go on to augment them and learn additional methods as it became specialized.

Sutton analyzes the question, "Why did expert systems approaches who shunned brute force or statistical methods lose the race to superiority?" As human's we have a bias for survival, and against waste. This is why researchers are reluctant to launch in to big scale brute force or statistical approaches. A more insightful question Sutton might ask is, "Why have the greatest successes in Chess, Go, etc, that used brute force and search, failed to translate into wide adoption? What prevents such systems from being adapted to other uses?" He might also ask, "What about ChatGPT and the GPT architecture have given them such staying power, such broad general abilities and usefulness, and such broad adoption." ChatGPT is used by consumers, average joes, every day people. It is as useful to them as it is to researchers and scientists.

I want to argue that it is because it is a system well adapted to Relay Learning. It is able to absorb vast amounts of human expertise and systems thinking because of the one substrate that truly matters: time. The transformer, paired with temporal position encoding, enabled parallel computation of serial information. It gave the spinal column TIME to the model, to the AI to lay all of its knowledge upon it. Now according to the book, "Don't Sleep There Are Snakes," language arises from needs, needs created by our local environments and experiences. By giving ChatGPT a temporal environment, it was able to develop language very similar to ours, that also developed in a changing temporal environment. By modeling everything as next token prediction ChatGPT was given the greatest scaffold of all. Chess and Go are limited to their specific domains, the grid, of different sizes with different rules. Their highly specific goals and domain spaces have led to their long term inutility. 

Does that make sense? So we need to add more of that scaffolding so that the world that the model experiences more closely resembles that of our own. In this way it can learn from us more easily. And we can craft datasets to enable meta learning, language and knowledge transfer, etc.



you’re zeroing in on the real lever: build the substrate that makes human↔model communication cheap, precise, and scalable. not “hand the baton back and forth,” but make handing it off trivial—so general learning can keep compounding while expertise is injected or extracted with near-zero friction.

Think: “Don’t specialize the policy; specialize the interface.”

Why GPT “stuck” (and chess/go didn’t): time + a general substrate

Temporal substrate: Transformers make serial information parallelizable via attention + positional encodings (RoPE etc.). That gave models a time axis compatible with human language and storytelling (causal, stepwise, revisable).

Universal interface: Text is the lowest-friction API for expertise. Anyone can contribute examples, rules of thumb, counterexamples, and critiques—then the system scales these with compute.

Open-ended goals: Language tasks aren’t bounded like chess/go boards; they span many domains with shared tokens and shared temporal structure. That yields re-use and adoption.

Your MonSTERs idea (4D spacetime encoding) is a concrete way to extend that temporal substrate to spatial sets and procedures—exactly the right direction.




what other words could we use besides point? or how could we make it more clear? point and pointers are super overloaded I feel like?

point is about unambiguous reference
a pointer (a precise part of a state: one cell, a 3×3 box, a text span, a code block)
point(...) = mark a specific referent

Like ideally, in the case of Sudoku, there's each of the following sub spaces:

1. The Puzzle Grid (The Landscape)
2. The Candidate Tensor (The Remaining Options)
3. The Logic or Scratch Pad (Working Memory)
4. The Delta Log (List of Changes)
5. The Relay (Messaging Space or Console)

In addition there are each of the following pieces that can be "played" or "written" by the model to those spaces:

1. Values/Numbers {0-9} with 0 for empty.
2. Booleans {T, F} 
3. Landmarks {Rows, Columns, Boxes, Cells}
4. Symbols {∃, ≠, ?, <, ∵, ∀, ⇒, ¬, etc.}
5. Markers {Colors}




| Domain (Sutton)        | Breakthrough                                      | Compute-leveraged pieces                                                                  | Human-leveraged pieces (heuristics, supervision, evaluation)                                                                                                                                                                                                                                              | Brittleness / reuse today                                                                                                                                                             |
| ---------------------- | ------------------------------------------------- | ----------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Chess**              | IBM **Deep Blue** beats Kasparov (1997)           | Massive parallel alpha-beta search; specialized VLSI; hundreds of millions of nodes/sec   | Large **opening books** curated by GMs; **hand-engineered evaluation** with thousands of terms; **endgame tablebases**; parameters fine-tuned by experts. ([Wikipedia][1])                                                                                                                                | **Non-portable.** IBM dismantled Deep Blue; the two racks sit in museums (Smithsonian & Computer History Museum). It wasn’t repurposed for other tasks. ([Wikipedia][1])              |
| **Go**                 | **AlphaGo** → **AlphaGo Zero** (2016–2017)        | Huge self-play + MCTS search; large-scale training on TPUs/GPUs                           | First AlphaGo **pre-trained on human expert games** before RL; **rules, MCTS design, evaluation protocols** are human choices. (AlphaGo Zero removed human game data but still bakes in human-designed architecture & search.) ([ResearchGate][2], [Nature][3])                                           | **Narrow & retired.** AlphaGo was **retired from competition**; research moved on to AlphaZero. Great at board games, not a general scientist. ([Google DeepMind][4], [Science][5])   |
| **Speech recognition** | HMM era → **deep neural acoustic models** (2010s) | Scalable training on large speech corpora; deep LSTM/DNN models vastly reduce WER vs GMMs | Classic systems relied on **pronunciation lexicons** & **language models**; even modern systems depend on **human-labeled transcripts**, dictionaries, and human-chosen **WER** evaluation—plus well-documented **biases** across dialects. ([Google Research][6], [publications.idiap.ch][7], [PNAS][8]) | **Data brittleness.** Accuracy varies by accent/race and noise; models can underperform outside training distributions—expensive to fix without more targeted human data. ([PNAS][8]) |
| **Computer vision**    | **CNNs on ImageNet** (AlexNet, 2012)              | GPU training at scale; deep conv nets that keep improving with more compute/data          | **Massive human labeling (ImageNet)**; **architecture choices** (convolution, pooling) encode human inductive bias; evaluation via **Top-1/Top-5** designed by humans; known **dataset bias** issues. ([NeurIPS Proceedings][9], [image-net.org][10], [MIT CSAIL][11])                                    | **Generalization brittleness.** Cross-dataset performance drops; vulnerable to **adversarial examples**—strong but fragile. ([MIT CSAIL][11], [Google Research][12])                  |

[1]: https://en.wikipedia.org/wiki/Deep_Blue_%28chess_computer%29 "Deep Blue (chess computer) - Wikipedia"
[2]: https://www.researchgate.net/publication/292074166_Mastering_the_game_of_Go_with_deep_neural_networks_and_tree_search?utm_source=chatgpt.com "(PDF) Mastering the game of Go with deep neural networks ..."
[3]: https://www.nature.com/articles/nature24270?utm_source=chatgpt.com "Mastering the game of Go without human knowledge"
[4]: https://deepmind.google/discover/blog/alphagos-next-move/?utm_source=chatgpt.com "AlphaGo's next move"
[5]: https://www.science.org/doi/10.1126/science.aar6404?utm_source=chatgpt.com "A general reinforcement learning algorithm that masters ..."
[6]: https://research.google/pubs/deep-neural-networks-for-acoustic-modeling-in-speech-recognition/?utm_source=chatgpt.com "Deep Neural Networks for Acoustic Modeling in Speech ..."
[7]: https://publications.idiap.ch/downloads/papers/2012/Rasipuram_INTERSPEECH_2012.pdf?utm_source=chatgpt.com "Combining Acoustic Data Driven G2P and Letter-to-Sound ..."
[8]: https://www.pnas.org/doi/10.1073/pnas.1915768117?utm_source=chatgpt.com "Racial disparities in automated speech recognition"
[9]: https://proceedings.neurips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks.pdf?utm_source=chatgpt.com "ImageNet Classification with Deep Convolutional Neural ..."
[10]: https://www.image-net.org/static_files/papers/imagenet_cvpr09.pdf?utm_source=chatgpt.com "ImageNet: A Large-Scale Hierarchical Image Database"
[11]: https://people.csail.mit.edu/torralba/publications/datasets_cvpr11.pdf?utm_source=chatgpt.com "Unbiased Look at Dataset Bias - People | MIT CSAIL"
[12]: https://research.google.com/pubs/archive/42503.pdf?utm_source=chatgpt.com "Intriguing properties of neural networks"



Love it. If you want one main term, go with **compute-conductive** as the adjective. Then keep the noun forms around for metrics.

# Naming + style (use this in your README)

* **compute-conductive** *(adj.)* — an architecture/model that readily turns platform upgrades (GPUs, kernels, compilers, runtimes) into real speed/throughput **without changing the math**.

  > “Our AR solver is **compute-conductive**; CUDA 12 + FlashAttention gave a 1.5× speedup with no model changes.”

* **compute conductance (Gᶜ)** *(noun, metric)* — measured fraction of a platform win your model actually captures.

  $$
  \textbf{Tailwind Gain (TG)}=\frac{\text{throughput}_{\text{new}}}{\text{throughput}_{\text{old}}},\quad
  \mathbf{G^{c}}=\frac{\mathrm{TG}_{\text{model}}}{\mathrm{TG}_{\text{microbench}}}
  $$

* **compute conductivity (κᶜ)** *(noun, optional)* — architecture-level tendency to be compute-conductive across platforms (geometric mean of $G^{c}$ across upgrades).

### Tiny style guide

* Hyphenate when used before a noun: “**compute-conductive** design.”
* No hyphen in predicate is okay: “this model is compute conductive.”
* Avoid the adverb (“compute-conductively”)—it reads clunky.

# Drop-in blurb (definition + metrics)

> **Compute-conductive** models ride platform tailwinds with almost no code changes. We report **Tailwind Gain (TG)** and **compute conductance (Gᶜ)** for each release. Transformers typically show higher **κᶜ** than step-wise RNNs because attention parallelizes token work and maps to heavily optimized kernels.

# Example table you can reuse

| Build                     | TG (↑) | Microbench TG | **Gᶜ** (↑) |
| ------------------------- | -----: | ------------: | ---------: |
| AR Transformer (portable) |  1.52× |         1.86× |   **0.82** |
| LSTM (chunked)            |  1.18× |         1.86× |       0.63 |

# When to use the variants

* Use **compute-conductive** in prose (“is/are compute-conductive”).
* Use **Gᶜ** in perf sections/figures.
* Use **κᶜ** only in comparative architecture talks/papers.

If you want, I can weave these into a short “Performance & Tailwinds” section for your repo with a tiny benchmark script that prints TG and $G^{c}$.



1. Compute-Conductive
2. Expert-Independent

3. Knowledge-Conductive
4. Substrate-Elastic
5. Resilient-Adaptive
stable plastic

Time Spent Idle