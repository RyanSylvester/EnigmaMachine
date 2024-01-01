import random
import string
from rotors import RotorsDict
from rotors import NotchDict


class PlugLead:
    def __init__(self, mapping):
        self.mapping = mapping

    def __str__(self):
        return self.mapping

    def encode(self, character):
        if character in self.mapping: # If the character has a conversion
            for l in self.mapping: # Go through each character in the string
                if l != character: # When we find the conversion, return it
                    return l
        return character # If no conversion is found, we return the same character


class Plugboard:
    def __init__(self):
        self.Leads = []

    # This is a function that quickly makes 10 random plug leads for our plugboard (only for quick demonstration)
    def GenerateBoard(self, PlugCount = 10):
        PlugCharacters = random.sample(AlphabetSample, k=PlugCount*2)
        CurrentLead = ""
        for x in range(len(PlugCharacters)):
            if (x+1) % 2 != 0:
                CurrentLead += PlugCharacters[x]
            elif (x+1) % 2 == 0:
                CurrentLead += PlugCharacters[x]
                self.add(PlugLead(CurrentLead))
                CurrentLead = ""

    # Adds a lead to the plugboard
    def add(self,NewLead):
        self.Leads.append(NewLead)

    # Encodes a single character across the plugboard
    def encode(self,character):
        for lead in self.Leads:
            if character in lead.mapping:
                return lead.encode(character)
        else:
            return character

class Rotor:
    def __init__(self, label,setting, position, RotorNumber):
        self.Label = label
        self.Mapping = RotorsDict[label]
        self.RotorNumber = RotorNumber
        self.Position = position
        self.Setting = setting
        self.Delta = PositionToDelta(self.RotorNumber, position, setting)

    # For encoding in a direction, we use a delta value to calculate the change in position
    def encode_right_to_left(self, letter, position):
        self.Position = position
        self.Delta = PositionToDelta(self.RotorNumber, self.Position, self.Setting)

        # Get mapping of the position
        OriginalMapping = self.Mapping[chr(NumberMapping(ord(letter)+self.Delta))]
        # Apply the delta back to the offset of the alphabet
        AdjustedMapping = chr(NumberMapping(ord(OriginalMapping) - self.Delta))

        return AdjustedMapping

    def encode_left_to_right(self, letter):
        self.Delta = PositionToDelta(self.RotorNumber, self.Position, self.Setting)

        StartingPosition = chr(NumberMapping(ord(letter)+self.Delta))
        for key, val in self.Mapping.items(): # Get the key from the value
            if StartingPosition == val:
                OriginalMapping = key
        AdjustedMapping = chr(NumberMapping(ord(OriginalMapping) - self.Delta))
        return AdjustedMapping

class Rotorboard:
    def __init__(self, RotorValues, Reflector, Settings, Position):
        self.RotorValues = RotorValues
        self.Reflector = Reflector
        self.Position = Position.upper()
        self.Settings = Settings
        self.Rotors = []

    # Iterate the position of the rotorboard
    def Iterate(self):
        NewPosition = ""
        NumericalPositions = []
        for x in range(len(self.Position)):
            NumericalPositions.append(ord(self.Position[x]))

        ToIterate = [] # This string will store whether or not a rotor will need to rotate

        # If we reach a notch, the next rotor should rotate
        # For now, we store this information in a list
        for x in range(len(NumericalPositions)-1):
            if chr(NumericalPositions[x+1]) == NotchDict[self.RotorValues[x+1]]:
                ToIterate.append(True)
            else:
                ToIterate.append(False)
        ToIterate.append(True)

        for x in range(len(ToIterate)-1): # Double step pass
            if ToIterate[x] == True:
                ToIterate[x+1] = True

        if len(self.Position) == 4: # If it is a 4+ rotor machine, the fourth can't rotate
            ToIterate[0] = False

        for x in range(len(ToIterate)): # Iterate the rotors that should be iterated
            if ToIterate[x] == True:
                NumericalPositions[x] = IterateAlphabet(NumericalPositions[x])

        for x in range(len(self.Position)): # Convert the new position list into a string
            NewPosition = NewPosition + chr(NumericalPositions[x])
        self.Position = NewPosition

    def Reflect(self, letter): # Reflection is simply a corresponding value from the dictionary in rotors.py
        return (RotorsDict[self.Reflector][letter])

class EnigmaMachine:
    def __init__(self, RotorboardClass, PlugboardClass):
        self.Rotorboard = RotorboardClass
        self.Plugboard = PlugboardClass

        self.CreateRotors()

    # Encodes the full message
    def EncodeMessage(self, Message):
        Message = Message.upper() # standardizes message to capitalized form
        OutputMessage = ""
        for x in range(len(Message)):
            if Message[x] >= "A" and Message[x] <= "Z":
                OutputMessage = OutputMessage + self.Encode(Message[x]) # Only encode a letter
        return OutputMessage

    # Does the full encoding process for a single character
    def Encode(self, Letter):
        self.Rotorboard.Iterate() # Iterate position (spin rotors)
        CurrentLetter = Letter # Start with the input letter
        CurrentLetter = self.Plugboard.encode(CurrentLetter) # Send current letter through the plugboard

        for x in range(len(self.Rotorboard.Position)-1, -1, -1): # For all rotors (right to left)
            CurrentLetter = self.Rotorboard.Rotors[x].encode_right_to_left(CurrentLetter, self.Rotorboard.Position) # encode leftwards

        CurrentLetter = self.Rotorboard.Reflect(CurrentLetter) # Send it into reflection

        for x in range(len(self.Rotorboard.Position)): # Send rightwards through all rotors
            CurrentLetter = self.Rotorboard.Rotors[x].encode_left_to_right(CurrentLetter)

        CurrentLetter = self.Plugboard.encode(CurrentLetter) # Final plugboard pass before output
        return CurrentLetter

    # Create the rotors inside of the machine
    def CreateRotors(self):
        self.Rotorboard.Rotors = []
        for x in range(len(self.Rotorboard.Position)):
            self.Rotorboard.Rotors.append(Rotor(self.Rotorboard.RotorValues[x], self.Rotorboard.Settings[x], self.Rotorboard.Position, x))

# Takes the current setup and returns the total offset
def PositionToDelta(RotorNumber, Position, Setting):
    return ord(Position[RotorNumber]) - (Setting-1) - (ord("A"))

# Iterates our alphabet by one, returns A if letter is Z and needs to increment
def IterateAlphabet(NumericalNumber):
    if NumericalNumber == 90:
        return 65
    else:
        return NumericalNumber + 1

# Takes a number and adjusts it if it went out of the 65-90 ascii bounds
def NumberMapping(Number):
    AlphabetSample = list(string.ascii_uppercase)
    if Number > 90:
        return Number - len(AlphabetSample)
    elif Number < 65:
        return Number + len(AlphabetSample)
    else:
        return Number


if __name__ == "__main__":
    plugboard = Plugboard()
    board = Rotorboard(["II", "I", "V", "IV", "Beta", "III","Gamma"], "A",[10,5,23,11,6,3,3], "BIGDOGS")
    plugboard.add(PlugLead("NI"))
    plugboard.add(PlugLead("AB"))

    enigma = EnigmaMachine(board, plugboard)

    translation = enigma.EncodeMessage("SECRETMESSAGE")
    print(translation)
