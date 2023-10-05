import warc

FILENAME = 'files/CC-MAIN-20230610164417-20230610194417-00798.warc'

count = 0

# Open a WARC file
with warc.open(FILENAME) as f:
    # Iterate over the records in the WARC file
    for record in f:
        print(f'Current count: {count}', end='                                   \r')
        # Print the type of the record
        # print(record.type)
        # Print the URL of the record (if available)
        if 'WARC-Target-URI' in record:
            count += 1
            # print(record['WARC-Target-URI'])
        # Print the content of the record (if available)
        # if 'content' in record:
        #     print(record.content[0:100])

print(f'Were found {count} records')
