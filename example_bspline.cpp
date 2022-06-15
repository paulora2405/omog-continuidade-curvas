#include <GL/glew.h>
#include <GLFW/glfw3.h>

#include <iostream>
#include <iterator>
#include <vector>

#define R 0.04
#define W 600
#define H 600

using namespace std;

//////// global variables /////////////////
double screenx, screeny;
double orderK = 2;
double parameterInc = 0.0005;
double cx, cy;
double currentParam = 0.0 - 0.1;
double gx, gy;
double angle = 0.0;
double angleX = 0.0;

vector<double> controlPointsX;
vector<double> controlPointsY;
vector<double> knotSequence;

vector<double> allPointsX;
vector<double> allPointsY;

bool drawCP = true;
bool Drag = false;
bool Draw = false;
bool before = false;
bool drawSurface = false;
bool showGeometry = false;
int clicked = 0;

vector<double>::iterator currenti;
vector<double>::iterator currentj;

///////// functions ////////////////
void getKnotSqeuence();
void drawCurve();
int delta(double);
void E_delta_1(double u);
void drawGeometry(double);
void drawSurfaceOfRevolution();

void render() {
  glEnable(GL_DEPTH_TEST);

  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

  glMatrixMode(GL_MODELVIEW);
  glLoadIdentity();

  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();
  glOrtho(-1.0f, 1.0f, -1.0f, 1.0f, -1.0f, 1.0f);

  vector<double>::iterator i;
  vector<double>::iterator j = controlPointsY.begin();

  glPointSize(8);
  glColor3f(0.5, 0.5, 1.0);

  ///////////////// draw control points ////////////
  if(drawCP == true) {
    glBegin(GL_POINTS);
    for(i = controlPointsX.begin(); i != controlPointsX.end(); ++i) {
      glVertex3f(*i, *j, 0.0f);
      ++j;
    }
    glEnd();
  }

  ////////////////// draw a square around the selected control point to move
  //////////////////
  if(Drag == true) {
    glColor3f(1.0, 1.0, 1.0);
    glBegin(GL_LINE_LOOP);
    glVertex3f(*currenti - R * 1.1, *currentj - R * 1.1, 0.0f);
    glVertex3f(*currenti - R * 1.1, *currentj + R * 1.1, 0.0f);
    glVertex3f(*currenti + R * 1.1, *currentj + R * 1.1, 0.0f);
    glVertex3f(*currenti + R * 1.1, *currentj - R * 1.1, 0.0f);
    glEnd();
  }

  ///////////////// call the function drawCurve() to draw all the points
  /////////////////////
  if(Draw == true) {
    glColor3f(1.0, 1.0, 0.0);
    glPointSize(3);
    drawCurve();
  }

  if(drawSurface == true) {
    glColor3f(1.0, 1.0, 0.0);
    glPointSize(1);
    drawSurfaceOfRevolution();
  }
}

void drawCurve() {
  ///////////// this function calls E_delta_1() to draw point for each parameter
  /// u ////////
  vector<double> param;
  double k = orderK;
  double m = controlPointsX.size() - 1;

  for(double i = 0.0; i <= 1; i = i + parameterInc) {
    glBegin(GL_POINTS);

    E_delta_1(i);

    glVertex3f(cx, cy, 0.0f);  //// drawing a prticular point
    glEnd();
  }

  ////// show geometry for a specific paramter ///////////////
  if(showGeometry == true) {
    drawGeometry(currentParam);  //// draw geometry
    glColor3f(1.0, 0.3, 0.0);
    glPointSize(10);
    glBegin(GL_POINTS);
    glVertex3f(gx, gy, 0.1f);
    glEnd();
  }
}

void drawSurfaceOfRevolution() {
  ///////  this function creates surface of revolution //////

  drawCP = false;
  Draw = false;

  vector<double> param;
  double k = orderK;
  double m = controlPointsX.size() - 1;
  double r;
  double sx, sy, sz, rx, ry, rz;

  glPushMatrix();
  glRotatef(angleX, 1, 0, 0);
  glRotatef(angle, 0, 1, 0);

  ////////// draw each curve /////////////

  for(double x = 0.0; x < 360; x = x + 25) {
    glPushMatrix();
    glRotatef(x, 1, 0, 0);

    for(int j = 0; j < allPointsX.size(); j++) {
      sx = allPointsX.at(j);
      sy = allPointsY.at(j);

      glBegin(GL_POINTS);

      glVertex3f(sx, sy, 0.0);  //// drawing a prticular point

      glEnd();
    }
    glPopMatrix();
  }

  ///////////// draw each circle /////////////////

  for(double x = 0.0; x < 360; x = x + 0.5) {
    glPushMatrix();
    glRotatef(x, 1, 0, 0);
    for(int j = 0; j < allPointsX.size(); j = j + 200) {
      sx = allPointsX.at(j);
      sy = allPointsY.at(j);

      glBegin(GL_POINTS);

      glVertex3f(sx, sy, 0.0);  //// drawing a prticular point

      glEnd();
    }
    glPopMatrix();
  }
  glPopMatrix();
}

int delta(double u) {
  ///// these function determines delta index ////////////////
  int j = 0;
  int m = controlPointsX.size() - 1;
  int k = orderK;
  for(int i = 0; i <= m + k - 1; i++) {
    if(u >= knotSequence.at(i) && u < knotSequence.at(i + 1)) {
      return i;
    }
    j++;
  }

  return -1;
}

void E_delta_1(double u) {
  ///// this function generates a point for parameter u based on the algorithm
  /////////////////
  vector<double> Cx;
  vector<double> Cy;
  double conX[50], conY[50];

  int m = controlPointsX.size() - 1;
  int k = orderK;
  int d;
  double a, b, omega;

  d = delta(u);  /// finding delta index

  for(int i = 0; i <= k - 1; i++) {
    a = controlPointsX.at(d - i);
    b = controlPointsY.at(d - i);
    conX[i] = a;
    conY[i] = b;
  }

  vector<double>::iterator p = Cx.begin();

  for(int r = k; r >= 2; r--) {
    int i = d;
    for(int s = 0; s <= r - 1; s++) {
      omega = (u - knotSequence.at(i)) / (knotSequence.at(i + r - 1) - knotSequence.at(i));

      conX[s] = omega * conX[s] + (1 - omega) * conX[s + 1];
      conY[s] = omega * conY[s] + (1 - omega) * conY[s + 1];
      i = i - 1;
    }
  }

  cx = conX[0];
  cy = conY[0];

  allPointsX.push_back(cx);
  allPointsY.push_back(cy);
}

void drawGeometry(double currentParam) {
  //// this function draws lines to show geometry for a specific paramtere
  //////////////
  double u = currentParam;
  vector<double> Cx;
  vector<double> Cy;
  double conX[50], conY[50];

  int m = controlPointsX.size() - 1;
  int k = orderK;
  int d;
  double a, b, omega;

  d = delta(u);

  for(int i = 0; i <= k - 1; i++) {
    a = controlPointsX.at(d - i);
    b = controlPointsY.at(d - i);
    conX[i] = a;
    conY[i] = b;
  }

  vector<double>::iterator p = Cx.begin();

  for(int r = k; r >= 2; r--) {
    int i = d;
    for(int s = 0; s <= r - 1; s++) {
      omega = (u - knotSequence.at(i)) / (knotSequence.at(i + r - 1) - knotSequence.at(i));

      glLineWidth(3);
      glColor3f(1.0, 0.0, 0.0);

      ////// drawing lines ///////////////
      glBegin(GL_LINES);
      glVertex3f(conX[s + 1], conY[s + 1], 0.0f);
      glVertex3f(conX[s], conY[s], 0.0f);
      glEnd();

      conX[s] = omega * conX[s] + (1 - omega) * conX[s + 1];
      conY[s] = omega * conY[s] + (1 - omega) * conY[s + 1];

      i = i - 1;
    }
  }

  gx = conX[0];  //// draw point at current parameter in geometry //////
  gy = conY[0];
}

void getKnotSqeuence() {
  ////// this function compute knot sequence for given set of control points and
  /// order /////////
  double m = controlPointsX.size() - 1;
  double k = orderK;
  double total = m + k + 1;
  double knotValue = 0;
  double inc = 1 / (m - k + 2);
  knotSequence.clear();

  ////// standard knot sequence criteria ///////////
  for(unsigned i = 0; i < total; i++) {
    if(i < k) {
      knotSequence.push_back(0);
    } else if(i >= k && i < total - k) {
      knotValue = knotValue + inc;
      knotSequence.push_back(knotValue);
    } else if(i >= total - k) {
      knotSequence.push_back(1);
    }
  }
}

////////////////////// key board handling /////////////////////

void keyboard(GLFWwindow *window, int key, int scancode, int action, int mods) {
  ////// to get the list of all current control points //////////////

  if(key == GLFW_KEY_C && action == GLFW_PRESS) {
    // system("CLS");
    cout << "\n\nCurrent Points are: " << endl;
    for(unsigned i = 0; i < controlPointsX.size(); i++) {
      cout << "(" << controlPointsX.at(i) << ", " << controlPointsY.at(i) << ")" << endl;
    }
  }

  ////////////// to clear the window /////////////////

  if(key == GLFW_KEY_S && action == GLFW_PRESS) {
    Draw = false;
    showGeometry = false;
    drawCP = false;
    drawSurface = false;
    controlPointsX.clear();
    controlPointsY.clear();
    allPointsX.clear();
    allPointsX.clear();
    angle = 0.0;
    angleX = 0.0;

    parameterInc = 0.0005;
    currentParam = 0.0 - 0.1;
    orderK = 2;
    // system("CLS");
    cout << "Order: " << orderK << endl;
  }

  ////////////////   Increase the order   //////////////

  if(key == GLFW_KEY_D && action == GLFW_PRESS) {
    if(orderK < controlPointsX.size()) {
      Draw = false;
      orderK = orderK + 1;
      getKnotSqeuence();
      // system("CLS");
      cout << "Order: " << orderK << endl;
      allPointsX.clear();
      allPointsY.clear();
      Draw = true;
    }
  }

  ////////////////   Decrease the order   //////////////

  if(key == GLFW_KEY_A && action == GLFW_PRESS) {
    if(orderK > 2) {
      Draw = false;
      orderK = orderK - 1;
      getKnotSqeuence();
      // system("CLS");
      cout << "Order: " << orderK << endl;
      Draw = true;
    }
  }

  ////////////////   to start showing geometry   //////////////

  if(key == GLFW_KEY_RIGHT && action == GLFW_PRESS && Draw == true) {
    currentParam = currentParam + 0.1;
    if(currentParam <= 1) {
      showGeometry = true;
    } else {
      showGeometry = false;
      currentParam = 0.0 - 0.1;
    }
  }

  /////////////// to increase the increment step of parameter u //////////////

  if(key == GLFW_KEY_UP && action == GLFW_PRESS) {
    if(parameterInc < 0.03) {
      parameterInc = parameterInc + 0.005;
    }
  }

  /////////////// to decrease the increment step of parameter //////////////

  if(key == GLFW_KEY_DOWN && action == GLFW_PRESS) {
    if(parameterInc > 0.001) {
      parameterInc = parameterInc - 0.005;
    }
  }

  if(key == GLFW_KEY_R && action == GLFW_PRESS) {
    glPointSize(1);
    drawSurface = true;
  }

  if(key == GLFW_KEY_E && action == GLFW_PRESS) {
    angle = angle + 5;
    if(angle > 360) {
      angle = angle - 360;
    }
  }
  if(key == GLFW_KEY_Q && action == GLFW_PRESS) {
    angle = angle - 5;
    if(angle < 0) {
      angle = angle + 360;
    }
  }
  if(key == GLFW_KEY_W && action == GLFW_PRESS) {
    angleX = angleX + 5;
    if(angleX > 360) {
      angleX = angleX - 360;
    }
  }
  if(key == GLFW_KEY_Z && action == GLFW_PRESS) {
    angleX = angleX - 5;
    if(angleX < 0) {
      angleX = angleX + 360;
    }
  }
}

//////////////////////////// mouse handling ////////////////////////////////

void mouseButton(GLFWwindow *window, int button, int action, int mods) {
  double getx, gety;

  //////////// adding new points and moving points //////////////////

  if(button == GLFW_MOUSE_BUTTON_LEFT && action == GLFW_PRESS) {
    clicked = clicked + 1;
    getx = (screenx / W) * 2.0 - 1.0;
    gety = 1.0 - (screeny / H) * 2.0;

    drawCP = true;
    // system("CLS");
    cout << "Order: " << orderK << endl;

    if(clicked == 1)  //// whenver first time clicked
    {
      Drag = false;
    } else if(clicked > 1 && Drag == true)  //// user wants to move
    {
      currenti = controlPointsX.erase(currenti);
      currentj = controlPointsY.erase(currentj);

      currenti = controlPointsX.insert(currenti, getx);
      currentj = controlPointsY.insert(currentj, gety);

      Drag = false;
      before = true;  //// a moving occured
      showGeometry = false;
    } else if(clicked > 1 && Drag == false)  // user selected a point to move it
    {
      vector<double>::iterator i;
      vector<double>::iterator j;
      j = controlPointsY.begin();

      for(i = controlPointsX.begin(); i != controlPointsX.end(); i++) {
        if(*i<getx + R && * i> getx - R && *j<gety + R && * j> gety - R) {
          Drag = true;
          showGeometry = false;
          currenti = i;
          currentj = j;
          break;
        } else {
          Drag = false;
        }
        j++;
      }
    }

    if(Drag == false) {
      if(before == false)  /// if no moving occured, create a new control point
      {
        controlPointsX.push_back(getx);
        controlPointsY.push_back(gety);
        if(controlPointsX.size() >= orderK) {
          getKnotSqeuence();
          Draw = true;
        }
      }

      before = false;
    }
  }

  //////////////////// reomving points ///////////////////////

  if(button == GLFW_MOUSE_BUTTON_RIGHT) {
    if(action == GLFW_PRESS && controlPointsX.size() > orderK)  /// limiting the deleting by order
    {
      getx = (screenx / W) * 2.0 - 1.0;
      gety = 1.0 - (screeny / H) * 2.0;
      vector<double>::iterator j = controlPointsY.begin();
      for(vector<double>::iterator i = controlPointsX.begin(); i != controlPointsX.end();) {
        if(*i<getx + R && * i> getx - R && *j<gety + R && * j> gety - R) {
          i = controlPointsX.erase(i);
          j = controlPointsY.erase(j);
          Draw = false;
          getKnotSqeuence();
          Draw = true;
        } else {
          i++;
          j++;
        }
      }
    }
  }
}
void mousePos(GLFWwindow *window, double x, double y) {
  screenx = x;
  screeny = y;
}

int main() {
  if(!glfwInit()) {
    std::cout << "Could not initialize.\n";
    return 1;
  }

  GLFWwindow *window = glfwCreateWindow(W, H, "B-Spline Curves", NULL, NULL);
  if(!window) {
    std::cout << "Could not create window.\n";
    glfwTerminate();
    return 1;
  }

  glfwSetKeyCallback(window, keyboard);
  glfwSetMouseButtonCallback(window, mouseButton);
  glfwSetCursorPosCallback(window, mousePos);

  glfwMakeContextCurrent(window);
  while(!glfwWindowShouldClose(window)) {
    render();
    glfwSwapBuffers(window);
    glfwPollEvents();
  }

  glfwDestroyWindow(window);
  glfwTerminate();

  return 0;
}
