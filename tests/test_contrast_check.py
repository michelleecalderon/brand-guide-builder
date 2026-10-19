import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "skills", "brand-guide-builder", "scripts"))
import contrast_check as cc  # noqa: E402


class ContrastTests(unittest.TestCase):
    def test_black_on_white_is_21(self):
        self.assertAlmostEqual(cc.contrast_ratio("#000000", "#FFFFFF"), 21.0, places=2)

    def test_identical_colors_is_1(self):
        self.assertAlmostEqual(cc.contrast_ratio("#336699", "#336699"), 1.0, places=2)

    def test_ratio_is_symmetric(self):
        self.assertAlmostEqual(cc.contrast_ratio("#2F5D50", "#FAF7F0"), cc.contrast_ratio("#FAF7F0", "#2F5D50"))

    def test_aa_threshold_boundary(self):
        # #767676 on white is the lightest grey that passes AA (4.54); #777777 just misses (4.48)
        self.assertGreaterEqual(cc.contrast_ratio("#767676", "#FFFFFF"), 4.5)
        self.assertLess(cc.contrast_ratio("#777777", "#FFFFFF"), 4.5)

    def test_short_hex_and_no_hash(self):
        self.assertEqual(cc.hex_to_rgb("fff"), (255, 255, 255))
        self.assertEqual(cc.hex_to_rgb("#0a0"), (0, 170, 0))

    def test_invalid_hex_raises(self):
        for bad in ("#12", "#GGGGGG", "", "#1234567"):
            with self.assertRaises(ValueError):
                cc.hex_to_rgb(bad)

    def test_pair_count_and_sorting(self):
        pal = [{"name": n, "hex": h} for n, h in (("A", "#000"), ("B", "#fff"), ("C", "#888"))]
        rows = cc.compute_pairs(pal)
        self.assertEqual(len(rows), 6)  # n * (n - 1) ordered pairs
        self.assertEqual([r["ratio"] for r in rows], sorted((r["ratio"] for r in rows), reverse=True))

    def test_duplicate_names_rejected(self):
        with self.assertRaises(ValueError):
            cc.compute_pairs([{"name": "A", "hex": "#000"}, {"name": "A", "hex": "#fff"}])

    def test_exit_code_when_fewer_than_two_aa_pairs(self):
        weak = '[{"name":"A","hex":"#eeeeee"},{"name":"B","hex":"#ffffff"}]'
        self.assertEqual(cc.main([weak]), 2)
        strong = '[{"name":"A","hex":"#000000"},{"name":"B","hex":"#ffffff"}]'
        self.assertEqual(cc.main([strong]), 0)


if __name__ == "__main__":
    unittest.main()
