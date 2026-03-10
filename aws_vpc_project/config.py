AWS_REGION = "us-west-2"

PROJECT_NAME = "sujay-vpc-demo"

VPC_CIDR = "10.0.0.0/16"

PUBLIC_SUBNET_CIDR = "10.0.1.0/24"
PRIVATE_SUBNET_CIDR = "10.0.2.0/24"

PUBLIC_AZ = "us-west-2a"
PRIVATE_AZ = "us-west-2b"

# Existing resource IDs from your successful run
VPC_ID = "vpc-0b3101187f4764095"
PUBLIC_SUBNET_ID = "subnet-039ee06437a238c77"
PRIVATE_SUBNET_ID = "subnet-0e3fff7327bfd843f"

# Replace this with a valid AMI in us-west-2
AMI_ID = "ami-0534a0fd33c655746"

INSTANCE_TYPE = "t2.micro"
KEY_NAME = "labsuser"   # change if your key pair name is different