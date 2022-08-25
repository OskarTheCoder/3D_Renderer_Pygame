import pygame as pg
import math
import random
pg.init()

SCREEN_W = 920;
SCREEN_H = 760;
ASPECT_RATIO = SCREEN_H / SCREEN_W;
SCREEN = pg.display.set_mode((SCREEN_W, SCREEN_H))
drawPoints = [0,0,0,0,0,0,0,0];
FOV = 60
P_MULTIPLIER = (SCREEN_W / 2.0) / math.tan((FOV / 2.0) * 3.14159265 / 180.0);

def translate(original, translation):
    toReturn = Point3D();
    toReturn.x = original.x + translation.x;
    toReturn.y = original.y + translation.y;
    toReturn.z = original.z + translation.z;
    return toReturn;

def rotate(original, rotation):

    # // Bare søk på wikipedia |:
    toReturn = Point3D();
    toReturn.x = original.x * (math.cos(rotation.z) * math.cos(rotation.y)) + original.y * (math.cos(rotation.z) * math.sin(rotation.y) * math.sin(rotation.x) - math.sin(rotation.z) * math.cos(rotation.x)) + original.z * (math.cos(rotation.z) * math.sin(rotation.y) * math.cos(rotation.x) + math.sin(rotation.z) * math.sin(rotation.x));
    toReturn.y = original.x * (math.sin(rotation.z) * math.cos(rotation.y)) + original.y * (math.sin(rotation.z) * math.sin(rotation.y) * math.sin(rotation.x) + math.cos(rotation.z) * math.cos(rotation.x)) + original.z * (math.sin(rotation.z) * math.sin(rotation.y) * math.cos(rotation.x) - math.cos(rotation.z) * math.sin(rotation.x));
    toReturn.z = original.x * (-math.sin(rotation.y)) + original.y * (math.cos(rotation.y) * math.sin(rotation.x)) + original.z * (math.cos(rotation.y) * math.cos(rotation.x));

    return toReturn;

def addPerspective(original):
    toReturn = Point3D(); 
    toReturn.x = original.x * P_MULTIPLIER / (P_MULTIPLIER + original.z);
    toReturn.y = original.y * P_MULTIPLIER / (P_MULTIPLIER + original.z);
    toReturn.z = original.z;
    return toReturn;


def centerOnScreen(original):
    toReturn = Point3D();
    toReturn.x = original.x + SCREEN_W/2
    toReturn.y = original.y + SCREEN_H/2
    toReturn.z = original.z;
    return toReturn;

class Point3D():
    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x;
        self.y = y;
        self.z = z;

class Triangle():
    def __init__(self, p1 = Point3D(), p2 = Point3D(), p3 = Point3D(), c = ((255,0,255))):
        self.points = [p1, p2, p3];
        self.c = c;
        self.pointsToDraw = [Point3D(), Point3D(), Point3D()];
        self.worldPoints = [Point3D(), Point3D(), Point3D()];
        self.averageZ = 0;
        self.normalZ = 0;

    def calculateWorldPoints(self, position, rotation):
        for i in range(3):
            self.worldPoints[i] = rotate(self.points[i], rotation);

        for i in range(3):
            self.worldPoints[i] = translate(self.worldPoints[i], position);

        # // Brukes for å sortere trianglene
        self.averageZ = (self.worldPoints[0].z + self.worldPoints[1].z + self.worldPoints[2].z) / 3.0;

    def CalculateDrawPoints(self):
        for i in range(3):
            self.pointsToDraw[i] = addPerspective(self.worldPoints[i]);
        
        for i in range(3):
            self.pointsToDraw[i] = centerOnScreen(self.pointsToDraw[i]);

        self.normalZ = (self.pointsToDraw[1].x - self.pointsToDraw[0].x) * (self.pointsToDraw[2].y - self.pointsToDraw[0].y) - (self.pointsToDraw[1].y - self.pointsToDraw[0].y) * (self.pointsToDraw[2].x - self.pointsToDraw[0].x); 

    def draw(self, position=Point3D(), rotation=Point3D()):
        #self.pointsToDraw = [Point3D(), Point3D(), Point3D()];
        
        #for i in range(3):
        #    self.pointsToDraw[i] = rotate(self.points[i], rotation);       

        #for i in range(3):
        #    self.pointsToDraw[i] = translate(self.pointsToDraw[i], position);
            
        #for i in range(3):
        #    self.pointsToDraw[i] = addPerspective(self.pointsToDraw[i]);
        
        #for i in range(3):
        #    self.pointsToDraw[i] = centerOnScreen(self.pointsToDraw[i]);

        pg.draw.polygon(SCREEN, self.c, ((self.pointsToDraw[0].x,self.pointsToDraw[0].y),(self.pointsToDraw[1].x,self.pointsToDraw[1].y),(self.pointsToDraw[2].x,self.pointsToDraw[2].y)));

def SortOrder(triangle1, triangle2):
    return triangle1.averageZ < triangle2.averageZ;

def GetNormalZ():
    pass

class Cube():
    def __init__(self, rot, pos):
        #self.points = [Point3D(), Point3D(), Point3D(), Point3D(), Point3D(), Point3D(), Point3D(), Point3D()];
        self.triangles = [];
        self.rotation = rot;
        self.position = pos;

def BubbleSortAverageZ(triangles):
    for y in range(len(triangles)):
        for x in range(len(triangles)-1):
            if SortOrder(triangles[x],triangles[x+1]):
                save = triangles[x+1]
                triangles[x+1] = triangles[x];
                triangles[x] = save;

    return triangles;



cube = Cube(Point3D(0,0,0), Point3D(0,0,400));
#cube.points[0] = Point3D(-200, -200, -200);
#cube.points[1] = Point3D(-200, 200, -200);
#cube.points[2] = Point3D(200, 200, -200);
#cube.points[3] = Point3D(200, -200, -200);
#cube.points[4] = Point3D(-200, -200, 200);
#cube.points[5] = Point3D(-200, 200, 200);
#cube.points[6] = Point3D(200, 200, 200);
#cube.points[7] = Point3D(200, -200, 200);

point0 = Point3D(-200, -200, -200);
point1 = Point3D(-200, 200, -200);
point2 = Point3D(200, 200, -200);
point3 = Point3D(200, -200, -200);
point4 = Point3D(-200, -200, 200);
point5 = Point3D(-200, 200, 200);
point6 = Point3D(200, 200, 200);
point7 = Point3D(200, -200, 200);



cube.triangles.append(Triangle(point0, point1, point3, ((random.randrange(0,255),random.randrange(0,255),random.randrange(0,255)))));
cube.triangles.append(Triangle(point1, point2, point3, ((random.randrange(0,255),random.randrange(0,255),random.randrange(0,255)))));

cube.triangles.append(Triangle(point7, point5, point4, ((random.randrange(0,255),random.randrange(0,255),random.randrange(0,255)))));
cube.triangles.append(Triangle(point7, point6, point5, ((random.randrange(0,255),random.randrange(0,255),random.randrange(0,255)))));

cube.triangles.append(Triangle(point4, point0, point7, ((random.randrange(0,255),random.randrange(0,255),random.randrange(0,255)))));
cube.triangles.append(Triangle(point0, point3, point7, ((random.randrange(0,255),random.randrange(0,255),random.randrange(0,255)))));

cube.triangles.append(Triangle(point1, point6, point2, ((random.randrange(0,255),random.randrange(0,255),random.randrange(0,255)))));
cube.triangles.append(Triangle(point1, point5, point6, ((random.randrange(0,255),random.randrange(0,255),random.randrange(0,255)))));

cube.triangles.append(Triangle(point4, point1, point0, ((random.randrange(0,255),random.randrange(0,255),random.randrange(0,255)))));
cube.triangles.append(Triangle(point4, point5, point1, ((random.randrange(0,255),random.randrange(0,255),random.randrange(0,255)))));

cube.triangles.append(Triangle(point3, point2, point7, ((random.randrange(0,255),random.randrange(0,255),random.randrange(0,255)))));
cube.triangles.append(Triangle(point7, point2, point6, ((random.randrange(0,255),random.randrange(0,255),random.randrange(0,255)))));
run = True



while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False;



    SCREEN.fill((0,0,0));

    cube.rotation.y += 0.001;

    allTriangles = [];
    for i in range(len(cube.triangles)):
        cube.triangles[i].calculateWorldPoints(cube.position, cube.rotation);
        allTriangles.append(cube.triangles[i]);

    cube.triangles = BubbleSortAverageZ(cube.triangles);

    for i in range(len(allTriangles)):
        allTriangles[i].CalculateDrawPoints();
        if (allTriangles[i].normalZ) < 0:
            allTriangles[i].draw();


    #for i in range(8):
    #    drawPoints[i] = rotate(cube.points[i], cube.rotation)
        

    #for i in range(8):
    #    drawPoints[i] = translate(drawPoints[i], cube.position);
        

    #for i in range(8):
    #    drawPoints[i] = addPerspective(drawPoints[i]);
        

    #for i in range(8):
    #    drawPoints[i] = centerOnScreen(drawPoints[i]);
        #print(drawPoints[i])

    #print(drawPoints)
    #pg.draw.line(SCREEN, ((255,255,255 )), (drawPoints[0].x,drawPoints[0].y), (drawPoints[1].x,drawPoints[1].y));
    #pg.draw.line(SCREEN, ((255,255,255 )), (drawPoints[1].x,drawPoints[1].y), (drawPoints[2].x,drawPoints[2].y));
    #pg.draw.line(SCREEN, ((255,255,255 )), (drawPoints[2].x,drawPoints[2].y), (drawPoints[3].x,drawPoints[3].y));
    #pg.draw.line(SCREEN, ((255,255,255 )), (drawPoints[3].x,drawPoints[3].y), (drawPoints[0].x,drawPoints[0].y));
    
    #pg.draw.line(SCREEN, ((255,255,255 )), (drawPoints[4].x,drawPoints[4].y), (drawPoints[5].x,drawPoints[5].y));
    #pg.draw.line(SCREEN, ((255,255,255 )), (drawPoints[5].x,drawPoints[5].y), (drawPoints[6].x,drawPoints[6].y));
    #pg.draw.line(SCREEN, ((255,255,255 )), (drawPoints[6].x,drawPoints[6].y), (drawPoints[7].x,drawPoints[7].y));
    #pg.draw.line(SCREEN, ((255,255,255 )), (drawPoints[7].x,drawPoints[7].y), (drawPoints[4].x,drawPoints[4].y));

    #pg.draw.line(SCREEN, ((255,255,255 )), (drawPoints[0].x,drawPoints[0].y), (drawPoints[4].x,drawPoints[4].y));
    #pg.draw.line(SCREEN, ((255,255,255 )), (drawPoints[1].x,drawPoints[1].y), (drawPoints[5].x,drawPoints[5].y));
    #pg.draw.line(SCREEN, ((255,255,255 )), (drawPoints[2].x,drawPoints[2].y), (drawPoints[6].x,drawPoints[6].y));
    #pg.draw.line(SCREEN, ((255,255,255 )), (drawPoints[3].x,drawPoints[3].y), (drawPoints[7].x,drawPoints[7].y));

    pg.display.update();