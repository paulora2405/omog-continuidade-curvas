# Curves Continuity
Geometric Modelling Project about curves continuity

---

## Dependencies
- `python>=3.10`
- `pygame==2.1.2`

There is a `requeriments.txt` file for easy installation of dependencies, do so by doing:
```sh
$ pip3 install -r requirements.txt
```

If you wish to use a virtual enviroment, do:
```sh
$ python3 -m venv <Nome-do-ambiente>
$ source <Nome-do-ambiente>/bin/activate
$ pip3 install -r requirements
```

## How to Run
Run by doing `python3 main.py`.

Hotkeys:
- `A` = Decrease the order of the B-Spline.
- `D` = Increaase the order of the B-Spline.
- `S` = Clears all Control Points.
- `Left Mouse Button` = Adds a Control Point or Moves Control Point below mouse position.
- `Right Mouse Button` = Removes a Control Point.
- `Escape` = Exits program.

## Functions and Classes
### BSpline Class
### ControlPoint Class