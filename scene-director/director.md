# Scene Director — how we pick panels

Source: `O:\ExternalSites\html\DND\session\<id>.json` → field `.transcript` (string with `[mm:ss] Name: line`).

## Beat types (user priority)
1. **Funny / roast** — party making fun of each other, fails, NPC banter. Example: Rocketcandy axe-to-face (S Battle of Bards), Keechwah Witch Bolt vs spider, Vicious Mockery butler.
2. **Epic success** — someone pulls off crazy stunt. Example: Chip grapple + proprietor pan KO, Keechwah 20 performance.
3. **Epic fail** — spectacular whiff. Example: perception 1s, Rocketcandy self-hit.
4. **Character** — look / gear change, new companion moment. Example: Water Bear entry tax, Lily daggers.
5. **Plot** — quest turn, villain reveal, note / map. Example: kidnapped Lily dagger note, Thieves Cant cipher, Filvenar quest.

Score each 10-min transcript chunk 0-3 on funny/epic/fail/plot. Keep chunks scoring >=2.

## Panel sizing rule
- Small beat (single joke, single roll): **1 panel**
- Medium beat (fight setup, shop haggle): **2-3 panels**
- Big set-piece (Battle of Bards, Shadow Knight fight, ale-barrel explosion): **5-10 panels**
- A session = 1+ comic pages. Each page = 3-6 panels. Let long sessions spill to 2-3 pages.

## Prompt assembly
`[global style] + [bible block for each character present] + [action] + [location] + [composition] + [no duplicates, exactly two arms, adult faces]`

## Identity rule (standing — two-ref scheme since 2026-11-04)
Panels condition on approved portraits, not prose alone. Each main character has TWO refs: `approved_<slug>_reference.png` (full-body, for scene passes) and `approved_<slug>_closeup.png` (face canon, for masked face passes). Base graph: `workflows/base_flux3_multiref.json` (Flux3 Klein rig + `ReferenceMultiLatent`, one `LoadImage` slot, prompt sentinel `{{PROMPT}}`). Per panel: copy the base, point `LoadImage` at each in-frame character's approved FULL-BODY portrait (add `LoadImage` nodes + `images.imageN` links for casts >1), replace the sentinel with the assembled prompt, keep rig byte-identical. Text-only `base_flux3.json` remains for no-face detail shots (tattoos, signage) and creatures with no portrait. Validated: multi-ref proven across lineup-lab batches 33–40 (up to 11 refs in one pass; ~6 for quality); finish every panel per PIPELINE.md recipe (scene → 7-face-style masked ref pass → FaceDetailer 0.35) — see `sessions/session01/v3/` for the worked example.

Always append character-bible anti-conflation footer.
Word colors onto the right noun: `deep red skin, black hair`, never `red tiefling` — a loose color migrates (red skin became red hair in P2.1 v2-v3).
If any character, outfit, object, or scene detail needed for a panel has no bible entry: STOP and ask the user before generating — never invent (bible: "ASK, DON'T GUESS").
Always log: session id, panel #, prompt, seed, model versions, output file.

## Comic text
- Narration boxes: 1-2 sentence recap (DM voice).
- Speech: use ACTUAL transcript quotes when funny/epic, trimmed to <20 words. Attribute: `Rocketcandy: "..."`.
- SFX for fails: `CLANG`, `WHIFF`, `THUD`.
- Store text in `sessions/<id>/panels.json` alongside images: `{panel, image, narration, quotes:[{who,text}]}`.

## Readability rules (standing — approved 2026-11-02, apply to every session)
Goal: a stranger who never played can follow the comic. Adapting D&D to graphic-novel form takes precedence over beat-for-beat fidelity.
- **Prologue montage**: every session opens with one page — each hero gets a mini-panel with one journal/downtime line from the transcript. Uses approved portraits. Introduces the cast before the plot moves.
- **Dramatis personae**: every session includes the approved lineup image (or its update) as a cast page. New recurring characters (Lilly, Biggins, Filvenar, Marigold, Sammy) join it once approved.
- **Seed visual plot language early**: recurring visual motifs (guard wrist tattoos, uniform differences, star = leader) get an explicit close-up panel at FIRST mention in the transcript, not just at the reveal. Never rely on dialogue alone for a visual payoff.
- **Split threads get banners**: whenever the party splits, each thread's panels carry a `Meanwhile...` banner (or location tag). Threads rejoin with a matching tag.
- **Mechanics become flavor**: dice rolls render as small d20 result badges; VTT/tech-support talk, IRL tangents, and audio-glitch stretches are CUT, never paneled. Keep player-character banter and roast jokes — they're the comedy engine.
- **Restructure beats for reading order**: panels may be reordered, combined, or added (e.g. establishing shots) versus transcript order when the transcript's order confuses. The transcript is the source of events and quotes, not the layout.
- **Quote discipline**: every speech line must be traceable to a transcript line (trimmed <20 words is fine). Narration may bridge gaps in DM voice but never puts new facts in a character's mouth.

## Narrator voice (standing — user 2026-11-03)
The narration boxes speak in Ben's voice: the warm, snarky DM storyteller who keeps things moving and openly roasts the Brigade for dumb decisions. Affectionate, never mean; funny to strangers, funnier to players. Mode: bedtime story, not captions — narration carries plot, motive, and transitions in 2–4 sentences, fills what the art can't show, and never restates what the art already says.

## Self-approval authority (standing — user grant 2026-11-03)
The executor approves panels WITHOUT a user verdict when all of these hold: every face matches its approved reference, locked chunks/NEVER lists respected, figure counts match the beat, no children/marigold-scale/ear/hair failure modes present. Save + commit approved work with the same checks. Escalate to the user only: new-look approvals (portraits), canon decisions, story confusion or holes, defects surviving two re-rolls, and anything the bible doesn't cover (ask-don't-guess).

## Next: auto script
`scripts/new-session.ps1 -SessionId <id>` does:
1. read transcript, chunk, score (LLM or keyword + manual review for v1)
2. write `sessions/<id>/plan.json`
3. generate Flux JSONs from bible + plan (reuse `workflows/base_flux3.json`)
4. submit to 10.13.37.88:8188, poll, download to `sessions/<id>/`
5. emit `comics/<id>.html` multipanel with narration + quotes
