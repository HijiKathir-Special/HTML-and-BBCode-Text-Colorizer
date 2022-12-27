# BBCode-HTML-Text-Colorizer 
### *For when you can't bother to color characters individually*


## Motivation

In HTML (and its easier-to-use forum counterpart, BBCode) text is often colored for emphasis, clarity, and/or aesthetic. Below is an example of coloring a line in both BBCode and HTML, repectively, and how they look when compiled.

```#BBCode
[color=#ff0000]THIS IS THE COLOR RED[/color]
```

```#HTML
<span style="color:#ff0000">THIS IS THE COLOR RED</span>
```

![](https://i.imgur.com/04drGb4.png)

Essentially, we have "opening" and "closing" commands to colorize a group characters. This is possible to do with multiple colors, as shown below.

```#BBCode
[color=#0000ff]THIS IS THE COLOR[/color][color=#ff0000] RED[/color]
```

```#HTML
<span style="color:#0000ff">THIS IS THE COLOR</span><span style="color:#ff0000"> RED</span>
```

![](https://i.imgur.com/KZduWoG.png)

When we want to colorize text in an organized way by letter, this becomes very tedious. For example, alternating red and blue characters will look like this:

```#BBCode
[color=#ff0000]T[/color][color=#0000ff]H[/color][color=#ff0000]I[/color][color=#0000ff]S[/color][color=#ff0000] [/color][color=#0000ff]I[/color][color=#ff0000]S[/color][color=#0000ff] [/color][color=#ff0000]T[/color][color=#0000ff]H[/color][color=#ff0000]E[/color][color=#0000ff] [/color][color=#ff0000]C[/color][color=#0000ff]O[/color][color=#ff0000]L[/color][color=#0000ff]O[/color][color=#ff0000]R[/color][color=#0000ff] [/color][color=#ff0000]R[/color][color=#0000ff]E[/color][color=#ff0000]D[/color]
```

```#HTML
<span style="color:#ff0000">T</span><span style="color:#0000ff">H</span><span style="color:#ff0000">I</span><span style="color:#0000ff">S</span><span style="color:#ff0000"> </span><span style="color:#0000ff">I</span><span style="color:#ff0000">S</span><span style="color:#0000ff"> </span><span style="color:#ff0000">T</span><span style="color:#0000ff">H</span><span style="color:#ff0000">E</span><span style="color:#0000ff"> </span><span style="color:#ff0000">C</span><span style="color:#0000ff">O</span><span style="color:#ff0000">L</span><span style="color:#0000ff">O</span><span style="color:#ff0000">R</span><span style="color:#0000ff"> </span><span style="color:#ff0000">R</span><span style="color:#0000ff">E</span><span style="color:#ff0000">D</span>
```

![](https://i.imgur.com/ZkpcUXM.png)

The goal of this project is to give the user an easy way to colorize text (that would otherwise be difficult and/or tedious) for HTML or BBCode.


## Coloring Methods

**To output usable HTML/BBCode, the program takes various parameters, including:**
- Desired text to be colorized
- Desired code output (HTML or BBCode)
- Type of colorization

**All types of colorization available fall into 2 categories:**
- Alternating: Like shown above, it takes n color inputs and outputs code that compiles to alternating colors.
- Color Shift: Interpolates between colors, giving each letter a slightly different color that results in a "color fluid" string output when compiled.


### How Alternating Operation Works
For the alternating options, we simply assign the inputted colors to each charcater in a rotating fashion until we reach the end of the string. Colors are inputted as hexcode. To learn about hexcode and RGB, [please refer to this link](https://www.pluralsight.com/blog/tutorials/understanding-hexadecimal-colors-simple).

**Here is an example alternating 3 colors (orange, green, yellow) over 10 characters**

The first color is `#ffae00` (orange-ish), the second color is `#00ff00` (green), and the final color is `#ffff00` (yellow). We convert these to RGB:

We now rotate through these colors for 10 characters, yielding this sequence: `#ffae00` `#00ff00` `#ffff00` `#ffae00` `#00ff00` `#ffff00` `#ffae00` `#00ff00` `#ffff00` `#ffae00` `#00ff00`

All we do from here is assign the colors to our text characters in the desired format. Below are examples of how this 10-character rotation looks with BBCode and HTML.

```#BBCode
[color=#ffae00]0[/color][color=#00e300]1[/color][color=#ffff00]2[/color][color=#ffae00]3[/color][color=#00e300]4[/color][color=#ffff00]5[/color][color=#ffae00]6[/color][color=#00e300]7[/color][color=#ffff00]8[/color][color=#ffae00]9[/color]
```

```#HTML
<span style="color:#ffae00">0</span><span style="color:#00e300">1</span><span style="color:#ffff00">2</span><span style="color:#ffae00">3</span><span style="color:#00e300">4</span><span style="color:#ffff00">5</span><span style="color:#ffae00">6</span><span style="color:#00e300">7</span><span style="color:#ffff00">8</span><span style="color:#ffae00">9</span>
```

![](https://i.imgur.com/HYSlhAE.png)

### How Color Shift Operation Works
In the case for color shift operations, we use the interpolation between 2 given colors as a base, and then apply this operation for however many colors the user inputs. Colors are inputted as hexcode, converted to RGB form, interpolated, and then converted back to hexcode before being assigned to their respective characters. To learn about hexcode and RGB, [please refer to this link](https://www.pluralsight.com/blog/tutorials/understanding-hexadecimal-colors-simple).

**Here is an example of interpolation from red to blue over 10 characters:**

The starting color is `#ff0000` (red) and the ending color is `#0000ff` (blue). We convert these to RGB:

`#ff0000` → `rgb(255, 0, 0)`

`#0000ff` → `rgb(0, 0, 255)`

We now interpolate 10 values from `rgb(255, 0, 0)` to `rgb(0, 0, 255)`. This is done individually for each value (r, g, b). Note that we take the floor value to avoid decimals.

The result for the interpolation with 10 values (along with their hexcode counterparts) are shown below:

`rgb(255, 0, 0)` → `#ff0000`

`rgb(226, 0, 28)` → `#e2001c`

`rgb(198, 0, 56)` → `#c60038`

`rgb(170, 0, 85)` → `#aa0055`

`rgb(141, 0, 113)` → `#8d0071`

`rgb(113, 0, 141)` → `#71008d`

`rgb(85, 0, 170)` → `#5500aa`

`rgb(56, 0, 198)` → `#3800c6`

`rgb(28, 0, 226)` → `#1c00e2`

`rgb(0, 0, 255)` → `#ff0000`

All we do from here is assign the colors to our text characters in the desired format. Below are exmaples of how this 10-character interpolation looks with BBCode and HTML.

```#BBCode
[color=#ff0000]0[/color][color=#e2001c]1[/color][color=#c60038]2[/color][color=#aa0055]3[/color][color=#8d0071]4[/color][color=#71008d]5[/color][color=#5500aa]6[/color][color=#3800c6]7[/color][color=#1c00e2]8[/color][color=#0000ff]9[/color]
```

```#HTML
<span style="color:#ff0000">0</span><span style="color:#e2001c">1</span><span style="color:#c60038">2</span><span style="color:#aa0055">3</span><span style="color:#8d0071">4</span><span style="color:#71008d">5</span><span style="color:#5500aa">6</span><span style="color:#3800c6">7</span><span style="color:#1c00e2">8</span><span style="color:#0000ff">9</span>
```

![](https://i.imgur.com/SQeXn5N.png)

By using this two-color operation multiple times for the n user inputs, we can output text that is a gradient. For example, if we want to colorize text across 3 colors (red, blue, green), we can do the two-color operation twice, yielding us code that compiles to the following:

![](https://i.imgur.com/6yQqRzM.png)


## Interaction With Program

All of the inputs are done in the terminal, and tkinter is used to display the results. In the outputted GUI, the desired code is dislpayed, along with a button that displays what the colors of the text looks like. An example of an input is shown below:

*First we input the text we want colorized, and the type of code we want*

![](https://i.imgur.com/DjY8oVd.png)

*Next, we input the kind of colorization we want (I have selected the multiple-color shift option), as well as the colors we want.*

![](https://i.imgur.com/UXk1Gno.png)

*A GUI is outputted, where we see the copy-pastable code in a text box, along with a button*

![](https://i.imgur.com/jSsW98d.png)

*Finally, we click the button, and a preview of what the colored text will look like is displayed.*

![](https://i.imgur.com/1S8dnj1.png)
