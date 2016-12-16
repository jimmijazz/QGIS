# Starts with an entire dataset and a CSV file of suburbs. Deletes all suburbs
# from the dataset that aren't in the CSV

from qgis.utils import iface
from PyQt4.QtCore import QVariant
import csv

CSV_FILE = '/Users/Joshua/Desktop/Property Passbook/QGIS/melbourne.csv'

suburbs_dict = {}   # Contains Suburb_Name : Municipality/Submarket

layer = iface.activeLayer() #Set currently active layer
layer.startEditing()

caps = layer.dataProvider().capabilities()  # Capabilities supported by data
caps_string = layer.dataProvider().capabilitiesString()

with open (CSV_FILE, 'rb') as csvfile:
    datafile = csv.reader(csvfile, delimiter=",")
    for row in datafile:
        # For each suburb add the name and municipality
        suburbs_dict[row[1]] = row[3]   # Add to CSV file
    for f in layer.getFeatures():   # For each suburb in layer
        if f['SSC_NAME'] in suburbs_dict:
            if caps & QgsVectorDataProvider.ChangeAttributeValues:
                print("Changing", f.id())

                # Change S
                layer.changeAttributeValue(f.id(),4, suburbs_dict[f['SSC_NAME']])
                del suburbs_dict[f['SSC_NAME']] # Remove from dataset
        else:
            layer.deleteFeature(f.id())


layer.commitChanges()
print suburbs_dict # Print the suburbs in the spreadsheet that weren't found
