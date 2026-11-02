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
`young adult halfling man, mid-20s, mature adult face, lean build, messy shaggy dark brown hair falling over and covering his ears, ears small and rounded beneath it, light stubble, no beard, warm brown eyes, subtle sly closed-mouth expression, worn dark linen shirt with rolled sleeves, scuffed brown leather vest, belt dagger at hips`
Approved identity ref (2026-11-01, Flux3 Klein): `character-bible/approved_shade_reference.png` — copy this face for any new Shade portrait; other gallery refs show pointed ears or wrong builds, face is secondary to this one.
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
`adult male hill dwarf cleric, short stocky, broad long white beard, heavy furs, frost-covered boots, large round shield with holy rune, warhammer`
Approved identity ref (2026-11-02, Flux3 Klein): `character-bible/approved_gulgrim_reference.png` — copy this look; face, gear, and expression approved in the Flux3 v1 portrait (full-body framing shows the frost boots).
NEVER: tall, thin, no-beard.
Gear: Holy Symbol + Biggins manor key (plot item), Mason's tools. Soldier background (Mintarn → Neverwinter watch, quit over corruption). Faith: Marthammor Du. Warhammer is canon (user decision — sheet's mace ignored).
Default expression: steadfast and resolute — stern veteran soldier-cleric, no smile.

### Chip — Male Human Druid (Josh)
`adult male human druid, wild long white hair and white beard, green/brown fur garb, holding wooden staff (HE holds it, never Vadania)`
NEVER: give staff to Vadania, merge with Vadania, bat on shoulder (Celeste rarely pictured), brown hair or beard (canon is white per sheet).
Expression: awkward observer — blurts insults without thinking, last to speak. Prop: his quarterstaff has the crystal Star Map slotted into it (Circle of the Stars).

### Vadania Amakiir — Male Wood Elf Ranger (Derek)
`adult male wood elf ranger, long brown hair, green eyes, pointed ears, masculine jaw stubble, green cloak, longbow on back, short swords at hips, scar on shoulder`
NEVER: female, dress, blonde hair (canon is brown per sheet — user decision 2026-11-01), long blonde woman in green (that is a misrender — re-roll), duplicate Vadania as barmaid.
Expression: action over theory, blunt and sincere, follows through. Weapon: Monster Hunter's Longbow +1 (ornate named longbow) + twin shortswords.

### Lilly — Adult woman early 20s (NOT a child)
`adult young woman early 20s, curly voluminous red hair, freckles, white ruffled shirt, red corset laced gold, cream skirt, brown boots, thigh dagger + rapier with mother-of-pearl handle`
Refs: gallery/NPCs/Lilly.png (LOCKED), Keechwah_and_Lilly_bonding.png. NEVER: child, little girl, schoolgirl.

### Water Bear — Owlbear, ONE creature
`single owlbear creature, massive grizzly bear body with coarse brown fur and bear paws with claws, head REPLACED by owl head with round eyes and hooked beak and feathered ruff, no wings, no second head, no separate owl`
NEVER: bear holding owl, two heads, wings, white snowy owl alone, bear head + owl head side by side.

### Biggins Aulswim — Lilly's protector, ex-Talons of Justice assassin
`tall adult human man in his 40s, slicked gray-streaked dark hair, sharp cheekbones, blue eyes, black three-piece suit with long coat, white shirt black tie, white gloves, pocket-watch chain, holding bloody dagger when hunting`
Ref: gallery/NPCs/Biggans_Aulswim.png (note filename typo Biggans). NOT old gentleman, NOT apothecary. First appears Session 2.

### Apothecary owner (S1 hooded figure) — NOT Biggins
`kindly older gentleman, gray beard, dark hooded cloak, cob pipe` — fun-loving shopkeeper, owns local apothecary. Keep distinct from Biggins.

### Lady Filvenar
`adult woman, fire-red Celtic-knot braid to mid-back, gray eyes, pirate shirt + tight corset, trousers, ready stance`

### Lady Elara Veyne
Ref gallery/NPCs/Lady_Elara_Veyne.png: `mature noblewoman dark hair updo, blue/silver court gown with lion crest, sapphire jewelry, throne room` — use ref image, do not freestyle.

### Lady Verruth, Matron of the Ashen Library
`female demon, long black hair, upward-curved horns, bat wings, barbed tail, glasses, black-red corset, thigh-high boots, burning book` Ref gallery/NPCs/Lady_Verruth...png. HAS wings (unlike Keechwah). NEVER confuse with Keechwah.

### Guild Shadow Knight (recurring villain)
`hooded black cloak, glowing white eyes, antler/deer-skull emblem on chest, twin crossbows, black smoke-wreathed blades` Ref gallery/NPCs/Guild_Shadowknight.png.

### City Guards (corrupt vs clean)
Corrupt: `ornate helm with red plume, red cape, gold phoenix crest, geometric diamond forearm tattoo (gallery/Objects/The_Tattoo.png), star above tattoo = leader`. Clean guards: plain steel, NO tattoo. Ref gallery/NPCs/City_Guards.png = corrupt look.

### Marigold / Sammy
Marigold: female innkeeper, warm, tray. Sammy: adult male cook in apron, menu/label in hand, loud. NEVER gender-swap Sammy, NEVER make Lilly the screamer in S1P3.

## Party sheet facts (canon — character-bible/Sheets/*.pdf, user-approved 2026-11-01)
Non-visual canon for direction, dialogue, and props. Sheet-vs-gallery conflicts resolved by user: Chip white hair (sheet wins), Gulgrim warhammer (bible wins over sheet's mace), Vadania brown hair + green eyes (sheet wins over gallery blonde), Rocketcandy nobility precision adopted.
- **Shade**: Rogue 5, Halfling, Criminal, Small. Custom nonchalant (DEX) skill; Thieves' Cant, Common Sign Language, Undercommon; Disguise Kit + Thieves' Tools. Spy-for-hire past — "the party's unseen shadow."
- **Chip**: Druid 5, Human, Sage, age 35, 5'11", brown eyes. Circle of the Stars, master astronomer. Awkward observer who blurts insults, last to speak. Druidic, Elvish, Gnomish, Goblin; Herbalism Kit. Wild shapes: warhorse, giant weasel, frog, giant goat, giant seahorse, cat.
- **Gulgrim**: Cleric 5, Hill Dwarf, Soldier (Mintarn island → Neverwinter city watch, quit over corruption), Life Domain, faith Marthammor Du, Neutral Good. Carries Holy Symbol + Biggins manor key (plot item). Mason's tools, playing cards; Dwarvish, Elvish, Goblin.
- **Keechwah**: Warlock 5, Tiefling, Sage, Chaotic Neutral, patron The Fiend, Pact of the Tome (Book of Shadows). Sold his soul for knowledge; loves mysteries, paranoid about secrets. Orb focus + lute. Infernal, Giant, Elvish; reads all writing, telepathic.
- **Rocketcandy**: Paladin 5, Human, Noble (lost Corlinn Hill — erased by Mount Hotenow), Lawful Good, faith Bahamut, Oath of the Open Sea (Marine Layer, Fury of the Tides). +3 battleaxe, Plate +2, signet ring. Draconic, Dwarvish, Giant; Sentinel feat.
- **Vadania**: Ranger 5, Wood Elf, Folk Hero, Neutral, Hunter (Horde Breaker), favored enemy Giants, favored terrain Mountain. Monster Hunter's Longbow +1, twin shortswords. Action over theory, blunt sincerity. Backstory: Night of Cinders (organized bandits burned his enclave, parents killed). Elvish, Giant; Woodcarver's Tools.

## Panel composition rules (anti-drift)
- Max 4 named characters per image. Split crowds into 2 panels.
- Name holders: `Chip holding wooden staff`, `Vadania holding longbow`, `Rocketcandy exactly two arms`.
- Ban barmaids that look like Lilly/Vadania: `one separate female human barmaid with brown ponytail, plain blue dress, holding tray, distinct from party`.
- If duplicate appears, re-roll SAME seed+1 with `single X, no duplicates` doubled — do not accept.
- Log: prompt, seed, model hashes per panel in sessions/<id>/panels.json (add next).
