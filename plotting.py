import numpy as np
import holoviews as hv
import argparse
from bokeh import io #.io import output_file, save
from bokeh.layouts import gridplot
hv.extension('bokeh')

parser = argparse.ArgumentParser()
parser.add_argument("dataset", help="name of dataset")
args = parser.parse_args()

all_data = np.load('all-data-dict.npy')
all_data = all_data[()]
data = all_data[args.dataset]
opts = {'width':600,'height':400,'colorbar':True}

# First two plots: cost at optimal capture ratio and 90%, with contour lines
levCost = [10,12.5,15,17.5,20,25,30,35,40,50]
im1 = hv.Image(data,vdims=[hv.Dimension('costOpt',range=(0,50))]).options(**opts,cmap='RdYlGn_r') 
im2 = hv.Image(data,vdims=[hv.Dimension('cost90',range=(0,50))]).options(**opts,cmap='RdYlGn_r')
im1 = im1 * hv.operation.contours(im1,levels=levCost).options(show_legend=False)
im2 = im2 * hv.operation.contours(im2,levels=levCost).options(show_legend=False)

# Next two plots: cost reduction optimal vs. 90 and capture ratio optimal
im3 = hv.Image(data,vdims=[hv.Dimension('costRedOpt90',range=(-1,0))]).options(**opts,cmap='Greens_r') 
im4 = hv.Image(data,vdims=[hv.Dimension('ccrOpt',range=(0,1))]).options(**opts,cmap='RdYlGn')
im3 = im3 * hv.operation.contours(im3,levels=np.arange(-0.5,0,0.1)).options(show_legend=False)
im4 = im4 * hv.operation.contours(im4,levels=np.arange(0,1,0.05)).options(show_legend=False)

# Final two plots: number of stages for optimal and 90% capture ratio
im5 = hv.operation.contours(hv.Image(data,vdims='nstagesOpt'),levels=[0.5,1.5,2.5,3.5],filled=True).options(**opts,cmap='Wistia',color_levels=3)
im6 = hv.operation.contours(hv.Image(data,vdims='nstages90'),levels=[0.5,1.5,2.5,3.5],filled=True).options(**opts,cmap='Wistia',color_levels=3)


image = im1+im2+im3+im4+im5+im6
image = image.cols(2)

renderer = hv.renderer('bokeh')
plot = renderer.get_plot(image).state
io.output_file("test.html",mode='inline')
io.show(plot)

