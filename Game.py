from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


W,H=500,500


start=0
duration=20000


end_flag=False
start_flag=False
pause=False


user_x=0
user_y=-210
move=0
fall=False
temp=user_y


p1_x=250
p1_y=-150


p2_x=0
p2_y=-100
p2_move=False


p3_x=-250
p3_y=20


p4_y=100


p1_flag=False
p2_flag=False
p3_flag=False
p4_flag=False


Fire_x=250
Fire_y=-125


portal_x=30
portal_move=1


time_1=False
time_2=False






def convert_coordinate(x,y):
    global W, H
    a = x - (W/2)
    b = (H/2) - y
    return a,b


def Points(x, y, r, g, b):
    glPointSize(3)
    glBegin(GL_POINTS)
    glColor3f(r,g,b)
    glVertex2f(int(x), int(y))
    glEnd()


def jump(flag):
    global fall


    if fall==True:
        fall=None


def specialKeyListener(key, x, y):
    global user_x, user_y, move, fall, temp, start_flag, pause
   
    if end_flag!=True:
        if pause==False:
            if key==GLUT_KEY_RIGHT:
                if user_x+7+move<250:
                    move+=7
                    start_flag=True


            if key==GLUT_KEY_LEFT:
                if user_x-7+move>-250:
                    move-=7
                    start_flag=True


            if fall==False:
                if key==GLUT_KEY_UP:
                    fall=True
                    temp=user_y
                    start_flag=True
                    glutTimerFunc(1200, jump, True)
           
            if fall==True:
                if key==GLUT_KEY_DOWN:
                    jump(True)


    glutPostRedisplay()


def mouseListener(button, state, x, y):
    global user_x, user_y, move, fall, p2_x, p2_move, start_flag, end_flag, p1_flag, p2_flag, p3_flag, p4_flag, start, pause, Fire_x, time_1, time_2
    if button==GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            a,b=convert_coordinate(x,y)
            if a<-200 and b>190:
                Fire_x=250
                pause=False
                start=0
                user_x=0
                user_y=-210
                move=0
                p2_x=0
                p2_move=False
                fall=False
                start_flag=False
                end_flag=False
                p1_flag=False
                p2_flag=False
                p3_flag=False
                p4_flag=False
                time_1=False
                time_2=False


            if a>200 and b>200:
                glutLeaveMainLoop()


def keyboardListener(key, x, y):
    global pause, end_flag
    if end_flag!=True:
        if key==b' ':
            if pause==False:
                pause=True
            else:
                pause=False


def FindZone(x1, y1, x2, y2):
        dx=x2-x1
        dy=y2-y1


        if dx == 0:
            Zone=1
            return y1, x1, y2, x2, Zone


        elif dy == 0:
            Zone=0
            return x1, y1, x2, y2, Zone


        elif abs(dx)>=abs(dy):
            if dx>0 and dy>0:
                Zone=0
            if dx<0 and dy>0:
                Zone=3
            if dx<0 and dy<0:
                Zone=4
            if dx>0 and dy<0:
                Zone=7
           
        else:
            if dx>0 and dy>0:
                Zone=1
            if dx<0 and dy>0:
                Zone=2
            if dx<0 and dy<0:
                Zone=5
            if dx>0 and dy<0:
                Zone=6


        new_x1=new_y1=new_x2=new_y2=False


        if Zone==0:
            new_x1,new_y1,new_x2,new_y2=x1,y1,x2,y2


        if Zone==1:
            new_x1,new_y1,new_x2,new_y2=y1,x1,y2,x2


        if Zone==2:
            new_x1,new_y1,new_x2,new_y2=y1,-x1,y2,-x2


        if Zone==3:
            new_x1,new_y1,new_x2,new_y2=-x1,y1,-x2,y2


        if Zone==4:
            new_x1,new_y1,new_x2,new_y2=-x1,-y1,-x2,-y2


        if Zone==5:
            new_x1,new_y1,new_x2,new_y2=-y1,-x1,-y2,-x2


        if Zone==6:
            new_x1,new_y1,new_x2,new_y2=-y1,x1,-y2,x2


        if Zone==7:
            new_x1,new_y1,new_x2,new_y2=x1,-y1,x2,-y2


        return new_x1,new_y1,new_x2,new_y2,Zone


def display():
    global user_x, user_y, p1_x, p1_y, p2_x, p2_y, p3_x, p3_y, p4_y, Fire_x, Fire_y, portal_x


    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0.5,0.7,1,0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0,0,200,  0,0,0,  0,1,0)
    glMatrixMode(GL_MODELVIEW)


    def ZoneRevert(x,y,Zone):
        temp_x,temp_y=False, False
        if Zone==0:
            temp_x,temp_y=x,y


        elif Zone==1:
            temp_x,temp_y=y,x


        elif Zone==2:
            temp_x,temp_y=-y,x


        elif Zone==3:
            temp_x,temp_y=-x,y


        elif Zone==4:
            temp_x,temp_y=-x,-y


        elif Zone==5:
            temp_x,temp_y=-y,-x


        elif Zone==6:
            temp_x,temp_y=y,-x


        elif Zone==7:
            temp_x,temp_y=x,-y


        return temp_x,temp_y


    def DrawLine(x1, y1, x2, y2, r, g, b):
        x1,y1,x2,y2,Zone=FindZone(x1, y1, x2, y2)
        dx = x2 - x1
        dy = y2 - y1
        d = 2*dy - dx
        incE = 2*dy
        incNE = 2*(dy - dx)
        y=y1
        for x in range(int(x1), int(x2+1)):
            new_x,new_y=ZoneRevert(x,y,Zone)
            Points(new_x, new_y , r, g, b)
            if (d>0):
                d = d + incNE
                y = y + 1
            else:
                d = d + incE
   
    def Circlepoints(x, y, value, r, g, b, zone):
        if zone[1]!=0:
            Points(x+value[0], y+value[1], r, g, b)
        if zone[0]!=0:
            Points(y+value[0], x+value[1], r, g, b)
        if zone[7]!=0:
            Points(y+value[0], -x+value[1], r, g, b)
        if zone[5]!=0:
            Points(-x+value[0], -y+value[1], r, g, b)
        if zone[6]!=0:
            Points(x+value[0], -y+value[1], r, g, b)
        if zone[4]!=0:
            Points(-y+value[0], -x+value[1], r, g, b)
        if zone[3]!=0:
            Points(-y+value[0], x+value[1], r, g, b)
        if zone[2]!=0:
            Points(-x+value[0], y+value[1], r, g, b)


    def MidpointCircle(radius, value, r, g, b, zone):
        d = 1 - radius
        x = 0
        y = radius


        Circlepoints(x, y, value, r, g, b, zone)


        while x < y:
            if d < 0:
                d = d + 2*x + 3
                x = x + 1
            else:
                d = d + 2*x - 2*y + 5
                x = x + 1
                y = y - 1


            Circlepoints(x,y, value, r, g, b, zone)


    #Restart
    DrawLine(-250, 220, -200, 220, 1,0.75, 0)
    DrawLine(-250, 220, -220, 250, 1, 0.75, 0)
    DrawLine(-250, 220, -220, 190, 1, 0.75, 0)


    #Close
    DrawLine(200,250,250,200, 1,0,0)
    DrawLine(250,250,200,200, 1,0,0)


    #Platform 1
    DrawLine(p1_x-100, p1_y, p1_x, p1_y, 0, 0.8, 0)
    DrawLine(p1_x-100, p1_y-30, p1_x, p1_y-30, 0.588, 0.294, 0)
    DrawLine(p1_x-100, p1_y-30, p1_x-100, p1_y, 0.588, 0.294, 0)


    #Platform 2
    DrawLine(p2_x-50, p2_y+15, p2_x+50, p2_y+15, 0, 0.8, 0)
    DrawLine(p2_x-50, p2_y-15, p2_x+50, p2_y-15, 0.588, 0.294, 0)
    DrawLine(p2_x-50, p2_y-15, p2_x-50, p2_y+15, 0.588, 0.294, 0)
    DrawLine(p2_x+50, p2_y-15, p2_x+50, p2_y+15, 0.588, 0.294, 0)


    #Platform 3
    DrawLine(p3_x, p3_y, p3_x+100, p3_y, 0, 0.8, 0)
    DrawLine(p3_x, p3_y-30, p3_x+100, p3_y-30, 0.588, 0.294, 0)
    DrawLine(p3_x+100, p3_y-30, p3_x+100, p3_y, 0.588, 0.294, 0)


    #Platform 4
    DrawLine(p1_x-260, p4_y, p1_x, p4_y, 0, 0.8, 0)
    DrawLine(p1_x-260, p4_y-30, p1_x, p4_y-30, 0.588, 0.294, 0)
    DrawLine(p1_x-260, p4_y-30, p1_x-260, p4_y, 0.588, 0.294, 0)


    #Portal
    DrawLine(portal_x, 100, portal_x+20, 100, 0, 0.5, 1)


    #Ball
    MidpointCircle(5, [Fire_x, Fire_y], 0.9, 0.7, 0.1, [1,1,1,1,1,1,1,1])


    #Player
    MidpointCircle(7, [user_x+move, user_y], 0.4, 0.25, 0.2, [1,1,1,1,1,1,1,1])
    DrawLine(user_x+7+move, user_y-25, user_x+7+move, user_y-8, 0, 0.5, 0)
    DrawLine(user_x-7+move, user_y-25, user_x-7+move, user_y-8, 0, 0.5, 0)
    DrawLine(user_x-7+move, user_y-8, user_x+7+move, user_y-8, 0, 0.5, 0)
    DrawLine(user_x-7+move, user_y-25, user_x+7+move, user_y-25, 0, 0.5, 0)
    DrawLine(user_x-7+move, user_y-40, user_x+7+move, user_y-40, 0, 0, 0.5)
    DrawLine(user_x-7+move, user_y-40, user_x-7+move, user_y-26, 0, 0, 0.5)
    DrawLine(user_x+7+move, user_y-40, user_x+7+move, user_y-26, 0, 0, 0.5)
    DrawLine(user_x+move, user_y-40, user_x+move, user_y-30, 0, 0, 0.5)




    glutSwapBuffers()


def animate():
    global pause, user_x, user_y, fall, temp, p1_x, p1_y, move, p1_flag, p2_x, p2_y, p2_move, p3_x, p3_y, p4_y, p2_flag, p3_flag, p4_flag, start, duration, start_flag, end_flag
    global Fire_x, Fire_y, portal_x, portal_move, time_1, time_2


    if end_flag!=True:
        if pause==False:
            if start_flag==True:
                start+=10


                if portal_move==1:
                    portal_x+=1
                    if portal_x+20>250:
                        portal_move=0


                if portal_move==0:
                    portal_x-=1
                    if portal_x<-10:
                        portal_move=1  
               
                if portal_x<user_x+move<portal_x+20 and user_y-40==100:
                    user_y=-210


                if user_x+move<p3_x+100 and user_y-40==p3_y:
                    move+=1.5


                if Fire_x<p1_x-100:
                    Fire_x=250
                else:
                    Fire_x-=0.4


                if user_x-7+move<Fire_x<user_x+7+move and user_y-40<Fire_y<user_y+7:
                    print("Game Over! Better Luck Next Time")
                    end_flag=True


                if user_x+move>=243 and user_y>=p4_y:
                    end_flag=True
                    print(f"Congratulations! You won with time remaining {int((duration-start)/1000)} seconds")


                if (duration-start)/1000==10 or (duration-start)/1000==5:
                    print(f"Time Remaining: {int((duration-start)/1000)} seconds")


                if start>=duration:
                    print("Time's Up! Better Luck Next Time")
                    end_flag=True


                if p2_move==False:
                    p2_x+=0.5


                if p2_x+50>120:
                    p2_move="Left"
               
                if p2_move=="Left":
                    p2_x-=0.6


                if p2_x-50<-120:
                    p2_move="Right"


                if p2_move=="Right":
                    p2_x+=0.6


                if fall==True:
                    user_y+=1


                if fall!=True:
                    if p1_x-100<user_x+move and user_y-40==p1_y:
                            if time_1==False:
                                start-=2000
                                time_1=True
                            p1_flag=True
                            fall=False


                if fall!=True:
                    if p2_x-50<user_x+move<p2_x+50 and user_y-40==p2_y+15:
                            p2_flag=True
                            fall=False


                if fall!=True:
                    if p3_x<user_x+move<p3_x+100 and user_y-40==p3_y:
                            if time_2==False:
                                start-=2000
                                time_2=True
                            p3_flag=True
                            fall=False


                if fall!=True:
                    if p1_x-260<user_x+move and user_y-40==p4_y:
                            p4_flag=True
                            fall=False


                if p1_flag==True:
                    if p1_x-100>user_x+move and user_y-40==p1_y:
                        p1_flag=False
                        fall=None


                if p2_flag==True:
                    if (p2_x-50>user_x+move or p2_x+50<user_x+move) and user_y-40==p2_y+15:
                        p2_flag=False
                        fall=None


                if p3_flag==True:
                    if p3_x+100<user_x+move and user_y-40==p3_y:
                        p3_flag=False
                        fall=None


                if p4_flag==True:
                    if p1_x-260>user_x+move and user_y-40==p4_y:
                        p4_flag=False
                        fall=None


                if fall==None:
                    user_y-=1
                    if user_y-40<=-250:
                        user_y=-210
                        fall=False
       


    glutPostRedisplay()
   
def init():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(104, 1,  1,  1000.0)


glutInit()
glutInitWindowSize(W, H)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
    ##Rafid
wind = glutCreateWindow(b"Trap Platformer")
init()


glutDisplayFunc(display)


glutSpecialFunc(specialKeyListener)


glutMouseFunc(mouseListener)


glutKeyboardFunc(keyboardListener)


glutIdleFunc(animate)


glutMainLoop()

