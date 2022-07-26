# Curves Continuity
Geometric Modelling Project about curves continuity

---

## Dependencies
- `python==3.10`
- `pygame==2.1.2`

There is a `requeriments.txt` file for easy installation of dependencies, do so by doing:
```sh
$ pip3 install -r requirements.txt
```

If you wish to use a virtual enviroment, do:
```sh
$ python3 -m venv <venv-name>
$ source <venv-name>/bin/activate
$ pip3 install -r requirements
```

## How to Run
Run by doing `$ python3 main.py`.
The default window resolution is `1280x720`, if you wish to change it, run with the following arguments `$ python3 main.py WIDTH HEIGHT`

Hotkeys:
- `A` = Decrease the degree of the Selected Curve.
- `D` = Increase the degree of the Selected Curve.
- `S` = Clears all Control Points.
- `Space` = Switches between the two curves.
- `Left Mouse Button` = Adds a Control Point to the Selected Curve or Moves the Control Point below mouse position.
- `Right Mouse Button` = Removes the Control Point below the mouse position.
- `Escape` = Exits program.
- `C` = Increase Continuity
- `0` = Continuity C0
- `1` = Continuity G1
- `2` = Continuity G2

## Functions and Classes
### ControlPoint Class
- Has `x` and `y` coordinate attribute and a `id` number.
- Has a collision with mouse detection and drawing function.

### BSpline Class
- Has a degree and order which can increased or decreased.
- Has a vector of Control Points, and a vector of the Knots.
- It can cache an already calculated curve and draw it faster if no changes are made to the state of the B-Spline.
- When the state does change, via moving, adding or removing Control Points, it calculates the knots and finds evenly spaced points in the curve, which are spaced according to the `BSpline.param` class attribute.
