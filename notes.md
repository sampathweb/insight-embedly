## Only for [‘query’][’a’] == video
##


CLIENT-“clientKey”***
VIDEO_URL-“query””u”
REFERRER=“headers””referrer”
UID-“query””uid”
EVENT-“query””a”
PROCESS_Start** PROCESS_End**
TIMESTAMP-“timestamp”*
IP-“clientIp”


* use [“timestamp”] NOT [“query”][“timestamp”]
** process_start / process_end:
 this key isn’t always around… only for “query””a”==“progress”, so it can be None or whatever if not present
 sometimes the key is “5-15” so PROCESS_start,PROCESS_end = 5,15
 sometimes the key is more complicated, like “5-9,20-25,32-37”  That case should make 3 entries into the database that are duplicated except for Process_start, Process_end

*** I guess if we are splitting these up by client key, that isn’t a necessary column.

I’m not sure how much data we should acquire per client, but it does seem like 2 hours of reddit is plenty.  Maybe we could aim for ~ that level for other clients too, but also set some maximum historical date, so drop results that are older than X months or something like that, and only fill the database with the newest Y videos with enough user interaction to model.  These are things we can think about over the next couple of days.

```
{
    "access_class": "shortening",
    "endpoint": "event",
    "timestamp": 1409923800, // UNIX timestamp
    "user-eid": "kHGiNdoyXfKe0uqT0k2C55A618ki5iQ67MiTjYQeFAVfLuykAAKGPndJjtLCL1",
    "headers": {
        "referrer": "http://cdn.embedly.com/widgets/media.html?src=http%3A%2F%2Fwww.youtube.com%2Fembed%2FB70Msi7vrmE%3Ffeature%3Doembed&url=http%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DB70Msi7vrmE&image=http%3A%2F%2Fi.ytimg.com%2Fvi%2FB70Msi7vrmE%2Fhqdefault.jpg&key=2aa3c4d5f3de4f5b9120b660ad850dc9&type=text%2Fhtml&schema=youtube",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:32.0) Gecko/20100101 Firefox/32.0"
    },
    "endpointVersion": 1,
    "eid_generated": true,
    "query": {
        "a": "progress", // Action the user took: play, load, hover or progress (an update on the viewing session of a piece of media)
        "l": "5-15", // only present for progress events; indicates a timerange of the media that was just observed
        "c": "video",
        "uid": "c4ea807adb334ae2908407731703eb29", // ID uniquely identifying a user
        "g": "media", // analytics group, generally "media" or "card" (i.e., embed via API or Embedly Cards)
        "s": "youtube",
        "r": "http://www.redditmedia.com/mediaembed/2fjpkw", // URL the embed was presented on
        "u": "http://www.youtube.com/watch?v=B70Msi7vrmE", // the URL that was embedded
        "t": "1409923800717", // ignore this timestamp, it's client-generated. Use the one above.
        "key": "2aa3c4d5f3de4f5b9120b660ad850dc9",
        "sid": "09cc8b6d05df40c0a488f0f64773a48b"
    },
    "clientIp": "174.115.103.139",
    "clientKey": "522bb206bd3911e08d854040d3dc5c07", // unique ID for the client, present only on "media" group
    "statusCode": 200
}
```