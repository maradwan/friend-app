#
# This script is deleting ami and snapshots for specific tag (ServerRole), 
# with defined retention days and will delete any ami that exceed that. 
# Needs : Region, tag(ServerRole) and retention_days
# Author Mohamed Radwan <maradwan@gmail.com>

import re
import boto3
from datetime import datetime, timedelta
import sys

region = sys.argv[1]
serverrole = sys.argv[2]
retention_days = int(sys.argv[3])

def deregister_ami(serverrole,retention_days=90):
    ec2 = boto3.resource("ec2", region_name=region)
    filters=[{'Name':'tag:ServerRole', 'Values':[serverrole]}]
    my_images = ec2.images.filter(Filters=filters)
    old_images = []
    for image in my_images:
        created_at = datetime.strptime(image.creation_date,"%Y-%m-%dT%H:%M:%S.000Z")
        if created_at < datetime.now() - timedelta(days=retention_days):
            old_images.append(image.id)
            print('Deregistering {} ({})'.format(image.name, image.id))
            image.deregister()
    old_snapshot_ami = []
    old_snapshot_id  = []
    for snapshot in ec2.snapshots.filter(Filters=filters):
        r =re.findall(r'ami-.{8}', snapshot.description)
        old_snapshot_ami.append(r)
        old_snapshot_id.append(snapshot.snapshot_id)
    for i in range(0,len(old_images)):
       for j in range(0,len(old_snapshot_ami)):
          if old_images[i] == old_snapshot_ami[j][0]:
             print('Deleting Snapshots for {} and snapshot id {}'.format(old_images[i], old_snapshot_id[j]))
             snapshot.delete(SnapshotId=old_snapshot_id[j])

deregister_ami(serverrole,retention_days=retention_days)
