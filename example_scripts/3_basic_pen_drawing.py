stroke(0)
strokeWidth(1)
ps = 2

# =====================================
# draw a square
# =====================================

color = (0,0,0,.2) # gray
fill(*color)
b = BezierPath()
b.moveTo((10,10)) # starting point
b.lineTo((110,10)) # draw line from previous point to (x,y)
b.lineTo((110, 110)) # draw line from previous point to (x,y)
b.lineTo((10, 110)) # draw line from previous point to (x,y)
b.closePath() # close the path
drawPath(b) # draw the pen's path
for p in b.points:
    fill(0)
    oval(p[0]-ps, p[1]-ps, ps*2, ps*2)

# =====================================
# draw a 4 sided polygon
# =====================================

color = (1,0,0,.2) # red
fill(*color)
b = BezierPath()
b.moveTo((122, 10))
b.lineTo((200, 10))
b.lineTo((338, 180))
b.lineTo((196, 180))
b.closePath()
drawPath(b)
for p in b.points:
    fill(0)
    oval(p[0]-ps, p[1]-ps, ps*2, ps*2)
    
# =====================================
# draw a rectangle with a builtin pen operator
# =====================================

color = (0,0,1,.2) # blue
fill(*color)
b = BezierPath()
b.rect(200,200,300,300)
drawPath(b)
for p in b.points:
    fill(0)
    oval(p[0]-ps, p[1]-ps, ps*2, ps*2)

# =====================================
# draw a circle
# =====================================

color = (0,1,0,.2) # green
fill(*color)
b = BezierPath()
b.moveTo((50, 750)) # starting point
b.curveTo((50, 780), (70, 800), (100, 800)) # draw curve from previous point to (x,y) with two offcurves in between
b.curveTo((130, 800), (150, 780), (150, 750)) # draw curve from previous point to (x,y) with two offcurves in between
b.curveTo((150, 720), (130, 700), (100, 700)) # draw curve from previous point to (x,y) with two offcurves in between
b.curveTo((70, 700), (50, 720), (50, 750)) # draw curve from previous point to (x,y) with two offcurves in between

b.closePath() # close the path
drawPath(b) # draw the pen's path
for p in b.points:
    fill(0)
    oval(p[0]-ps, p[1]-ps, ps*2, ps*2)
    
# =====================================
# draw a circle with parameters
# =====================================

color = (0,1,1,.2) # teal
fill(*color)
b = BezierPath()

start_point = 232, 684
sx,sy = start_point
size = 222
tt = 3.6
tension = size/tt

b.moveTo(start_point) # starting point
b.curveTo((sx,sy+tension), (sx+(size/2)-tension, sy+(size/2)), (sx+(size/2), sy+(size/2)))
b.curveTo((sx+(size/2)+tension, sy+(size/2)), (sx+size, sy+tension), (sx+(size), sy))
b.curveTo((sx+(size), sy-tension),(sx+(size/2)+tension, sy-(size/2)), (sx+(size/2), sy-(size/2)))
b.curveTo((sx+(size/2)-tension, sy-(size/2)), (sx, sy-tension), (sx, sy))

b.closePath() # close the path
drawPath(b) # draw the pen's path
for p in b.points:
    fill(0)
    oval(p[0]-ps, p[1]-ps, ps*2, ps*2)