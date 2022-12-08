# The MIT License (MIT)
#
# Copyright (c) 2022 Alex Yaple
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""
CSV Splitter

Author: Alex Yaple
"""


import csv
import os
import shutil


dir_path = os.getcwd()

# Variables to change based on your needs
Delimiter: str = '\t'
Row_Size: int = 699  # Row_Size does not include the header if limit is an absolute requirement
Original_File_Ext: str = 'txt'  # Original file extension
File_Output_Ext: str = 'txt'  # Output file extension
Keep_Headers: bool = True  # Dictates if the subsequent files retain the header of the original document
Output_Path: str = ''  # Change if the desired output location of the files needs to be in a different directory

# Optional feature
# If you need to upload the files manually and wish to transfer the files to a new directory once complete

Pending_Move: bool = True  # Set to False if the feature is not needed
directory: str = "C:/"  # Set to the desired end directory


def split(file, output_name_template,
          file_type=File_Output_Ext, delimiter=Delimiter, row_limit=Row_Size,
          output_path=Output_Path, keep_headers=Keep_Headers):

    reader = csv.reader(file, delimiter=delimiter)
    current_piece = 1
    file_number = 0
    current_out_path = os.path.join(f"{output_path}{output_name_template}_{file_number}.{file_type}")
    current_out_writer = csv.writer(open(current_out_path, 'w', newline=''), delimiter=delimiter)
    current_limit = row_limit  # Needed to track which line to work next
    if keep_headers:
        headers = next(reader)
        current_out_writer.writerow(headers)
    for i, row in enumerate(reader):
        if i + 1 > current_limit:  # Plus one due to the Header
            current_piece += 1
            file_number += 1
            current_limit = row_limit * current_piece
            current_out_path = os.path.join(f"{output_path}{output_name_template}_{file_number}.{file_type}")
            current_out_writer = csv.writer(open(current_out_path, 'w', newline='', ), delimiter=delimiter)
            if keep_headers:
                current_out_writer.writerow(headers)
        current_out_writer.writerow(row)


for file in os.listdir(dir_path):
    file_name, file_ext = os.path.splitext(file)
    Output_Name_Template = file_name
    if file_ext == f".{Original_File_Ext}":
        file_to_del = file
        split(open(file, 'r'), Output_Name_Template)

try:
    os.remove(file_to_del)
except OSError as e:
    print(e)
    input("File open please close")
    os.remove(file_to_del)

while Pending_Move:
    initials = input('Please enter your initials:')
    check = input('Enter \"y\" to move the files after you are done uploading or \"n\" to leave the files: ')
    if check.lower() == 'y':
        dir_path = os.getcwd()
        for file in os.listdir(dir_path):
            file_name, file_ext = os.path.splitext(file)
            if file_ext == '.txt':
                shutil.move(file, f'{directory}/{file_name}-{initials}{file_ext}')
        input('Complete - Press enter to exit')
        break
    elif check.lower() == 'n':
        break
    else:
        print('Invalid input if you wish to close the program use \"n\" to leave the files')
        pass
while not Pending_Move:
    input("Complete - Press enter to exit")
