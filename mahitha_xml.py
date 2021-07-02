import xml.etree.ElementTree as ET
import csv

#Full path of input xml file
input_file = r'C:\Users\SManigan\Desktop\New Text Document.xml'

#Full path of outpur csv file
output_file = 'output.csv'

root = ET.parse(input_file)
root = root.getroot()

namespace = root.tag.split('}')[0].strip('{')
namespace = {'wd': namespace}

rows = root.iterfind('wd:Report_Entry', namespaces=namespace)
fields = []
data = []
for row in rows:
    columns = list(row.iter())
    col_len = len(columns)
    new_row = []
    for column in columns:
        if 'Report_Entry' in column.tag:
            continue
        elif len(fields) < col_len - 1:
            try:
                if column.text.strip():
                    fields.append(list(column.attrib.values())[0])
                else:
                    fields.append(list(column.attrib.keys())[0])
            except IndexError:
                fields.append(column.tag.replace('{'+namespace['wd']+'}', ''))
        try:
            value = column.text.strip()
        except AttributeError:
            pass
        if not value:
            try:
                value = list(column.attrib.values())[0]
            except IndexError:
                pass
        new_row.append(value)
    data.append(new_row)

with open(output_file, 'w') as file:
    writer = csv.writer(file)
    writer.writerow(fields)
    writer.writerows(data)
