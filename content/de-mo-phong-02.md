# Đề mô phỏng SAA-C03 — Bộ 02

Hướng dẫn: 65 câu, 130 phút, đạt 720/1000, làm xong mới mở file đáp án. Mỗi câu chỉ chọn một đáp án, trừ các câu ghi rõ "Select TWO" thì chọn hai đáp án.

**Câu 1.** A gaming company uses Amazon DynamoDB for leaderboard data. Millions of players read the same popular items during tournaments, and the application requires single-digit millisecond latency to become microsecond latency for repeated reads. Provisioned throughput is already sufficient, but hot items cause uneven load. Which solution will provide in-memory caching with microsecond response times for DynamoDB?
A. Increase the DynamoDB table's read capacity units and enable adaptive capacity
B. Enable DynamoDB Accelerator (DAX) and route the application's DynamoDB API calls through the DAX cluster
C. Create an Amazon ElastiCache for Memcached cluster and manually cache every DynamoDB query result
D. Enable DynamoDB Streams and copy the data into Amazon OpenSearch Service for faster reads


**Câu 2.** A serverless API experiences sudden traffic spikes. During spikes, downstream Amazon DynamoDB writes are overwhelmed and some Lambda invocations are throttled. The company wants Lambda functions that process orders to never exceed a safe maximum number of simultaneous executions, while other functions in the account remain unaffected. What should a solutions architect do?
A. Place the Lambda function inside a VPC with a NAT gateway
B. Set a reserved concurrency limit on the order-processing Lambda function
C. Set a provisioned concurrency limit on the order-processing Lambda function
D. Increase the Lambda function memory to the maximum value


**Câu 3.** A payment application must process transactions in the exact order they were received and must ensure each transaction is processed exactly once, even when producers retry sending the same message. Standard queues have caused duplicate charges. Which solution meets these requirements?
A. Use an Amazon SQS FIFO queue with message deduplication enabled and a message group ID per account
B. Use an Amazon SQS standard queue with long polling enabled
C. Use an Amazon SNS standard topic with message filtering
D. Use an Amazon SQS standard queue with a dead-letter queue

**Câu 4.** A company runs an Amazon Aurora PostgreSQL cluster in one AWS Region for a global application. The company requires a disaster recovery solution in a second Region with a recovery point objective (RPO) of about 1 second and a recovery time objective (RTO) of less than 1 minute for cross-Region failover. Which solution meets these requirements with the least operational effort?
A. Take hourly Aurora snapshots and copy them to the second Region
B. Use an Aurora Global Database with a secondary cluster in the disaster recovery Region
C. Use AWS Backup to copy Aurora backups to the second Region once a day
D. Create Aurora read replicas in the second Region and manually promote one during a disaster


**Câu 5.** A social application needs a cache that supports sorted sets for a leaderboard, pub/sub messaging, and data persistence. The cache must rank users by score in real time. Which Amazon ElastiCache option should a solutions architect choose?
A. ElastiCache for Memcached with cluster mode enabled
B. ElastiCache for Redis with sorted sets
C. ElastiCache for Memcached with write-through caching
D. Amazon DynamoDB Accelerator (DAX)


**Câu 6.** A media company stores thousands of large video files that are uploaded once and downloaded many times by users worldwide. The files do not need to be mounted as a file system, and the company wants the most durable and cost-effective storage for this access pattern. Which storage service should be used?
A. Amazon S3 Standard storage
B. Amazon Elastic File System (Amazon EFS) with the General Purpose performance mode
C. Amazon Elastic Block Store (Amazon EBS) volumes attached to EC2 instances
D. Instance store volumes on Amazon EC2 instances


**Câu 7.** A company stores a database password used by an application on Amazon EC2. Regulations require the password to be rotated automatically every 30 days without redeploying the application, and the application must always retrieve the current password. Which solution meets these requirements?
A. Store the password in AWS Secrets Manager and enable automatic rotation with a Lambda function
B. Store the password in an encrypted Amazon EBS volume and create a new volume every 30 days
C. Store the password in AWS Systems Manager Parameter Store as a plain text parameter
D. Store the password in an Amazon S3 bucket with versioning enabled

**Câu 8.** A public web application is exposed through an Application Load Balancer. The security team wants protection against common web exploits such as SQL injection and cross-site scripting by using rules that AWS maintains and updates. Which solution should a solutions architect implement?
A. Enable Amazon GuardDuty and Amazon Inspector for the account
B. Enable AWS Shield Advanced on the Application Load Balancer
C. Attach AWS WAF to the Application Load Balancer and enable AWS Managed Rules
D. Add restrictive rules to the security group of the Application Load Balancer


**Câu 9.** Several private subnets route internet traffic through a single NAT gateway, which generates high data processing charges. Instances in the private subnets mostly access Amazon S3 and Amazon DynamoDB. How can a solutions architect reduce NAT gateway costs for this traffic?
A. Move the instances into public subnets and assign Elastic IP addresses
B. Replace the NAT gateway with a NAT instance in a public subnet
C. Create gateway VPC endpoints for Amazon S3 and Amazon DynamoDB and add routes for them in the private route tables
D. Enable NAT gateway flow logs and delete the NAT gateway during weekends


**Câu 10.** A company runs a steady-state production database on Amazon EC2 that must run continuously for 3 years and cannot tolerate interruptions. A separate batch workload can be interrupted at any time. Which purchasing options are MOST cost-effective for each workload?
A. Dedicated Hosts for the database, and Reserved Instances for the batch workload
B. On-Demand Instances for both workloads
C. Spot Instances for the database, and On-Demand Instances for the batch workload
D. Compute Savings Plans or Reserved Instances for the database, and Spot Instances for the batch workload


**Câu 11.** An event-driven application must route orders to different processing services based on the content of each event, such as order amount and Region. Producers should publish events without knowing which consumers will receive them, and new consumers must be added without changing producers. Which service should be used for content-based event routing?
A. Amazon EventBridge with event buses and rules that match event patterns
B. Amazon Kinesis Data Streams with enhanced fan-out
C. AWS Step Functions with parallel branches
D. Amazon Simple Queue Service (Amazon SQS) standard queues

**Câu 12.** A company wants one published order event to be delivered simultaneously to a billing service, a shipping service, and an analytics service. Each service must be able to process events independently, at its own pace, and must not lose events when a service is temporarily unavailable. (Select TWO)
A. Publish the event to a single Amazon DynamoDB table and require each service to scan the table
B. Subscribe an Amazon SQS queue for each service to the SNS topic so each service buffers its own copy
C. Invoke three Lambda functions directly from the producer in sequence
D. Publish the event to an Amazon SNS topic
E. Store the event in a single shared SQS queue that all three services poll competitively


**Câu 13.** A startup wants to run Docker containers for a web API without provisioning or managing servers or clusters. Traffic varies, and the team wants the least operational overhead while still integrating with an Application Load Balancer. Which compute option should a solutions architect recommend?
A. Amazon Elastic Kubernetes Service (Amazon EKS) with self-managed worker nodes
B. Amazon Elastic Container Service (Amazon ECS) with the AWS Fargate launch type
C. AWS Elastic Beanstalk with a Docker environment and custom capacity management
D. Amazon EC2 instances in an Auto Scaling group with the containers installed manually


**Câu 14.** A business process involves receiving an order, checking inventory, charging a payment, and arranging shipment. Some steps run in parallel, failed steps must be retried with backoff, and the entire workflow state must be visible and auditable for up to several weeks. Which AWS service is MOST suitable to orchestrate this workflow?
A. AWS Lambda functions that call each other directly
B. Amazon EventBridge scheduled rules
C. AWS Step Functions state machines
D. Amazon Simple Queue Service (Amazon SQS) with visibility timeouts


**Câu 15.** A company must ingest a continuous stream of clickstream records at up to 800 MB per second for real-time analytics. Multiple independent applications need to read the same stream with their own read positions, and the data must be replayable for 7 days. Which service meets these requirements?
A. Amazon Simple Queue Service (Amazon SQS) FIFO queues
B. Amazon MSK Serverless with a single partition
C. Amazon Kinesis Data Firehose
D. Amazon Kinesis Data Streams with extended retention


**Câu 16.** Analysts need to run ad hoc SQL queries directly on several terabytes of JSON and Parquet data stored in Amazon S3, without provisioning servers. The data structure must be cataloged so table definitions can be reused across queries. Which combination of services should be used?
A. Amazon Athena for queries and AWS Glue Data Catalog for table metadata
B. Amazon Redshift for queries and Amazon RDS for table metadata
C. Amazon EMR for queries and Amazon DynamoDB for table metadata
D. Amazon Kinesis Data Analytics for queries and AWS Lake Formation for table metadata only

**Câu 17.** A new application uses Amazon DynamoDB. Traffic is highly unpredictable, with long idle periods followed by sudden large spikes. The operations team does not want to forecast capacity or manage throughput settings. Which DynamoDB capacity mode is MOST appropriate?
A. Provisioned capacity without Auto Scaling
B. Provisioned capacity with Auto Scaling
C. On-demand capacity mode
D. Reserved capacity with provisioned throughput


**Câu 18.** An AWS Lambda function that transcodes video files regularly needs 45 minutes to complete, but Lambda stops the work before it finishes. The processing is container-based and does not require a stateful server. Which solution should a solutions architect recommend?
A. Increase the Lambda function memory to 10 GB to make it finish faster
B. Move the workload to containers on AWS Fargate orchestrated as a longer-running task
C. Store the video in Amazon S3 Glacier and process it after retrieval
D. Split the Lambda function into smaller functions chained by Amazon SQS and keep each run under the Lambda timeout


**Câu 19.** A queue-based worker occasionally takes longer than expected to process a message. Other workers then receive and process the same message, causing duplicate work. Processed messages that repeatedly fail must be isolated for investigation. Which combination addresses this problem in Amazon SQS?
A. Enable FIFO ordering and reduce the message retention period to 60 seconds
B. Increase the visibility timeout to exceed processing time and configure a dead-letter queue with a maximum receive count
C. Use long polling and delete messages before processing begins
D. Shorten the visibility timeout and disable dead-letter queues


**Câu 20.** A development database on Amazon Aurora PostgreSQL has variable usage that drops to near zero at night and spikes during tests. The company wants the database capacity to scale automatically and to pay only for capacity used, without managing instances. Which option should be used?
A. Amazon RDS for PostgreSQL with storage Auto Scaling only
B. Aurora Provisioned with the smallest instance class
C. Aurora Serverless v2 configured with minimum and maximum Aurora Capacity Units (ACUs) so capacity scales automatically with usage
D. Amazon DynamoDB on-demand tables migrated from PostgreSQL


**Câu 21.** A read-heavy application uses Amazon ElastiCache for Redis in front of a database. Most reads are for a small set of popular items, and the application can tolerate occasionally stale data for a few minutes. The team wants the simplest caching strategy that populates the cache only when data is actually requested. Which strategy should be used?
A. Lazy loading (cache-aside)
B. Write-through caching
C. Write-behind (write-back) caching
D. Refresh-ahead caching managed by the database

**Câu 22.** A company stores compliance documents in Amazon S3. The documents are accessed frequently for 30 days, occasionally for the next 90 days, and almost never afterwards, but they must be retained for 7 years and remain retrievable within hours. Which lifecycle design is MOST cost-effective?
A. Transition objects to S3 One Zone-IA after 30 days and delete them after 120 days
B. Keep the objects in S3 Standard for the full 7 years
C. Transition objects to S3 Standard-IA after 30 days and to S3 Glacier Flexible Retrieval after 120 days, with expiration after 7 years
D. Copy the objects to Amazon EFS after 30 days and to Amazon EBS snapshots after 120 days


**Câu 23.** A retail company needs an Amazon DynamoDB table that is actively readable and writable in two AWS Regions at the same time. Users in each Region must write to their local Region with low latency, and changes must replicate automatically between Regions. Which DynamoDB feature meets these requirements?
A. DynamoDB export to Amazon S3 with cross-Region replication
B. DynamoDB Streams with a Lambda function that copies items to the other Region
C. DynamoDB point-in-time recovery with cross-Region backup copies
D. DynamoDB global tables


**Câu 24.** Whenever a new item is added to an Amazon DynamoDB table, a downstream process must update a search index and send a notification. The process must react to inserts and updates only, without continuously polling the table. Which solution should be used?
A. Enable DynamoDB Streams and use an AWS Lambda function as the stream consumer
B. Create an Amazon SQS queue and require producers to send duplicate messages
C. Enable DynamoDB Accelerator (DAX) and query the cache for changed items
D. Schedule an Amazon EventBridge rule to scan the DynamoDB table every minute


**Câu 25.** An API built with Amazon API Gateway and AWS Lambda serves product data that changes only every few minutes. Repeated identical requests increase Lambda invocations and latency. Which API Gateway feature will reduce backend calls for repeated responses?
A. Convert the REST API to a WebSocket API
B. Enable API Gateway caching for the stage with an appropriate TTL
C. Enable API Gateway request validation
D. Use a usage plan with a lower quota


**Câu 26.** An application uses Amazon DynamoDB. Each authenticated user must be allowed to read and write only items where the partition key equals that user's ID. No application code change should be trusted to enforce this isolation alone. How can this be enforced in IAM?
A. Enable DynamoDB Streams and audit access after the fact
B. Enable DynamoDB encryption at rest with a customer managed KMS key
C. Give each user a separate DynamoDB table
D. Use an IAM policy with a condition that uses dynamodb:LeadingKeys tied to the user's identity


**Câu 27.** A company must encrypt Amazon S3 objects with keys it controls and audits. Every use of the encryption key must be logged, and the company must be able to disable the key to immediately block access to the data. Which approach meets these requirements?
A. Use server-side encryption with Amazon S3 managed keys (SSE-S3)
B. Use server-side encryption with AWS KMS keys (SSE-KMS) using a customer managed key
C. Enable S3 Bucket Versioning and MFA Delete
D. Use client-side compression before uploading objects to Amazon S3


**Câu 28.** Private subnets have no internet route. Applications on Amazon EC2 in those subnets need frequent access to Amazon S3 and Amazon DynamoDB, and the security team wants this traffic to stay on the AWS network without traversing the internet. Which solution is MOST appropriate and cost-effective?
A. Create interface VPC endpoints powered by AWS PrivateLink for Amazon S3 and Amazon DynamoDB
B. Peer the VPC with another VPC that has an internet gateway
C. Deploy a NAT gateway in each private subnet
D. Create gateway VPC endpoints for Amazon S3 and Amazon DynamoDB


**Câu 29.** A company's website is protected by AWS Shield Standard. After a large, sophisticated Layer 7 DDoS attack, the company needs 24/7 access to the AWS DDoS Response Team, cost protection for scaling during attacks, and advanced attack diagnostics. Which service should the company use?
A. AWS Network Firewall
B. AWS WAF with AWS Managed Rules only
C. Amazon GuardDuty
D. AWS Shield Advanced


**Câu 30.** A development team needs to store a small configuration value securely and retrieve it from Lambda functions. (Select TWO statements that correctly distinguish the services.)
A. AWS Secrets Manager stores values in plain text by default with no encryption option
B. AWS Secrets Manager supports automatic rotation of secrets using Lambda functions
C. AWS Systems Manager Parameter Store cannot encrypt parameters with AWS KMS
D. Both services require the secret to be stored in an Amazon S3 bucket
E. AWS Systems Manager Parameter Store SecureString parameters can be used for secrets but automatic rotation is a native Secrets Manager feature, not a native Parameter Store feature


**Câu 31.** A company exposes a web application through an Application Load Balancer and wants HTTPS with a certificate that is automatically renewed by AWS. The domain's DNS is managed outside AWS. Which solution should be used?
A. Request a public certificate in AWS Certificate Manager (ACM), validate it, and attach it to the ALB HTTPS listener
B. Generate a self-signed certificate on each EC2 instance and open port 80 on the ALB
C. Store a certificate in AWS Secrets Manager and attach it directly to the ALB
D. Enable AWS WAF on the ALB and use its default certificate

**Câu 32.** A new Amazon S3 bucket must never be publicly accessible, even if a future bucket policy or ACL mistakenly grants public access. The compliance team also requires least-privilege access for a single application role. Which control provides the account- and bucket-level block?
A. Enable S3 Versioning and Object Lock on the bucket
B. Create an AWS WAF web ACL for the bucket
C. Enable server access logging on the bucket
D. Enable S3 Block Public Access settings on the bucket


**Câu 33.** A security team needs to find which IAM user made a specific Amazon S3 API call 60 days ago and needs to run SQL queries over the historical API activity without building a server. Which solution should be used?
A. Query AWS CloudTrail events stored in Amazon S3 by using Amazon Athena
B. Enable Amazon GuardDuty findings and search them in the console
C. Download AWS Cost and Usage Reports and filter by user
D. Review Amazon CloudWatch metrics for the S3 bucket


**Câu 34.** All new Amazon EBS volumes in an account must be encrypted at rest by default, including volumes created from snapshots. The security team wants no unencrypted volumes to be created by developers. Which account-level setting should be enabled?
A. Enable AWS Config with a rule to delete unencrypted volumes after 30 days
B. Enable EBS encryption by default for the AWS Region
C. Enable Amazon Inspector for EC2 instances
D. Require MFA for all IAM users in the account


**Câu 35.** An AWS Lambda function currently reads a database password from a plain text environment variable. Security review requires the password to be stored centrally, encrypted, rotated, and retrieved at runtime instead of being kept in plain text. Which solution should a solutions architect implement?
A. Encrypt the Lambda deployment package and keep the password in the code
B. Store the password in AWS Secrets Manager and grant the Lambda execution role permission to retrieve it
C. Store the password in a DynamoDB table without encryption
D. Store the password in an Amazon S3 object with bucket encryption enabled


**Câu 36.** An Application Load Balancer fronts a web application that is receiving SQL injection and cross-site scripting attempts in HTTP requests. The team wants to block these requests before they reach the application, using AWS-managed protections. Which solution should be used?
A. Add a network ACL that blocks the attackers' country
B. Increase the size of the EC2 instances behind the ALB
C. Enable Amazon CloudFront signed URLs for the application
D. Attach AWS WAF with the AWS Managed Rules SQL database and Core rule sets to the ALB


**Câu 37.** A security team wants two different types of continuous detection. (Select TWO correct pairings.)
A. Amazon Inspector automatically assesses EC2 instances and container images for software vulnerabilities
B. Amazon Inspector provides a managed web application firewall for ALBs
C. Amazon GuardDuty analyzes logs to detect malicious activity and compromised credentials in an AWS account
D. Amazon GuardDuty patches operating system vulnerabilities on EC2 instances
E. Both services replace the need for IAM policies


**Câu 38.** Containers running on Amazon ECS must access Amazon S3 and Amazon DynamoDB with permissions that apply only to the running containers, not to the underlying hosts or other tasks. Credentials must be provided automatically and rotated by AWS. Which IAM construct should be used?
A. An instance role shared by all ECS container instances with administrator access
B. An ECS task role assigned to the task definition
C. A bucket policy that allows access from any principal
D. An IAM user with access keys stored in the container image


**Câu 39.** A company uses Amazon SQS queues that contain sensitive data. Compliance requires encryption at rest with a customer managed AWS KMS key, and only a specific application role may decrypt messages. Which configuration meets these requirements?
A. Use an HTTPS endpoint for SQS and rely only on transport encryption
B. Enable SQS message deduplication and FIFO ordering
C. Store messages in an encrypted Amazon EBS volume instead of SQS
D. Enable server-side encryption with a customer managed KMS key on the queue and control access through the key policy and IAM policy


**Câu 40.** An Amazon Aurora MySQL cluster stores sensitive data. The company wants database users to authenticate using IAM credentials instead of static database passwords, in addition to encryption at rest. Which Aurora feature should be enabled?
A. Aurora Serverless auto pause
B. IAM database authentication
C. Aurora Global Database
D. Aurora backtrack


**Câu 41.** A team uses Amazon ElastiCache for Redis for session data. Compliance requires that data is encrypted while moving between clients and the cluster, and that clients must present an authentication token to connect. Which features should be enabled?
A. Lazy loading and TTL on session keys
B. Redis append-only file and cluster mode
C. In-transit encryption (TLS) and Redis AUTH
D. Memcached SASL and multi-threading


**Câu 42.** Analysts query sensitive data in Amazon S3 by using Amazon Athena. Different teams must have separate query limits and cost controls, and query results must be encrypted. Which Athena feature helps organize and control this usage?
A. Athena provisioned capacity with EC2 instances
B. Glue crawlers with automatic schema discovery only
C. Athena workgroups with per-workgroup settings for result locations, encryption, and bytes-scanned limits
D. S3 Object Lock on the query results bucket only


**Câu 43.** An AWS Step Functions workflow invokes several Lambda functions. Each function needs different, minimal permissions, and the workflow must not use a single highly privileged role for all steps. Which design follows least privilege?
A. Give the Step Functions state machine and all Lambda functions administrator access
B. Disable IAM roles and rely on resource policies on Amazon S3 only
C. Store one IAM user's access keys in the state machine definition
D. Create a separate IAM execution role for each Lambda function with only the permissions that function needs


**Câu 44.** An AWS Lambda function is triggered by an Amazon SQS queue. During traffic spikes, messages must not be lost, failed messages must be retried a limited number of times and then isolated, and successful messages must be removed automatically. Which configuration should be used?
A. Configure the Lambda function to poll the queue manually with a scheduled rule and delete all messages on each run
B. Configure the queue as the Lambda event source with a dead-letter queue and a maxReceiveCount on the source queue's redrive policy
C. Use an SNS topic instead of SQS and disable Lambda retries
D. Increase Lambda memory and set the queue retention period to 60 seconds


**Câu 45.** A company runs an Amazon Aurora cluster with a primary instance and one read replica in the same Region. The application needs automatic failover to a synchronous standby with no data loss during an Availability Zone failure, rather than promotion of an asynchronous replica. Which configuration should a solutions architect recommend?
A. Use an Aurora Multi-AZ DB cluster deployment with a reader endpoint for failover
B. Keep only read replicas and rely on manual promotion
C. Take snapshots every hour and restore them during a failure
D. Use Aurora Global Database across two Regions

**Câu 46.** Multiple Amazon EC2 instances in different Availability Zones must read and write the same shared file system concurrently using standard POSIX semantics. The file system must be regional and highly available across AZs. Which storage service meets these requirements?
A. Amazon S3 mounted as a local file system on each instance
B. EC2 instance store volumes synchronized with a cron job
C. Amazon Elastic File System (Amazon EFS) in Regional mode mounted by instances in multiple AZs
D. A single Amazon EBS volume attached to instances in all AZs


**Câu 47.** A company must replicate objects from an Amazon S3 bucket in one Region to a bucket in another Region for disaster recovery. (Select TWO requirements for S3 Cross-Region Replication.)
A. Versioning must be enabled on both the source and destination buckets
B. The source bucket owner must have permissions to replicate objects, typically through an IAM role assumed by S3
C. Cross-Region Replication works only when both buckets have Block Public Access disabled
D. The destination bucket must be in the same Availability Zone as the source bucket
E. Objects must be stored in the S3 One Zone-IA storage class in both buckets


**Câu 48.** An Amazon EventBridge bus routes events to several targets. Occasionally a target is unavailable and events fail delivery. The team must capture failed events, investigate them, and replay archived events after the target is fixed. Which EventBridge features should be used?
A. AWS Step Functions Catch blocks for every rule
B. Amazon SQS FIFO deduplication and message group IDs
C. Dead-letter queues for targets and event archive and replay
D. EventBridge Scheduler and input transformers only


**Câu 49.** A containerized service runs on Amazon ECS behind an Application Load Balancer. The service must maintain a desired number of healthy tasks, replace unhealthy tasks automatically, and scale out when CPU utilization is high. Which ECS feature combination provides this?
A. A scheduled ECS task that runs once a day
B. A single standalone ECS task that is restarted manually
C. An ECS service with a desired count, ALB health checks, and Application Auto Scaling based on CPU utilization
D. An ECS task definition with host networking and no service


**Câu 50.** An Amazon DynamoDB table holds critical order data. The company must be able to restore the table to any point in time within the last 35 days after accidental deletes or writes. Which DynamoDB feature should be enabled?
A. On-demand capacity mode
B. DynamoDB Accelerator (DAX)
C. DynamoDB Streams with a 24-hour retention window only
D. Point-in-time recovery (PITR)


**Câu 51.** An AWS Lambda function that serves a latency-sensitive API has unpredictable cold starts that cause spikes above the required response time during business hours. The function is used continuously throughout the day. Which feature will keep execution environments initialized and ready to respond immediately?
A. Provisioned concurrency for the Lambda function
B. Reserved concurrency for the Lambda function
C. Increasing the function timeout to 15 minutes
D. Lambda SnapStart for Python functions only, with no other change


**Câu 52.** An Amazon ElastiCache for Redis workload has grown beyond the memory and throughput of a single node. The team needs to partition data across multiple shards while retaining Redis data structures within each shard. Which configuration should be used?
A. DynamoDB Accelerator (DAX) with a larger cluster
B. Memcached with a single large node
C. Redis with cluster mode disabled and a larger node type only
D. Redis cluster mode enabled with multiple shards and replicas


**Câu 53.** An Amazon Kinesis Data Streams application experiences hot shards because many records share the same partition key. Throughput per shard is exceeded even though total stream capacity seems sufficient. What is the MOST appropriate first action?
A. Distribute records across more varied partition keys and add shards or switch the stream to on-demand capacity mode
B. Reduce the retention period to 24 hours
C. Enable server-side encryption with a customer managed KMS key
D. Convert the stream to Kinesis Data Firehose

**Câu 54.** An application on Amazon EC2 needs a boot and data volume with consistently high IOPS and low latency for a transactional database, while a second workload needs a cost-effective general-purpose SSD volume with a balance of price and performance. Which pairing is correct?
A. st1 for the database, and Cold HDD (sc1) for the general-purpose workload
B. gp3 for the database with the lowest IOPS, and io2 for all general files
C. io2 or io2 Block Express for the database, and gp3 for the general-purpose workload
D. Instance store for the database with durability, and gp3 for backups only


**Câu 55.** A reporting application must run read queries against an Amazon Aurora PostgreSQL cluster without affecting the performance of the primary writer. Replica lag must stay minimal and the reporting endpoint must automatically include new replicas. Which solution should be used?
A. Direct reporting queries to the cluster (writer) endpoint during off-peak hours only
B. Copy the Aurora data to Amazon S3 hourly and query it with the reporting application
C. Increase the primary instance size and run all queries on the writer
D. Create Aurora read replicas and direct reporting queries to the Aurora reader endpoint


**Câu 56.** Users in multiple continents upload large files to a central Amazon S3 bucket. Uploads over long-distance networks are slow and unreliable for files larger than 1 GB. Which S3 practices will improve large uploads?
A. Compress all files into a single archive in S3 Glacier before users download them
B. Store large files on a single EBS volume and sync them nightly
C. Use multipart upload for large objects, and consider S3 Transfer Acceleration for long-distance uploads
D. Upload each large file in a single request over HTTP without retries


**Câu 57.** A fault-tolerant batch processing workload runs on Amazon ECS and can handle interruptions with checkpointing. The workload does not need guaranteed capacity and cost is the main concern. (Select TWO best practices for this workload on Spot capacity.)
A. Design the application to checkpoint progress and handle task interruptions gracefully
B. Use Spot Instances for a latency-sensitive primary database with no replication
C. Store all intermediate state only in local container memory with no external storage
D. Use Spot Instances or Fargate Spot for the ECS tasks
E. Request the highest possible Spot price in a single Availability Zone to guarantee no interruptions


**Câu 58.** An AWS Lambda function is allocated 3 GB of memory but typically uses very little CPU and finishes quickly. Billing analysis suggests the function is over-provisioned for its workload, while another function is CPU-bound and finishes faster with more memory. Which principle should guide cost optimization for Lambda?
A. Always set every Lambda function to the maximum memory to reduce cost
B. Tune the memory allocation for each function, because memory also controls CPU, and measure duration versus cost to find the lowest total cost per invocation
C. Always set every Lambda function to the minimum memory to reduce cost
D. Increase the timeout setting to reduce the number of invocations billed


**Câu 59.** A worker polls an Amazon SQS queue that is often empty. The application makes many empty ReceiveMessage calls, increasing cost and unnecessary API traffic. Which SQS feature reduces empty receives?
A. Enable short polling with WaitTimeSeconds set to 0
B. Enable FIFO ordering on a standard queue
C. Enable long polling by setting WaitTimeSeconds to a value greater than 0, such as 20 seconds
D. Reduce the message retention period to 60 seconds


**Câu 60.** A VPC has private subnets in three Availability Zones, each with its own NAT gateway. Finance asks to reduce cost, while architecture requires high availability. A proposal suggests using a single NAT gateway for all AZs. Which statement correctly evaluates this tradeoff?
A. NAT gateways are free, so the number deployed does not affect cost
B. A single NAT gateway improves both cost and high availability in all cases
C. A single NAT gateway reduces cost but creates a single point of failure and can incur cross-AZ data transfer charges if one AZ fails or traffic crosses AZs
D. Each private subnet must use an internet gateway instead of a NAT gateway to save cost


**Câu 61.** A company commits to a consistent level of compute usage for 1 year across multiple instance families, Regions, and services including Amazon EC2, AWS Fargate, and AWS Lambda. The company wants the flexibility to change instance families without losing the discount. (Select TWO correct statements about Compute Savings Plans.)
A. Compute Savings Plans require the company to commit to a specific instance family in a specific Region
B. Compute Savings Plans provide capacity reservation in a specific Availability Zone
C. Compute Savings Plans offer flexibility to change instance family, size, Region, and compute service while retaining the discount commitment
D. Compute Savings Plans automatically apply across EC2, Fargate, and Lambda usage
E. Compute Savings Plans can be interrupted and reclaimed by AWS like Spot Instances


**Câu 62.** A session table in Amazon DynamoDB contains millions of expired session items that are no longer needed. Manually deleting them consumes write capacity and adds cost. Which DynamoDB feature deletes expired items automatically at no extra throughput cost?
A. Point-in-time recovery (PITR)
B. Time to Live (TTL) with an attribute that stores the expiry timestamp
C. DynamoDB Streams with a Lambda function that deletes items continuously
D. DynamoDB Accelerator (DAX) cache eviction


**Câu 63.** Analysts run Amazon Athena queries over data in Amazon S3. Queries are expensive because Athena scans large amounts of CSV data for every query, even when analysts filter by a single date. (Select TWO actions that will reduce Athena cost and improve performance.)
A. Disable the AWS Glue Data Catalog so every query scans all files
B. Convert the data to a columnar format such as Parquet
C. Store the data as many small uncompressed CSV files with no partitioning
D. Run queries more frequently so Athena caches the full data set permanently
E. Partition the data in S3 by the filter column, such as date, so queries scan only relevant partitions


**Câu 64.** A shared file system on Amazon EFS contains project files. Most files are not accessed after 30 days, but must remain available with low latency when occasionally needed. Storage costs must be reduced without manual file movement. Which EFS feature should be used?
A. Enable EFS lifecycle management to transition infrequently accessed files to the EFS Infrequent Access (IA) storage class
B. Create a second EFS file system in another Region and replicate all files
C. Copy files manually to Amazon S3 Glacier and delete them from EFS after 30 days
D. Switch the file system to Max I/O performance mode

**Câu 65.** A company must archive backup data in Amazon S3 for 5 years for compliance. The data is almost never accessed, but when an audit occurs it must be retrievable within a few hours. The company wants the lowest storage cost that still meets this retrieval requirement. Which S3 storage class is MOST appropriate?
A. S3 Standard-IA
B. S3 Intelligent-Tiering with no archive tiers enabled
C. S3 Glacier Flexible Retrieval
D. S3 Standard
