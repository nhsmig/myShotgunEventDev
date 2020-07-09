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
    
    script_name = 'clientOK2finishedFlag'
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
        clientOK2finishedFlag,
        eventFilter,
        None,
    )

    # Set the logging level for this particular plugin. Let debug and above
    # messages through (don't block info, etc). This is particularly usefull
    # for enabling and disabling debugging on a per plugin basis.
    reg.logger.setLevel(logging.DEBUG)



#태스크의 status가 바뀌었을 때 연결된 하위 태스크들의 status를 자동변경.
def clientOK2finishedFlag(sg, logger, event, args):
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
