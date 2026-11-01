# Chaos Brigade — Character Bible v1 (locked 2026-11-01)

Approved reference: `character-bible/approved_S1P1_reference.png` (S1P1 v7)
Gallery refs: `O:\ExternalSites\html\DND\gallery\`

## Global style
cinematic fantasy film still, photorealistic, highly detailed adult faces, no duplicates, no conflation, exactly two arms per humanoid, six distinct characters unless noted.

## Flux 2 pin (remote 10.13.37.88:8188)
- Template base: `image_flux2_text_to_image`
- VAE: `flux2-vae.safetensors`
- CLIP: `mistral_3_small_flux2_fp8.safetensors`, type `flux2`
- UNET: `flux2_dev_fp8mixed.safetensors`
- Size panels: 1344x768 | portraits: 768x1344
- Steps: 20, sampler euler, guidance 4.0
- Always specify: adult, male/female, no wings unless noted, single creature, no duplicates.

## Party

### Shade (St3v3D / David) — Male Halfling / Rogue
- Adult halfling man, SHORT stature but grown man face, stubble, NOT a child
- Leather armor, dual daggers, Bullseye Lantern when scouting
- Sly confident grin, Guild contacts
- Prompt core: `adult halfling man short stature grown man face stubble leather armor dagger`
- Do NOT: child, boy, teen, bare feet hobbit, wings

### Rocketcandy (Andrew) — Male Human / Paladin
- Adult man, shining plate armor with gold wing crest on chest, exactly two arms
- Red cape / red plume on helm for formal scenes, holy symbol
- Noble bearing, former nobility Neverwinter
- Prompt core: `human paladin shining plate armor gold wing crest exactly two arms`
- Do NOT: extra limbs, female, modern clothes

### Keechwah (ABush1707 / Aaron) — Male Tiefling / Warlock
- Adult MALE, deep red skin, large curved horns, glowing purple eyes, male facial features
- Dark robes / armor, purple arcane glow, blue Witch Bolt lightning in hands
- Patron voice in head, book that thrums
- Prompt core: `male tiefling warlock red skin curved horns glowing purple eyes NO wings`
- Do NOT: female, wings, hooves unless specified, duplicate Keechwahs

### Gulgrim Frozenboots (Bearnuts / James) — Male Hill Dwarf / Cleric
- Stout adult dwarf, broad white beard, heavy furs, frost-covered boots
- Large round shield with holy rune, warhammer / mace
- Warm kind eyes, protector
- Prompt core: `hill dwarf cleric broad white beard heavy furs frost boots round shield`
- Gallery note: `St3v3D_Chaos_Brigade.png` shows blue ice magic version — use sparingly.

### Chip (Byodan / Josh) — Male Human / Druid
- Adult man, wild long brown hair and beard, wooden staff (HE holds it, not Vadania)
- Green / fur garb, celestial glitter when transformed, Daylight crystal on staff
- Companion: Water Bear owlbear, bat Celeste (tiny, rarely pictured)
- Prompt core: `male human druid wild brown hair beard holding wooden staff`
- Do NOT: give staff to Vadania, merge with Vadania

### Vadania Amakiir (xenophase / Derek) — Male Wood Elf / Ranger
- Adult MALE, long blonde hair (or long hair per player — no blond in v5 approved, keep long hair), pointed ears, green cloak
- Longbow on back, short swords at hips, crossbow-bolt scar on shoulder
- Prompt core: `male wood elf ranger long hair pointed ears green cloak holding longbow`
- Do NOT: female, dress, duplicate Vadania as barmaid

## NPCs

### Lilly
- Adult young woman early 20s, curly voluminous red hair, white ruffled shirt, red corset laced gold, cream skirt, brown boots
- Knife + thigh dagger, rapier with mother-of-pearl handle (gift from Gulgrim)
- Prompt core: `adult young woman early 20s curly red hair white shirt red corset cream skirt`
- Gallery: `gallery/NPCs/Lilly.png` — never a little girl
- Do NOT: child, little girl

### Water Bear (Chip companion)
- ONE creature: grizzly bear body + owl head REPLACING bear head, no wings, no second head
- Large, furry, owl eyes / beak, bear paws with claws
- Prompt core: `owlbear Waterbear one creature grizzly bear body owl head replacing bear head no wings no second head`
- Do NOT: bear holding owl, two heads, wings, white snowy owl alone

### Guild Shadow Knight (recurring villain)
- Hooded black cloak, glowing white eyes, antler / deer-skull emblem on chest, twin crossbows
- Black smoke-wreathed blades
- Gallery: `gallery/NPCs/Guild_Shadowknight.png`
- Prompt core: `hooded black cloak glowing white eyes antler skull emblem twin crossbows black smoke blades`

### Biggins Aulswim
- Kindly old gentleman, gentle smile, dark hooded cloak + cob pipe when mysterious
- Gallery: `gallery/NPCs/Biggans_Aulswim.png` (check spelling Biggins_Aulswim.png)
- Former Talons of Justice, Lilly's adoptive father

### Lady Filvenar
- Adult woman, fire red Celtic-knot braided hair to mid-back, gray eyes, pirate shirt + tight corset
- Regal but rough-and-tumble

### Lady Elara Veyne / Lady Verruth / City Guards
- See `gallery/NPCs/` — use reference images directly when introducing.

## Anti-conflation rules (learned from S1)
- Always list headcount: `six distinct characters no duplicates`
- Specify holder: `Chip holding wooden staff`, `Vadania holding longbow`
- Separate NPCs: `one separate female human barmaid standing holding tray`
- Ban wings on tieflings, ban extra arms, ban second heads on owlbear.
- If duplicate appears, regenerate with `single X, no duplicates` added twice.
