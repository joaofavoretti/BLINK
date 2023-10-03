import warc

FILENAME = 'urls.warc.wet'

# Open a WARC file
with warc.open(FILENAME) as f:
    # Iterate over the records in the WARC file
    for record in f:
        # Print the type of the record
        print(record.type)
        # Print the URL of the record (if available)
        if 'WARC-Target-URI' in record:
            print(record['WARC-Target-URI'])
        # Print the content of the record (if available)
        if 'content' in record:
            print(record.content[0:100])

        