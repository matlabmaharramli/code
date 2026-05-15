from nuclei import Nuclei

def main():

    try:
        decay_constant = float(input("Enter the desired nuclei decay constant: "))
    except ValueError:
        print("Error: Valid value not received. The value [0.02775] will be used for the decay constant")
        decay_constant = 0.02775
    
    try:
        array_length = int(input("Enter the desired nuclei grid array length: "))
    except ValueError:
        print("Error: Valid value not received. The value [50] will be used for the array length.")
        array_length = 50

    nuclei = Nuclei(decay_constant, array_length)
    nuclei.simulate_half_life(0.01)
    print(nuclei)
    # help(Nuclei)

if __name__ == "__main__":
    main()