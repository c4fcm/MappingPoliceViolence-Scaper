import logging, unicodecsv, time, os, json, sys

from mpv import basedir, db

# set up logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.info("---------------------------------------------------------------------------")
start_time = time.time()

timestr = time.strftime("%Y%m%d_%H%M%S")
filename = 'mpv_story_data_{0}.csv'.format(timestr)
filepath = os.path.join(basedir, "data", filename)
log.info('Writing data to %s' % filename)

outfile = open(filepath, 'wb')
fieldnames = ['full_name', 'first_name', 'last_name', 'sex', 'date_of_death', 'age', 'city', 
                'state', 'cause', 'story_date', 'bitly_clicks', 'population', 'story_id', 'url', 
                'facebook', 'facebook_comments', 'facebook_likes', 'facebook_shares', 'twitter', 
                'resolved_url' ]
outcsv = unicodecsv.DictWriter(outfile, fieldnames = fieldnames, 
    extrasaction='ignore', encoding='utf-8')
outcsv.writeheader()

log.info("Found %d stories" % db.storyCount())

idx = 0
for story in db._db.stories.find().sort( [['_id', -1]] ):
    if (idx % 1000) == 0:
        log.info("  at story %d" % idx)
    if 'social_shares' in story:
        if 'facebook' in story['social_shares']:
            story['facebook'] = story['social_shares']['facebook']
        if 'facebookfql' in story['social_shares']:
            story['facebook_comments'] = story['social_shares']['facebookfql']['comments']
            story['facebook_likes'] = story['social_shares']['facebookfql']['likes']
            story['facebook_shares'] = story['social_shares']['facebookfql']['shares']
        if 'twitter' in story['social_shares']:
            story['twitter'] = story['social_shares']['twitter']
    outcsv.writerow(story)
    outfile.flush()
    idx = idx+1

outfile.close()
duration_secs = float(time.time() - start_time)
log.info("Finished!")
log.info("  took %d seconds total" % duration_secs)
