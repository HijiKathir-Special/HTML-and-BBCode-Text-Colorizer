#this code takes inputs from the user to colorize text, and outputs a GUI with the html/bbcode, as well as a preview as to what the colors will look like.

import time
import tkinter as tk

print(
  '''Welcome! This is a text colorizer for BBCode and HTML. Enter your text, code preference, and desired color scheme, and this will output BBCode/HTML for you to copy/paste that compiles to your desired aesthetic.
''')

#This is a color dictionary for entry shortcuts for users
colordict = {
  'blue':
  '#0000ff',
  'orange':
  '#ffae00',
  'yellow':
  '#ffff00',
  'gray':
  '#808080',
  'grey':
  '#808080',
  'white':
  '#ffffff',
  'black':
  '#000000',
  'green':
  '#00e300',
  'red':
  '#ff0000',
  'purple':
  '#8a00bd',
  'pink':
  '#ff52cb',
  'rainbow': 
  ['#9400d3', '#4b0082', '#0000ff', '#00ff00', '#ffff00', '#ff7f00', '#ff0000']
}


def errmsg():  #This is the message that will occur when something that isn't a valid color is entered
  print(
    '''you probabaly entered a color that hasn't been added yet, or your hex color code is invalid. don't forget to put a hashtag at the beginning of the 6 characters. Start from the beginning, loser!
  quitting...
  ''')
  time.sleep(6)
  quit()


class Text_Edit:  #This class contains the functions for going between hex code and RBG, as well as parsing the input text

  def __init__(self, text, n):  #creates a list with empty lists (one for each letter) to be filled by color codes
    self.text = text
    self.l = len(text)
    self.rgblist = []
    for i in range(self.l):
      self.rgblist += [[]]
    self.n = n

  def hex2dec(self,color):  #changes hex color format into (r,g,b) so we can interpolate
    R = int(color[1:3], 16)
    G = int(color[3:5], 16)
    B = int(color[5:], 16)
    return [R, G, B]

  def dec2hex(self, rgb):  #changes rgb values back into hex color format
    R = hex(rgb[0])[2:]
    if rgb[0] < 16: R = "0" + R
    G = hex(rgb[1])[2:]
    if rgb[1] < 16: G = "0" + G
    B = hex(rgb[2])[2:]
    if rgb[2] < 16: B = "0" + B
    return "#" + R + G + B


class Alternating_Color(Text_Edit):  #This outputs html and bbcode by assigning alternating specified colors to each character

  def evaluateN(self, colorset): #assigns letter to colors in bbcode string
    n = self.n
    bbcode = ''
    for i in range(len(self.text)):
      bbcode += "[color=" + colorset[i % n] + "]" + self.text[i] + "[/color]"
    return bbcode

  def evaluateNhtml(self, colorset): #assigns letter to colors in html string
    n = self.n
    html = ''
    for i in range(len(self.text)):
      html += "<span style=\"color:" + colorset[i % n] + "\">" + self.text[i] + "</span>"
    return html

  def hex_code_return(self, colorset):
    n = self.n
    allhex = []
    for i in range(len(self.text)):
      allhex += [colorset[i % n]]
    return allhex


class Two_Color_Shift(Text_Edit):  #this is used only as an operator for the N_Color class, and contains the code to interpolate from one color to the next over a certain range

  def evaluate2(self, color1, color2):
    start = self.hex2dec(color1)
    end = self.hex2dec(color2)
    l = self.l

    for i in range(3):  #one for each color (r,g,b)
      for j in range(l):  #appends interpolated values to each empty set for a given color
        n = start[i] + j * (end[i] - start[i]) / (l - 1)
        self.rgblist[j].append(int(n))

    #turns rgb into hex for each letter
    for i in range(l):
      self.rgblist[i] = self.dec2hex(self.rgblist[i])

    #takes each letter's list within the list, and outputs usable bbcode
    bbcode = ""
    for i in range(l):
      bbcode += "[color=" + self.rgblist[i] + "]" + self.text[i] + "[/color]"
    return bbcode

  def evaluate2html(self, color1, color2):
    start = self.hex2dec(color1)
    end = self.hex2dec(color2)
    l = self.l

    for i in range(3):  #one for each color (r,g,b)
      for j in range(l):  #appends interpolated values to each empty set for a given color
        n = start[i] + j * (end[i] - start[i]) / (l - 1)
        self.rgblist[j].append(int(n))

    #turns rgb into hex for each letter
    for i in range(l):
      self.rgblist[i] = self.dec2hex(self.rgblist[i])

    #takes each letter's list within the list, and outputs usable html
    html = ""
    for i in range(l):
      html += "<span style=\"color:" + self.rgblist[i] + "\">" + self.text[i] + "</span>"
    return html

  def hex_color_return(self, color1, color2):
    #returns hex color list (segment) for use instead of a string
    start = self.hex2dec(color1)
    end = self.hex2dec(color2)
    l = self.l

    for i in range(3):  #one for each color (r,g,b)
      for j in range(l):  #appends interpolated values to each empty set for a given color
        n = start[i] + j * (end[i] - start[i]) / (l - 1)
        self.rgblist[j].append(int(n))

    #turns rgb into hex for each letter
    for i in range(l):
      self.rgblist[i] = self.dec2hex(self.rgblist[i])

    return self.rgblist


class N_Color_Shift(Two_Color_Shift): #by putting together various 2 color shifts, we get a gradient over many colors

  def evaluateN(self, colorset): #outputs bbcode by putting together the two-part-pieces
    n = self.n
    allparts = Two_Color_Shift(self.text[:self.l // (n - 1) + 1], n).evaluate2(colorset[0], colorset[1])

    for i in range(1, n - 1):
      nth_text_piece = Two_Color_Shift(self.text[self.l * i // (n - 1):self.l * (i + 1) // (n - 1) + 1], n)
      nth_part = nth_text_piece.evaluate2(colorset[i], colorset[i + 1])[24:]
      allparts += nth_part

    return allparts

  def evaluateNhtml(self, colorset): #outputs html by putting together the two-part-pieces
    n = self.n
    allparts = Two_Color_Shift(self.text[:self.l // (n - 1) + 1], n).evaluate2html(colorset[0], colorset[1])

    for i in range(1, n - 1):
      nth_text_piece = Two_Color_Shift(self.text[self.l * i // (n - 1):self.l * (i + 1) // (n - 1) + 1], n)
      nth_part = nth_text_piece.evaluate2html(colorset[i], colorset[i + 1])[36:]
      allparts += nth_part

    return allparts

  def hex_code_return(self, colorset):
    n = self.n
    allhex = Two_Color_Shift(self.text[:self.l // (n - 1) + 1], n).hex_color_return(colorset[0], colorset[1])

    for i in range(1, n - 1):
      nth_text_piece = Two_Color_Shift(self.text[self.l * i // (n - 1):self.l * (i + 1) // (n - 1) + 1], n)
      nth_part = nth_text_piece.hex_color_return(colorset[i], colorset[i + 1])[:-1]
      allhex += nth_part

    return allhex


def Alternating_Prompt(text, n):  #takes input and gives output for alternating operation
  #each input being changed to hex color code format
  colorset = []
  for i in range(n):
    colorset += [None]
  for i in range(n):
    colorset[i] = input(
      'ENTER COLOR ' + str(i + 1) +
      ''' (entering the hexcode as '#0a1b2c' or a color in lower case like "orange" should work):
    ''')
    if colorset[i] in colordict:  #shortcutting for colors
      colorset[i] = colordict[colorset[i]]
    elif not (len(colorset[i]) == 7 and colorset[i][0] == "#"):
      errmsg()

  #code result
  bbcode = Alternating_Color(text, n).evaluateN(colorset)
  html = Alternating_Color(text, n).evaluateNhtml(colorset)
  #for list of colors
  colorlist = Alternating_Color(text, n).hex_code_return(colorset)

  return [bbcode, html, colorlist]


def Alternating_Rainbow_Prompt(text, n):  #takes input and gives output for alternating rainbow operation
  #each input being changed to hex color code format
  colorset = colordict['rainbow']

  #code result
  bbcode = Alternating_Color(text, n).evaluateN(colorset)
  html = Alternating_Color(text, n).evaluateNhtml(colorset)
  #for list of colors
  colorlist = Alternating_Color(text, n).hex_code_return(colorset)

  return [bbcode, html, colorlist]


def N_Color_Shift_Prompt(text, n): #takes input and gives output for n_color_shift operation
  #each input being changed to hex color code format
  colorset = []
  for i in range(n):
    colorset += [None]
  for i in range(n):
    colorset[i] = input(
      'ENTER COLOR ' + str(i + 1) +
      ''' (entering the hexcode as '#0a1b2c' or a color in lower case like "orange" should work):
    ''')
    if colorset[i] in colordict:  #shortcutting for colors
      colorset[i] = colordict[colorset[i]]
    elif not (len(colorset[i]) == 7 and colorset[i][0] == "#"):
      errmsg()

  #code result
  bbcode = N_Color_Shift(text, n).evaluateN(colorset)
  html = N_Color_Shift(text, n).evaluateNhtml(colorset)
  #for list of colors
  colorlist = N_Color_Shift(text, n).hex_code_return(colorset)

  return [bbcode, html, colorlist]


def Rainbow_Shift_Prompt(text, n): #takes input and gives output for rainbow_color_shift operation
  #7 colors of the rainbow
  colorset = colordict['rainbow']
  #code result
  bbcode = N_Color_Shift(text, n).evaluateN(colorset)
  html = N_Color_Shift(text, n).evaluateNhtml(colorset)

  colorlist = N_Color_Shift(text, n).hex_code_return(colorset)

  return [bbcode, html, colorlist]


def main():
  #entering text, code preference, and operation
  text = input('''ENTER TEXT TO BE EDITED:
  ''')
  code = input('''Would you like bbcode or html? (type 'bbcode' or 'html')
  ''')
  while code not in ['html', 'bbcode']:
    code = input(
      '''That's not one of the options! Please type 'html' or 'bbcode'.
    ''')
  option = input('''Enter the number for which type of stylization you'd like:
  1. Alternating: colorizes characters individually in an alternating fashion with 2 or more characters
  2. Rainbow: outputs alternating color text, but with the colors of the rainbow
  3. Color Shift: colorizes text fluidly, phasing through specified colors
  4. Rainbow Color Shift: outputs color shift, but for the colors of the rainbow
  ''')
  while option not in ["1", "2", "3", "4"]:
    option = input(
      '''That's not one of the options! Please type the number corresponding to the type of stylization you want.
    ''')

  #defining what each option will do
  if option == '1':
    n = input('''how many colors would you like to phase through in your text?
      ''')
    while type(n) == str:
      try:
        n = int(n)
      except:
        n = input('''please enter an integer!
      ''')
    output = Alternating_Prompt(text, n)
    bbcode = output[0]
    html = output[1]
    colorlist = output[2]

  elif option == '2':
    n = 7
    output = Alternating_Rainbow_Prompt(text, n)
    bbcode = output[0]
    html = output[1]
    colorlist = output[2]

  elif option == '3':
    n = input('''how many colors would you like to phase through in your text?
      ''')
    while type(n) == str:
      try:
        n = int(n)
      except:
        n = input('''please enter an integer!
      ''')

    if len(text) < n or n == 1:
      output = Alternating_Prompt(text, n)
      bbcode = output[0]
      html = output[1]
      colorlist = output[2]
    else:
      output = N_Color_Shift_Prompt(text, n)
      bbcode = output[0]
      html = output[1]
      colorlist = output[2]

  elif option == '4':
    n = 7
    if len(text) < n:
      output = Alternating_Rainbow_Prompt(text, n)
      bbcode = output[0]
      html = output[1]
      colorlist = output[2]
    else:
      output = Rainbow_Shift_Prompt(text, n)
      bbcode = output[0]
      html = output[1]
      colorlist = output[2]

  return [bbcode, html, colorlist, text, code]


#outputs for main() to be used in GUI display
output = main()
bbcode = output[0]
html = output[1]
colorlist = output[2]
inputtext = output[3]
code = output[4]

print("opening your code in a new window...")
time.sleep(2)

#GUI display of results
window = tk.Tk()
window.title(code + " code display")
window.configure(bg="white")
window_width = 550
window_height = 450
window.geometry(str(window_width) + "x" + str(window_height))

#message at the top
msg = tk.Label(text=("your " + code +
                     " blurb is below! feel free to copy+paste"),
               bg="white")
msg.place(x=10, y=10)

#box with code in it for copypaste
codebox = tk.Text(width=45, height=10)
codebox.place(x=10, y=35)
if code == "html": outcode = html
elif code == "bbcode": outcode = bbcode


#putting code in the textbox and coloring+placing characters
def show_results(): 
  codebox.delete(1.0,tk.END)
  codebox.insert(1.0, outcode)
  
  jx = 0
  w = int(window_width / 11)
  jy = 0
  for i in range(len(inputtext)):
    output = tk.Label(text=inputtext[i], bg="white", fg=colorlist[i])
    output.configure(font=("Courier", 10))
    output.place(x=20 + (jx * 10) % (10 * w), y=250 + int(jy) * 25)
    jx += 1
    jy += 1 / w


#boldens text objects and adds bold command to start and end of code
def bold():
  jx = 0
  w = int(window_width / 11)
  jy = 0
  for i in range(len(inputtext)):
    output = tk.Label(text=inputtext[i], bg="white", fg=colorlist[i])
    output.configure(font=("Courier", 10, "bold"))
    output.place(x=20 + (jx * 10) % (10 * w), y=250 + int(jy) * 25)
    jx += 1
    jy += 1 / w
  
  if code == "bbcode": 
    codebox.delete(1.0,tk.END)
    codebox.insert(1.0, "[b]"+outcode+"[/b]")
  elif code == "html": 
    codebox.delete(1.0,tk.END)
    codebox.insert(1.0, "<b>"+outcode+"</b>")

def italicize():
  jx = 0
  w = int(window_width / 11)
  jy = 0
  for i in range(len(inputtext)):
    output = tk.Label(text=inputtext[i], bg="white", fg=colorlist[i])
    output.configure(font=("Courier", 10, "italic"))
    output.place(x=20 + (jx * 10) % (10 * w), y=250 + int(jy) * 25)
    jx += 1
    jy += 1 / w
  
  if code == "bbcode": 
    codebox.delete(1.0,tk.END)
    codebox.insert(1.0, "[i]"+outcode+"[/i]")
  elif code == "html": 
    codebox.delete(1.0,tk.END)
    codebox.insert(1.0, "<i>"+outcode+"</i>")


#button that prompts the compiling
button = tk.Button(text="generate and compile " + code + " blurb", command=show_results)
button.place(x=10, y=210)

#button that adds bold option
button = tk.Button(text="italicize text", command=italicize)
button.place(x=220, y=210)

#button that adds italics option
button = tk.Button(text="bold text", command=bold)
button.place(x=320, y=210)

tk.mainloop()
