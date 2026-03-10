def launch_public_web_instance(
    ec2,
    ami_id,
    instance_type,
    key_name,
    subnet_id,
    security_group_id,
    name
):
    user_data_script = """#!/bin/bash
yum update -y
yum install -y httpd
systemctl enable httpd
systemctl start httpd
echo "<h1>Hello from Sujay's Public EC2 Web Server</h1>" > /var/www/html/index.html
"""

    instances = ec2.create_instances(
        ImageId=ami_id,
        InstanceType=instance_type,
        #KeyName=key_name,
        MinCount=1,
        MaxCount=1,
        NetworkInterfaces=[
            {
                "AssociatePublicIpAddress": True,
                "DeviceIndex": 0,
                "SubnetId": subnet_id,
                "Groups": [security_group_id],
            }
        ],
        UserData=user_data_script,
        TagSpecifications=[
            {
                "ResourceType": "instance",
                "Tags": [{"Key": "Name", "Value": name}]
            }
        ]
    )

    instance = instances[0]
    print(f"Launching public EC2 instance: {instance.id}")

    instance.wait_until_running()
    instance.reload()

    print(f"Public EC2 running: {instance.id}")
    return instance


def launch_private_instance(
    ec2,
    ami_id,
    instance_type,
    key_name,
    subnet_id,
    security_group_id,
    name
):
    instances = ec2.create_instances(
        ImageId=ami_id,
        InstanceType=instance_type,
        KeyName=key_name,
        MinCount=1,
        MaxCount=1,
        NetworkInterfaces=[
            {
                "AssociatePublicIpAddress": False,
                "DeviceIndex": 0,
                "SubnetId": subnet_id,
                "Groups": [security_group_id],
            }
        ],
        TagSpecifications=[
            {
                "ResourceType": "instance",
                "Tags": [{"Key": "Name", "Value": name}]
            }
        ]
    )

    instance = instances[0]
    print(f"Launching private EC2 instance: {instance.id}")

    instance.wait_until_running()
    instance.reload()

    print(f"Private EC2 running: {instance.id}")
    return instance