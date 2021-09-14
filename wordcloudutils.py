#!/usr/bin/env python
# encoding: utf-8

# Copyright (c) 2021 Grant Hadlich
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE. 
import numpy as np
import json
import re
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib as mpl
mpl.use('Agg')

import matplotlib.pyplot as plt

def read_tweets(filename):
    # Reads in Tweets from a JSON File
    data = None
    with open(filename) as json_file:
        data = json.load(json_file)

    return data

def get_text_from_tweets(filename):
    # Reads in Tweets from a JSON File
    data = read_tweets(filename)
    
    data = ["{0}".format(tweet["text"]) for tweet in data]

    string = " ".join(data)

    string = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                    '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', string)

    for i in range(int(len(data) / 100)):
        string += "Copyright_Grant_Hadlich_2021 the "

    string = string.replace("&amp;", "")

    string = string.replace(u'\u2019', "'")
    string = string.replace("\\'", "'")
    string = string.replace("“", "")
    string = string.replace("”", "")

    return string

def transform_format(val):
    if val[0] == 0:
        return 255
    else:
        return val[0]

def create_image_from_file(file_path, img_path, word_cloud_path, date, width=15, height=9, max_words=300):

    text = get_text_from_tweets(file_path)

    create_image(text, img_path, word_cloud_path, date, width=width, height=height, max_words=1000)


def create_image(tweets, img_path, word_cloud_path, date, width=15, height=9, max_words=1000):
    mask = np.array(Image.open(img_path))

    # Transform mask
    transformed_mask = np.ndarray((mask.shape[0],mask.shape[1]), np.int32)

    for i in range(len(mask)):
        transformed_mask[i] = list(map(transform_format, mask[i]))

    stopwords = set(STOPWORDS)
    stopwords.update(["amp", "amps", "m", "city", "u", "will", "s", "one", "lt", "gt", "fuck"])
    wordcloud = WordCloud(width=1125, height=625, max_words=max_words, stopwords=stopwords, normalize_plurals=False, background_color="white", mask=mask, contour_width=1, contour_color='black').generate(tweets)
    plt.figure(figsize=(width, height), dpi=400)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    #plt.title(f"© Grant Hadlich - {date}", loc='center')
    plt.tight_layout()
    plt.savefig(word_cloud_path)
