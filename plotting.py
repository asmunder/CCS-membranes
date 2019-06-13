import numpy as np
import holoviews as hv
from bokeh import io #.io import output_file, save
from bokeh.layouts import gridplot
hv.extension('bokeh')

# List of names of applications
appl_list = ['Cement','Steel','Coal','FCC','FG','LSFO']
# List of corresponding abbreviations used in data file
appl_abbrv = ['cem','steel','coal','fcc','fg','lsfo']
# Zip the lists together and create a dict so we can lookup abbreviation from name
appl_dict = dict(zip(appl_list,appl_abbrv))

# Load the data from a list of dict of Pandas dataframes
all_data = np.load('all-data-dict.npy')
all_data = all_data[()]

def get_baseplot(sel_appl,**kwargs):

    # Get abbreviation for this application
    appl = appl_dict[sel_appl]
    # Get the data set for this application
    data = all_data[appl]

    # Set some common options for all the figures
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
    return image#im1+im2

# Define the dimension over which to make the HoloMap
kdim = hv.Dimension(('appl','Application'),default=appl_list[0])
# Make the HoloMap and collate it
hmap = hv.HoloMap( {appl : get_baseplot(appl) for appl in appl_list},kdims=kdim)
hmap = hmap.collate()
#hmap = hv.DynamicMap(get_baseplot, kdims=kdim).redim.values(appl=appl_list)
#hmap.options(framewise=True)
# Render this to a file
renderer = hv.renderer('bokeh')
renderer.save(hmap,'test')
#plot = renderer.get_plot(hmap).state
#io.output_file("test.html",mode='inline')
#io.show(plot)
