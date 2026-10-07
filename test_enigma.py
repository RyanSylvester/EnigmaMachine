import unittest

from enigma import EnigmaMachine, PlugLead, Plugboard, Rotorboard


def make_machine(rotors, reflector, rings, positions, plugs=()):
    plugboard = Plugboard()
    for pair in plugs:
        plugboard.add(PlugLead(pair))
    board = Rotorboard(list(rotors), reflector, list(rings), positions)
    return EnigmaMachine(board, plugboard)


def window_letters(machine, keys):
    seen = []
    for _ in range(keys):
        machine.Encode("A")
        seen.append(machine.Rotorboard.Position)
    return seen


class KnownVectors(unittest.TestCase):
    def test_textbook_aaa(self):
        machine = make_machine(["I", "II", "III"], "B", [1, 1, 1], "AAA")
        self.assertEqual(machine.EncodeMessage("AAAAA"), "BDZGO")

    def test_barbarossa_1941(self):
        # Enigma I message from 7 July 1941: rotors II IV V, reflector B,
        # rings B U L, message key BLA.
        plugs = ["AV", "BS", "CG", "DL", "FU", "HZ", "IN", "KM", "OW", "RX"]
        machine = make_machine(["II", "IV", "V"], "B", [2, 21, 12], "BLA", plugs)
        cipher = "EDPUDNRGYSZRCXNUYTPOMRMBOFKTBZREZKMLXLVEFGUEYSIOZVEQMIKUBPMMYLKLTTDEISMDICAGYKUACTCDOMOHWXMUUIAUBSTSLRNBZSZWNRFXWFYSSXJZVIJHIDISHPRKLKAYUPADTXQSPINQMATLPIFSVKDASCTACDPBOPVHJK"
        plain = "AUFKLXABTEILUNGXVONXKURTINOWAXKURTINOWAXNORDWESTLXSEBEZXSEBEZXUAFFLIEGERSTRASZERIQTUNGXDUBROWKIXDUBROWKIXOPOTSCHKAXOPOTSCHKAXUMXEINSAQTDREINULLXUHRANGETRETENXANGRIFFXINFXRGTX"
        self.assertEqual(machine.EncodeMessage(cipher), plain)


class Stepping(unittest.TestCase):
    def test_double_step(self):
        machine = make_machine(["I", "II", "III"], "B", [1, 1, 1], "ADU")
        self.assertEqual(window_letters(machine, 3), ["ADV", "AEW", "BFX"])

    def test_four_rotor_double_step(self):
        machine = make_machine(["Beta", "I", "II", "III"], "B", [1, 1, 1, 1], "AADU")
        self.assertEqual(window_letters(machine, 3), ["AADV", "AAEW", "ABFX"])

    def test_four_rotor_slow_rotor_on_its_notch_stays_put(self):
        # A real M4 has no pawl reading the slow rotor's notch, so only the
        # fast rotor moves. The 2021 version stepped the slow and middle
        # rotors on every key here (AQAA -> ARBB).
        machine = make_machine(["Beta", "I", "II", "III"], "B", [1, 1, 1, 1], "AQAA")
        self.assertEqual(window_letters(machine, 3), ["AQAB", "AQAC", "AQAD"])

    def test_greek_rotor_never_moves(self):
        machine = make_machine(["Gamma", "V", "IV", "III"], "C", [1, 1, 1, 1], "ZZJV")
        self.assertTrue(all(w[0] == "Z" for w in window_letters(machine, 700)))

    def test_four_rotor_matches_pawl_model(self):
        notches = {"I": "Q", "II": "E", "III": "V", "IV": "J", "V": "Z"}
        rotors = ["Beta", "IV", "V", "I"]
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for slow in alphabet:
            for middle in alphabet:
                for fast in "PQRZ":
                    start = "A" + slow + middle + fast
                    machine = make_machine(rotors, "B", [1, 1, 1, 1], start)
                    machine.Encode("A")
                    steps = [False, False, False, True]
                    for i in (1, 2):  # pawls between the three moving rotors
                        if start[i + 1] == notches[rotors[i + 1]]:
                            steps[i] = steps[i + 1] = True
                    expected = "".join(
                        alphabet[(alphabet.index(c) + s) % 26] for c, s in zip(start, steps)
                    )
                    self.assertEqual(machine.Rotorboard.Position, expected, start)


if __name__ == "__main__":
    unittest.main()
