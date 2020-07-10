#-*-encoding:utf-8-*-
# Copyright 2018 Autodesk, Inc.  All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license agreement
# provided at the time of installation or download, or which otherwise accompanies
# this software in either electronic or hard copy form.
#

# See docs folder for detailed usage info.

import os
import logging
import pprint as pp


def registerCallbacks(reg):
    """
    Register all necessary or appropriate callbacks for this plugin.
    """

    # Specify who should recieve email notifications when they are sent out.
    #
    # reg.setEmails('me@mydomain.com')

    # Use a preconfigured logging.Logger object to report info to a log file or
    # email. By default error and critical messages will be reported via email
    # and logged to file, all other levels are logged to a file.
    #
    # reg.logger.debug('Loading logArgs plugin.')

    # Register a callback to into the event processing system.
    #
    # Arguments:
    # - Shotgun script name
    # - Shotgun script key
    # - Callable
    # - A filter to match events to so the callable is only invoked when
    #   appropriate
    # - Argument to pass through to the callable

    # eventFilter = None
    
    script_name = 'changeDownstreamTaskStatus'
    script_key = 'sbscnwybnxrrgnactW7dl&kfa'
    
    # 이벤트 중 스테이터스 변화만 필터링
    eventFilter = {
        'Shotgun_Task_Change':['sg_status_list', 'sg_description']
        }

    # reg.registerCallback(
    #     os.environ["SGDAEMON_TEST_NAME"],
    #     os.environ["SGDAEMON_TEST_KEY"],
    #     changeDownstreamStatus,
    #     eventFilter,
    #     None,
    # )

    reg.registerCallback(
        script_name,
        script_key,
        changeDownstreamStatus,
        eventFilter,
        None,
    )

    # Set the logging level for this particular plugin. Let debug and above
    # messages through (don't block info, etc). This is particularly usefull
    # for enabling and disabling debugging on a per plugin basis.
    reg.logger.setLevel(logging.DEBUG)



#태스크의 status가 바뀌었을 때 연결된 하위 태스크들의 status를 자동변경.
def changeDownstreamStatus(sg, logger, event, args):
    """
    A callback that logs its arguments.

    :param sg: Shotgun API handle.
    :param logger: Logger instance.
    :param event: A Shotgun EventLogEntry entity dictionary.
    :param args: Any additional misc arguments passed through this plugin.
    """
    
    #필터링된 이벤트 내용을 문자열(딕셔너리)로 반환
    # logger.info("%s" % str(event)) 

    # 필터링된 이벤트 딕셔너리를 key와 value로 반환
    # for k, v in event.iteritems():
    #     logger.info("%s, %s" % (k, v))

 
    #전달된 이벤트로 딕셔너리로부터 태스크 아이디를 추출
    currentTask = sg.find_one(
            'Task',
            [
                ['id', 'is', event['entity']['id']]
            ],
            ['content', 'step']
        )
    # pp.pprint(currentTask)        
    #추출한 태스크아이디로부터 하위로 연결된 태스크와 스테이터스 정보를 확인              
    downstreamTask = sg.find(
            'Task',
            [
                ['upstream_tasks', 'is', currentTask]
            ],
            ['sg_status_list', 'entity', 'project']
        )                                                                                           
    #전달된 태스크의 바뀐 스테이터스 value 체크??
    currentTaskStep = event['entity']['name']
    currentTaskStatus = event['meta']['new_value']                                       
    
    #소스 태스크와 다운스트림 태스크의 스테이터스 체크용 리스트
    sourceStatusCheck = {'go':['fin', 'pub'], 'stop':['ret', 'hld']}
    targetStatusGroup_notStarted = ['new', 'hld']
    targetStatusGroup_onGoing = ['wip', 'rev', 'rdy', 'ret']
    targetStatusGroup_finished = ['ok', 'pub', 'fin']
 
    #모든 다운스트림 태스크의 스테이터스에 대한 처리
    
    if downstreamTask:
        for task in downstreamTask:
            # pp.pprint(task)
            currentTargetStatus = task['sg_status_list']
            if currentTaskStatus in sourceStatusCheck['go']:
                if currentTargetStatus in targetStatusGroup_notStarted:
                    sg.update(
                        'Task', 
                        task['id'],
                        {'sg_status_list': 'rdy'}
                    )
                else:
                    continue
            elif currentTaskStatus in sourceStatusCheck['stop']:
                if currentTargetStatus in targetStatusGroup_onGoing:
                    sg.update(
                        'Task',
                        task['id'],
                        {'sg_status_list': 'hld'}
                    )
                elif currentTargetStatus in targetStatusGroup_finished:
                    print('Updating downstream task...')
                    sg.update(
                        'Task',
                        task['id'],
                        {'sg_status_list': 'ret'}
                    )
                else:
                    continue
            else:
                continue
    else:
        print ("No downstream tasks found")

