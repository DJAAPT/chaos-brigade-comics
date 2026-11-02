import json
import os
import unittest


class TestPrepareFlux3Base(unittest.TestCase):
    def test_base_graph_sentinel_and_flux3_rig(self):
        self.assertTrue(
            os.path.exists("workflows/base_flux3.json"),
            "workflows/base_flux3.json missing (Task 1 not run yet)",
        )
        with open("workflows/base_flux3.json", encoding="utf-8") as f:
            g = json.load(f)

        texts = [n["inputs"]["text"] for n in g.values() if "text" in n.get("inputs", {})]
        self.assertEqual(texts.count("{{PROMPT}}"), 1)
        self.assertFalse(any(t.startswith("cinematic fantasy film still") for t in texts))

        self.assertTrue(
            any(n["inputs"].get("unet_name") == "flux3-image-klein-nvfp4.safetensors" for n in g.values())
        )
        self.assertTrue(
            any(n["inputs"].get("clip_name") == "qwen3vl_4b_int8_convrot.safetensors" for n in g.values())
        )

        ks = next(n for n in g.values() if n["class_type"] == "KSampler")
        self.assertEqual(ks["inputs"]["steps"], 15)
        self.assertEqual(ks["inputs"]["cfg"], 1.0)

        lat = next(n for n in g.values() if n["class_type"] == "EmptyFlux2LatentImage")
        self.assertEqual((lat["inputs"]["width"], lat["inputs"]["height"]), (1344, 768))


if __name__ == "__main__":
    unittest.main()
