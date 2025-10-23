import pandas
import DBsqlstatements

def scrub_FranklinOhio_addresses(filepath):
    franklin_df = pandas.read_csv(filepath)

    data_toadd = []
    chunk_size = 1000
    count = 0
    for row in franklin_df.itertuples(index=True, name='row'):
        STHNUM = str(row.STHNUM)
        STADDR = str(row.STADDR)
        USPS_CITY = str(row.USPS_CITY)
        ZIPCODE = str(row.ZIPCODE)
        DESCR1 = str(row.DESCR1)
        NAME1 = str(row.NAME1)

        if row.Index >= 483999:
            data_toadd.append((STHNUM, STADDR, USPS_CITY, ZIPCODE, DESCR1, NAME1))
    DBsqlstatements.insert_data(data_toadd)

        # if len(data_toadd) >= chunk_size:
        #     data_toadd = []
        #     count += 1
        #     print(count)

    return