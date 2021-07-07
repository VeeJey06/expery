import xml.etree.ElementTree as ET
import datetime
import pandas as pd


input_file=r'C:\Users\SManigan\Desktop\New Text Document.xml'
output_file=r'output.csv')

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
    # print('Added %s columns' %str(len(fields)))
fields = list(set(fields))
fields.sort()

rows = root.iterfind('wd:Report_Entry', namespaces=namespace)
for row in rows:
    columns = list(row.iter())
    parent = ''
    field = ''
    prev_col = ''
    record = []
    unpivot_rows = []
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
                if record[fields.index(field)] != '' and (prev_col == field or prev_col ==''):
                    prev_col = field
                    unpivot_rows.append([i for i in record])
                else:
                    record[fields.index(field)] = value
                if unpivot_rows:
                    for unpivot_row in unpivot_rows:
                        if unpivot_row[fields.index(field)] == '' or unpivot_row[fields.index(field)] == record[fields.index(field)]:
                            unpivot_row[fields.index(field)] = value
                break
            except IndexError:
                record.append('')
                for unpivot_row in unpivot_rows:
                    unpivot_row.append('')
    data.append(record)
    data.extend(unpivot_rows) if unpivot_rows else ''
    # print('Added %s records' %str(len(data)))

df = pd.DataFrame(data)
df.astype(str)
df.columns = fields
df.reindex(sorted(df.columns), axis=1)
df.to_csv(output_file, index=False)
print("Time taken: ",datetime.datetime.today() - s)
