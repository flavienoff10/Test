from Static.Values import StaticValues
class Handler:
    def integer_handler(question,min=0,max=0):
        while True:
            try:
                return int(input(f"{question} "))
            except ValueError:
                print(f"{StaticValues.WARNING} Invalid Input, please enter a valid Integer!")