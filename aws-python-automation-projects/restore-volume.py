import boto3
from operator import itemgetter

# Define the method of calling the AWS API
ec2_client = boto3.client('ec2', region_name="eu-west-2")
ec2_resource = boto3.resource('ec2', region_name="eu-west-2")

# Get - by filtering, volumes attached to the specific instance to be restored
instance_id = "i-0f9ef16b5ed274da3"
volumes = ec2_client.describe_volumes(
    Filters=[
            {
                'Name': 'attachment.instance-id',
                'Values': [instance_id]
            },
        ]
)

# Get - by filtering, the snapshots associated with the volume
instance_volume = volumes['Volumes'][0]
snapshots = ec2_client.describe_snapshots(
    OwnerIds=['self'],
    Filters=[
         {
            'Name': 'volume-id',
            'Values': [instance_volume['VolumeId']]
         },
    ]
)

latest_snapshot = sorted(snapshots['Snapshots'], key=itemgetter('StartTime'), reverse=True)[0]

# Restore/create the volume from the snapshot
new_volume = ec2_client.create_volume(
    SnapshotId=latest_snapshot['SnapshotId'],
    AvailabilityZone="eu-west-2b",
    TagSpecifications=[
        {
            'ResourceType': 'volume',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'prod'
                },
            ]
        },
    ],
)

# Attach volume to the EC2 Instance
while True:
    vol = ec2_resource.Volume(new_volume['VolumeId'])
    print(vol.state)
    if vol.state == 'available':
        ec2_resource.Instance(instance_id).attach_volume(
            Device='/dev/xvdb',
            VolumeId=new_volume['VolumeId']
        )
        break
