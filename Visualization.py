from Behaviors import Behavior
from Representation import Shape
from matplotlib.pyplot import plot, axis, figure, show, legend, gca, fill
from celluloid import Camera

FRAMERATE = 20/5
TIME = 30
FRAMES = TIME * FRAMERATE
COUNT = 0
fig = figure()
axis('equal')
axis('off')
camera = Camera(fig)

def run(me, ball, peerList, opponentList, field):

    dt = 0.5
    do = 0.5
    db = 0.25

    x, y = field.shape.exterior.xy
    plot(x,y, 'green', label = 'field')

    goals = [field.ownGoal, field.oppGoal]
    for goal in goals:
        x,y = goal.exterior.xy
        plot(x,y, 'green', label = 'field')
       
    for opponent in opponentList: 
        repr = Shape.circle(opponent.pos, do)
        x,y = repr.exterior.xy
        plot(x,y, 'magenta', label = 'opponent')

    for peer in peerList: 
        repr = Shape.circle(peer.pos, dt)
        x,y = repr.exterior.xy
        plot(x,y, 'cyan', label = 'peer')  
    
    repr = Shape.circle(me.pos, dt)
    x,y = repr.exterior.xy
    plot(x,y, 'purple', label = 'me')

    repr = Shape.circle(ball.pos, db)
    x,y = repr.exterior.xy
    plot(x,y, 'yellow', linewidth = 2.5, label = 'ball')

    d = Behavior.all
    plotbehavior(d, 'avoidopp', 'orange', False)
    plotbehavior(d, 'shot', 'darkred', False)
    plotbehavior(d, 'Pass', 'grey')
    plotbehavior(d, 'dribble','blue')

    #LEGEND
    handles, labels = gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    legend(by_label.values(), by_label.keys())

    camera.snap()

    #DEBUG

    #Print area
    #print(f"area of the field: {area(field.shape)}")
    #print(f"area of the feasible design space (all skill spaces combined): {area(d)}")

    
    
    show()
    
    global COUNT
    print(f" COUNT: {COUNT}")
    if COUNT == FRAMES:
        animation = camera.animate()
        animation.save('SMDM.mp4')
        show()
        print("---------------- ANIMATION CREATED! ----------------")
        COUNT = COUNT + 1
    else:
        COUNT = COUNT + 1


def plotbehavior(dict, key, color, plottarget = True,):
    try:
        for behavior in dict[key]:
            x,y = behavior.shape.exterior.xy
            tx, ty = behavior.pos[0], behavior.pos[1]
            plot(x,y, color , linewidth = 2.5, label = key)
            if plottarget:
                plot(tx,ty, color , linewidth = 1, marker = 'o')
    except:
        return

def area(input):
    area = 0
    try:
        values = list(input.values())
        for regions in values:
            for region in regions:
                area = area + Shape.area(region.shape)
    except:
        area = Shape.area(input)
    return area