import numpy as np
import holoviews as hv
import argparse
from bokeh import io #.io import output_file, save
hv.extension('bokeh')

parser = argparse.ArgumentParser()
parser.add_argument("dataset", help="name of dataset")
args = parser.parse_args()

all_data = np.load('all-data-dict.npy')
all_data = all_data[()]
d = all_data[args.dataset]

yaxis = d['xaxis']
xaxis = d['yaxis']
costOpt = d['costOpt']
ds_c90 = hv.Dataset((xaxis,yaxis,d['cost90']),['x','y'],'Total cost($)')
ds_copt = hv.Dataset((xaxis,yaxis,d['costOpt']),['x','y'],'Total cost($)')
ds_n90 = hv.Dataset((xaxis,yaxis,d['nstages90']),['x','y'],'No. of stages')
ds_nopt = hv.Dataset((xaxis,yaxis,d['nstagesOpt']),['x','y'],'No. of stages')
image  = hv.Image(ds_c90).options(width=1000,height=800,cmap='RdYlGn_r',colorbar=True)
image += hv.Image(ds_copt).options(width=1000,height=800,cmap='RdYlGn_r',colorbar=True)
image += hv.Image(ds_n90).options(width=1000,height=800,cmap='Pastel1',colorbar=True)
image += hv.Image(ds_nopt).options(width=1000,height=800,cmap='Pastel1',colorbar=True)
renderer = hv.renderer('bokeh')
plot = renderer.get_plot(image).state
#renderer.save(image,'test')
io.output_file("test.html",mode='inline')
io.show(plot)


