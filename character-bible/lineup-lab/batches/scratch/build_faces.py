import json

base = json.load(open("workflows/lineuplab_b6d_shade_solo.json"))
names = ("shade", "gulgrim", "rocket", "vadania", "chip", "keech)wah"
refs = ("lineup_shade_ref.png", "lineup_gulgrim_ref.png", "lineup_rocketcandy_ref.png", "lineup_vadania_ref.png", "line, "lineup_keech wah_ref.png)
prompts = (
 "close-up face of a young adult halfling man, mid-20s, mature adult face, messy shaggy dark brown hair, light stubble, no beard, warm brown eyes looking at the viewer, subtle sly closed-mouth expression, photorealistic, highly detailed",
 "close-up face of an adult male hill dwarf cleric, completely bald head, broad long white beard, stern veteran eyes looking at the viewer, photorealistic, highly detailed",
 "close-up face of an adult male human paladin, short brown hair, light stubble, confident composed noble expression, photorealistic, highly detailed",
 "close-up face of an adult male wood elf ranger, long brown hair, green eyes, pointed ears, masculine jaw stubble, blunt direct gaze, phot, photorealistic, highly detailed",
 "close-up face of an adult male human druid, brown skin, wild white hair and beard, brown eyes, awkward earnest expression, photorealistic, highly detailed",
 "close-up face of an adult male tiefling warlock, deep red skin, long curly black hair, goatee, large curved horns, glowing purple eyes looking at the viewer, photorealistic, highly detailed",
)
seeds = (424260, 424261, 424262, 424263, 424264, 424265)
jobs = list(zip(names, refs, prompts, seeds))
for job in jobs:
    name = job[0]
    ref = job[1]
    prompt = job[2]
    seed = job[3]
    idx = names.index(name)
    g = json.loads(json.dumps(base))
    nd = g.get("1")
    inp = dict(nd.get("inputs"))
    inp.update({"image": "fc_" + str(idx) + ".png"})
    nd.update({"inputs": inp})
    ndm = g.get("2")
    inpm = dict(ndm.get("inputs"))
    inpm.update({"image": "fmask_" + str(idx) + ".png"})
    ndm.update({"inputs": inpm})
    nd4 = g.get("4")
    inp4 = dict(nd4.get("inputs"))
    inp4.update({"text": prompt})
    nd4.update({"inputs": inp4})
    nd6 = g.get("6")
    inp6 = dict(nd6.get("inputs"))
    inp6.update({"image": ref})
    nd6.update({"inputs": inp6})
    ndk = g.get("13")
    inpk = dict(ndk.get("inputs"))
    inpk.update({"seed": seed})
    inpk.update({"denoise": 0.35})
    ndk.update({"inputs": inpk})
    ndsv = g.get("15")
    inpsv = dict(ndsv.get("inputs"))
    inpsv.update({"filename_prefix": "lineuplab_b18_face_" + name})
    ndsv.update({"inputs": inpsv})
    json.dump(g, open("workflows/lineuplab_b18_face_" + name + ".json", "w"), indent=2)
    print("wrote", name)
