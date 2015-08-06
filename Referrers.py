import os
import sys

import googleanalytics as ga

import Analytics
import ReferrerBlacklist


def get_referrers(profile):
    query = profile.core.query
    query = query.range(sys.argv[5], sys.argv[6])
    query = query.metrics('sessions')
    query = query.set({'dimensions': ['ga:source']})
    query = query.set({'filters': Analytics.filter_referral})

    return query.rows


def make_bad_referrer_filter(profile):
    match_list = ReferrerBlacklist.referrer_blacklist.splitlines()
    ref_filter = ""
    for row in get_referrers(profile):
        source = row[0]
        for match in match_list:
            if source.lower().find(match) != -1:
                ref_filter += "ga:source!@%s;" % source
    return ref_filter[:-1]


def get_cleared_referrers(profile):
    query = profile.core.query
    query = query.range(sys.argv[5], sys.argv[6])
    query = query.metrics('sessions')
    query = query.set({'dimensions': ['ga:source']})
    query = query.set({'filters': '%s;%s' % (make_bad_referrer_filter(profile), Analytics.filter_referral)})

    return query.rows


def main():
    if len(sys.argv) < 7:
        print("Referrers.py <identity> <account> <webproperty> <profile> <start date> <end date>")

    profile = ga.authenticate(
        identity=sys.argv[1], save=True, interactive=True,
        client_id=os.environ['GOOGLE_ANALYTICS_CLIENT_ID'],
        client_secret=os.environ['GOOGLE_ANALYTICS_CLIENT_SECRET'],
        account=sys.argv[2], webproperty=sys.argv[3], profile=sys.argv[4]
    )

    referrers = get_cleared_referrers(profile)
    for row in referrers:
        print(row[0])


if __name__ == "__main__":
    main()