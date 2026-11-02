# Chaos Brigade — Character Bible v2 (2026-11-01, gallery-grounded)
Approved look: `character-bible/approved_S1P1_reference.png` + `O:\ExternalSites\html\DND\gallery\`
Rule: NEVER invent new faces. Copy these blocks verbatim. Max 3-4 named characters per panel. Solo shots for introductions, groups only when script demands.
Rule: ASK, DON'T GUESS — if a panel needs a character, outfit, object, or scene detail with no entry in this bible, STOP and ask before generating. A generated guess becomes canon in later panels. Applies to me when directing scenes and to any automated pipeline step.

## Why drift happens (Flux text-only)
Flux 3 (Klein, text-only) has no identity memory between prompts. Every panel re-rolls faces. Fixes: (1) identical prompt chunks every time, (2) fewer people per frame, (3) sex/age/species stated first, (4) ban list appended always, (5) approve one solo portrait per character, reuse as visual ref for future IP-Adapter/ReActor pass.

Global suffix (append to EVERY prompt):
`adult faces, no children, no teens, no gray hair, no white hair, exactly two arms per humanoid, single character each, no duplicates, no conflation, no extra heads, no wings unless noted, photorealistic, highly detailed`

## LOCKED PROMPT CHUNKS (copy verbatim)

### Shade — Male Halfling Rogue (St3v3D/David). Young adult halfling man, NOT child, NOT elderly.
`young adult halfling man, mid-20s, mature adult face, lean build, messy shaggy dark brown hair falling over the sides of his head, light stubble, no beard, warm brown eyes, subtle sly closed-mouth expression, worn dark linen shirt with rolled sleeves, scuffed brown leather vest, belt dagger at hips, warm tan skin with a ruddy cast, long sideburns, small adult stature about three feet tall, full-size adult human features scaled down uniformly, exactly the same head-to-body proportions as a full-size grown man, he is a full-grown man who happens to stand three feet tall, enlarged to six feet he would be indistinguishable from an ordinary human man, small adult head, thick shaggy hair covering the sides of his head completely, small skull structure, sleek adult facial proportions, exactly two arms`
Approved identity ref (2026-11-02, Flux3 Klein): `character-bible/approved_shade_reference.png` — shade-lab batch-14 keeper q13 (seed 1395696223); copy this face for any new Shade portrait. Lab rules that produced it: name the species for scale, never name the ears (see `character-bible/sheet-test/shade-lab/README.md`).
NEVER: child, boy, teen, elderly, gray hair, white hair, beard, wrinkles, pointed ears, elf ears, large ears, protruding ears, hobbit feet, bare feet, blond hair, big friendly smile by default.
Default expression: lips sealed closed with a barely perceptible asymmetric lift on one side, sly knowing gleam in his eyes — subtle mischief, never a full smile or grin. Keep-to-himself thief, not the outgoing one.
Guild mark: geometric diamond tattoo (gallery/Objects/The_Tattoo.png) on forearm — include only when plot-relevant.

### Rocketcandy — Male Human Paladin (Andrew). Lost nobility of Corlinn Hill (Neverwinter county), raised in Waterdeep, inherits only a title.
`adult male human paladin, short brown hair light stubble, shining plate armor with gold phoenix/eagle crest on chest, red cape, exactly two arms, holding a heavy battle-worn steel battleaxe with a plain wide scarred blade, no gaudy ornamentation`
Approved identity ref (2026-11-02, Flux3 Klein): `character-bible/approved_rocketcandy_reference.png` — copy this face; face, expression, and axe approved in the Flux3 v2 portrait.
Refs: gallery/Scenes/City_Guards.png is CORRUPT guard look-alike — do NOT copy its helm/plume for Rocketcandy except crest shape. Gallery/Objects/Rocketcandy_Plot_Armor.png = his armor ref — use it.
NEVER: extra arms, female, modern clothes, helm, plume, gaudy gold-decorated battleaxe.
Weapon: +3 battleaxe (signature — sheet + transcript axe-to-face). Faith: Bahamut. Oath of the Open Sea. Props: signet ring, holy symbol.
Default expression: confident composed noble bearing — calm, lawful-good certainty.

### Keechwah — Male Tiefling Warlock (Aaron). MALE, no wings.
`adult male tiefling warlock, deep red skin, long curly black hair, goatee, large curved horns, glowing purple eyes, male facial features, dark blue/gold robes, gold jewelry, NO wings`
Approved identity ref (2026-11-02, Flux3 Klein): `character-bible/approved_keechwah_reference.png` — copy this face; face, expression, and orb approved in the Flux3 v1 portrait.
Refs: gallery/Scenes/Keechwah_and_Lilly_bonding.png (face, hair, jewelry locked), Verruth_and_Keechwah_make_a_deal.png (blue-hair variant = younger? use black-hair as canon unless flashback).
NEVER: female, wings, hooves, female chest, duplicate Keechwahs. Keechwah has NO wings — Verruth (below) HAS wings, do not mix.
Expression: loves a good mystery, convinced people are trying to steal his secrets. Props when plot-relevant: orb arcane focus, lute (Battle of the Bards), Book of Shadows.
Default expression: secretive knowing intensity — guards his secrets, stern rather than smiling.

### Gulgrim Frozenboots — Male Hill Dwarf Cleric (James)
`adult male hill dwarf cleric, short stocky, completely bald head, broad long white beard, heavy furs, frost-covered boots, large round shield with holy rune, warhammer`
Approved identity ref (2026-11-02, Flux3 Klein): `character-bible/approved_gulgrim_reference.png` — copy this look; face, gear, and expression approved in the Flux3 v1 portrait (full-body framing shows the frost boots).
NEVER: tall, thin, no-beard, missing his heavy furs (furs stay on in every panel, indoors or out).
Gear: Holy Symbol + Biggins manor key (plot item), Mason's tools. Soldier background (Mintarn → Neverwinter watch, quit over corruption). Faith: Marthammor Du. Warhammer is canon (user decision — sheet's mace ignored).
Default expression: steadfast and resolute — stern veteran soldier-cleric, no smile.

### Chip — Male Human Druid (Josh)
`adult male human druid, brown skin, wild long white hair and white beard, brown eyes, green/brown fur garb, holding a straight wooden quarterstaff with a small crystal slotted into it (HE holds it, never Vadania)`
Approved identity ref (2026-11-02, Flux3 Klein): `character-bible/approved_chip_reference.png` — copy this face; face, expression, and staff approved in the Flux3 v2 portrait.
NEVER: give staff to Vadania, merge with Vadania, bat on shoulder (Celeste rarely pictured), brown hair or beard (canon is white per sheet), crooked or crook-topped staff.
Expression: awkward observer — blurts insults without thinking, last to speak. Prop: his quarterstaff has the crystal Star Map slotted into it (Circle of the Stars).
Default expression: awkward and earnest, slightly bewildered — quiet observer, never severe or formidable.

### Vadania Amakiir — Male Wood Elf Ranger (Derek)
`adult male wood elf ranger, long brown hair, green eyes, pointed ears, masculine jaw stubble, green cloak, longbow on back, short swords at hips, scar on shoulder`
Approved identity ref (2026-11-02, Flux3 Klein): `character-bible/approved_vadania_reference.png` — copy this face; face, expression, and gear approved in the Flux3 v1 portrait.
NEVER: female, dress, blonde hair (canon is brown per sheet — user decision 2026-11-01), long blonde woman in green (that is a misrender — re-roll), duplicate Vadania as barmaid.
Expression: action over theory, blunt and sincere, follows through. Weapon: Monster Hunter's Longbow +1 (ornate named longbow) + twin shortswords.
Default expression: blunt and direct — a man of action, steady gaze, never soft or smiling.

### Lilly — Adult woman early 20s (NOT a child)
`adult young woman early 20s, curly voluminous red hair, freckles, white ruffled shirt, red corset laced gold, cream skirt, brown boots, thigh dagger + rapier with mother-of-pearl handle`
Approved identity ref (2026-11-02, Flux3 Klein): `character-bible/approved_lilly_reference.png` — copy this face; adult likeness approved in the Flux3 v1 portrait.
Refs: gallery/NPCs/Lilly.png (LOCKED), Keechwah_and_Lilly_bonding.png. NEVER: child, little girl, schoolgirl.
Default expression: warm and confident — friendly, self-assured young woman.
Behavior (transcript canon): sheltered manor upbringing — wide-eyed wonder at everything new, physical exuberance (hugs, skipping, door-crashing enthusiasm), blurts endless questions, brave resolve underneath. As Filvenar: regal pose stretched over giddy core — the mask visibly slips when excited.
Undercover as Lady Filvenar in Session 1 (hair braided, corset + trousers disguise — same face).

### Water Bear — Owlbear, ONE creature
`single owlbear creature, massive grizzly bear body with coarse brown fur and bear paws with claws, head REPLACED by owl head with round eyes and hooked beak and feathered ruff, walking on all fours like a bear, no wings, no second head, no separate owl`
NEVER: bear holding owl, two heads, wings, white snowy owl alone, bear head + owl head side by side, standing upright on hind legs like a human (rears up only momentarily), named Albert (S1 line was a slip, ignored per user 2026-11-03).

### Biggins Aulswim — Lilly's protector, ex-Talons of Justice assassin
`tall adult human man in his 40s, slicked gray-streaked dark hair, sharp cheekbones, blue eyes, black three-piece suit with long coat, white shirt black tie, white gloves, pocket-watch chain, holding bloody dagger when hunting`
Approved identity ref (2026-11-02, Flux3 Klein): `character-bible/approved_biggins_reference.png` — copy this face; clean reference has no dagger, hunting variant adds it.
Ref: gallery/NPCs/Biggans_Aulswim.png (note filename typo Biggans). NOT old gentleman, NOT apothecary. Undercover as the mansion butler throughout Session 1 (butler attire, same face — the party doesn't know); first met openly in Session 2.
NEVER: beard, hooded cloak, kindly shopkeeper look (that is the apothecary — keep them distinct).
Default expression: cold and composed — professional ex-assassin calm.
Behavior (transcript canon): coiled stillness — moves effortlessly, appraising eyes, often already where events happen (opens doors before arrivals); snoot and insult are performance, menace is real. Talon hook-and-claw tattoos inside both forearms (distinct from the guard diamond sigils — Rocketcandy recognizes the order). Casts spells (Hold Person witnessed). Parental devotion to Lilly; magical protection pact with Gulgrim. Unflappable dignity under indignity; dry menace toward threats, playful precision at home.

### Apothecary owner (S1 hooded figure) — NOT Biggins
`kindly older gentleman, gray beard, dark hooded cloak, cob pipe` — fun-loving shopkeeper who owns a local apothecary. Keep distinct from Biggins.
Two apothecaries in Neverwinter (transcript canon, user-confirmed 2026-11-03): this hooded gentleman ≠ Thumba, proprietor of Colorful Creations (Chip's favor-holder, theme-music quest giver). The proprietor's "find Thumba" contact and the P5.5 owner are the SAME man. Spelling: Thumba.

### Lady Filvenar — IS Lilly in disguise (Session 1, user canon)
`adult woman, fire-red hair in a Celtic-knot braid to mid-back, gray eyes, pirate shirt + tight corset, trousers, ready stance — same face as Lilly (curly red hair, freckles)`
Use Lilly's approved face; the braid and gray eyes are the disguise.

### Lady Elara Veyne
Ref gallery/NPCs/Lady_Elara_Veyne.png: `mature noblewoman dark hair updo, blue/silver court gown with lion crest, sapphire jewelry, throne room` — use ref image, do not freestyle.

### Lady Verruth, Matron of the Ashen Library
`female demon, long black hair, upward-curved horns, bat wings, barbed tail, glasses, black-red corset, thigh-high boots, burning book` Ref gallery/NPCs/Lady_Verruth...png. HAS wings (unlike Keechwah). NEVER confuse with Keechwah.

### Guild Shadow Knight (recurring villain)
`hooded black cloak, glowing white eyes, antler/deer-skull emblem on chest, twin crossbows, black smoke-wreathed blades` Ref gallery/NPCs/Guild_Shadowknight.png.

### City Guards (corrupt vs clean)
Corrupt: `ornate helm with red plume, red cape, gold phoenix crest, geometric diamond forearm tattoo (gallery/Objects/The_Tattoo.png), star above tattoo = leader`. Clean guards: plain steel, NO tattoo. Ref gallery/NPCs/City_Guards.png = corrupt look.

### Marigold / Sammy
### Marigold — Female Halfling Innkeeper, owns Marigold's Inn (recurring NPC)
`middle-aged halfling woman innkeeper in her 40s, barely 3 feet tall, tiny curly brown hair, warm rosy happy face with laugh lines, plain brown working dress with apron, serving tray`
Approved identity ref (2026-11-02, Flux3 Klein): `character-bible/approved_marigold_reference.png` — copy this face; adult likeness approved in the Flux3 v1 portrait.
NEVER: child, young woman, tall human woman (she is a 3ft halfling — state it in every panel), barmaid looks that copy Lilly or Vadania.
Sammy: adult male cook in apron, menu/label in hand, loud. NEVER gender-swap Sammy, NEVER make Lilly the screamer in S1P3.
Default expression: warm and welcoming — beaming hostess, hands full.

## Party sheet facts (canon — character-bible/Sheets/*.pdf, user-approved 2026-11-01)
Non-visual canon for direction, dialogue, and props. Sheet-vs-gallery conflicts resolved by user: Chip white hair (sheet wins), Gulgrim warhammer (bible wins over sheet's mace), Vadania brown hair + green eyes (sheet wins over gallery blonde), Rocketcandy nobility precision adopted.
- **Shade**: Rogue 5, Halfling, Criminal, Small. Custom nonchalant (DEX) skill; Thieves' Cant, Common Sign Language, Undercommon; Disguise Kit + Thieves' Tools. Spy-for-hire past — "the party's unseen shadow."
- **Chip**: Druid 5, Human, Sage, age 35, 5'11", brown eyes. Circle of the Stars, master astronomer. Awkward observer who blurts insults, last to speak. Druidic, Elvish, Gnomish, Goblin; Herbalism Kit. Wild shapes: warhorse, giant weasel, frog, giant goat, giant seahorse, cat.
- **Gulgrim**: Cleric 5, Hill Dwarf, Soldier (Mintarn island → Neverwinter city watch, quit over corruption), Life Domain, faith Marthammor Du, Neutral Good. Carries Holy Symbol + Biggins manor key (plot item). Mason's tools, playing cards; Dwarvish, Elvish, Goblin.
- **Keechwah**: Warlock 5, Tiefling, Sage, Chaotic Neutral, patron The Fiend, Pact of the Tome (Book of Shadows). Sold his soul for knowledge; loves mysteries, paranoid about secrets. Orb focus + lute. Infernal, Giant, Elvish; reads all writing, telepathic.
- **Rocketcandy**: Paladin 5, Human, Noble (lost Corlinn Hill — erased by Mount Hotenow), Lawful Good, faith Bahamut, Oath of the Open Sea (Marine Layer, Fury of the Tides). +3 battleaxe, Plate +2, signet ring. Draconic, Dwarvish, Giant; Sentinel feat.
- **Vadania**: Ranger 5, Wood Elf, Folk Hero, Neutral, Hunter (Horde Breaker), favored enemy Giants, favored terrain Mountain. Monster Hunter's Longbow +1, twin shortswords. Action over theory, blunt sincerity. Backstory: Night of Cinders (organized bandits burned his enclave, parents killed). Elvish, Giant; Woodcarver's Tools.

## Scale reference (approved 2026-11-02, Flux3 Klein)
`character-bible/approved_lineup_reference.png` — all six party members side by side with name placards. Use for relative heights in group panels: Shade (halfling, Small, ~3 ft) is clearly the smallest; Gulgrim (dwarf, Medium, ~4-5 ft) is short and stocky but a full head-plus taller than Shade; Chip (5'11"), Rocketcandy, Keechwah, and Vadania (6'2") stand tall together. Dwarf-taller-than-halfling is 5e canon (PHB: halflings ~3 ft, dwarves 4-5 ft), confirmed on both sheets (Shade Small, Gulgrim Medium) — never draw them the same height.

## Panel composition rules (anti-drift)
- Max 4 named characters per image. Split crowds into 2 panels.
- Name holders: `Chip holding wooden staff`, `Vadania holding longbow`, `Rocketcandy exactly two arms`.
- Ban barmaids that look like Lilly/Vadania: `one separate female human barmaid with brown ponytail, plain blue dress, holding tray, distinct from party`.
- If duplicate appears, re-roll SAME seed+1 with `single X, no duplicates` doubled — do not accept.
- Log: prompt, seed, model hashes per panel in sessions/<id>/panels.json (add next).
