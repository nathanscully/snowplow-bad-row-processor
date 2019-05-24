# snowplow-bad-row-processor
Simple framework to download and process bad snowplow rows locally.

Rather than trying to spin up external services and EMR, this script targets a 'bad' snowplow bucket on S3, downloads files based on a filter path and processes them to clean them up before storing them locally.

Once processed, they can be uploaded to a given s3 bucket and the Snowplow team can


# Installation:

## Build the docker image

    docker build -t nathanscully/badrows .

## Create an .env file

Create a _.env_ file in the root directory based on the sample. It should contain the AWS S3 access details.

## Determine your error dates

You need to identify the filter to use for the bad rows. The best way to do this is via Kibana and the 'bad' index. Once you have a range of dates, write a regex filter to use. E.g. pass in _2019-05-1[0-9]_ to process all data between 2019-05-10 and 2019-05-19.

## Determine your error

You need to determine a string flag that can be used to identify the error. Once again use Kibana and look for the error  message such as

    errors":[{"level":"error","message":"error: instance type (integer) does not match any allowed primitive type (allowed: [\"string\"])\n    level: \"error\"\n    schema: {\"loadingURI\":\"#\",\"pointer\":\"/properties/notification_id\"}\n    instance: {\"pointer\":\"/notification_id\"}\n    domain: \"validation\"\n    keyword: \"type\"\n    found: \"integer\"\n    expected: [\"string\"]\n"}]


We can simplify this to:

    {"pointer":"/notification_id"}

## Update the error fixing function

In _app/process.py_ there is a method definition called *parse_event*.

This needs to be updated in the _CHANGE ME_ block to fix the issue that causing the error. I,e for the notification_id being set to the wrong type, we can recast it like this:

    if 'notification_id' in cx_event:
        cx_event['notification_id'] = str(cx_event['notification_id'])
        cx[i] = cx_event

Note that the reason we need to use _cx[i]_ is multiple events can be in a single encoded context.


## Run the image

    docker run -it -v "$PWD":/app --env-file  .env nathanscully/badrows app/run.py --bucket snowplow-au-com-oneflare-enrichment-output --filter '2019-05-1[0-9]' --error '{"pointer":"/notification_id"}'

This will download all the files and generate a new output folder of the files that need to be uploaded to S3.

You can also use the flag `--no-dl` to skip the download part if you have issues processing but have already succesfully downloaded the data.
