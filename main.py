import pydicom
import pandas as pd
import glob


def dicom2csv(extract=[],
              move_on=[(0x7FE0, 0x0008), (0x7FE0, 0x0009), (0x7FE0, 0x0010)],
              folder_path=str(),
              csv_file_name="metadata.csv",
              return_dataframe=False):
    '''
  Extract specific DICOM metadata from multiple DICOM files collected in a
  specified folder.
  ::Params
      - extract (list):
          The keywords of the DICOM attributes you want to extract.
      - move_on (list):
          The tags of the DICOM attributes you don't want to move on.
          By default,it contains a list of the tags of pixel data:
          [(0x7FE0,0x0008), (0x7FE0,0x0009), (0x7FE0,0x0010)]
          If you want to move on onto some attributes, it's recommended
          to append its unique tags in addition to pixel data tags.
      - folder_path (string):
          Path of the folder that contains the DICOM files.
      - csv_file_name (string):
          The name of the CSV file.
      - return_dataframe (bool):
          if True, returns a pandas dataframe of the extracted data for
          direct use.

  :: Returns
      - CSV file contains DICOM metadata specified the parameter extracted.
      - Pandas dataframe when return_dataframe is set to True.

  :: Example:
      dicom2csv(extract = ['StudyDate'],
                folder_path = 'content/dicomfolder',
                csv_file_name = "Study_Dates.csv",
                return_dataframe = True)
  '''

    # Initialize the meta dictionary that will have the specified attributes
    meta = {keyword: [] for keyword in extract}

    # List the files' names that we want to extract data from
    dicom_files = glob.glob(folder_path + '/*.dcm')

    # Iterate over each DICOM file in the folder and read it using dcmread()
    for file_path in dicom_files:
        # Read the DICOM file from the specified path
        dcm = pydicom.dcmread(file_path)

        # Iterate over the DICOM attributes in the current DICOM file "dcm"
        for elem in dcm.iterall():
            # Ensure that the attribute is not a pixel data, and it's one of the
            # required attributes

            if (elem.tag not in move_on) and (elem.keyword in extract):
                print('available elem', elem)
                # Append the value of the current attribute
                meta[elem.keyword].append(elem.value)

    # Create a pandas dataframe for better use of the data
    df = pd.DataFrame(data=meta, columns=extract)

    # Create the CSV file with the specified name
    df.to_csv(csv_file_name, index=False)
    # Return the extracted dataframe for direct use
    if return_dataframe:
        return df


df = dicom2csv(extract=['PatientID', 'ReasonForStudy', 'StudyDescription'],
               folder_path='./sample2',
               csv_file_name='data.csv',
               return_dataframe=True)


print(df)
