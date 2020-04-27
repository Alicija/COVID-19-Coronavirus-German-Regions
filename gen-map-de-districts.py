# Based on
# https://raw.githubusercontent.com/ythlev/covid-19/master/run.py
# by Chang Chia-huan

import os
import glob
# import argparse
# import pathlib
import json
# import csv
# import io
# import urllib.request
# import urllib.parse
import math
import statistics
# import datetime
import re

# my helper modules
import helper

unit = 1000000

# https://www.w3schools.com/colors/colors_picker.asp
d_color_scales = {
    'template': [
        "#fee5d9", "#fcbba1", "#fc9272", "#fb6a4a", "#de2d26", "#a50f15"
    ],
    'blue': [
        '#e6e6ff',
        '#b3b3ff',
        '#8080ff',
        '#4d4dff',
        '#1a1aff',
        '#0000e6'
    ],
    'red':
    [
        '#ffe6e6',
        '#ffb3b3',
        '#ff8080',
        '#ff4d4d',
        '#ff1a1a',
        '#cc0000'
    ]
}

d_all_date_data = {}
# TODO: Typo in filename -> district
for f in glob.glob('data/de-districts/de-distict_timeseries-*.json'):
    lk_id = int(re.search('^.*de-distict_timeseries\-(\d+)\.json$', f).group(1))
    l = helper.read_json_file(f)
    for d in l:
        date = d['Date']
        if date[0:7] == '2020-01' or date[0:7] == '2020-02':
            continue
        if not d['Date'] in d_all_date_data:
            d_all_date_data[d['Date']] = {}
        del d['Timestamp'], d['Date'], d['Days_Past'], d['Days_Since_2nd_Death'], d['Cases_Change_Factor'], d['Deaths_Change_Factor']
        d_all_date_data[date][lk_id] = d
del f, d, l

# check if last date has as many values as the 2nd last, of not drop it
dates = sorted(d_all_date_data.keys())
if len(d_all_date_data[dates[-1]]) != len(d_all_date_data[dates[-2]]):
    print("WARNIGN: last date is incomplete, so removing it")
    del d_all_date_data[dates[-1]]
del dates


# property_to_plot = 'Deaths_Last_Week_Per_Million'
l_subprocesses = []
for property_to_plot in ('Cases_Last_Week_Per_Million', 'Deaths_Last_Week_Per_Million'):

    if property_to_plot == 'Cases_Last_Week_Per_Million':
        meta = {"colour": d_color_scales['blue']}
    elif property_to_plot == 'Deaths_Last_Week_Per_Million':
        meta = {"colour": d_color_scales['red']}

    values = []
    # collect all values for autoscaling
    for date_str, l_districts in d_all_date_data.items():
        for lk_id, d in l_districts.items():
            values.append(d[property_to_plot])
    del d, l_districts, lk_id

    # generate color scale range
    q = statistics.quantiles(values, n=100, method="inclusive")
    step = math.sqrt(statistics.mean(values) - q[0]) / 3
    threshold = [0, 0, 0, 0, 0, 0]
    for i in range(1, 6):
        threshold[i] = math.pow(i * step, 2) + q[0]
    del q, step, i

    with open('maps/template_de-districts.svg', mode="r", newline="", encoding="utf-8") as file_in:
        # plot loop for each date
        # date_str = '2020-04-24'
        # l_districts = d_all_date_data[date_str]
        for date_str, l_districts in d_all_date_data.items():
            file_in.seek(0, 0)  # reset file pointer
            main = {}
            for lk_id, d in l_districts.items():
                area = lk_id
                pcapita = d[property_to_plot]
                main[area] = {'pcapita': pcapita}

            with open(f'maps/out/de-districts/{property_to_plot}-{date_str}.svg', mode="w", newline="", encoding="utf-8") as file_out:
                if threshold[5] >= 10000:
                    num = "{:_.0f}"
                elif threshold[1] >= 10:
                    num = "{:.0f}"
                else:
                    num = "{:.2f}"

                for row in file_in:
                    written = False
                    for area in main:
                        if row.find('id="{}"'.format(area)) > -1:
                            i = 0
                            while i < 5:
                                if main[area]["pcapita"] >= threshold[i + 1]:
                                    i += 1
                                else:
                                    break
                            file_out.write(row.replace('id="{}"'.format(
                                area), 'style="fill:{}"'.format(meta["colour"][i])))
                            written = True
                            break
                    if written == False:
                        if row.find('>Date') > -1:
                            file_out.write(row.replace(
                                'Date', date_str))
                        elif row.find('>level') > -1:
                            for i in range(6):
                                if row.find('level{}'.format(i)) > -1:
                                    if i == 0:
                                        file_out.write(row.replace('level{}'.format(
                                            i), "&lt; " + num.format(threshold[1]).replace("_", "&#8201;")))
                                    else:
                                        file_out.write(row.replace('level{}'.format(
                                            i), "≥ " + num.format(threshold[i]).replace("_", "&#8201;")))
                        elif row.find('<path fill="#') > -1:
                            s = row
                            for i in range(6):
                                s = s.replace(
                                    d_color_scales["template"][i], meta["colour"][i])
                            file_out.write(s)
                        # elif row.find('!!!TYPE!!!') > -1:
                        #     if property_to_plot == 'Cases_Last_Week_Per_Million':
                        #         file_out.write(row.replace(
                        #             '!!!TYPE!!!', 'Infizierte'))
                        #     elif property_to_plot == 'Deaths_Last_Week_Per_Million':
                        #         file_out.write(row.replace(
                        #             '!!!TYPE!!!', 'Verstorbene'))
                        else:
                            file_out.write(row)
        # break

    # generate .gif out of .svgs
    # from https://janakiev.com/blog/python-shell-commands/
    import subprocess

    process = subprocess.Popen(['magick', 'convert', '-delay', '150x1000', '-size', '480x', f'maps/out/de-districts/{property_to_plot}-*.svg', '-coalesce', '-fuzz', '2%', '+dither', '-resize', '480x', '-layers', 'Optimize', f'maps/de-districts-{property_to_plot}.gif'],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               universal_newlines=True)
    l_subprocesses.append(process)

# wait for subprocesses to finish
i = 1
for process in l_subprocesses:
    stdout, stderr = process.communicate()
    print(f'{i}:\t{stdout}\t{stderr}')
    i += 1

# cleanup
for f in glob.glob('maps/out/de-districts/*.svg'):
    os.remove(f)