# this script assumes Python 3.5 is in use

# imports
import aplpy
import matplotlib.pyplot as plt

#..........................................................................main
def main(image1, image2, image3, text) :
    
    fig = plt.figure(figsize=(15, 5))
    
    f1 = aplpy.FITSFigure(image1, figure=fig, subplot=[0.025,0,0.325,0.975])
    f1.tick_labels.hide()
    f1.ticks.hide()
    f1.axis_labels.set_ytext(text)
    f1.axis_labels.set_font(size='x-large')
    f1.axis_labels.hide_x()
    f1.show_grayscale()
    
    f2 = aplpy.FITSFigure(image2,figure=fig,subplot=[0.35,0,0.325,0.975])
    f2.tick_labels.hide()
    f2.ticks.hide()
    f2.axis_labels.hide()
    f2.show_grayscale(stretch='arcsinh')
    
    f3 = aplpy.FITSFigure(image3,figure=fig,subplot=[0.675,0,0.325,0.975])
    f3.tick_labels.hide()
    f3.ticks.hide()
    f3.axis_labels.hide()
    f3.show_grayscale()
    
    fig.canvas.draw()
    plt.savefig(text + '_images.pdf')
    plt.close()
    
    return
#..............................................................end of functions
