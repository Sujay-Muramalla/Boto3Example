def create_vpc(ec2, cidr_block, name):
    vpc = ec2.create_vpc(CidrBlock=cidr_block)
    vpc.wait_until_available()

    vpc.create_tags(
        Tags=[
            {"Key": "Name", "Value": name}
        ]
    )

    # Enable DNS support and hostnames
    vpc.modify_attribute(EnableDnsSupport={"Value": True})
    vpc.modify_attribute(EnableDnsHostnames={"Value": True})

    print(f"VPC created: {vpc.id}")
    return vpc