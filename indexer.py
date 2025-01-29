import argparse, os, time
import pandas as pd

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

    index_df.to_csv('!drive_index.csv')
    with open('!index_log.txt') as text_file:
        text_file.write(index_log_str)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A simple directory indexer that saves filenames and full paths of a directory as CSV for easy searching.")
    parser.add_argument("directory", type=float, help="Directory to be indexed.")
 
    args = parser.parse_args()
 
index_drive(args.directory)