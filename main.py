import boto3


s3 = boto3.resource('s3')

s3_c = boto3.client("s3")

# Print out bucket names
for bucket in s3.buckets.all():
    print(bucket.name)
    
file_name = "sample.txt"

with open(file_name, "w") as file:
    file.write("Hello from Python!\n")
    file.write("This file was created using a Python script.\n")
    file.write("Now we will upload it to Amazon S3.\n")

print("sample.txt file created successfully")

bucket_name = "sujay-demo-bucket-2026"
s3.Bucket(bucket_name).upload_file(file_name, file_name)
print("File uploaded to S3 successfully")


bucket_name = "sujay-test-bucket-2"
s3.Bucket(bucket_name).upload_file(file_name, file_name)
print("File uploaded to S3 successfully")

bucket_name = "sujay-demo-bucket-2026"
object_key = "sample.txt"

response = s3_c.get_object(Bucket=bucket_name, Key=object_key)
file_content = response["Body"].read().decode("utf-8")

print(file_content)



