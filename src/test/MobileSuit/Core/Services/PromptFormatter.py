#PromptFormatter.py
import unittest
from typing import List
from colour import Color
from ReFreSH.MobileSuit.PrintUnit import PrintUnit
from ReFreSH.MobileSuit.Resources import Lang
from ReFreSH.MobileSuit.Core.Services.PromptFormatter import  PromptFormatters

class TestPromptFormatters(unittest.TestCase):

    def setUp(self):
        self.units = [
            PrintUnit("Hello", Color("red"), Color("black")),
            PrintUnit("World", Color("green"), Color("blue")),
            PrintUnit("", Color("yellow"), Color("purple")),  # Empty text unit
            PrintUnit("!", Color("white"), Color("grey"))
        ]

    def test_BasicPromptFormatter(self):
        expected_output = [
            PrintUnit(" [Hello] ", Color("red"), Color("black")),
            PrintUnit("[World] ", Color("green"), Color("blue")),
            PrintUnit("[!] >", Color("white"), Color("grey"))
        ]
        result = list(PromptFormatters.BasicPromptFormatter(self.units))
        self.assertEqual(result, expected_output)

    def test_PowerLineFormatter(self):
        expected_output = [
            PrintUnit(" ", Color("black"), Color("red")),
            PrintUnit("Hello", Color("black"), Color("red")),
            PrintUnit(" ", Color("black"), Color("red")),
            PrintUnit(" ", Color("red"), Color("green")),
            PrintUnit("World", Color("blue"), Color("green")),
            PrintUnit(" ", Color("blue"), Color("green")),
            PrintUnit(" ", Color("green"), Color("yellow")),
            PrintUnit("!", Color("gray"), Color("white")),
            PrintUnit(" ", Color("gray"), Color("white"))
        ]
        result = list(PromptFormatters.PowerLineFormatter(self.units))
        self.assertEqual(result, expected_output)
if __name__ == '__main__':
    unittest.main()