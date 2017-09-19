from module_sonochem import *


def show_menu():
    decorating_bar('*', 'MENU')
    print('''[1] Load measurements from single files
[2] Load measurements from directory
[3] Select for processing
[4] Delete data
[5] Show info
[6] Plot kinetics
[7] Plot raw counts data
[8] Plot processed counts data
[9] Plot counts vs. rate constants''')
    decorating_bar('*')
    print('''[m] Show menu
[q] Quit''')
    decorating_bar('*')

paths_kinetics = []
paths_counts = []
measurements = []
data_to_process = MeasurementList(list())
menu = ('m', 'q', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10')
show_menu()
while True:
    try:
        action = input('Select option: ')
        assert action in menu
    except AssertionError:
        print('Incorrect input. Try Again!')
        decorating_bar('~', 'ERROR')
        continue

    if action == 'm':
        show_menu()

    elif action == 'q':
        decorating_bar('*', 'END')
        quit()

    elif action == '1':
        decorating_bar('-', 'Loading data')
        try:
            num = int(input('Number of measurements to load: '))
            assert num > 0
            are_counts = input('Load counts data? [y/n]: ')
            assert are_counts in ('y', 'n')
        except AssertionError:
            print('Incorrect input!')
            continue

        try:
            for i in range(num):
                print('Select KINETICS file - number ' + str(i + 1))
                path_1 = open_file('kin', 'Kinetics file #' + str(i + 1))
                assert path_1 != ''
                print('\tFile loaded successfully!')
                if are_counts == 'y':
                    print('Select COUNTS file - number ' + str(i + 1))
                    path_2 = open_file('cts', 'Counts file #' + str(i + 1))
                    assert path_2 != ''
                    print('\tFile loaded successfully!')
                    temp = create(path_1, path_2)
                    paths_counts.append(path_2)
                else:
                    temp = create(path_1)
                paths_kinetics.append(path_1)
                measurements.append(temp)
        except AssertionError:
            print('\tYou did not select any file, try again!')
            decorating_bar('~', 'ERROR')
            continue
        except ValueError:
            print('Fitting unsuccessful, change values range and try again!')
            decorating_bar('~', 'ERROR')
            continue
        data_to_process = MeasurementList(measurements)
        decorating_bar('-', 'Done')

    elif action == '2':
        decorating_bar('-', 'Loading full data')
        try:
            path = open_dir('Directory with full data')
            assert path != ''
            files = os.listdir(path)
        except (FileNotFoundError, AssertionError):
            print('Directory not selected')
            decorating_bar('~', 'ERROR')
            continue
        kin_files = []
        cts_files = []
        kinfit_files = []
        ctsfit_files = []
        for file in files:
            if file.endswith('.kin'):
                kin_files.append(file[:-4])
            elif file.endswith('.cts'):
                cts_files.append(file[:-4])
            elif file.endswith('.kinfit'):
                kinfit_files.append(file[:-7])
            elif file.endswith('.ctsfit'):
                ctsfit_files.append(file[:-7])
            else:
                print('There are other files!')
        if len(cts_files) == len(ctsfit_files) == 0:
            try:
                assert kin_files == kinfit_files
                for item in kin_files:
                    path_1 = os.path.join(path, item + '.kin')
                    measurements.append(create(path_1))
                    paths_kinetics.append(path_1)
            except AssertionError:
                print('Data not complete')
                decorating_bar('~', 'ERROR')
                continue
        else:
            try:
                assert cts_files == ctsfit_files
                for item in cts_files:
                    path_1 = os.path.join(path, item + '.kin')
                    path_2 = os.path.join(path, item + '.cts')
                    measurements.append(create(path_1, path_2))
                    paths_kinetics.append(path_1)
                    paths_counts.append(path_2)
            except AssertionError:
                print('Data not complete')
                decorating_bar('~', 'ERROR')
                continue
        data_to_process = MeasurementList(measurements)
        print('Data loaded successfully!')
        decorating_bar('-', 'Done')

    elif action == '3':
        decorating_bar('-', 'Selecting for processing')
        print('Loaded:')
        for index, item in enumerate(measurements):
            print('\t[' + str(index) + ']', item.label)
        data_to_process.print()
        user_input = input('Type space separated numbers (for all type \'a\'): ')
        try:
            if user_input == 'a':
                data_to_process = MeasurementList(measurements)
            else:
                indices = [int(i) for i in user_input.split()]
                data_to_process = MeasurementList([measurements[j] for j in indices])
            data_to_process.print()
        except ValueError:
            print('Incorrect input, try again!')
            continue
        print('Data selected!')
        decorating_bar('-', 'Done')

    elif action == '4':
        decorating_bar('-', 'Deleting data')
        print('Loaded:')
        for index, item in enumerate(measurements):
            print('\t[' + str(index) + ']', item.label)
        data_to_process.print()
        user_input = input('Type space separated numbers (for all type \'a\'): ')
        try:
            if user_input == 'a':
                measurements = []
                data_to_process = MeasurementList(measurements)
            else:
                indices = [int(i) for i in user_input.split()]
                measurements = [j for ind, j in enumerate(measurements) if ind not in indices]
                data_to_process = MeasurementList(measurements)
        except ValueError:
            print('Incorrect input, try again!')
            continue
        print('Data deleted!')
        decorating_bar('-', 'Done')

    elif action == '5':
        decorating_bar('-', 'Showing info')
        data_to_process.show_info()
        decorating_bar('-', 'Done')

    elif action == '6':
        decorating_bar('-', 'Plotting kinetics')
        print('''Select option:
    [1] plot with exponential decay
    [2] plot only experimental data
    [3] plot data and straight lines
    [4] plot \'-\' and \'--\'
    [5] plot with axis break''')
        try:
            option = int(input('Your choice: '))
            assert option in (1, 2, 3, 4, 5)
            data_to_process.plot_kinetics(option)
            print('Plotting successful')
            decorating_bar('-', 'Done')
        except:
            print('Wrong input, try again!')
            decorating_bar('~', 'ERROR')
            continue

    elif action == '7':
        decorating_bar('-', 'Plotting raw counts data')
        data_to_process.plot_counts_raw()
        print('Plotting successful')
        decorating_bar('-', 'Done')

    elif action == '8':
        decorating_bar('-', 'Plotting processed counts data')
        data_to_process.plot_counts_intervals()
        print('Plotting successful')
        decorating_bar('-', 'Done')

    elif action == '9':
        decorating_bar('-', 'Plotting counts vs. rate constants')
        print('''Select option:
    [1] plot without error bars
    [2] plot with error bars''')
        try:
            option = int(input('Your choice: '))
            assert option in (1, 2)
            data_to_process.plot_counts_rate_const(option)
            print('Plotting successful')
            decorating_bar('-', 'Done')
        except:
            print('Wrong input, try again!')
            decorating_bar('~', 'ERROR')
            continue
