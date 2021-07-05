from typing import Sequence
import xml.etree.ElementTree as ET
import datetime
import pandas as pd

#Full path of input xml file
input_file = r'C:\Users\SManigan\Desktop\New Text Document.xml'

#Full path of outpur csv file
output_file = 'output.csv'

s = datetime.datetime.today()
root = ET.parse(input_file)
root = root.getroot()

namespace = root.tag.split('}')[0].strip('{')
namespace = {'wd': namespace}

rows = root.iterfind('wd:Report_Entry', namespaces=namespace)
fields = []
data = []
for row in rows:
    columns = list(row.iter())
    parent = ''
    for column in columns:
        if 'Report_Entry' in column.tag:
            continue
        if list(column):
            parent = column.tag.replace('{'+namespace['wd']+'}', '')
        try:
            if column.text and column.text.strip():
                field = list(column.attrib.values())[0] #Ex: WID
                fields.append(parent + '_' + field)
            else:
                field = list(column.attrib.keys())[0].replace('{'+namespace['wd']+'}', '') #ex Descriptor
                fields.append(parent + '_' + field)
        except IndexError:
            fields.append(column.tag.replace('{'+namespace['wd']+'}', ''))
    print('Added %s columns' %str(len(fields)))
fields = list(set(fields))
fields.sort()

rows = root.iterfind('wd:Report_Entry', namespaces=namespace)
for row in rows:
    columns = list(row.iter())
    parent = ''
    columns = list(row.iter())
    field = ''
    record = []
    for column in columns:
        if 'Report_Entry' in column.tag:
            continue
        if list(column):
            parent = column.tag.replace('{'+namespace['wd']+'}', '')
        try:
            if column.text and column.text.strip():
                field = list(column.attrib.values())[0] #Ex: WID
                field = parent + '_' + field
            else:
                field = list(column.attrib.keys())[0].replace('{'+namespace['wd']+'}', '') #ex: Descriptor
                field = parent + '_' + field
        except IndexError:
            field = column.tag.replace('{'+namespace['wd']+'}', '')
        try:
            value = column.text.strip()
        except AttributeError:
            value = ''
        if not value:
            try:
                value = list(column.attrib.values())[0]
            except IndexError:
                pass
        while True:
            try:
                record[fields.index(field)] = value
                break
            except IndexError:
                record.append('')
    data.append(record)
    print('Added %s records' %str(len(data)))

df = pd.DataFrame(data)
df.astype(str)
df.columns = fields
df.reindex(sorted(df.columns), axis=1)
df.to_csv(output_file, index=False)
print("Time taken: ",datetime.datetime.today() - s)
