import unittest
import os
import json
from mental import MentalMemory, process_input, MEMORY_FILE

class TestMentalAI(unittest.TestCase):
    def setUp(self):
        # Backup existing memory if any
        if os.path.exists(MEMORY_FILE):
            os.rename(MEMORY_FILE, MEMORY_FILE + ".bak")
        self.memory = MentalMemory()

    def tearDown(self):
        # Restore backup
        if os.path.exists(MEMORY_FILE + ".bak"):
            os.rename(MEMORY_FILE + ".bak", MEMORY_FILE)
        elif os.path.exists(MEMORY_FILE):
            os.remove(MEMORY_FILE)

    def test_memory_save_load(self):
        self.memory.remember("Test Note")
        notes = self.memory.get_notes()
        self.assertIn("Test Note", notes)

        # Verify persistence
        new_mem = MentalMemory()
        self.assertIn("Test Note", new_mem.get_notes())

    def test_website_guide(self):
        response = process_input("Build website", self.memory)
        self.assertIn("Folder structure", response)
        self.assertIn("HTML", response)

    def test_code_request(self):
        response = process_input("Code do html", self.memory)
        self.assertIn("<!DOCTYPE html>", response)

        response = process_input("Code do python", self.memory)
        self.assertIn("def hello():", response)

    def test_persona_sad(self):
        response = process_input("I am sad", self.memory)
        self.assertIn("Aww, kya hua?", response)

    def test_yaad_rakho(self):
        response = process_input("Yaad rakho Buy milk", self.memory)
        self.assertIn("Theek hai, yaad rakhungi!", response)
        self.assertIn("Buy milk", self.memory.get_notes())

if __name__ == '__main__':
    unittest.main()
