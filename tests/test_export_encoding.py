import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
from PIL import Image

from mapgen.export import write_all


class ExportEncodingTest(unittest.TestCase):
    def test_write_all_uses_utf8_for_unicode_metadata_on_windows(self):
        original_write_text = Path.write_text
        original_read_text = Path.read_text

        def cp932_write_text(path, data, encoding=None, errors=None, newline=None):
            return original_write_text(
                path, data, encoding=encoding or "cp932", errors=errors, newline=newline
            )

        def cp932_read_text(path, encoding=None, errors=None, newline=None):
            return original_read_text(
                path, encoding=encoding or "cp932", errors=errors, newline=newline
            )

        with tempfile.TemporaryDirectory() as temp_dir:
            with patch.object(Path, "write_text", cp932_write_text), patch.object(
                Path, "read_text", cp932_read_text
            ):
                out = write_all(
                    Path(temp_dir) / "map",
                    kinds=np.zeros((1, 1), dtype=np.int64),
                    tiles=np.zeros((1, 1), dtype=np.int64),
                    tileset=Image.new("RGBA", (16, 16)),
                    source_img=Image.new("RGB", (1, 1)),
                    semantic_img=Image.new("RGB", (1, 1)),
                    labels=[],
                    meta={
                        "place": "福岡市",
                        "source": "gsi",
                        "tile_m": 8,
                        "attribution": "Map data ©Google",
                    },
                )

            tmj = (out / "map.tmj").read_bytes().decode("utf-8")
            self.assertIn("Map data ©Google", tmj)


if __name__ == "__main__":
    unittest.main()
