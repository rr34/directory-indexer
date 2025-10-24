import os, time, pandas as pd
import DBsqlstatements


def keystone_scrub(target_directory):
    dirs_list = list()
    filenames_list = list()
    fullpath_list = list()
    filetypes_list = list()
    index_log_str = 'Indexed by little-tools by rr34. See github.com/rr34/little-tools\n'
    directories_count = 0
    files_count = 0
    start_time = time.time()
    for (root, dirs, files) in os.walk(target_directory):
        directories_count += 1
        for filename in files:
            files_count += 1
            filetype = os.path.splitext(filename)[-1]
            if filetype in ('.csv', '.txt'):
                fullpath = os.path.join(root, filename)

                valid_csv = True
                try:
                    file_df = pd.read_csv(fullpath, header=None)
                except:
                    print('File is invalid csv: ' + fullpath)
                    valid_csv = False
                num_columns = file_df.shape[1]

                numeric_cols = file_df.iloc[1:, 0:3]  # first 3 columns not including the index column
                is_numeric = numeric_cols.apply(pd.to_numeric, errors='coerce').dropna(how='all').notna().all().all()

                if num_columns == 5 and is_numeric and valid_csv:
                    print('5 columns wide and probably a points file: ' + filename)
                    # get the full text of the file to save
                    with open(fullpath, "r", encoding="utf-8") as f:
                        file_str = f.read()

                    col1_dummy = (file_df[1] < 20000).all()
                    col2_dummy = (file_df[2] < 20000).all()

                    if col1_dummy and col2_dummy:
                        data_source = 'nate scrub of dummy coordinate file'
                        UTMZone = 'NA because relative points'
                        north_field = 'NDummy'
                        east_field = 'EDummy'
                        elev_field = 'ElevDummy'
                    else:
                        data_source = 'nate scrub of state plane coordinate file'
                        UTMZone = 'Georgia West'
                        north_field = 'Northing'
                        east_field = 'Easting'
                        elev_field = 'Elevation'
                        
                    file_data_toadd = (fullpath, filename, filetype, file_str, data_source)
                    FileID = DBsqlstatements.insert_keystone_filedata(file_data_toadd)

                    # get the data 
                    pts_data_toadd = []
                    for row in file_df.itertuples(index=False, name=None):  # avoid pandas index
                        description_parts = []

                        # Try converting numeric columns; if fails, append to description
                        try:
                            pt_index = float(row[0]) if pd.notna(row[0]) and row[0] != '' else None
                        except Exception:
                            pt_index = None
                            description_parts.append(str(row[0]))

                        try:
                            northing = float(row[1]) if pd.notna(row[1]) and row[1] != '' else None
                        except Exception:
                            northing = None
                            description_parts.append(str(row[1]))

                        try:
                            easting = float(row[2]) if pd.notna(row[2]) and row[2] != '' else None
                        except Exception:
                            easting = None
                            description_parts.append(str(row[2]))

                        try:
                            elevation = float(row[3]) if pd.notna(row[3]) and row[3] != '' else None
                        except Exception:
                            elevation = None
                            description_parts.append(str(row[3]))

                        # Original description column
                        original_desc = str(row[4]) if pd.notna(row[4]) and row[4] != '' else ''
                        description_parts.append(original_desc)

                        # Combine any parts into a single string for DB
                        description = " | ".join(filter(None, description_parts)) or None

                        pts_data_toadd.append((FileID, pt_index, northing, easting, elevation, UTMZone, description))
                    DBsqlstatements.insert_keystone_ptdata(north_field, east_field, elev_field, pts_data_toadd)

                

            dirs_list.append(root)
            filenames_list.append(filename)
            fullpath_list.append(os.path.join(root, filename))
            filetypes_list.append(filetype)



        print(f'Directories count: {directories_count}. Directory: {root}')
    elapsed_time = int(time.time() - start_time)
    elapsed_time_str = f'{int(elapsed_time/60)} minutes, {elapsed_time%60} seconds'
    time_now = time.time()
    index_completed_time = time.strftime('%Y-%m-%d %H:%M', time.localtime(time_now))

    index_log_str += f'Directory indexed: {target_directory}\nCompleted at date/time: {index_completed_time}\nIndexing elapsed time: {elapsed_time_str}\nDirectories count: {directories_count}\nFiles count: {files_count}\n\n'
    print(index_log_str)

    index_df = pd.DataFrame({'directory': dirs_list, 'filename': filenames_list, 'fullpath': fullpath_list, 'filetype': filetypes_list})

    drive_index_path = os.path.join(target_directory, '!drive_index.csv')
    index_log_path = os.path.join(target_directory, '!index_log.txt')

    index_df.to_csv(drive_index_path)
    with open(index_log_path, 'w') as text_file:
        text_file.write(index_log_str)




def scrub_FranklinOhio_addresses(filepath):
    franklin_df = pd.read_csv(filepath)

    data_toadd = []
    chunk_size = 1000
    count = 0
    for row in franklin_df.itertuples(index=True, name='row'):
        STHNUM = str(row.STHNUM)
        STADDR = str(row.STADDR)
        USPS_CITY = str(row.USPS_CITY)
        ZIPCODE = str(row.ZIPCODE)
        DESCR1 = str(row.DESCR1)
        DESCR2 = str(row.DESCR2)
        DESCR3 = str(row.DESCR3)
        NAME1 = str(row.NAME1)

        data_toadd.append((STHNUM, STADDR, USPS_CITY, ZIPCODE, DESCR1, NAME1))
        DBsqlstatements.insert_data(data_toadd)

        if len(data_toadd) >= chunk_size:
            data_toadd = []
            count += 1
            print(count)

    return