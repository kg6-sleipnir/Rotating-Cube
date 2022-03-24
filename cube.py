import math
import numpy
import time

#length of each side
side_length = 10

#size of screen
screen_width = 35
screen_height = 35

#distance from screen to center of cube
zprime = 30


distance = screen_width * zprime  / (8 * side_length)


#array containing every point on the cube
points = []

#add every point of a cube into points array
for x in range(-side_length, side_length+1):
    for y in range(-side_length, side_length+1):
        for z in range(-side_length, side_length+1):
            points.append((x,y,z))

#delete all points inside the cube to get only points on surface of the cube
for x in range(-side_length+1, side_length):
    for y in range(-side_length+1, side_length):
        for z in range(-side_length+1, side_length):
            points.remove((x,y,z))
            
            
#array containing all points in the center of each face to get normal vectors for the faces
centers = [(0,0,side_length), (0,0,-side_length), (0,side_length,0), (0,-side_length,0), (side_length,0,0), (-side_length,0,0)]
            
    
def CalculateNormal(x,y,z,a,b):
    #precompute cosines and sines of the rotation angles
    cosa = math.cos(a)
    cosb = math.cos(b)
    sina = math.sin(a)
    sinb = math.sin(b)
    
    #array holding the center points of each face after rotation
    centers_prime = []
    
    #rotate each center about the x and y axis at the point (0,0,zprime)
    for center in centers:
        #get x,y,z values of each center
        x1 = center[0]
        y1 = center[1]
        z1 = center[2]
        
        #rotate each center around the x and y axis
        xp = x1 * cosb - (y1 * cosa - z1 * sina) * sinb
        yp = cosb * (y1 * cosa - z1 * sina) + x1 * sinb
        
        #make sure we add zprime to get the new center point for the cube during rotation
        zp = zprime + (z1 * cosa + y1 * sina)
        
        #append the new coordinate to the array
        centers_prime.append((xp,yp,zp))
    
    
    
    #variables holding the center that is the closest distance from a point on the face
    #since no point is farther away than sqrt(side_length**2 + side_length**2)
    #we can choose an arbitrarily large number to get points that are closer
    closestDistance = side_length*10
    closestCenter = (0,0,0)
    
    #get the closest center point from the current position
    for center in centers_prime:
        #get the distance from the point to each center
        vector = (x - center[0], y - center[1], z - center[2])
        magnitude = numpy.linalg.norm(vector)
        
        #check if the center is closer than the current closest center
        if magnitude < closestDistance:
            closestCenter = center
            closestDistance = magnitude
       
    #get a new vector from the center of the cube to the closest center
    #after calculating this vector, it will be parallel to the normal vector of the face
    normalVector = closestCenter - numpy.array([0,0,zprime])
            
    #return the normal vector as a unit normal vector
    return normalVector / numpy.linalg.norm(normalVector)
    

#calculate the luminance of a point on the cube
def CalculateLuminance(vector):
    #the luminance is a value between 0 and the magnitude of an arbitrary vector describing the direction of the lighting
    #and is calculated by using the dot product of the vector from the center of the cube to a point on the cube
    #and the arbitrary vector
    return numpy.dot(vector, numpy.array([0, 0, 1]))
    
    
#rotate and print the cube to the console
def MakeCube(a, b):
    #precompute the cosines and sines of the rotation angles
    cosa = math.cos(a)
    cosb = math.cos(b)
    sina = math.sin(a)
    sinb = math.sin(b)
    
    #make a two dimensional buffer containing a character based on lighting values and its distance from the screen
    #later, we will make sure we only use the point closest to the screen using the zbuffer
    output = [[' '] * screen_width for i in range(screen_height)]
    zbuffer = [[0] * screen_width for i in range(screen_height)]
    
    #loop over each point in the points array to rotate it and calculate its position on the screen
    for vertice in points:
        
        #get the x,y,z values in the point
        x = vertice[0]
        y = vertice[1]
        z = vertice[2]
        
        #rotate the point around the x and y axis
        xp = x * cosb - (y * cosa - z * sina) * sinb
        yp = cosb * (y * cosa - z * sina) + x * sinb
        
        #make sure we use the correct center point when rotating by adding zprime (the distance from the screen to the center)
        zp = zprime + (z * cosa + y * sina)

        #calculate the position of the point on the screen
        xpos = int(screen_width / 2 + distance * xp /(zp))
        ypos = int(screen_height / 2 - distance * yp /(zp))
        
        #make sure we choose the point with the z coordinate closest to the screen using the zbuffer
        if zbuffer[xpos][ypos] < 1/(zp):
            zbuffer[xpos][ypos] = 1/(zp)

            #calculate the lighting value for the point
            L = abs(int(CalculateLuminance(CalculateNormal(xp,yp,zp,a,b)) * 11))
            
            #put the character corresponding to a light value in the output buffer
            output[xpos][ypos] = '.,-~:;=!*#$@'[L]


    #print the ouptut buffer to the screen
    for i in output:
        for j in i:
            print j,
        print
 
#initial values for the rotation angles
a1 = 0
b1 = 0

#main loop for rotating and outputing the loop
for i in range(1000):
    a1 += 0.1
    b1 += 0.2
    MakeCube(a1,b1)
    time.sleep(0.1)
