import os, time
import pandas as pd
import datetime

def index_drive(directory):
    dirs_list = list()
    filenames_list = list()
    fullpath_list = list()
    index_log_str = 'Indexed by directory-indexer by rr34. See github.com/rr34/directory-indexer\n'
    directories_count = 0
    files_count = 0
    start_time = time.time()
    for (root, dirs, files) in os.walk(directory):
        directories_count += 1
        for filename in files:
            files_count += 1
            dirs_list.append(root)
            filenames_list.append(filename)
            fullpath_list.append(os.path.join(root, filename))
        print(f'Directories count: {directories_count}. Directory: {root}')
    elapsed_time = int(time.time() - start_time)
    elapsed_time_str = f'{int(elapsed_time/60)} minutes, {elapsed_time%60} seconds'
    time_now = time.time()
    index_completed_time = time.strftime('%Y-%m-%d %H:%M', time.localtime(time_now))

    index_log_str += f'Directory indexed: {directory}\nCompleted at date/time: {index_completed_time}\nIndexing elapsed time: {elapsed_time_str}\nDirectories count: {directories_count}\nFiles count: {files_count}\n\n'
    print(index_log_str)

    index_df = pd.DataFrame({'directory': dirs_list, 'filename': filenames_list, "fullpath": fullpath_list})

    drive_index_path = os.path.join(directory, '!drive_index.csv')
    index_log_path = os.path.join(directory, '!index_log.txt')

    index_df.to_csv(drive_index_path)
    with open(index_log_path, 'w') as text_file:
        text_file.write(index_log_str)


def date_formatter(working_dir):
    for file in os.listdir(working_dir):
        file_type = os.path.splitext(file)[-1]
        if file_type.lower() == '.csv':
            bank_df = pd.read_csv(os.path.join(working_dir, file))
            bank_df.columns = bank_df.columns.str.lower()
            ISO8601_format = '%Y-%m-%d'
            bank_df['date2'] = pd.to_datetime(bank_df['date']).dt.strftime(ISO8601_format)

            new_filename = 'output - ' + file
            new_filepath = os.path.join(working_dir, new_filename)
            bank_df.to_csv(new_filepath)