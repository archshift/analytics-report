import os
import csv
import io
import sys

import googleanalytics as ga

import Referrers

filter_social = 'ga:channelGrouping==Social'
filter_organic = 'ga:channelGrouping==Organic Search'
filter_direct = 'ga:channelGrouping==Direct'
filter_referral = 'ga:channelGrouping==Referral'

csv_data = ["Descriptor1,Descriptor2,Sessions,% New Sessions,Bounce Rate,Pageviews/Session,Avg. Session Duration"]
def add_to_csv(name, rows):
    global csv_data
    for row in rows:
        row_str = name + ","
        for item in row:
            row_str += str(item) + ","
        csv_data.append(row_str)


def output_csv():
    global csv_data
    output_data = io.StringIO()
    data = list(csv.reader(csv_data, delimiter=',', quotechar='"'))
    writer = csv.writer(output_data, delimiter=',', quotechar='"')

    for row in data[1:]:
        for i in range(0, len(row)):
            if 3 <= i <= 6:
                # For columns 3-6, truncate to 2 decimals
                row[i] = "%.2f" % float(row[i])
            if 3 <= i <= 4:
                # For columns 3-4, add '%' to the values
                row[i] += "%"

    writer.writerows(data)
    print(output_data.getvalue())


def make_query(profile, limit=0, dimensions=None, filters=None):
    query = profile.core.query
    query = query.range(sys.argv[5], sys.argv[6])
    query = query.metrics('sessions', 'percentNewSessions', 'bounceRate', 'pageviewsPerSession', 'avgSessionDuration')
    query = query.sort('sessions', descending=True)
    if limit != 0:
        query = query.limit(limit)
    if dimensions is not None:
        for dimension in dimensions:
            query = query.dimensions(dimension)
    if query is not None:
        query = query.set({'filters': filters})

    return query


# Adds device category data rows to the CSV
# @param filter_fmt Filter string, where row[0] replaces the first format token
def add_device_data(profile, name, query_rows, filter_fmt=""):
    for row in query_rows:
        if filter_fmt != "":
            device_query_rows = make_query(profile, dimensions=['deviceCategory'], filters=filter_fmt % row[0]).rows
        else:
            device_query_rows = make_query(profile, dimensions=['deviceCategory']).rows
        add_to_csv("%s - %s" % (name, row[0]), device_query_rows)


def add_channel_grouping_data(profile, name, filter):
    page_query_rows = make_query(profile, limit=3, dimensions=['landingPagePath'], filters=filter).rows
    add_to_csv(name + " - Pages", page_query_rows)
    add_device_data(profile, name + " - Pages", page_query_rows, filter_fmt="ga:pagePath==%s;" + filter)

    if name == "Social":
        source_dimension = "socialNetwork"
    else:
        source_dimension = "source"
    source_query_rows = make_query(profile, limit=3, dimensions=[source_dimension], filters=filter).rows
    add_to_csv(name + " - Sources", source_query_rows)
    add_device_data(profile, name + " - Sources", source_query_rows, "ga:%s==%%s;%s" % (source_dimension, filter))


def main():
    global csv_data

    if len(sys.argv) < 7:
        print("Analytics.py <identity> <account> <webproperty> <profile> <start date> <end date>")

    profile = ga.authenticate(
        identity=sys.argv[1], save=True, interactive=True,
        client_id=os.environ['GOOGLE_ANALYTICS_CLIENT_ID'],
        client_secret=os.environ['GOOGLE_ANALYTICS_CLIENT_SECRET'],
        account=sys.argv[2], webproperty=sys.argv[3], profile=sys.argv[4]
    )

    bad_referrers = Referrers.make_bad_referrer_filter(profile)

    total_overall_query_rows = make_query(profile, filters=bad_referrers).rows
    add_to_csv("Total Overall,Overall", total_overall_query_rows)
    device_query_rows = make_query(profile, dimensions=['deviceCategory'], filters=bad_referrers).rows
    add_to_csv("Total Overall", device_query_rows)

    grouping_overall_query_rows = make_query(profile, dimensions=['channelGrouping'], filters=bad_referrers).rows
    add_to_csv("Grouping Overall", grouping_overall_query_rows)
    add_device_data(profile, "Grouping Overall", grouping_overall_query_rows, "ga:channelGrouping==%s;" + bad_referrers)

    add_channel_grouping_data(profile, "Social", filter_social)
    add_channel_grouping_data(profile, "Organic", filter_organic)
    add_channel_grouping_data(profile, "Direct", filter_direct)
    add_channel_grouping_data(profile, "Referral", "%s;%s" % (bad_referrers, filter_referral))

    output_csv()


if __name__ == "__main__":
    main()