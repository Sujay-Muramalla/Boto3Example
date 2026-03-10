def create_public_sg(ec2, vpc_id, name):
    sg = ec2.create_security_group(
        GroupName=name,
        Description="Allow SSH and HTTP for public web server",
        VpcId=vpc_id
    )

    sg.create_tags(
        Tags=[{"Key": "Name", "Value": name}]
    )

    # Allow SSH
    sg.authorize_ingress(
        IpPermissions=[
            {
                "IpProtocol": "tcp",
                "FromPort": 22,
                "ToPort": 22,
                "IpRanges": [{"CidrIp": "0.0.0.0/0", "Description": "SSH access"}],
            },
            {
                "IpProtocol": "tcp",
                "FromPort": 80,
                "ToPort": 80,
                "IpRanges": [{"CidrIp": "0.0.0.0/0", "Description": "HTTP access"}],
            },
        ]
    )

    print(f"Public security group created: {sg.id}")
    return sg


def create_private_sg(ec2, vpc_id, name, public_sg_id):
    sg = ec2.create_security_group(
        GroupName=name,
        Description="Allow SSH only from public EC2 security group",
        VpcId=vpc_id
    )

    sg.create_tags(
        Tags=[{"Key": "Name", "Value": name}]
    )

    # Allow SSH only from public EC2 SG
    sg.authorize_ingress(
        IpPermissions=[
            {
                "IpProtocol": "tcp",
                "FromPort": 22,
                "ToPort": 22,
                "UserIdGroupPairs": [
                    {
                        "GroupId": public_sg_id,
                        "Description": "SSH from public EC2"
                    }
                ],
            }
        ]
    )

    print(f"Private security group created: {sg.id}")
    return sg