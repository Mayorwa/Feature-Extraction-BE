import pydicom

dcm_data = pydicom.dcmread('./samples/000000.dcm')
print(dcm_data)
