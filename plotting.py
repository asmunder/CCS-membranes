import numpy as np
import holoviews as hv
from bokeh import io #.io import output_file, save
from bokeh.layouts import gridplot
hv.extension('bokeh')

all_data = np.load('all-data-dict.npy')
all_data = all_data[()]

def get_data(appl):
    return all_data[appl]

def get_baseplot(appl):

    data = get_data(appl)

    opts = {'width':600,'height':400,'colorbar':True,'tools':['hover']}
    xylab = [hv.Dimension('xval'),hv.Dimension('yval')]
    hvargs = {'kdims':xylab}
    levCost = [10,12.5,15,17.5,20,25,30,35,40,50]

    # First two plots: cost at optimal capture ratio and 90%, with contour lines
    im1 = hv.Image(data,**hvargs,label='Cost ($) at optimal CCR',
            vdims=[hv.Dimension('costOpt',range=(0,50))]).options(**opts,cmap='RdYlGn_r') 
    im2 = hv.Image(data,**hvargs,group=appl,label='Cost ($) at 90% CCR',
            vdims=[hv.Dimension('cost90',range=(0,50))]).options(**opts,cmap='RdYlGn_r')
    im1 = im1 * hv.operation.contours(im1,levels=levCost).options(show_legend=False)
    im2 = im2 * hv.operation.contours(im2,levels=levCost).options(show_legend=False)

    # Next two plots: cost reduction optimal vs. 90 and capture ratio optimal
    im3 = hv.Image(data,**hvargs,group=appl,label='Cost reduction, optimal vs. 90% CCR',
            vdims=[hv.Dimension('costRedOpt90',range=(-1,0))]).options(**opts,cmap='Greens_r') 
    im4 = hv.Image(data,**hvargs,group=appl,label='CCR for the optimal case',
            vdims=[hv.Dimension('ccrOpt',range=(0,1))]).options(**opts,cmap='RdYlGn')
    im3 = im3 * hv.operation.contours(im3,levels=np.arange(-0.5,0,0.1)).options(show_legend=False)
    im4 = im4 * hv.operation.contours(im4,levels=np.arange(0,1,0.05)).options(show_legend=False)

    # Final two plots: number of stages for optimal and 90% capture ratio
    im5 = hv.operation.contours(
            hv.Image(data,**hvargs,group=appl,label='No. of stages, optimal CCR',vdims='nstagesOpt'),
            levels=[1.0,2.0,3.0],filled=True
        ).options(**opts,cmap='Wistia',color_levels=3)
    im6 = hv.operation.contours(
            hv.Image(data,**hvargs,group=appl,label='No. of stages, 90% CCR',vdims='nstages90'),
            levels=[1.0,2.0,3.0],filled=True
        ).options(**opts,cmap='Wistia',color_levels=3)

    image = im1+im2+im3+im4+im5+im6
    image = image.cols(2)
    return image

renderer = hv.renderer('bokeh')
appl_list = ['cem','steel','coal','fcc','fg','lsfo']
#image = hv.HoloMap( {appl : get_baseplot(appl) for appl in appl_list },kdims="Application")
image = hv.DynamicMap(get_baseplot, kdims='Appl').redim.values(Appl=appl_list)
image.options(framewise=True)
#image = image.collate()
plot = renderer.get_plot(image).state
io.output_file("test.html",mode='inline')
io.show(plot)
