######################################################################
# Author: Rafael Hermoza
# Username: hermozafreitasr
#
# Assignment: HW09: UPC Barcodes with classes
#
# Purpose: Verify a barcode and draw it, if valid
#
######################################################################
# Acknowledgements:
#
# None: Original work

# licensed under a Creative Commons
# Attribution-Noncommercial-Share Alike 3.0 United States License.
####################################################################################
import turtle


def create_turtle():
    """
    Creates a turtle object and returns it
    :param: none
    :return: a turtle object
    """
    t = turtle.Turtle()
    t.shape("turtle")
    t.speed(0)
    t.pensize(6)
    t.color("red")
    t.shapesize(1)
    t.pencolor("black")
    t.penup()
    return t
def white_line(t, length):
    """
    Draws a white line for the bar code

    :param t: a turtle object
    :param length: how long will the line be
    :return: none
    """
    t.pendown()
    t.color("white")
    t.forward(length)
    t.penup()
    t.goto(t.xcor() + 6, 125)
def black_line(t, length):
    """
    Draw a black line for the bar code
    :param t: a turtle object
    :param length: how long will the line be
    :return: none
    """
    t.pendown()
    t.color("black")
    t.forward(length)
    t.penup()
    t.goto(t.xcor()+6, 125)
def beg_end(t, length):
    black_line(t, 200)
    white_line(t, 200)
    black_line(t, 200)
def mid(t, length):
    white_line(t, 200)
    black_line(t, 200)
    white_line(t, 200)
    black_line(t, 200)
    white_line(t, 200)
def draw_code(upc, t):
    """
    Function to draw the barcode
    :param upc: the object with the barcode
    :param t: a turtle object
    :return: none
    """
    t.goto(-275, 125)
    t.right(90)
    #draw the default first lines
    beg_end(t,200)
    pos = 1
    for i in upc.code:
        lines = upc.translate(i, pos)
        for j in lines:
            if int(j)==0:
                white_line(t,150)
            else:
                black_line(t,150)
        if pos==6:
            mid(t, 200)
        pos+=1
    beg_end(t, 200)


class UPC:
    def __init__(self, c):
        self.code = c
        self.t = create_turtle()
        pass


    def is_valid_input(self):
        """
        Boolean function to check if barcode is valid
        :return: true if it has 12 digits
        """
        # we have to check that despite being a string it only contains numbers
        for i in self.code:
            if not i.isdigit():
                return False
        if len(self.code) == 12:
            return True
        else:
            return False

    def is_valid_modulo(self):
        """
        Boolean function to check the last digit of the bar code, indicating true if the math operations
        match the number given
        :return: True if the math operations match the number given
        """
        odds = 0
        evens = 0
        for i in self.code:
            if int(i) % 2 != 0:
                odds += int(i)
            else:
                evens += int(i)

        n = (3 * odds + evens) % 10
        # print(n)
        if (10 - n) == int(self.code[-1]):
            return True
        elif n == self.code[-1]:
            return True
        else:
            return False

    def translate(self, barcode_num, pos):
        """
            Analyzes the collection of binary values that every digit has, then returns a string with the 7 binary digits
            :param barcode_num: receives a single digit of the overall bar code at a time
            :param pos: the position of that digit in the overall bar code
            :return: a string with the 7 binary digits
            """
        left_encoding = {
            "0": "0001101",
            "1": "0011001",
            "2": "0010011",
            "3": "0111101",
            "4": "0100011",
            "5": "0110001",
            "6": "0101111",
            "7": "0111011",
            "8": "0110111",
            "9": "0001011"
        }

        right_encoding = {
            "0": "1110010",
            "1": "1100110",
            "2": "1101100",
            "3": "1000010",
            "4": "1011100",
            "5": "1001110",
            "6": "1010000",
            "7": "1000100",
            "8": "1001000",
            "9": "1110100"
        }
        if pos <= 6:
            return left_encoding[barcode_num]
        else:
            return right_encoding[barcode_num]


def main():
    wn = turtle.Screen()
    wn.screensize(800, 500)
    rafael = create_turtle()
    input_code = input("Enter a 12 digit code [0-9]: ")
    upc = UPC(input_code)

    while not upc.is_valid_input():
        input_code = input("Enter a 12 digit code [0-9]: ")

    if upc.is_valid_modulo():
        draw_code(upc, rafael)
        rafael.hideturtle()
    else:
        rafael.goto(-200, 0)
        rafael.write("Error, the information doesn't match", font=("Arial", 20, "normal"))
        rafael.hideturtle()
    wn.exitonclick()

if __name__ == "__main__":
    main()
