"""
Plot reads in Bering Sea Ice Concentration data for monthly data 1850-2018 and
also creates a netcdf file of the data!

Notes
-----
    Author : Zachary Labe
    Date   : 24 March 2019
"""

### Import modules
import numpy as np
from netCDF4 import Dataset
import datetime

### Define directories
directorydata = '/surtsey/zlabe/seaice/SIC_Alaska/' 
directoryfigure = '/home/zlabe/Documents/Projects/BeringSeaIce2018/Figures/'

### Define time           
now = datetime.datetime.now()
currentmn = str(now.month)
currentdy = str(now.day)
currentyr = str(now.year)
currenttime = currentmn + '_' + currentdy + '_' + currentyr
titletime = currentmn + '/' + currentdy + '/' + currentyr
print('\n' '----Plotting Bering SIC - %s----' % titletime)

### Define years
years = np.arange(1850,2018+1,1)

### Retrieve data from historical sea ice atlas
filename = directorydata + 'SNAP_SEA_ICE_ATLAS_APR.nc'

data = Dataset(filename)
ice = data.variables['sic_con_pct'][:]
lat1 = data.variables['lat'][:]    
lon1 = data.variables['lon'][:]
time = data.variables['time'][:]
data.close()

print('Completed: Data read!')

### Retrieve ice atlas monthly data
feb = ice[::12,:,:] # starts on mo/15/1850 to mo/15/2017

### Meshgrid
lon2,lat2 = np.meshgrid(lon1,lat1)

### Read data for 2018
filename2 = 'Alaska_SIC_Apr_2017.nc'
data = Dataset(directorydata + filename2)
ice18q = data.variables['sic'][:]
ice18 = ice18q[np.newaxis,:,:]

filename2 = 'Alaska_SIC_Apr_2018.nc'
data = Dataset(directorydata + filename2)
ice19q = data.variables['sic'][:]
ice19 = ice19q[np.newaxis,:,:]


### Append time series for 1850-2018
iceallq = np.append(feb,ice18,axis=0)
iceall = np.append(iceallq,ice19,axis=0)

### Create netCDF4 file for February data
def netcdfAlaska(lats,lons,var,years,directory):
    print('\n>>> Using netcdfAlaska function!')
    
    name = 'Alaska_SIC_Apr_1850-2018.nc'
    filename = directory + name
    ncfile = Dataset(filename,'w',format='NETCDF4')
    ncfile.description = 'April 1850-2018 SIC from ' \
                        'Alaska Sea Ice Atlas'
    
    ### Dimensions
    ncfile.createDimension('year',var.shape[0])
    ncfile.createDimension('lat',var.shape[1])
    ncfile.createDimension('lon',var.shape[2])
    
    ### Variables
    years = ncfile.createVariable('years','f4',('year'))
    latitude = ncfile.createVariable('lat','f4',('lat'))
    longitude = ncfile.createVariable('lon','f4',('lon'))
    varns = ncfile.createVariable('sic','f4',('year','lat','lon'))
    
    ### Units
    varns.units = '%'
    ncfile.title = 'SIC on AK Sea Ice Atlas Grid'
    ncfile.instituion = 'Dept. ESS at University of California, Irvine'
    ncfile.source = 'http://seaiceatlas.snap.uaf.edu/'
    ncfile.references = 'see Atlas documentation for various sources'
    
    ### Data
    years[:] = years
    latitude[:] = lats
    longitude[:] = lons
    varns[:] = var
    
    ncfile.close()
    print('*Completed: Created netCDF4 File!')
    
netcdfAlaska(lat1,lon1,iceall,years,directorydata)
