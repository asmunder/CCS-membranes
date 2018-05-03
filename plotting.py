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
lev = [10,12.5,15,17.5,20,25,30,35,40,50]

im1 = hv.Image(data,vdims='costOpt').redim.range(z=[0,100]).options(width=600,height=400,cmap='RdYlGn_r',colorbar=True)
im1 = im1 * hv.operation.contours(im1,levels=lev)
im2 = hv.Image(data,vdims='cost90').options(width=600,height=400,cmap='RdYlGn_r',colorbar=True)
im2 = im2 * hv.operation.contours(im2,levels=lev)
im3 = hv.operation.contours(hv.Image(data,vdims='nstagesOpt'),levels=[1,2,3],filled=True).options(width=600,height=400,cmap='Pastel1',colorbar=True)
im4 = hv.operation.contours(hv.Image(data,vdims='nstages90'),levels=[1,2,3],filled=True).options(width=600,height=400,cmap='Pastel1',colorbar=True)
image = im1+im2+im3+im4
image = image.cols(2)
renderer = hv.renderer('bokeh')
plot = renderer.get_plot(image).state
#plot = gridplot([[p1,p2],[p3,p4]])
#renderer.save(image,'test')
io.output_file("test.html",mode='inline')
io.show(plot)


