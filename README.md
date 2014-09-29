# Powering Recommendations @ embed.ly
Developed by Ramesh Sampath


I built a data pipeline for embed.ly that converts log files coming from user activity at popular websites into a queryable data store in Redshift.

Embed.ly provides a service that enables popular websites and to understand what content is more engaging in for users.  Embed.ly helps its clients know part of an video users like the most.

By sitting between users and popular websites, Embedly collects a lot of data that can be analyzed to provide greater value to its clients.  Embedly wants to build a data pipeline that a data scientist can build recommendation models from.  This project is an attempt to make this possible.  I am reviewing this with Embedly's engineering team to integrate it with their system.

I worked on this project along with Zach, a data science fellow @ Insight, who built the recommendation model.

## Data Pipeline

![Alt Text](https://github.com/sampathweb/insight-embedly/blob/master/images/datapipeline.png "Data Pipeline")

## ETL Process

* Embed.ly creates log files at a rate of 2GB / 30 minutes

* A cron job would upload these files into S3 bucket

* AWS Elastic MapReduce process takes these json events and extracts the fields we need for building the recommendation model.  The results of the EMR job is put in another S3 bucket

* AWS data pipeline process loads these processed files from S3 and loads them into RedShift data warehouse.

## User interface

![alt tag](https://github.com/sampathweb/insight-embedly/blob/master/images/web-ui.png "Data Dashboard")

![alt tag](https://github.com/sampathweb/insight-embedly/blob/master/images/ipy-ui.png "Interactive Analysis")


## Credits

* John Emhoff, Engineering Team @ Embed.ly(https://embed.ly) for helping us understand the data challenges faced by embedly and how we can help

* Zach Gazak, Insight Data Science Fellow, for the various whiteboard sessions to understand what features we need for the recommendation model

* Insight Data Engineering Program for making this possible in four weeks

More details at [SlideShare](http://www.slideshare.net/slideshow/embed_code/39669785)