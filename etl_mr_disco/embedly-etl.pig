-- Join Customer and Cases to get case count by customer

events = LOAD 's3://insight-ramesh-s3/embedly-events/'
        USING JsonLoader();

DESCRIBE events;

store events into 's3://insight-ramesh-s3/embedly-out' using JsonStorage();
