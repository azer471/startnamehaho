from __future__ import unicode_literals
# Scrapy settings for posts project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

import os, sys

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "example_project.settings")
sys.path.insert(0, os.path.join(PROJECT_ROOT, "../../..")) #only for example_project


BOT_NAME = 'posts'

LOG_STDOUT = True

SPIDER_MODULES = ['dynamic_scraper.spiders', 'posts.scraper',]
USER_AGENT = '{b}/{v}'.format(b=BOT_NAME, v='1.0')

ITEM_PIPELINES = {
    'dynamic_scraper.pipelines.DjangoImagesPipeline': 200,
    'dynamic_scraper.pipelines.ValidationPipeline': 400,
    'posts.scraper.pipelines.DjangoWriterPipeline': 800,
}

