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
from wordcloudutils import create_image_from_file
from datetime import datetime
from twitterutils.twitterutils import recent_search_query
from twitterutils.twitterutils import tweet
import json
import re

if __name__ == "__main__":
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")

    tweets = "./seattle/raw_tweets/seattle_" + str(date) + ".txt"
    mask = "./seattle/mask.png"
    output_file = "./seattle/raw_tweets/seattle_" + str(date) + ".png"

    # Choose number of tweets
    number_of_tweets = 20000

    # Pull latest 1000 tweets about the entity Seattle	
    print("Pulling Tweets")
    recent_search_query(f"-is:retweet lang:en Seattle", 
                        output_file=tweets,
                        max_results = number_of_tweets,
                        max_raw_tweets = number_of_tweets)

    # Create the word cloud, with vertical aspect ratio
    print("Creating Word Cloud")
    create_image_from_file(tweets, mask, output_file, date, height=15, width=9, max_words=1000)

    # Tweet it out
    print("Creating Tweet")
    text = f"I pulled ~{number_of_tweets} tweets that mention #Seattle and created a #wordcloud of what people are saying about the #EmeraldCity!"
    id = tweet(text, image_path=output_file)