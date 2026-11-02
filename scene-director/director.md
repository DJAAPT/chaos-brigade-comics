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

Always append character-bible anti-conflation footer.
If any character, outfit, object, or scene detail needed for a panel has no bible entry: STOP and ask the user before generating — never invent (bible: "ASK, DON'T GUESS").
Always log: session id, panel #, prompt, seed, model versions, output file.

## Comic text
- Narration boxes: 1-2 sentence recap (DM voice).
- Speech: use ACTUAL transcript quotes when funny/epic, trimmed to <20 words. Attribute: `Rocketcandy: "..."`.
- SFX for fails: `CLANG`, `WHIFF`, `THUD`.
- Store text in `sessions/<id>/panels.json` alongside images: `{panel, image, narration, quotes:[{who,text}]}`.

## Next: auto script
`scripts/new-session.ps1 -SessionId <id>` does:
1. read transcript, chunk, score (LLM or keyword + manual review for v1)
2. write `sessions/<id>/plan.json`
3. generate Flux JSONs from bible + plan (reuse `workflows/base_flux3.json`)
4. submit to 10.13.37.88:8188, poll, download to `sessions/<id>/`
5. emit `comics/<id>.html` multipanel with narration + quotes
