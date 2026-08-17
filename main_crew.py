import sys
from src.crew import PostPublisherCrew


def main():
    if len(sys.argv) > 1:
        tip = " ".join(sys.argv[1:])
    else:
        tip = input("Enter tip: ")

    crew = PostPublisherCrew(tip=tip)
    result = crew.run()
    print(result)


if __name__ == "__main__":
    main()
