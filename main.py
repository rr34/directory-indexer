import argparse
import os
import time


def index_drive(directory, index_name='!drive_index.csv', log_name='!index_log.txt', quiet=False):
    import pandas as pd

    dirs_list = []
    filenames_list = []
    fullpath_list = []
    filetypes_list = []
    index_log_str = 'Indexed by little-tools by rr34. See github.com/rr34/little-tools\n'
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
            filetype = os.path.splitext(filename)[-1]
            filetypes_list.append(filetype)
        if not quiet:
            print(f'Directories count: {directories_count}. Directory: {root}')
    elapsed_time = int(time.time() - start_time)
    elapsed_time_str = f'{int(elapsed_time/60)} minutes, {elapsed_time%60} seconds'
    time_now = time.time()
    index_completed_time = time.strftime('%Y-%m-%d %H:%M', time.localtime(time_now))

    index_log_str += f'Directory indexed: {directory}\nCompleted at date/time: {index_completed_time}\nIndexing elapsed time: {elapsed_time_str}\nDirectories count: {directories_count}\nFiles count: {files_count}\n\n'
    if not quiet:
        print(index_log_str)

    index_df = pd.DataFrame({'directory': dirs_list, 'filename': filenames_list, 'fullpath': fullpath_list, 'filetype': filetypes_list})

    drive_index_path = os.path.join(directory, index_name)
    index_log_path = os.path.join(directory, log_name)

    index_df.to_csv(drive_index_path)
    with open(index_log_path, 'w') as text_file:
        text_file.write(index_log_str)
    return drive_index_path, index_log_path


def date_formatter(working_dir, output_prefix='output - ', quiet=False):
    import pandas as pd

    output_files = []
    for file in os.listdir(working_dir):
        file_type = os.path.splitext(file)[-1]
        if file_type.lower() == '.csv':
            bank_df = pd.read_csv(os.path.join(working_dir, file))
            bank_df.columns = bank_df.columns.str.lower()
            iso_8601_format = '%Y-%m-%d'
            bank_df['date2'] = pd.to_datetime(bank_df['date']).dt.strftime(iso_8601_format)

            new_filename = output_prefix + file
            new_filepath = os.path.join(working_dir, new_filename)
            bank_df.to_csv(new_filepath)
            output_files.append(new_filepath)
            if not quiet:
                print(f'Wrote {new_filepath}')
    return output_files


def build_parser():
    parser = argparse.ArgumentParser(
        description='little-tools command line utilities.',
    )
    subparsers = parser.add_subparsers(dest='command', required=True)

    index_parser = subparsers.add_parser(
        'index-drive',
        help='Walk a directory tree and write an index CSV plus log file.',
    )
    index_parser.add_argument('directory', help='Directory to index.')
    index_parser.add_argument(
        '--index-name',
        default='!drive_index.csv',
        help='Filename for the generated CSV index.',
    )
    index_parser.add_argument(
        '--log-name',
        default='!index_log.txt',
        help='Filename for the generated log file.',
    )
    index_parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress progress output.',
    )
    index_parser.set_defaults(func=run_index_drive_command)

    format_parser = subparsers.add_parser(
        'format-dates',
        help='Normalize the date column in CSV files within a directory.',
    )
    format_parser.add_argument('working_dir', help='Directory containing CSV files.')
    format_parser.add_argument(
        '--output-prefix',
        default='output - ',
        help='Prefix for each generated CSV filename.',
    )
    format_parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress per-file output.',
    )
    format_parser.set_defaults(func=run_date_formatter_command)

    return parser


def run_index_drive_command(args):
    directory = os.path.abspath(args.directory)
    if not os.path.isdir(directory):
        raise SystemExit(f'Directory not found: {directory}')

    drive_index_path, index_log_path = index_drive(
        directory=directory,
        index_name=args.index_name,
        log_name=args.log_name,
        quiet=args.quiet,
    )
    if args.quiet:
        print(drive_index_path)
        print(index_log_path)


def run_date_formatter_command(args):
    working_dir = os.path.abspath(args.working_dir)
    if not os.path.isdir(working_dir):
        raise SystemExit(f'Directory not found: {working_dir}')

    output_files = date_formatter(
        working_dir=working_dir,
        output_prefix=args.output_prefix,
        quiet=args.quiet,
    )
    if not output_files:
        print(f'No CSV files found in {working_dir}')
    elif args.quiet:
        for output_file in output_files:
            print(output_file)


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
