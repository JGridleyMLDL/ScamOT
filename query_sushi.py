import requests
import json
import csv
import flatten_json

start_block = 10794352
end_block = 16869613


def make_query(skip_num):
    s = """
    {
        pairs(first:1000, skip:%s){
            name
            id
            token0{
                id
                symbol
                name
                decimals
            }
            token1{
                id
                symbol
                name
                decimals
            }
            totalSupply
            volumeUSD
            txCount
        }
    }""" % skip_num
    return s


def make_user_pos_query(skip, lower, upper):
    block = "block_gte: {0}, block_lt: {1}".format(lower, upper)
    query = """
    {
        liquidityPositionSnapshots(first: 1000, skip:%s, where:{%s} orderBy: block){
            id
            block
            timestamp
                liquidityTokenTotalSupply
            liquidityTokenBalance
            pair{
            id
            name
            token0{
                id
            }
            token1{
                id
            }
            }
            user{
            id
            }
            liquidityPosition{
            id
            }
        }
    }""" % (skip, block)

    return query


# URLs to send query requests to
SUSHI_URL_EXCHANGE = "https://api.thegraph.com/subgraphs/name/sushiswap/exchange"


# Send request
def make_request(url, query):
    '''
    Function to query TheGraph using requests, checks for failure
    before returning
    '''

    head = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    r = requests.post(url,
                      headers=head,
                      json={'query': query, 'variables': {}})

    if r.status_code != 200:
        raise Exception("Query Request failed with code " + str(r.status_code))

    return r.json()


# Saving the JSON Data
def save_data(json_data, outfile):
    '''
    Saves data to an file
    '''
    o = open(outfile, "w")

    json.dump(json_data, o, indent=4)

    o.close()
    print("JSON data written to {0}".format(outfile))


# Flattening the JSON and saving to CSV
def writeCSV(data, file, data_name, access, header=False):
    """Writes data from TheGraph query to csv file

    Args:
        data (dict): JSON File coming from the query result
        file (string): filename to write too
        data_name (string): nName of data you queried
        access (string or char): file access needed
        header (bool, optional): whether to write header in csv. Defaults to False.

    Returns:
        n: number of rows written
        max_time: current max timestamp in the csv
    """

    f = open(file, mode=access, newline='')

    csv_writer = csv.writer(f)

    n = 0
    for s in data["data"][data_name]:

        s = flatten_json.flatten(s, ".")

        if n == 0 and header == True:
            csv_writer.writerow(s)

        l = []                # This is slow -- optimize before pub
        for i in s.keys():
            l.append(s[i])
        csv_writer.writerow(l)

        n += 1

    f.close()
    #print("Wrote {0} rows to {1}".format(n, file))
    return n


def bulk_csv_data_request(write_file):
    """Organizes requests to TheGraph compiles results from multiple
    queries into one file.

    Args:
        total_num (int): estimate of number of records to record
        start_time (int): Unix time to start pulling txns from
        write_file (string): file to write csv results to.
    """
    print("(START)\t Starting Bulk Data Request.")

    block_lower = 10838352
    block_upper = block_lower + 500

    num_rows_read = 41908
    while block_lower < end_block:

        if num_rows_read == 0:
            write_header = True
            access = 'w'
        else:
            write_header = False
            access = 'a'

        try:
            query = make_user_pos_query(0, block_lower, block_upper)
            res = make_request(SUSHI_URL_EXCHANGE, query)
            n = writeCSV(res, write_file, "liquidityPositionSnapshots",
                         access, write_header)
            num_rows_read += n
        except:
            try:
                query = make_user_pos_query(0, block_lower, block_upper-400)
                res = make_request(SUSHI_URL_EXCHANGE, query)
                n = writeCSV(res, write_file, "liquidityPositionSnapshots",
                             access, write_header)
                num_rows_read += n
            except:
                print(res)
                print("(DATA LOSS): Missing Block on The Graph")

        print(
            "(UPDATE)\t Wrote {0} rows, ts: {1}".format(num_rows_read, block_lower))
        if n == 1000:
            print("(MAX QUERY ALERT)")

            i = 1
            while n == 1000:
                query = make_user_pos_query(i*1000, block_lower, block_upper)
                res = make_request(SUSHI_URL_EXCHANGE, query)
                try:
                    n = writeCSV(res, write_file, "liquidityPositionSnapshots",
                                 access, write_header)
                    num_rows_read += n
                except:
                    print(res)
                    print("(DATA LOSS): Missing Block on The Graph")
                i += 1

        # if n == 0:
        #    break

        block_lower = block_upper
        block_upper = block_lower + 500


if __name__ == "__main__":
    bulk_csv_data_request("sushi_liquidity_position_snapshots.csv")
