from aws_session import get_ec2_resource
from config import (
    PROJECT_NAME,
    VPC_CIDR,
    PUBLIC_SUBNET_CIDR,
    PRIVATE_SUBNET_CIDR,
    PUBLIC_AZ,
    PRIVATE_AZ
)
from vpc import create_vpc
from subnet import create_subnet
from gateway import create_internet_gateway
from route_table import (
    create_route_table,
    associate_route_table,
    add_igw_route,
    add_nat_route
)
from nat_gateway import (
    allocate_elastic_ip,
    create_nat_gateway,
    wait_for_nat_gateway
)


def main():
    ec2 = get_ec2_resource()

    # 1. Create VPC
    vpc = create_vpc(ec2, VPC_CIDR, f"{PROJECT_NAME}-vpc")

    # 2. Create subnets
    public_subnet = create_subnet(
        ec2=ec2,
        vpc_id=vpc.id,
        cidr_block=PUBLIC_SUBNET_CIDR,
        availability_zone=PUBLIC_AZ,
        name=f"{PROJECT_NAME}-public-subnet",
        public=True
    )

    private_subnet = create_subnet(
        ec2=ec2,
        vpc_id=vpc.id,
        cidr_block=PRIVATE_SUBNET_CIDR,
        availability_zone=PRIVATE_AZ,
        name=f"{PROJECT_NAME}-private-subnet",
        public=False
    )

    # 3. Create and attach IGW
    igw = create_internet_gateway(ec2, vpc, f"{PROJECT_NAME}-igw")

    # 4. Create public route table and associate with public subnet
    public_rt = create_route_table(ec2, vpc.id, f"{PROJECT_NAME}-public-rt")
    add_igw_route(public_rt, igw.id)
    associate_route_table(public_rt, public_subnet.id)

    # 5. Create private route table and associate with private subnet
    private_rt = create_route_table(ec2, vpc.id, f"{PROJECT_NAME}-private-rt")
    associate_route_table(private_rt, private_subnet.id)

    # 6. Allocate EIP for NAT Gateway
    allocation_id = allocate_elastic_ip(ec2, f"{PROJECT_NAME}-nat-eip")

    # 7. Create NAT Gateway in public subnet
    nat_gateway_id = create_nat_gateway(
        ec2,
        public_subnet.id,
        allocation_id,
        f"{PROJECT_NAME}-nat-gw"
    )

    # 8. Wait until NAT Gateway becomes available
    wait_for_nat_gateway(ec2, nat_gateway_id)

    # 9. Add route from private route table to NAT Gateway
    add_nat_route(private_rt, nat_gateway_id)

    print("\nNetwork + NAT layer created successfully!")
    print(f"VPC ID: {vpc.id}")
    print(f"Public Subnet ID: {public_subnet.id}")
    print(f"Private Subnet ID: {private_subnet.id}")
    print(f"Internet Gateway ID: {igw.id}")
    print(f"Public Route Table ID: {public_rt.id}")
    print(f"Private Route Table ID: {private_rt.id}")
    print(f"NAT Gateway ID: {nat_gateway_id}")
    print(f"EIP Allocation ID: {allocation_id}")


if __name__ == "__main__":
    main()