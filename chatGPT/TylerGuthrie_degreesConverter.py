import sys

numArgs = len(sys.argv)

if numArgs < 3:
    print("Too few arguments passed!\nUsage: python3 degreesConverter.py degrees unit(capital)\n")
    sys.exit()

if numArgs > 3:
    print("Too many arguments passed!\nUsage: python3 degreesConverter.py degrees unit(capital)\n")
    sys.exit()

degrees = float(sys.argv[1])
degreesFahrenheit = 0.0
degreesCelcius = 0.0
degreesKelvin = 0.0
isF = False
isC = False
isK = False

if sys.argv[2] == 'F':
    degreesCelcius = (degrees - 32) * (5/9)
    degreesKelvin = (degrees - 32) * (5/9) + 273.15
    isF = True
elif sys.argv[2] == 'C':
    degreesFahrenheit = (degrees * (9/5)) + 32
    degreesKelvin = degrees + 273.15
    isC = True
elif sys.argv[2] == 'K':
    degreesFahrenheit = (degrees - 273.15) * (9/5) + 32
    degreesCelcius = degrees - 273.15
    isK = True
else:
    print("Invalid unit entered!\nValid units include F, C, and K")
    sys.exit()

if isF == True:
    print("Celcius: ")
    print(degreesCelcius)
    print("\nKelvin: ")
    print(degreesKelvin)
    print("\n")
elif isC == True:
    print("Fahrenheit: ")
    print(degreesFahrenheit)
    print("\nKelvin: ")
    print(degreesKelvin)
    print("\n")
elif isK == True:
    print("Fahrenheit: ")
    print(degreesFahrenheit)
    print("\nCelcius: ")
    print(degreesCelcius)
    print("\n")

