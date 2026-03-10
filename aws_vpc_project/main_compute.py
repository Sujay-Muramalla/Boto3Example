from aws_session import get_ec2_resource
from config import (
    PROJECT_NAME,
    VPC_ID,
    PUBLIC_SUBNET_ID,
    PRIVATE_SUBNET_ID,
    AMI_ID,
    INSTANCE_TYPE,
    KEY_NAME
)
from security_group import create_public_sg, create_private_sg
from ec2 import launch_public_web_instance, launch_private_instance


def main():
    ec2 = get_ec2_resource()

    # 1. Create security groups
    public_sg = create_public_sg(
        ec2,
        VPC_ID,
        f"{PROJECT_NAME}-public-sg"
    )

    private_sg = create_private_sg(
        ec2,
        VPC_ID,
        f"{PROJECT_NAME}-private-sg",
        public_sg.id
    )

    # 2. Launch public EC2 web server
    public_instance = launch_public_web_instance(
        ec2=ec2,
        ami_id=AMI_ID,
        instance_type=INSTANCE_TYPE,
        key_name=KEY_NAME,
        subnet_id=PUBLIC_SUBNET_ID,
        security_group_id=public_sg.id,
        name=f"{PROJECT_NAME}-public-ec2"
    )

    # 3. Launch private EC2 instance
    private_instance = launch_private_instance(
        ec2=ec2,
        ami_id=AMI_ID,
        instance_type=INSTANCE_TYPE,
        key_name=KEY_NAME,
        subnet_id=PRIVATE_SUBNET_ID,
        security_group_id=private_sg.id,
        name=f"{PROJECT_NAME}-private-ec2"
    )

    print("\nCompute layer created successfully!")
    print(f"Public SG ID: {public_sg.id}")
    print(f"Private SG ID: {private_sg.id}")
    print(f"Public EC2 ID: {public_instance.id}")
    print(f"Public EC2 Public IP: {public_instance.public_ip_address}")
    print(f"Private EC2 ID: {private_instance.id}")
    print(f"Private EC2 Private IP: {private_instance.private_ip_address}")


if __name__ == "__main__":
    main()