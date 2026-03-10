import time


def allocate_elastic_ip(ec2, name):
    """
    Allocate an Elastic IP for the NAT Gateway.
    Uses the underlying EC2 client through the resource object.
    """
    response = ec2.meta.client.allocate_address(Domain="vpc")

    allocation_id = response["AllocationId"]
    public_ip = response["PublicIp"]

    # Tag the Elastic IP
    ec2.meta.client.create_tags(
        Resources=[allocation_id],
        Tags=[{"Key": "Name", "Value": name}]
    )

    print(f"Elastic IP allocated: {allocation_id} ({public_ip})")
    return allocation_id


def create_nat_gateway(ec2, subnet_id, allocation_id, name):
    """
    Create a NAT Gateway in the public subnet.
    """
    response = ec2.meta.client.create_nat_gateway(
        SubnetId=subnet_id,
        AllocationId=allocation_id,
        TagSpecifications=[
            {
                "ResourceType": "natgateway",
                "Tags": [{"Key": "Name", "Value": name}]
            }
        ]
    )

    nat_gateway_id = response["NatGateway"]["NatGatewayId"]
    print(f"NAT Gateway creation started: {nat_gateway_id}")

    return nat_gateway_id


def wait_for_nat_gateway(ec2, nat_gateway_id, timeout=900, interval=15):
    """
    Wait until NAT Gateway becomes available.
    Simple polling loop because waiters can vary by setup/version.
    """
    elapsed = 0

    while elapsed < timeout:
        response = ec2.meta.client.describe_nat_gateways(
            NatGatewayIds=[nat_gateway_id]
        )

        state = response["NatGateways"][0]["State"]
        print(f"NAT Gateway {nat_gateway_id} state: {state}")

        if state == "available":
            print(f"NAT Gateway is available: {nat_gateway_id}")
            return True

        if state in ["failed", "deleted", "deleting"]:
            raise Exception(f"NAT Gateway entered unexpected state: {state}")

        time.sleep(interval)
        elapsed += interval

    raise TimeoutError(f"Timed out waiting for NAT Gateway {nat_gateway_id}")