#_*_coding:utf-8_*_
import requests
import json
import time
import sys
import os


# console_url='http://192.168.6.230:6800'
console_url='http://127.0.0.1:6800'

def get_all_spiders():
    '''
    通过scrapyd来获取所有的spider
    :return:
    '''
    response1=requests.get(url=console_url+'/listspiders.json?',params={'project':'default'})
    result1=json.loads(response1.text)
    print('爬虫项目状态是-------------',result1['status'],'可用的爬虫数量：-------',len(result1['spiders']))
    print('可用的爬虫列表：')
    for onespider in result1['spiders']:
        print(onespider)
    return result1['spiders']


def start_a_spider_job(project='default',spidername=None):
    '''
    根据爬虫名来生成一个spider
    :param project:
    :param spidername:
    :return:
    '''
    if spidername:
        spider_task={
            'project':project,
            'spider':spidername,
            'setting':None,
            'jobid':None
        }
        respons1=requests.post(url=console_url+'/schedule.json',data=spider_task)
        print(respons1.text)

    else:
        print('请输入一个正确的爬虫名称')


def cancel_job(jobId=None,project='default'):
    '''
    根据jobid来取消一个任务

    :param jobId:
    :param project:
    :return:
    '''
    if jobId:
        cancel_spider={
            'project':project,
            'job':jobId
        }
        response1=requests.post(url=console_url+'/cancel.json',data=cancel_spider)

        print(response1.text)


def get_all_Jobs(project='default'):
    '''
    获取scrapyd中所有正在运行的jobs

    :param project:
    :return:
    '''
    all_job_url=console_url+'/listjobs.json'
    all_job_dict={
        'project':project
    }
    response1=requests.get(url=all_job_url,params=all_job_dict)
    datajson=json.loads(response1.text)
    runingSpider=datajson['running']
    dependingSpider = datajson['pending']
    # for i in runingSpider:
    #     print('start_time:  ',i['start_time'])
    #     print('pid:         ',i['pid'])
    #     print('jobid:       ',i['id'])
    #     print('spiderName:  ',i['spider'])
    #     print('-----------------------------------')

    return runingSpider,dependingSpider
    # print(response1.text)



def start_all_spider():
    '''
    启动项目中所有的spiders

    :return:
    '''
    #get_all_spiders()
    all_spider_avalid=get_all_spiders()
    #优先加载重点人物爬取方法
    prior_start_spider_list = ['doubanmovie', 'vgtime','rrmj','doubanSearch']

    for one_spidername in prior_start_spider_list:
        start_a_spider_job(spidername=one_spidername)
    
    #start_a_spider_job(spidername="vipuser")
    #for one_spidername in all_spider_avalid:
        #if one_spidername != 'vipuser':
            #start_a_spider_job(spidername=one_spidername)

    print('_____________\n'
          ' all start  \n'
          '_____________')

def cancel_all_spider_job():
    '''
    取消所有正在运行的job，注意，正在pendding中的jobs不会被取消，所以取消正在运行的爬虫后，那些后边排队等待启动的爬虫会继续跟进，所以
    要取消所有的jobs，那么就要持续运行这个函数

    :return:
    '''

    all_jobs_id=get_all_Jobs()
    for one_jod in all_jobs_id:
        print('cancel jobId-----',one_jod)
        cancel_job(jobId=str(one_jod['id']))
        time.sleep(1)

    print('_____________\n'
          ' all cancel  \n'
          '_____________')


def lanch_spider_runing_just_10Min():
    '''
    debug专用，用来启动每个爬虫，每个爬虫只跑10分钟！！！！！！！！！！检测项目下所有的爬虫是不是可以运行。

    :return:
    '''
    start_all_spider()
    while True:
        all_spider_jobs=get_all_Jobs()
        for onejob in all_spider_jobs:
            start_time=onejob['start_time'].split('.')[0]
            pid=onejob['pid']
            jobid=onejob['id']
            spider=onejob['spider']

            timenow=time.time()
            spidertime_str=start_time
            spider_start_time_touple=time.strptime(spidertime_str,'%Y-%m-%d %H:%M:%S')
            spider_start_time_stamp=time.mktime(spider_start_time_touple)
            if timenow-spider_start_time_stamp>60*2:
                cancel_job(jobid)
                print('has cancle a job,which name is ',spider,' which id is ',jobid)


        time.sleep(20)





if __name__ == '__main__':
    # get_all_spiders()
    # start_a_spider_job(spidername='chinainperspective')
    # cancel_job(jobId='27cf4bf04de011e880a40862667c7ee1')
    # get_all_Jobs()
    # cancel_all_spider_job()
    while(1>0):
        #获取目前列表中的正在运行的和待推入队列的爬虫
        all_jobs_id,dependingspider = get_all_Jobs()
        if len(all_jobs_id)==1:
            job = all_jobs_id[0]
            if job == 'sinahuatitopic':
                cancel_all_spider_job()
        if len(all_jobs_id )<=0 and len(dependingspider)<=0:
            start_all_spider()
        time.sleep(10*60)
    #sys.path.append(os.path.dirname(sys.path[0]))
    #lanch_spider_runing_just_10Min()
