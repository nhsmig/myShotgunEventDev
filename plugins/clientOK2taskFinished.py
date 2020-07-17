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
import shotgun_api3
import pprint as pp

def registerCallbacks(reg):
    # Register a callback to into the event processing system.
    #
    # Arguments:
    # - Shotgun script name
    # - Shotgun script key
    # - Callable
    # - A filter to match events to so the callable is only invoked when
    #   appropriate
    # - Argument to pass through to the callable
    #

    # server = 'https://b1.shotgunstudio.com'
    script_name = 'clientOK2taskFinished'
    script_key = 'zqtezL$gvumodcykerubqil2s'

    eventFilter = {'Shotgun_Version_Change': ['client_approved']}

    args = {
        # "date_approved_field": "client_approved_at",
        # "date_approved_timezone": "US/Pacific",
        "approved_status_code": "apr",
        }

    reg.registerCallback(
        script_name,
        script_key,
        clientOK2taskFinished,
        eventFilter,
        None,
    )

    # Set the logging level for this particular plugin. Let debug and above
    # messages through (don't block info, etc). This is particularly usefull
    # for enabling and disabling debugging on a per plugin basis.
    reg.logger.setLevel(logging.DEBUG)


def clientOK2taskFinished(sg, logger, event, args):
    """
    A callback that logs its arguments.

    :param sg: Shotgun API handle.
    :param logger: Logger instance.
    :param event: A Shotgun EventLogEntry entity dictionary.
    :param args: Any additional misc arguments passed through this plugin.
    """
 
    if not event:
        return
 
 
    #필터링된 이벤트 내용을 문자열(딕셔너리)로 반환
    # logger.info("%s" % str(event)) 

    # 필터링된 이벤트 딕셔너리를 key와 value로 반환
    for k, v in event.iteritems():
        logger.info("%s, %s" % (k, v))


    entity_id = event["entity"]["id"]
    entity_name = event["entity"]["name"]
    clientApproval = event['meta']['new_value']
    logger.info("ID : %s" % str(entity_id))
    logger.info("name : %s" % str(entity_name))
    logger.info('clientOK: %s' % str(clientApproval))

    currentVersion = sg.find_one(
        'Version',
        [["id", "is", entity_id]],
        ['sg_task', 'entity', 'sg_status_list', 'sg_task.Task.sg_status_list']
    )
    pp.pprint(currentVersion)

    currentVersionStatus = currentVersion['sg_status_list']
    currentTaskStatus = currentVersion['sg_task.Task.sg_status_list']

    if clientApproval == True:
        sg.update(
            'Task',
            currentVersion['sg_task']['id'],
            {'sg_status_list':'fin'}
        )
    else:
        pass
    

'''
def version_status_changed(sg, logger, event, args):
    """
    A callback that logs its arguments.

    :param sg: Shotgun API handle.
    :param logger: Logger instance.
    :param event: A Shotgun EventLogEntry entity dictionary.
    :param args: Any additional misc arguments passed through this plugin.
    """
    if not event:
        return

    # Return if we don't have all the field values we need.
    if (not event.get("entity", {}).get("id") or
        not event.get("entity", {}).get("name") or
        not event.get("id")):
            return

    logger.info("%s" % str(event))
    entity_id = event["entity"]["id"]
    entity_name = event["entity"]["name"]
    logger.info("ID : %s" % str(entity_id))
    logger.info("name : %s" % str(entity_name))


    sg_version = sg.find_one(
        "Version",
        [["id", "is", entity_id]],
        ["sg_task", "entity", "sg_status_list", "sg_task.Task.sg_status_list"]
    )
    if not sg_version:
        logger.info("Unable to retrieve Version (%d) %s from SG for event %d!" % (
            entity_id, entity_name, event["id"])
        )
        return

    new_version_status = sg_version["sg_status_list"]
    batch_cmds = []

    # if we have a linked Task, check to see if we can update its status
    if sg_version["sg_task"]:
        cur_task_status = sg_version["sg_task.Task.sg_status_list"]

        # Determine which, if any, status to set the linked Task to.
        new_task_status = None
        if new_version_status:
            sg_status = sg.find_one(
                "Status",
                [["code", "is", new_version_status]],
                ["sg_task_status_mapping"]
            )
            new_task_status = sg_status.get("sg_task_status_mapping")
            logger.debug("Status [%s] Task Status mapping: %s" % (new_version_status, new_task_status))
            logger.debug("Task current status: %s" % cur_task_status)

            if new_task_status and new_task_status != cur_task_status:
                # Verify the new Task status is a valid Task status.  We need to check
                # this here rather than before we register the plugin because the
                # sg_task_status_mapping value can be changed at any time.
                task_status_list = sg.schema_field_read(
                    "Task",
                    "sg_status_list"
                )["sg_status_list"]["properties"]["valid_values"]["value"]

                if new_task_status not in task_status_list:
                    logger.info("Invalid Task status detected: %s" % new_task_status)
                    logger.info("Cannot update Version [%d] Task status." % entity_id)
                    new_task_status = None
                logger.debug("New Task status: %s" % new_task_status)

        logger.debug("Version Task: %s" % sg_version["sg_task"])
        if new_task_status and new_task_status != cur_task_status:
            # Update the linked Task's status to the value resolved from
            # Version.sg_status_list.Status.sg_task_status_mapping
            batch_cmds.append({
                "request_type": "update",
                "entity_type": sg_version["sg_task"]["type"],
                "entity_id": sg_version["sg_task"]["id"],
                "data": {"sg_status_list": new_task_status}
            })

    if batch_cmds:
        # Execute the batch command(s)
        logger.info("Running [%d] batch command(s) to update Version and Task values ..." % (
            len(batch_cmds))
        )
        [logger.debug("    %s" % bc) for bc in batch_cmds]
        results = sg.batch(batch_cmds)
        logger.debug("    RESULTS: %s" % results)
'''