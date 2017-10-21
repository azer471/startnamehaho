from celery.task import task

from dynamic_scraper.utils.task_utils import TaskUtils
from posts.models import NewsWebsite, Article



@task()
def run_spiders():
    print ("funciona cada x minutod")
    t = TaskUtils()
    t.run_spiders(NewsWebsite, 'scraper', 'scraper_runtime', 'article_spider')
    
@task()
def run_checkers():
    t = TaskUtils()
    t.run_checkers(Article, 'news_website__scraper', 'checker_runtime', 'article_checker')

