def create_subnet(ec2, vpc_id, cidr_block, availability_zone, name, public=False):
    subnet = ec2.create_subnet(
        VpcId=vpc_id,
        CidrBlock=cidr_block,
        AvailabilityZone=availability_zone
    )

    subnet.create_tags(
        Tags=[
            {"Key": "Name", "Value": name}
        ]
    )

    if public:
        subnet.meta.client.modify_subnet_attribute(
            SubnetId=subnet.id,
            MapPublicIpOnLaunch={"Value": True}
        )

    print(f"Subnet created: {subnet.id} ({name})")
    return subnet