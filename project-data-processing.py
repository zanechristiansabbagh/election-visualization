import json

START_YEAR = 1892
END_YEAR = 2020
N_YEARS = int((END_YEAR - START_YEAR) / 4 + 1)
ELECTORAL_LENGTH = 4
CENSUS_START_YEAR = 1890
CENSUS_END_YEAR = 2020
NUM_OF_CENSUSES = int((CENSUS_END_YEAR - CENSUS_START_YEAR) / 10 + 1)
CENSUS_LENGTH = 10


def main():

    print("saving data...")
    data = {}

    # finds closest census year to each election
    # adds state population estimate at election year to data
    census_year_to_elec_year(data, 'uspop.csv')

    # adds electoral votes and party nomination for each state to data
    add_data(data, 'uselec.csv')
    add_data(data, 'usparty.csv')
    json.dump(data, open('b.json', 'w'), indent=2)

    # adds victorious president and vice president in each election year
    pres_data = {}
    add_pres_data(pres_data, 'uspres.csv')
    json.dump(pres_data, open('c.json', 'w'), indent=2)

    # adds information about each election
    info_data = {}
    add_elec_info(info_data, 'useinfo.csv')
    json.dump(info_data, open('d.json', 'w'), indent=2)


def add_pres_data(pres_data, filename):
    for line in open(filename):
        line = line.strip()
        parts = line.split(',')
        year = int(parts[0])
        president = parts[1]
        vice = parts[2]
        pres_data[year] = {}
        pres_data[year]['pres'] = president
        pres_data[year]['vice'] = vice

def add_elec_info(info_data, filename):

    for line in open(filename):
        line = line.strip()
        parts = line.split(' ')
        words = parts[1:]
        info_data[parts[0]] = words

def census_year_to_elec_year(data, filename):

    key = str(filename.split('.')[0])

    for line in open(filename):
        line = line.strip()
        parts = line.split(',')
        state_name = parts[0]

        for i in range(N_YEARS):
            year = START_YEAR + ELECTORAL_LENGTH * i
            dif = 1000
            target_index = None

            for i in range(NUM_OF_CENSUSES):
                census_year = CENSUS_START_YEAR + CENSUS_LENGTH * i
                if abs(census_year - year) < dif:
                    dif = abs(census_year - year)
                    target_index = i + 1

            next_value = parts[target_index]

            if year not in data:
                data[year] = {}

            if state_name not in data[year]:
                year_data = data[year]
                year_data[state_name] = {}

            year_data[state_name][key] = next_value


def add_data(data, file_name):

    key = str(file_name.split('.')[0])

    for line in open(file_name):
        line = line.strip()

        parts = line.split(',')

        state_name = parts[0]

        for i in range(N_YEARS):

            next_value = parts[i + 1]
            year = START_YEAR + 4 * i
            data[year][state_name][key] = next_value


if __name__ == '__main__':
    main()
