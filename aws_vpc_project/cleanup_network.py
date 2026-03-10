import boto3
import time

REGION = "us-west-2"

VPC_ID = "vpc-0910918800038f775"

ec2 = boto3.resource("ec2", region_name=REGION)
client = ec2.meta.client


def delete_nat_gateways():
    print("\nSearching for NAT Gateways...")

    response = client.describe_nat_gateways(
        Filters=[{"Name": "vpc-id", "Values": [VPC_ID]}]
    )

    for nat in response["NatGateways"]:
        nat_id = nat["NatGatewayId"]
        print(f"Deleting NAT Gateway: {nat_id}")

        client.delete_nat_gateway(NatGatewayId=nat_id)

        # wait until deleted
        while True:
            nat_state = client.describe_nat_gateways(NatGatewayIds=[nat_id])[
                "NatGateways"
            ][0]["State"]

            print(f"NAT Gateway state: {nat_state}")

            if nat_state == "deleted":
                print(f"NAT Gateway deleted: {nat_id}")
                break

            time.sleep(10)


def release_elastic_ips():
    print("\nReleasing Elastic IPs...")

    addresses = client.describe_addresses()

    for addr in addresses["Addresses"]:
        if "AllocationId" in addr:
            allocation_id = addr["AllocationId"]

            print(f"Releasing EIP: {allocation_id}")
            client.release_address(AllocationId=allocation_id)


def detach_delete_igw():
    print("\nDeleting Internet Gateway...")

    igws = list(ec2.internet_gateways.filter(
        Filters=[{"Name": "attachment.vpc-id", "Values": [VPC_ID]}]
    ))

    for igw in igws:
        print(f"Detaching IGW: {igw.id}")
        igw.detach_from_vpc(VpcId=VPC_ID)

        print(f"Deleting IGW: {igw.id}")
        igw.delete()


def delete_route_tables():
    print("\nDeleting custom route tables...")

    vpc = ec2.Vpc(VPC_ID)

    for rt in vpc.route_tables.all():

        # skip main route table
        associations = list(rt.associations)

        main = False
        for assoc in associations:
            if assoc.main:
                main = True

        if main:
            continue

        print(f"Deleting route table: {rt.id}")

        for assoc in associations:
            if not assoc.main:
                assoc.delete()

        rt.delete()


def delete_subnets():
    print("\nDeleting subnets...")

    vpc = ec2.Vpc(VPC_ID)

    for subnet in vpc.subnets.all():
        print(f"Deleting subnet: {subnet.id}")
        subnet.delete()


def delete_vpc():
    print("\nDeleting VPC...")

    vpc = ec2.Vpc(VPC_ID)

    vpc.delete()

    print(f"VPC deleted: {VPC_ID}")


def main():

    delete_nat_gateways()

    release_elastic_ips()

    delete_route_tables()

    detach_delete_igw()

    delete_subnets()

    delete_vpc()

    print("\nCleanup completed successfully.")


if __name__ == "__main__":
    main()