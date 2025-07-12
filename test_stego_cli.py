
import unittest
from PIL import Image
import os
from stego_cli import encode, decode  # This assumes the CLI code is in stego_cli.py

class TestSteganographyCLI(unittest.TestCase):
    def setUp(self):
        self.input_image = "test_input.png"
        self.output_image = "test_output.png"
        self.secret_message = "Hello CLI!"
        self._create_blank_image()

    def _create_blank_image(self):
        img = Image.new('RGB', (100, 100), color='white')
        img.save(self.input_image)

    def tearDown(self):
        if os.path.exists(self.input_image):
            os.remove(self.input_image)
        if os.path.exists(self.output_image):
            os.remove(self.output_image)

    def test_encode_and_decode(self):
        encode(self.input_image, self.secret_message, self.output_image)
        decoded_msg = decode(self.output_image)
        self.assertEqual(decoded_msg, self.secret_message)

    def test_decode_empty_image(self):
        decoded = decode(self.input_image)
        self.assertEqual(decoded, "")  # No EOF should be found in untouched image

if __name__ == '__main__':
    unittest.main()
