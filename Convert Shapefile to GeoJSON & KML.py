from Tkinter import *
import Tkconstants,tkFileDialog
from osgeo import ogr
import os

#For GUI
root=Tk()

#Storing in string
var=StringVar(root)
format=StringVar(root)
data_dir=StringVar(root)

lyr_name=""

def fileOpen():
    directory=tkFileDialog.askopenfilename()
    data_dir.set(directory)
    data_str=data_dir.get()
    lyr_name=data_str.rsplit('/',1)[1]
    print lyr_name
    var.set(lyr_name)

def shptoJson(driver, file_path):

    file_name = var.get()
    datadir = file_path.split(file_name)[0]
    dataStr = data_dir.get()
    # split directory from name
    datadir = dataStr.rsplit('/', 1)[0]
    ds_shp = ogr.Open(datadir)
    name_file = file_name.rsplit('.', 1)[0]

    # output layer create can be json or kml
    output_file_name = name_file + "." + format.get()
    ds_output = driver.CreateDataSource(os.path.join(datadir, output_file_name))
    outLayer = ds_output.CreateLayer(str(output_file_name), geom_type=ogr.wkbUnknown)
    # read feature and write to output
    in_lyr = ds_shp.GetLayerByName(str(file_name.rsplit('.', 1)[0]))
    outLayer.CreateFields(in_lyr.schema)
    out_defn = outLayer.GetLayerDefn()
    out_feat = ogr.Feature(out_defn)
    for feat in in_lyr:
        geom = feat.geometry()
        out_feat.SetGeometry(geom)
        for i in range(feat.GetFieldCount()):
            value = feat.GetField(i)
            out_feat.SetField(i, value)
            outLayer.CreateFeature(out_feat)
        print 'process complete'


def convertfile():
    file_path=data_dir.get()
    driver=ogr.GetDriverByName(format.get())
    inputlayer_name=var.get()
    shptoJson(driver,str(file_path))


#input file label
Label(root,text="Input File:").grid(row=0,column=0)
#Target format
Label(root,text="Target Format:").grid(row=1,column=0)
#Background colour
root.configure(background='#ffffff')
#Button for selecting Shapefile
btn=Button(text="Browse",command=fileOpen)
btn.grid(row=0, column=1)
#For targeet format option list
w=OptionMenu(root,var,"hjhj")
format.set("GEOJSON")
format_option=OptionMenu(root,format,"KML","GEOJSON")
format_option.grid(row=1,column=1)
#Button to convert the file
Button(root,text="Convert",command=convertfile).grid(row=3,column=1)
root.mainloop()
