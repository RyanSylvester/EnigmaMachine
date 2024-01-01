import string

# Create list of the alphabet
Alphabet = string.ascii_uppercase

# Create an ordered list of every corresponding rotor value
BetaSource = ["L","E","Y","J","V","C","N","I","X","W","P","B","Q","M","D","R","T","A","K","Z","G","F","U","H","O","S"]
GammaSource = ["F","S","O","K","A","N","U","E","R","H","M","B","T","I","Y","C","W","L","Q","P","Z","X","V","G","J","D"]
ISource = ["E","K","M","F","L","G","D","Q","V","Z","N","T","O","W","Y","H","X","U","S","P","A","I","B","R","C","J"]
IISource = ["A","J","D","K","S","I","R","U","X","B","L","H","W","T","M","C","Q","G","Z","N","P","Y","F","V","O","E"]
IIISource = ["B","D","F","H","J","L","C","P","R","T","X","V","Z","N","Y","E","I","W","G","A","K","M","U","S","Q","O"]
IVSource = ["E","S","O","V","P","Z","J","A","Y","Q","U","I","R","H","X","L","N","F","T","G","K","D","C","M","W","B"]
VSource =	["V","Z","B","R","G","I","T","Y","U","P","S","D","N","H","L","X","A","W","M","J","Q","O","F","E","C","K"]

# Create an ordered list of reflections
ASource = ["E","J","M","Z","A","L","Y","X","V","B","W","F","C","R","Q","U","O","N","T","S","P","I","K","H","G","D"]
BSource =	["Y","R","U","H","Q","S","L","D","P","X","N","G","O","K","M","I","E","B","F","Z","C","W","V","J","A","T"]
CSource =	["F","V","P","J","I","A","O","Y","E","D","R","Z","X","W","G","C","T","K","U","Q","S","B","N","M","H","L"]

# Create a dictionary for each element
Beta = {}
Gamma = {}
I = {}
II = {}
III = {}
IV = {}
V = {}
A = {}
B = {}
C = {}

# Create values for each letter key
for i in range(26):
    Beta[Alphabet[i]] = BetaSource[i]
    Gamma[Alphabet[i]] = GammaSource[i]
    I[Alphabet[i]] = ISource[i]
    II[Alphabet[i]] = IISource[i]
    III[Alphabet[i]] = IIISource[i]
    IV[Alphabet[i]] = IVSource[i]
    V[Alphabet[i]] = VSource[i]
    A[Alphabet[i]] = ASource[i]
    B[Alphabet[i]] = BSource[i]
    C[Alphabet[i]] = CSource[i]

# Store it all in one dictionary
RotorsDict = {}
RotorsDict["Beta"] = Beta
RotorsDict["Gamma"] = Gamma
RotorsDict["I"] = I
RotorsDict["II"] = II
RotorsDict["III"] = III
RotorsDict["IV"] = IV
RotorsDict["V"] = V
RotorsDict["A"] = A
RotorsDict["B"] = B
RotorsDict["C"] = C

# Create a dictionary for the notch values
NotchDict = {}
NotchDict["Beta"] = ""
NotchDict["Gamma"] = ""
NotchDict["I"] = "Q"
NotchDict["II"] = "E"
NotchDict["III"] = "V"
NotchDict["IV"] = "J"
NotchDict["V"] = "Z"
