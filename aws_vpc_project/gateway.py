def create_internet_gateway(ec2, vpc, name):
    igw = ec2.create_internet_gateway()

    igw.create_tags(
        Tags=[
            {"Key": "Name", "Value": name}
        ]
    )

    vpc.attach_internet_gateway(InternetGatewayId=igw.id)

    print(f"Internet Gateway created and attached: {igw.id}")
    return igw