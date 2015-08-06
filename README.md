# Analytics Report

### Instructions for use

#### Dependencies:

- `python3`
- `googleanalytics`

On Mac, install these dependencies using [homebrew](http://brew.sh/). Follow the directions on their website for
installing homebrew. Then, install `python3` using homebrew with `brew install python3`.
On Windows, install `python3` from the [python website](https://www.python.org/) Follow the directions on their website
for installing python.

Open up a command-line window. You will use pip to install the `googleanalytics` dependency:
```
pip3 install googleanalytics
```

#### Usage:

First, set up analytics. To do so, follow steps 1-3 of [the instructions, provided here]
(https://github.com/debrouwere/google-analytics/wiki/Authentication).

Use python3 to run the script:
```
python3 path/to/Analytics.py <identity> "<account>" "<webproperty>" "<profile>" <start date> <end date>
```

Identity is the same identity you used when setting up googleanalytics.
See below for indications about the account, webproperty, and profile (make sure to put quotes around them!).
The start and end date should be in the format `mm/dd/yy`.
![Analytics information](http://i.imgur.com/Rm5UVNu.png)

#### Bad Referrers:
Use python3 to run the script:
```
python3 path/to/Referrers.py <identity> "<account>" "<webproperty>" "<profile>" <start date> <end date>
```

This will output all the referrers that have cleared the referrer blacklist. If you spot a referrer here that does not
belong, add it to `ReferrerBlacklist.py`.


#### Making a CSV file:

You can either copy the output of Analytics.py into a text file and save it with the extension CSV, or you can redirect
the script's output to a file:
```
python3 Analytics.py <args> > output.csv
```

Note that it's the `> output.csv` which you need to be able to redirect the output to a file. The resulting file will
open with any spreadsheet editor and be formatted correctly.