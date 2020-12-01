from scrapyd_api import ScrapydAPI

scrapyd = ScrapydAPI('http://127.0.0.1:6800')

jobs_dict = scrapyd.list_jobs('default')
jobs_dict.values()
for k, v in jobs_dict.items():
    if isinstance(v, list):
        if 'finished' != k:
            for job in v:
                try:
                    scrapyd.cancel('default', job.get('id'))
                    print(k, job, '取消成功')
                except Exception as e:
                    print('Wrong!!', str(e))

