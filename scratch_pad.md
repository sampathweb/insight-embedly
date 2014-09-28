EPOH to Time:  datetime.datetime.fromtimestamp(1411597799, pytz.utc).strftime('%Y-%m-%d %H:%M')

Time to Epoh: (datetime.datetime(2012,04,01,0,0) - datetime.datetime(1970,1,1)).total_seconds()

'2014-09-24 22:00' - 1411596000
1411597799 '2014-09-24 22:29'
1411597800-1411599599 '2014-09-24 22:30' - '2014-09-24 22:59'


for dt_start in ['2014-09-20', '2014-09-21', '2014-09-22', '2014-09-23', '2014-09-24', '2014-09-25', '2014-09-26']:
    yr, mon, day = dt_start.split('-')
    yr = int(yr)
    mon = int(mon)
    day = int(day)
    for time_start in ['22:00', '22:30']:
        hr, min = time_start.split(':')
        hr = int(hr)
        min = int(min)
        epoh_start = int((datetime.datetime(yr, mon, day, hr, min) - datetime.datetime(1970,1,1)).total_seconds())
        epoh_end = epoh_start + 1799
        print 'events:time:' + str(epoh_start) + '-' + str(epoh_end)

In [34]: for dt_start in ['2014-09-20', '2014-09-21', '2014-09-22', '2014-09-23', '2014-09-24', '2014-09-25', '2014-09-26']:
   ....:         yr, mon, day = dt_start.split('-')
   ....:         yr = int(yr)
   ....:         mon = int(mon)
   ....:         day = int(day)
   ....:         for time_start in ['22:00', '22:30']:
   ....:                 hr, min = time_start.split(':')
   ....:                 hr = int(hr)
   ....:                 min = int(min)
   ....:                 epoh_start = int((datetime.datetime(yr, mon, day, hr, min) - datetime.datetime(1970,1,1)).total_seconds())
   ....:                 epoh_end = epoh_start + 1799
   ....:                 print 'events:time:' + str(epoh_start) + '-' + str(epoh_end)
   ....:
events:time:1411250400-1411252199
events:time:1411252200-1411253999
events:time:1411336800-1411338599
events:time:1411338600-1411340399
events:time:1411423200-1411424999
events:time:1411425000-1411426799
events:time:1411509600-1411511399
events:time:1411511400-1411513199
events:time:1411596000-1411597799
events:time:1411597800-1411599599
events:time:1411682400-1411684199
events:time:1411684200-1411685999
events:time:1411768800-1411770599
events:time:1411770600-1411772399
