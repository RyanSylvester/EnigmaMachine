from enigma import *
import itertools

class Decoder:
    def __init__(self, PlugCount = 0):
        self.BRotors =  []
        self.BReflectors = []
        self.BSettings = []
        self.BPositions = []
        self.Pairs = []
        self.BPairs = []
        self.BLeadCharacters = []
        self.GLeadCharacters = []
        self.PlugCount = PlugCount

    # Adds the component so that we can eliminate all possibilities that aren't the input value
    # Elimninated values are denoted with a "B". ie. self.BRotors is a list of "bad" rotors
    def addComponent(self,value,type):
        CharactersUsed = []

        # Eliminate all rotor values that don't match our added rotor setup
        if type == "Rotors":
            for x in range(7): # Rotor 1
                for y in range(7): # Rotor 2
                    for z in range(7): # Rotor 3
                        if value != [self.RotorValueToRotor(x),self.RotorValueToRotor(y),self.RotorValueToRotor(z)] and value not in self.BRotors:
                            self.BRotors.append([self.RotorValueToRotor(x),self.RotorValueToRotor(y),self.RotorValueToRotor(z)])

        # Eliminate all reflectors that don't match our added reflector
        elif type == "Reflectors":
            for x in range(3):
                if value != str(chr(x+65)) and value not in self.BReflectors:
                    self.BReflectors.append(str(chr(x+65)))

        # Eliminate bad settings combos
        elif type == "Settings":
            for S1 in range(26):
                for S2 in range(26):
                    for S3 in range(26):
                        if value != [S1+1,S2+1,S3+1] and value not in self.BSettings:
                            self.BSettings.append([S1+1,S2+1,S3+1])

        # Eliminate bad positions combos
        elif type == "Positions":
            for P1 in range(26):
                for P2 in range(26):
                    for P3 in range(26):
                        if value != str((str(chr(P1 + 65)) + str(chr(P2 + 65)) + str(chr(P3 + 65)))) and value not in self.BPositions:
                            self.BPositions.append(str((str(chr(P1 + 65)) + str(chr(P2 + 65)) + str(chr(P3 + 65)))))

        # Elimnate pairs
        elif type == "Pairs":
            for Lead in range(len(value)):
                self.Pairs.append(value[Lead])
                for char in range(len(value[Lead])):
                    CharactersUsed.append(str(value[Lead][char]))

            for letter in range(26):
                if str(chr(letter+65)) in CharactersUsed and str(chr(letter+65)) not in self.BLeadCharacters:
                    self.BLeadCharacters.append(str(chr(letter+65))) # Store all GOOD characters
                else:
                    self.GLeadCharacters.append(str(chr(letter+65))) # Store all bad characters

            # Eliminate all of the bad pairs
            for Lead in range((self.PlugCount)):
                for L1 in range(26):
                    for L2 in range(26):
                        if str(chr(L1+65)) in self.BLeadCharacters or str(chr(L2+65)) in self.BLeadCharacters and (str(chr(L1+65) + str(chr(L2+65)))) not in self.BPairs:
                            self.BPairs.append((str(chr(L1+65) + str(chr(L2+65)))))

    # Main decoding function
    def decode(self, message, crib):
        # Set up a machine (settings don't matter here)
        plugboard = Plugboard()
        rotorboard = Rotorboard(["I","I","I"], "A", [1,1,1], "AAA")
        enigma = EnigmaMachine(rotorboard,plugboard)

        Predictions = []
        OriginalPosition = enigma.Rotorboard.Position

        # We now set up all combinations that we want to test
        # This is done after we have cut down to the smallest possible set
        Rotors = []
        Reflectors = []
        Positions = []
        Settings = []
        PairCombos = []

        # Go through all rotor combinations and store all values not in the elimnated comboes
        Rcount = 0
        for R1 in range(7): # Rotor 1
            for R2 in range(7): # Rotor 2
                for R3 in range(7): # Rotor 3
                    if [self.RotorValueToRotor(R1),self.RotorValueToRotor(R2),self.RotorValueToRotor(R3)] not in self.BRotors:
                        Rotors.append([self.RotorValueToRotor(R1),self.RotorValueToRotor(R2),self.RotorValueToRotor(R3)])
                        Rcount += 1
        RefCount = 0

        # Store all rotors that aren't elinated
        for Reflector in range(3):
            if str(chr(Reflector+65)) not in self.BReflectors:
                Reflectors.append(str(chr(Reflector+65)))
                RefCount += 1

        # Go through all position combinations and store all values not in the eliminated combos
        PCount = 0
        for P1 in range(26):
            for P2 in range(26):
                for P3 in range(26):
                    if str((str(chr(P1 + 65)) + str(chr(P2 + 65)) + str(chr(P3 + 65)))) not in self.BPositions:
                        Positions.append(str((str(chr(P1 + 65)) + str(chr(P2 + 65)) + str(chr(P3 + 65)))))
                        PCount += 1

        # Go through all settings combinations and store all values not in the eliminated combos
        SCount = 0
        for S1 in range(26):
            for S2 in range(26):
                for S3 in range(26):
                    if [S1+1,S2+1,S3+1] not in self.BSettings:
                        Settings.append([S1+1,S2+1,S3+1])
                        SCount += 1

        # Add all possible plugbaord combinations
        PLCount = 0
        MissingLeads = []
        FullPairs = []
        ComboList = []

        # Start by getting the entered values from the board
        for pair in range((self.PlugCount)):
            if len(self.Pairs[pair]) == 1:
                MissingLeads.append(self.Pairs[pair])

        # Create an ordered list the size of how many non-used plugboard characters we need to test
        possibilities = []
        for x in range(len(self.GLeadCharacters)):
            possibilities.append(x) # If there are 10 unused characters, this looks like [0,1,2,3,4,5,6,7,8,9]

        # Get all possible combinations of those possibilities, as long as the amount of missing leads
        ComboPossibilities = (list(itertools.product(possibilities,repeat = len(MissingLeads))))

        # Now we go through each of those combo number and turn them into letters
        for x in range(len(ComboPossibilities)):
            SingleCombination = []
            for i in range(len(MissingLeads)):
                SingleCombination.append(self.GLeadCharacters[ComboPossibilities[x][i]])
            ComboList.append(SingleCombination) # Create a list of all possible letter combinations to try

        # Now we go through that combo list and convert them into full useable sets for the plugboard
        for GLead in range(len(ComboList)):
            IncompleteCombo = []
            for missing in range(len(MissingLeads)):# Take the letter from half-lead and merge it with the corresponding combo letter
                IncompleteCombo.append(MissingLeads[missing] + ComboList[GLead][missing])
            for pair in range((self.PlugCount)): # Simple add the plug leads we already know of
                if len(self.Pairs[pair]) == 2:
                    IncompleteCombo.append(self.Pairs[pair])
            FullPairs.append(IncompleteCombo)
            PLCount += 1


        # Display the amount of combinations for each enigma feature
        print(f"Pairs: {PLCount}")
        print(f"Rotors: {Rcount}")
        print(f"Reflectors: {RefCount}")
        print(f"Positions: {PCount}")
        print(f"Settings: {SCount}")
        print(f"Total combinations that will be decoded: {Rcount*RefCount*PCount*SCount * PLCount}")

        # Go through each feature and test on every possible combo
        for r in range(len(Rotors)):
            enigma.Rotorboard.RotorValues =  Rotors[r]
            for ref in range(len(Reflectors)):
                enigma.Rotorboard.Reflector = Reflectors[ref]
                for s in range(len(Settings)):
                    enigma.Rotorboard.Settings = Settings[s]
                    for PL in range(len(FullPairs)):
                        enigma.Plugboard.Leads = []
                        DisplayLeads = []
                        for LeadNum in range(len(self.Pairs)):
                            enigma.Plugboard.add(PlugLead(FullPairs[PL][LeadNum]))
                            DisplayLeads.append(FullPairs[PL][LeadNum])
                        for p in range(len(Positions)):
                            enigma.Rotorboard.Position = Positions[p]

                            enigma.CreateRotors() # Recreate the rotors each time
                            InitialPosition = enigma.Rotorboard.Position # store the position before it changes in the decoding process
                            output = enigma.EncodeMessage(message) # Run the machine

                            IoC = self.IoC(output) # Calculate the IoC to help analyse
                            # Put all results into an organized list
                            Predictions.append([enigma.Rotorboard.RotorValues, enigma.Rotorboard.Reflector, enigma.Rotorboard.Settings, InitialPosition, DisplayLeads, IoC, output])

        # Go through all predictions and store/display possibilities that contain the crib
        Matching = []
        for x in range(len(Predictions)):
            if crib in Predictions[x][6]:
                Matching.append(Predictions[x])
        for x in range(len(Matching)):
            print(Matching[x])

    # Special function for Question 3
    def EliminateOdds(self):
        # Store all values that would be "odd"
        OddValues = []
        for n in range(26):
            string = str(n+1)
            for letter in range(len(string)):
                if int(string[letter]) % 2 != 0 and (string not in OddValues):
                    OddValues.append(int(string))

        # If settings are "odd", we eliminate that settings set
        for S1 in range(26):
            for S2 in range(26):
                for S3 in range(26):
                    if ((S1 + 1) in OddValues) or ((S2 + 1) in OddValues) or ((S3 + 1) in OddValues):
                        if [S1+1,S2+1,S3+1] not in self.BSettings:
                            self.BSettings.append([S1+1,S2+1,S3+1])

        # Same process as before, but hardcoded the three "odd" rotors
        OddRotors = ["I", "III", "V"]
        for R1 in range(7):
            for R2 in range(7):
                for R3 in range(7):
                    if self.RotorValueToRotor(R1) in OddRotors or self.RotorValueToRotor(R2) in OddRotors or self.RotorValueToRotor(R3) in OddRotors:
                        if [self.RotorValueToRotor(R1), self.RotorValueToRotor(R2), self.RotorValueToRotor(R3)] not in self.BRotors:
                            self.BRotors.append([self.RotorValueToRotor(R1), self.RotorValueToRotor(R2), self.RotorValueToRotor(R3)])

    # Function that calculates index of coincidence
    def IoC(self, string):
        string = string.upper()
        index = 0
        for x in range(26):
            character = chr(x+65)
            occurences = 0
            for l in range(len(string)):
                if string[l] == character:
                    occurences += 1
            update = ((occurences * (occurences - 1))/(len(string)*(len(string)-1)))
            index += update
        return index


    # A function that allows us to quickly convert numbers 0-6 into their corresponding rotor names
    def RotorValueToRotor(self,value):
        if value == 0:
            return "I"
        elif value == 1:
            return "II"
        elif value == 2:
            return "III"
        elif value == 3:
            return "IV"
        elif value == 4:
            return "V"
        elif value == 5:
            return "Beta"
        elif value == 6:
            return "Gamma"


def decode1():
    # CODE 1
    code = "DMEXBMKYCVPNQBEDHXVPZGKMTFFBJRPJTLHLCHOTKOYXGGHZ"
    crib = "SECRETS"
    decoder1 = Decoder(3)
    decoder1.addComponent(["Beta", "Gamma", "V"], "Rotors")
    decoder1.addComponent(["KI", "XN", "FL"], "Pairs")
    decoder1.addComponent("MJM", "Positions")
    decoder1.addComponent([4,2,14], "Settings")
    result = decoder1.decode(code, crib)


if __name__ == "__main__":
    Decode1()