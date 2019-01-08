from vision import Vision
from controller import Controller
from ai import AI

def main():
    vision = Vision()
    controller = Controller()
    ai = AI(vision, controller, 0.510066, 0.760666, 0.35663, 0.184483, 0)
    ai.run()

if __name__ == "__main__":
    main()
