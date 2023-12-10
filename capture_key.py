import msvcrt

running = True

def capture_keys():
    global running
    while running:
        if msvcrt.kbhit():
            char = msvcrt.getch()
            print("Char :", char)
            if char == b'\r':
                print("Exiting Loop")
                running = False
    input("Press Enter to exit...\n")

capture_keys()
