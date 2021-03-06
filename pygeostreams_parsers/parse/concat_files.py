#!/usr/bin/env python

"""
    This script will concatenate files within a specified directory
    and create a separate file with only one Header Row for parsing data
"""

# Imports #
import os
import string
import argparse
import yaml
import datetime


def main():
    """
        MAIN Function
    """

    # Required command line argument for the parser
    ap = argparse.ArgumentParser()
    ap.add_argument('-c', "--config",
                    help="Path to the Multiple Config File",
                    default=r'/multi_config.yml',
                    required=True)
    ap.add_argument('-d', "--debug",
                    help="Enter DEBUG mode",
                    default=r'False',
                    required=False)
    ap.add_argument('-p', "--printout",
                    help="Print Non-Error Messages to the Screen",
                    default=r'False',
                    required=False)
    opts = ap.parse_args()
    if not opts.config:
        ap.print_usage()
        quit()

    # If debug is True, only the first file in each directory will be processed
    if opts.debug:
        debug = opts.debug
    else:
        debug = False

    # If printout is True, Non-Error messages will print to the screen
    if opts.printout:
        printout = eval(opts.printout)
    else:
        printout = False

    multi_config = yaml.load(open(opts.config, 'r'))
    
    # Main Directory
    main_dir = multi_config['inputs']['file_path']
    
    # Directory with the files to be concatenated
    data_dir = os.path.join(main_dir, multi_config['inputs']['downloads'])
    
    # CSV with the list of files to be concatenated
    new_files = multi_config['inputs']['new_files']
    
    # The file that will contain the aggregated data
    current_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    # Will contain the current time concatenation starts
    file_set_name = (multi_config['inputs']['aggregate'] + str(current_time) +
                      multi_config['inputs']['aggregate_file_type'])
    concat_file_name = os.path.join(main_dir, file_set_name)
    
    # The file that will contain the data for parsing
    parse_file_name = os.path.join(main_dir, multi_config['inputs']['parse'])
    
    # How many rows of headers should be present? (start counting at one)
    total_header_rows = int(multi_config['inputs']['headers'])
    
    # File Extension Type
    file_type = multi_config['inputs']['file_type']
    
    # Header Verification Text
    verify_header =  multi_config['inputs']['verify']

    header_status = False
    
    if not os.path.isfile(os.path.join(main_dir, new_files)):
        print "ERROR: VALID new_files NOT SUPPLIED - EXITING"
        quit()

    if printout is True:
        print "INFO: file to write is: " + str(concat_file_name)
        print " "

    if os.path.isdir(data_dir):
    
        # Create the header if it does not exist
        if header_status is False:
            header_status = \
                create_header(main_dir, new_files, data_dir, file_type,
                              concat_file_name, parse_file_name,
                              verify_header, total_header_rows, printout)

            if printout is True:
                print "INFO: Header is = "
                for row in header_status:
                    print row[:-1]
                print " "
    
        # Now to add the non-header data to the file
        if header_status is not False:
            if printout is True:
                print "INFO: Concatenating the data"
            concat_files(debug, data_dir, header_status, main_dir,
                         new_files, file_type, concat_file_name,
                         parse_file_name, total_header_rows, printout)
    
    else:
        print "ERROR: VALID data_dir NOT SUPPLIED"
        print " "

    if printout is True:
        print ""
        print "DONE with Concatenation"


def create_header(main_dir, new_files, data_dir, file_type, concat_file_name,
                  parse_file_name, verify_header, total_header_rows,
                  timestamp='TIMESTAMP', printout=False):
    """
        Create the header
        NOTE: 'timestamp' has a default value
    """

    new_files = open(os.path.join(main_dir, new_files), 'rb')
    new_file_list = new_files.read()
    new_files.close()

    # locate the data files
    datafiles = [datafile for datafile in os.listdir(data_dir) if
                 os.path.isfile(os.path.join(data_dir, datafile)) and
                 datafile.endswith(file_type) and datafile in new_file_list]

    x = 0

    header_rows = None
    combo_header_rows = None

    # step through one file at a time
    for datafile in datafiles:
        if x < 1:
            filename = os.path.join(data_dir, datafile)
            x += 1
            csv_reader = open(filename, 'rb')
            output_file = open(concat_file_name, 'w')
            parse_file = open(parse_file_name, 'w')

            # Erase old lines in parse_file
            parse_file.truncate()

            # Handle CSV Files differently
            if file_type == '.csv':
                # header information
                y = 0
                for row in csv_reader:
                    # check if the header exists
                    if not header_rows or combo_header_rows:
                        if printout is True:
                            print "INFO: Header row does not exist - Creating"
                        if verify_header not in row:
                            print("ERROR: INVALID HEADER IN FILE")
                            return
                        # create header if it does not exist
                        header_rows = []
                        combo_header_rows = []
                    # There should only be this many header rows
                    if y < total_header_rows:
                        header_rows.append(str(row))
                        y += 1
                        output_file.write(str(row))
                    if y == total_header_rows:
                        num_params = len(header_rows[0].split(','))
                        for n in range(num_params):
                            combo_header_rows.append('')
                        for x in header_rows:
                            temp = x.split(',')
                            for n in range(num_params):
                                if n == 0 and 'time' in temp[n].lower():
                                    combo_header_rows[n] = "Time"
                                else:
                                    no_special_chars = ''.join(
                                        filter(lambda x: x in string.printable,
                                               temp[n]))
                                    combo_header_rows[n] = (
                                            combo_header_rows[n] + ' ' +
                                            no_special_chars.rstrip('\r\n'))
                        header_counter = 0
                        for csv_header_val in combo_header_rows:
                            # Remove leading and following whitespace
                            csv_header_val = csv_header_val.strip()
                            if header_counter < num_params-1:
                                parse_file.write(csv_header_val + ',')
                            else:
                                parse_file.write(csv_header_val)
                            header_counter += 1
                        parse_file.write('\n')
                        break
            else:
                # header information
                y = 0
                for row in csv_reader:
                    # check if the header exists
                    if not header_rows:
                        if printout is True:
                            print "INFO: Header row does not exist - Creating"
                        if verify_header not in row:
                            print("ERROR: INVALID HEADER IN FILE")
                            return
                        # create header if it does not exist
                        header_rows = []
                    # There should only be this many header rows
                    if y < total_header_rows:
                        header_rows.append(str(row))
                        if timestamp in str(row):
                            parse_file.write(str(row))
                        y += 1
                        output_file.write(str(row))
                    if y == total_header_rows:
                        break

            # Ensure the files are closed properly regardless
            output_file.close()
            parse_file.close()
            csv_reader.close()

            if printout is True:
                print "INFO: CONCAT File should have header from " + str(filename)

    return header_rows


def concat_files(debug, data_folder, header_data, main_dir,
                 new_files, file_type, concat_file_name,
                 parse_file_name, total_header_rows, printout=False):
    """
        Concatenate the data in the files
        while not duplicating the headers
    """

    if not header_data:
        print("ERROR: No Valid Header Supplied")
        return

    # Current data directory for the Concatenation
    data_directory = os.path.join(main_dir, data_folder)

    if printout is True:
        print "INFO: Directory for concatenation: " + str(data_directory)

    new_files = open(os.path.join(main_dir, new_files), 'rb')
    new_file_list = new_files.read()
    new_files.close()

    if printout is True:
        print "Files to Concatenate"
        print new_file_list

    # locate the data files
    datafiles = [datafile for datafile in os.listdir(data_directory) if
                 os.path.isfile(os.path.join(data_directory, datafile)) and
                 datafile.endswith(file_type) and datafile in new_file_list]

    if debug:
        max_num_files = 1
    else:
        max_num_files = datafiles.__len__()

    if printout is True:
        print ("INFO: Number of Files to concatenate in this directory = "
               + str(max_num_files))
        print ""

    # step through one file at a time
    x = 0
    for datafile in datafiles:
        if x < max_num_files:
            filename = os.path.join(data_directory, datafile)
            x += 1
            csv_reader = open(filename, 'rb')
            output_file = open(concat_file_name, 'a')
            parse_file = open(parse_file_name, 'a')

            # check header information
            y = 0
            for row in csv_reader:
                # check proper headers present
                if y < total_header_rows:
                    if (
                        ((y == 0) and (row[:20] != header_data[y][:20]))
                        or ((y >= 1) and (row != header_data[y]))
                    ):
                        print("ERROR: INVALID HEADER IN FILE")
                        print("str(row)           = " + str(row))
                        print("str(header_data[y] = " + str(header_data[y]))
                        print("")
                        break
                    else:
                        y += 1
                        continue
                if y >= total_header_rows and row not in header_data:
                    # write the data
                    if (y == (total_header_rows + 1)) and (debug == True):
                        output_file.write(filename + "\n")
                        parse_file.write(filename + "\n")
                    output_file.write(str(row))
                    parse_file.write(str(row))
                    y += 1
                else:
                    print("ERROR: INVALID DATA IN FILE")
                    break

            # provide a line break between files if CSV
            if file_type == '.csv':
                output_file.write("\n")
                parse_file.write("\n")

            # Ensure the files are closed properly regardless
            output_file.close()
            csv_reader.close()
            parse_file.close()
            if printout is True:
                print "INFO: CONCAT File should have data for " + str(filename)


if __name__ == "__main__":
    main()
