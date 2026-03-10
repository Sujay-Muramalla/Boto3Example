def create_route_table(ec2, vpc_id, name):
    route_table = ec2.create_route_table(VpcId=vpc_id)

    route_table.create_tags(
        Tags=[
            {"Key": "Name", "Value": name}
        ]
    )

    print(f"Route table created: {route_table.id}")
    return route_table


def associate_route_table(route_table, subnet_id):
    route_table.associate_with_subnet(SubnetId=subnet_id)
    print(f"Route table {route_table.id} associated with subnet {subnet_id}")


def add_igw_route(route_table, igw_id):
    route_table.create_route(
        DestinationCidrBlock="0.0.0.0/0",
        GatewayId=igw_id
    )
    print(f"Added IGW route to {route_table.id}")
    
    
def add_nat_route(route_table, nat_gateway_id):
    route_table.create_route(
        DestinationCidrBlock="0.0.0.0/0",
        NatGatewayId=nat_gateway_id
    )
    print(f"Added NAT Gateway route to {route_table.id}")