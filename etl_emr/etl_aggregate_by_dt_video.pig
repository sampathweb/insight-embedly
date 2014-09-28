-- Join Customer and Cases to get case count by customer

SET job.name 'aggregate_by_date_video';

events = LOAD 's3://insight-ramesh/embedly-etl-emr-out/emr2/' USING PigStorage('\t')
            AS (ev_date:chararray,
                client_key:chararray,
                client_ip:chararray,
                uid:chararray,
                sid:chararray,
                content_type:chararray,
                client_host:chararray,
                client_url:chararray,
                content_host:chararray,
                content_url:chararray,
                os:chararray,
                browser:chararray,
                row_count:int,
                activity:chararray,
                act_count:int,
                act_length:int);


video_grouped = GROUP events BY (ev_date, content_host, content_url, activity);

data_out = FOREACH video_grouped GENERATE FLATTEN(group), COUNT(events.row_count), COUNT(events.act_count), MEDIAN(events.act_length);

store data_out into 's3://insight-ramesh/embedly-etl-emr-out/pig2/' using PigStorage('\t');
