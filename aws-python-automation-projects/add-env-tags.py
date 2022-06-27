import boto3

ec2_client_paris = boto3.client('ec2', region_name="eu-west-3")
ec2_resource_paris = boto3.resource('ec2', region_name="eu-west-3")

ec2_client_london = boto3.client('ec2', region_name="eu-west-2")
ec2_resource_london = boto3.resource('ec2', region_name="eu-west-2")

instance_ids_paris = []
instance_ids_london = []

reservations_paris = ec2_client_paris.describe_instances()['Reservations']
for res in reservations_paris:
    instances = res['Instances']
    for ins in instances:
        instance_ids_paris.append(ins['InstanceId'])

response = ec2_resource_paris.create_tags(
    Resources=instance_ids_paris,
    Tags=[
        {
            'Key': 'environment',
            'Value': 'prod'
        },
    ]
)


reservations_london = ec2_client_london.describe_instances()['Reservations']
for res in reservations_london:
    instances = res['Instances']
    for ins in instances:
        instance_ids_london.append(ins['InstanceId'])

response = ec2_resource_london.create_tags(
    Resources=instance_ids_london,
    Tags=[
        {
            'Key': 'environment',
            'Value': 'dev'
        },
    ]
)
