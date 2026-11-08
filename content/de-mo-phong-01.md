# Đề mô phỏng SAA-C03 — Bộ 01

**Hướng dẫn:** 65 câu, 130 phút, đạt 720/1000. Làm xong mới mở file đáp án. Mỗi câu chỉ chọn 1 đáp án đúng, trừ các câu ghi rõ "Select TWO" thì chọn 2 đáp án.

---

**Câu 1.** A company uses AWS Organizations with multiple OUs. The security team must ensure that no account, including member account administrators, can disable AWS CloudTrail or leave the organization. Which solution meets this requirement with the LEAST operational overhead?
A. Attach an SCP to the root of the organization that explicitly denies cloudtrail:StopLogging, cloudtrail:DeleteTrail, and organizations:LeaveOrganization.
B. Create an IAM policy in each member account that denies those actions and attach it to all administrator roles.
C. Use AWS Config rules in each account to detect when CloudTrail is disabled and automatically re-enable it.
D. Remove administrator access from all member accounts and require all changes through the management account.

**Câu 2.** A production application uses Amazon RDS for MySQL in a single Availability Zone. During an AZ failure, the application was unavailable for over an hour. The company needs automatic failover with no data loss for synchronous replication and minimal application changes. What should a solutions architect recommend?
A. Create a read replica in another Availability Zone and promote it manually when a failure occurs.
B. Enable Multi-AZ DB instance deployment with a standby in a different Availability Zone.
C. Take hourly EBS snapshots and restore the database in another Availability Zone during a failure.
D. Migrate to Amazon DynamoDB with global tables.

**Câu 3.** A company stores 500 TB of image archives in Amazon S3 Standard. The images are accessed frequently in the first 30 days, rarely after 90 days, and must be retrievable within a few hours after 1 year for compliance. The company wants the MOST cost-effective storage strategy.
A. Keep all objects in S3 Standard for their entire lifecycle.
B. Use an S3 Lifecycle policy to transition objects to S3 Standard-IA after 30 days, to S3 Glacier Flexible Retrieval after 90 days, and expire them after 7 years.
C. Use an S3 Lifecycle policy to transition objects to S3 One Zone-IA after 30 days and delete them after 90 days.
D. Copy all objects to S3 Glacier Deep Archive immediately after upload.

**Câu 4.** An application uses Amazon RDS for PostgreSQL. Read queries for reporting are slowing down the primary database and increasing CPU to 95%. The reporting workload can tolerate a few seconds of replication lag and must not affect write performance. What is the MOST appropriate solution?
A. Enable Multi-AZ deployment to offload reads to the standby instance.
B. Create an Amazon RDS read replica and direct reporting queries to the replica endpoint.
C. Increase the DB instance class to a larger size.
D. Enable RDS storage autoscaling.

**Câu 5.** A company must encrypt data in Amazon S3 using keys it can audit and control. The security team needs automatic annual rotation of the key material and a CloudTrail log of every key usage. Which solution meets these requirements?
A. Use S3-managed keys (SSE-S3) with bucket policies.
B. Use an AWS KMS customer managed key with automatic key rotation enabled for server-side encryption (SSE-KMS).
C. Use client-side encryption with keys stored in an on-premises server.
D. Use SSE-C with customer-provided keys sent on each request.

**Câu 6.** A global media company serves static images and videos from Amazon S3 through Amazon CloudFront. Origin requests are still high and users in Asia report slow load times for popular content that rarely changes. Which change will MOST improve performance and reduce origin load?
A. Increase the CloudFront default TTL and configure cache policies to cache popular objects longer at edge locations.
B. Move the S3 bucket to a Region in Asia.
C. Enable S3 Transfer Acceleration on the bucket.
D. Add a second S3 bucket and use Route 53 latency-based routing.

**Câu 7.** A company runs a web application on EC2 instances in Region us-east-1 with a standby environment in eu-west-1. If the primary Region fails, traffic must automatically move to the standby within minutes, based on health checks. Which Route 53 configuration should be used?
A. Simple routing policy with a health check on the primary endpoint.
B. Weighted routing policy with weights 100 for primary and 0 for standby.
C. Failover routing policy with health checks, primary record pointing to us-east-1 and secondary record pointing to eu-west-1.
D. Latency-based routing policy with health checks on both endpoints.

**Câu 8.** A batch processing job runs for 3 hours every night, can be interrupted and resumed without data loss, and currently runs on On-Demand EC2 instances. The company wants to reduce compute cost as much as possible for this workload. Which purchasing option should be used?
A. Standard Reserved Instances for 3 years, all upfront.
B. Convertible Reserved Instances for 1 year.
C. EC2 Spot Instances with a Spot Fleet and multiple instance types.
D. Dedicated Hosts.

**Câu 9.** A company stores private documents in Amazon S3. External auditors who have no AWS account need temporary access to download one specific document for the next 15 minutes only. The solution must follow least privilege. What should a solutions architect recommend?
A. Make the bucket public for 15 minutes and then revert the setting.
B. Create an IAM user for each auditor and share the credentials.
C. Generate an S3 presigned URL for that object with a 15-minute expiration.
D. Copy the document to a public website hosted on EC2.

**Câu 10.** A session-based web application stores frequently accessed session data in an RDS database, causing high read latency. The data is key-value, needs sub-millisecond latency, and can expire after 30 minutes. Which service is the BEST fit?
A. Amazon ElastiCache for Redis with TTL configured on session keys.
B. Amazon DynamoDB with DynamoDB Accelerator (DAX).
C. Amazon EFS.
D. Amazon RDS read replica.

**Câu 11.** A web application must remain available if one Availability Zone fails. It runs on EC2 behind an Application Load Balancer. Traffic varies predictably during the day. Which architecture provides high availability with the LEAST operational overhead?
A. One EC2 instance in each of two Regions behind a Route 53 simple record.
B. An Auto Scaling group spanning multiple Availability Zones in one Region, behind an Application Load Balancer, with target tracking scaling.
C. A single large EC2 instance with an Elastic IP and daily AMI backups.
D. EC2 instances in one AZ with Auto Scaling set to a fixed capacity of 1.

**Câu 12.** An EC2 instance in a private subnet must not be reachable from the internet on any port, but it must be able to initiate outbound HTTPS connections. A network engineer is deciding between security groups and network ACLs. Which statement correctly describes the control to use for instance-level, stateful filtering?
A. Use network ACLs, because they are stateful and apply to a single instance.
B. Use security groups, because they are stateful, apply at the instance/ENI level, and return traffic is automatically allowed.
C. Use network ACLs, because they support allow rules only and are stateful.
D. Use security groups, because they are stateless and require explicit inbound and outbound rules for return traffic.

**Câu 13.** A company uploaded 200 TB of log files to S3 Standard. Analysis shows 95% of the objects are never accessed after 45 days, but the access pattern for the remaining 5% is unknown and unpredictable. Manually classifying objects is not practical. Which S3 storage class will MOST reduce cost without a major performance penalty for the unpredictable objects?
A. S3 Glacier Deep Archive for all objects after 45 days.
B. S3 One Zone-IA for all objects after 45 days.
C. S3 Intelligent-Tiering with a lifecycle transition after 45 days.
D. Keep all objects in S3 Standard-IA.

**Câu 14.** A DynamoDB table for a product catalog experiences millions of reads per second from a product detail page. The same popular items are read repeatedly and read latency must be in microseconds. Writes are infrequent. Which solution will BEST improve read performance?
A. Enable DynamoDB Streams.
B. Add DynamoDB Accelerator (DAX) as a write-through cache in front of the table.
C. Increase the provisioned read capacity units to the maximum.
D. Create a global secondary index on the product name.

**Câu 15.** A developer needs temporary access to manage S3 and RDS from an EC2 instance for a production application. Long-term access keys have previously been leaked from a workstation. Which method follows AWS best practices for granting access from EC2?
A. Store an IAM user's access key and secret key in an environment file on the instance.
B. Attach an IAM role with an instance profile to the EC2 instance and grant least-privilege permissions in the role policy.
C. Use the AWS account root user credentials in the application configuration.
D. Embed access keys in the AMI so every new instance has the same credentials.

**Câu 16.** A company has an RPO of 24 hours and an RTO of 8 hours for a non-critical internal application. It wants the LOWEST-cost disaster recovery strategy that still restores data and infrastructure in another Region when needed. Which strategy should be used?
A. Multi-site active-active across two Regions.
B. Warm standby with a scaled-down environment running in the DR Region.
C. Pilot light with core data replicated to the DR Region.
D. Backup and restore, with backups copied to the DR Region and infrastructure recreated from templates during a disaster.

**Câu 17.** A company runs a steady-state, predictable database workload on EC2 instances 24/7 for at least 3 years and will not change instance family or Region. It wants the LARGEST discount for this specific instance configuration. Which purchasing option provides the highest discount?
A. Compute Savings Plans for 1 year, no upfront.
B. Standard Reserved Instances for 3 years, all upfront.
C. Convertible Reserved Instances for 3 years, partial upfront.
D. On-Demand Instances with a volume discount.

**Câu 18.** A company must ensure an S3 bucket containing customer data can never become public, even if a bucket policy or ACL is misconfigured by a developer. The control must apply at the bucket and account level. Which solution meets this requirement?
A. Enable S3 Block Public Access settings on the bucket and at the account level.
B. Enable S3 Versioning on the bucket.
C. Add a bucket policy that denies s3:GetObject to everyone.
D. Enable MFA Delete on the bucket.

**Câu 19.** A company is migrating a high-performance computing workload that requires very low latency and high throughput between EC2 instances for tightly coupled processing. Instances must communicate with each other as directly as possible. Which placement strategy should be used?
A. Spread placement group across multiple Availability Zones.
B. Partition placement group.
C. Cluster placement group in a single Availability Zone.
D. No placement group; launch instances in different Regions.

**Câu 20.** An application uses an Application Load Balancer and EC2 instances in two Availability Zones. To survive the loss of an entire AZ without manual intervention and keep serving traffic from the remaining AZ, which design is required?
A. Deploy instances in only one AZ and enable cross-zone load balancing.
B. Deploy the ALB and Auto Scaling group across multiple AZs so instances are registered in each AZ.
C. Use a Classic Load Balancer with a single instance and an Elastic IP.
D. Store session data on a single EBS volume shared by all instances.

**Câu 21.** An application on Lambda needs database credentials that must be automatically rotated every 30 days, with previous versions retained and rotation performed without application downtime. Hardcoding credentials is not allowed. Which service is the BEST choice?
A. AWS Systems Manager Parameter Store with a SecureString parameter.
B. AWS Secrets Manager with automatic rotation enabled using a rotation Lambda function.
C. Environment variables encrypted with an AWS KMS key in the Lambda configuration.
D. An encrypted file stored in Amazon S3.

**Câu 22.** A company's primary Region becomes unavailable. Core network and DNS data were continuously replicated to a DR Region, but compute resources are not running there. During a disaster, the team will start the required EC2 instances and scale them up. The RTO is a few hours and cost must stay low during normal operations. Which DR strategy is this?
A. Backup and restore.
B. Pilot light.
C. Warm standby.
D. Multi-site active-active.

**Câu 23.** An order processing system must preserve the exact order of messages for each customer and ensure each message is processed only once, even with multiple consumers in a group. Throughput per customer group is modest. Which queue type should be used?
A. Amazon SQS standard queue with visibility timeout increased.
B. Amazon SQS FIFO queue with a message group ID per customer and deduplication enabled.
C. Amazon SNS topic with multiple subscribers.
D. Amazon Kinesis Data Streams with one shard.

**Câu 24.** A company serves private S3 content through CloudFront. Users must not be able to bypass CloudFront and access the S3 bucket directly via its URL. The bucket must remain private. Which configuration achieves this?
A. Make the bucket public and rely on CloudFront signed URLs.
B. Use CloudFront Origin Access Control (OAC) and update the S3 bucket policy to allow access only from the CloudFront distribution.
C. Use a bucket policy that allows access from any IP address that CloudFront uses.
D. Enable S3 website hosting and set CloudFront to use the website endpoint.

**Câu 25.** A financial application has an RTO of minutes and an RPO of seconds. A scaled-down but fully functional version of the environment runs continuously in the DR Region and can be scaled up quickly during failover. Which DR strategy is described?
A. Backup and restore.
B. Pilot light.
C. Warm standby.
D. Snapshot copy once per day.

**Câu 26.** A company commits to a consistent amount of compute usage ($/hour) for 1 year across EC2, Lambda, and Fargate, and wants flexibility to change instance families, sizes, and Regions within EC2 while keeping a high discount. Which option is MOST suitable?
A. Standard Reserved Instances.
B. EC2 Instance Savings Plans.
C. Compute Savings Plans.
D. Spot Instances.

**Câu 27.** A healthcare company must encrypt EBS volumes and needs to understand how data keys are protected. A solutions architect explains envelope encryption with AWS KMS. Which statement is correct?
A. KMS stores the plaintext data key alongside the data for fast decryption.
B. A data key encrypts the data, and the KMS key encrypts the data key; only the encrypted data key is stored with the data.
C. The KMS key itself is sent to EC2 and used directly to encrypt every disk block.
D. Envelope encryption requires customers to manage master keys entirely outside AWS.

**Câu 28.** An application needs a shared file system that multiple EC2 instances in multiple Availability Zones can mount concurrently using the NFS protocol, with data automatically replicated across AZs. Which storage service meets this requirement?
A. Amazon EBS with Multi-Attach.
B. Instance store volumes.
C. Amazon EFS.
D. Amazon S3 mounted with a third-party tool.

**Câu 29.** A company must protect RDS database data against accidental deletion and be able to restore to any point in time within the last 7 days. It also needs automated backups with minimal manual work. Which feature should be enabled?
A. Create a read replica and rely on it as a backup.
B. Enable automated backups with a 7-day retention period to use point-in-time recovery.
C. Export the database manually to S3 once per month.
D. Enable Multi-AZ and assume no backups are needed.

**Câu 30.** An organization has separate OUs for Production and Development. Developers in Development must be prevented from launching large, expensive instance types, even if their IAM policies allow it. The control must apply to the entire Development OU. Which solution should be used?
A. Add a condition to each developer's IAM policy in each account.
B. Attach an SCP to the Development OU that denies ec2:RunInstances when the requested instance type is not in an approved list.
C. Use a VPC endpoint policy to block large instance launches.
D. Set a billing budget alert for the Development accounts.

**Câu 31.** A data analytics team stores access logs in S3. About 80% of objects are accessed once and then never again, but the team cannot predict which objects will be accessed again. After 30 days, retrieval can tolerate standard access latency but data must stay highly durable across multiple AZs. Which class BEST balances cost and risk?
A. S3 One Zone-IA.
B. S3 Intelligent-Tiering.
C. S3 Glacier Deep Archive.
D. S3 Standard, with no lifecycle policy.

**Câu 32.** Users in multiple continents experience high latency and frequent TCP connection issues when connecting to a single-Region application on EC2. The application uses a static public IP requirement for firewall allowlisting by partners. Which service will improve global performance and provide static anycast IPs?
A. Amazon CloudFront with a custom origin.
B. AWS Global Accelerator with an Application Load Balancer endpoint.
C. Route 53 geolocation routing.
D. S3 Transfer Acceleration.

**Câu 33.** A company uses Route 53 for a public website backed by an ALB. If the ALB endpoint becomes unhealthy, Route 53 must stop returning its IP address to clients. Which Route 53 feature must be configured and associated with the DNS record?
A. A Route 53 health check associated with the record, with DNS failover/evaluate target health enabled.
B. A weighted routing policy with equal weights.
C. A geoproximity routing policy.
D. DNSSEC signing for the hosted zone.

**Câu 34.** EC2 instances in private subnets need frequent, high-volume access to Amazon S3 and Amazon DynamoDB without traffic traversing the internet or a NAT gateway. The solution must be at no additional hourly charge for the endpoint itself. Which solution meets this requirement?
A. Create Interface VPC endpoints (AWS PrivateLink) for S3 and DynamoDB.
B. Create Gateway VPC endpoints for S3 and DynamoDB and add them to the private subnet route tables.
C. Place a NAT gateway in each private subnet.
D. Create an internet gateway and restrict access with security groups.

**Câu 35.** A company runs a CPU-intensive, non-critical workload on x86 EC2 instances and wants to reduce cost without changing application code significantly. The application is built for ARM and has been tested successfully. Which action provides a cost-performance benefit with minimal risk after testing?
A. Migrate the workload to AWS Graviton-based instances.
B. Move the workload to Dedicated Hosts.
C. Increase the instance size in the same x86 family.
D. Convert all instances to Standard Reserved Instances without testing.

**Câu 36.** A database application requires the lowest possible latency block storage directly attached to a single EC2 instance, with very high IOPS and durability handled by application-level replication across instances. Temporary data loss on instance failure is acceptable. Which storage is BEST?
A. Amazon EFS.
B. EC2 instance store (NVMe SSD).
C. Amazon EBS General Purpose SSD (gp3).
D. Amazon S3.

**Câu 37.** A regulated company must retain financial records in S3 for 7 years. Records must be impossible to delete or overwrite during the retention period, even by the account root user. Which feature must be used?
A. S3 Versioning with MFA Delete.
B. S3 Object Lock in compliance mode with a 7-year retention period.
C. A bucket policy that denies s3:DeleteObject.
D. S3 Glacier Vault Lock only, without Object Lock.

**Câu 38.** A company runs Amazon Aurora PostgreSQL in one Region and needs a disaster recovery solution in a second Region with an RPO of typically less than 1 second of lag and an RTO of less than 1 minute for a managed failover, while the secondary must support read queries during normal operations. (Select TWO)
A. Use Aurora Global Database with a secondary Region cluster.
B. The secondary cluster in Aurora Global Database can serve read queries with its own reader endpoint.
C. Restore daily snapshots in the second Region when a disaster occurs.
D. Use DMS to copy data once per day to the second Region.
E. Rely on Aurora Multi-AZ replicas in the same Region for cross-Region DR.

**Câu 39.** Several EC2 instances are consistently running at 15% CPU and 20% memory utilization. A finance team asks for a data-driven recommendation to rightsize instances and reduce waste. Which AWS tool provides resource-specific rightsizing recommendations based on utilization history?
A. AWS Trusted Advisor basic checks only.
B. AWS Compute Optimizer.
C. Amazon CloudWatch billing alarms.
D. AWS Cost Explorer forecasts only.

**Câu 40.** A security audit finds that developers have IAM policies granting full S3 access to all buckets. The company wants to identify unused permissions and generate a least-privilege policy based on actual access history. Which tool should be used?
A. AWS IAM Access Analyzer policy generation based on CloudTrail activity.
B. Amazon Macie.
C. AWS Trusted Advisor security checks.
D. Amazon Inspector.

**Câu 41.** An application must ingest a continuous stream of clickstream events at 500 MB/s, retain the data for 24 hours for replay, and allow multiple independent consumers to process the same data in order per partition key. Which service is BEST suited?
A. Amazon SQS standard queue.
B. Amazon Kinesis Data Streams with sufficient shards and enhanced fan-out or separate consumers.
C. Amazon SNS.
D. Amazon EventBridge with a schedule rule.

**Câu 42.** A company stores critical objects in S3 in us-east-1 and must keep a copy in eu-west-1 for disaster recovery. New objects must be replicated automatically, with versioning enabled on both buckets. Which feature should be configured?
A. S3 Cross-Region Replication between versioning-enabled buckets.
B. S3 Lifecycle policy with a transition to another Region.
C. AWS DataSync run manually once per month.
D. S3 Batch Copy run on demand.

**Câu 43.** A company must ensure all data in transit between clients and its Application Load Balancer uses TLS, with certificates automatically renewed and no manual certificate management. Which service should be used for the certificates?
A. Store a self-signed certificate on each EC2 instance.
B. Use AWS Certificate Manager (ACM) certificates on the ALB with automatic renewal.
C. Use an S3 bucket to host the certificate files.
D. Use AWS KMS to generate TLS certificates for the ALB.

**Câu 44.** A company runs a nightly ETL job that queries only a small subset of columns and rows from 10 TB of CSV data stored in S3. Running a full cluster for this query is expensive. Which approach is MOST cost-effective for ad hoc queries directly on S3 data?
A. Load all data into Amazon Redshift every night before querying.
B. Use Amazon Athena with partitioned data and a columnar format such as Parquet to reduce scanned data.
C. Copy data to EBS volumes and query with EC2 instances.
D. Use Amazon RDS for MySQL to import the CSV files.

**Câu 45.** A product recommendation engine needs a fast in-memory data store that supports sorted sets, leaderboards, and geospatial queries, with persistence and automatic failover. Which ElastiCache engine is the BEST fit?
A. ElastiCache for Memcached.
B. ElastiCache for Redis (Valkey/Redis OSS) with Multi-AZ automatic failover.
C. DynamoDB DAX.
D. Amazon RDS read replica.

**Câu 46.** A stateless containerized application runs on Amazon ECS with Fargate. It must survive an AZ failure automatically and scale based on request count without managing EC2 instances. Which configuration achieves this?
A. Deploy the ECS service in one AZ with a desired count of 1.
B. Deploy the ECS service across multiple AZs in a VPC, behind an ALB, with Application Auto Scaling.
C. Run containers on a single EC2 instance with ECS.
D. Use ECS with a capacity provider of one Dedicated Host.

**Câu 47.** A public web application must be protected against common web exploits such as SQL injection and cross-site scripting at the application layer, and against large-scale DDoS attacks at the network edge. (Select TWO)
A. Attach AWS WAF to the Application Load Balancer or CloudFront distribution with managed rule groups for SQL injection and XSS.
B. Enable AWS Shield Advanced or rely on AWS Shield Standard for DDoS protection at no additional configuration for supported resources.
C. Use security groups to inspect HTTP request bodies for SQL injection patterns.
D. Use S3 Block Public Access to filter web exploits.
E. Use Route 53 health checks to block SQL injection.

**Câu 48.** A new application has unpredictable DynamoDB traffic with sharp, infrequent spikes. The team wants to avoid capacity planning and throttling, and is willing to pay per request rather than provision capacity that sits idle. Which capacity mode is MOST cost-effective for this pattern?
A. Provisioned capacity with a fixed high RCU/WCU set for peak load.
B. Provisioned capacity with Auto Scaling set to a minimum of peak load.
C. DynamoDB on-demand capacity mode.
D. Use RDS instead to avoid DynamoDB capacity settings.

**Câu 49.** Many Lambda functions and EC2 applications open thousands of short-lived connections to an RDS database, causing "too many connections" errors and uneven load. The company wants connection pooling and reduced failover time without changing application code significantly. Which service should be placed in front of RDS?
A. Amazon RDS Proxy.
B. Amazon ElastiCache for Memcached.
C. An Application Load Balancer in front of the database.
D. Amazon Route 53 weighted records for the DB endpoint.

**Câu 50.** A company manages hundreds of accounts and needs a centralized backup solution that can enforce backup policies across accounts and Regions, with reporting and no per-server agent management for AWS resources such as EBS, RDS, and DynamoDB. Which service meets this requirement?
A. Manually create snapshots in each account.
B. AWS Backup with backup plans and an organization-wide backup policy.
C. S3 Lifecycle policies for all resources.
D. AWS Systems Manager Run Command to copy data nightly.

**Câu 51.** Employees of a company need single sign-on access to multiple AWS accounts in AWS Organizations using their existing corporate identity provider credentials, without creating separate IAM users in each account. Which solution should be implemented?
A. Create an IAM user for each employee in every AWS account.
B. Use IAM Identity Center integrated with the external identity provider and assign permission sets to accounts.
C. Share one IAM user and password among all employees.
D. Store corporate passwords in Secrets Manager.

**Câu 52.** An Auto Scaling group runs a fault-tolerant workload that can mix purchasing options. The company needs a guaranteed baseline of capacity that is always available, plus additional low-cost capacity that can be interrupted for the flexible portion. Which configuration is BEST?
A. Use only Spot Instances for the entire group.
B. Use a mixed instances policy with On-Demand Instances for the baseline capacity and Spot Instances for capacity above the baseline.
C. Use only Dedicated Hosts for all capacity.
D. Use a fixed number of On-Demand Instances with no Auto Scaling.

**Câu 53.** A query workload on large datasets in S3 needs interactive SQL analysis by many analysts. Data is structured, queries are ad hoc, and the team does not want to manage servers or load data into a database first. Which service is BEST?
A. Amazon Athena.
B. Amazon RDS for PostgreSQL.
C. Amazon EMR with a long-running cluster kept idle 24/7.
D. Amazon EC2 instances with a self-managed database.

**Câu 54.** An application deployed with Elastic Beanstalk needs a deployment that minimizes downtime and allows immediate rollback if the new version fails health checks, by swapping environment URLs. Which deployment approach in Elastic Beanstalk provides this?
A. All-at-once deployment to the existing environment.
B. Blue/green deployment by creating a new environment and swapping CNAMEs after validation.
C. Delete the old environment before deploying the new version.
D. In-place deployment without health checks.

**Câu 55.** EC2 instances in private subnets need to call AWS APIs such as SSM and Secrets Manager, but the VPC must have no internet gateway and no NAT gateway. Outbound internet access must be completely blocked. Which solution allows access to those AWS services privately?
A. Add an internet gateway and allow 0.0.0.0/0 in the route table.
B. Create Interface VPC endpoints (AWS PrivateLink) for the required services and associate them with the private subnets.
C. Use a public subnet for the instances instead.
D. Peer the VPC with a VPC that has internet access.

**Câu 56.** A company stores backup data that is rarely accessed and can be recreated from other sources if an Availability Zone is lost. It wants the lowest-cost S3 storage class that still provides 99.5% availability for infrequently accessed data stored in a single AZ. Which class should be chosen, accepting the AZ-loss risk?
A. S3 Standard.
B. S3 Standard-IA.
C. S3 One Zone-IA.
D. S3 Intelligent-Tiering.

**Câu 57.** A database workload requires sustained 80,000 IOPS, low single-digit millisecond latency, and up to 64 TB of block storage per volume that persists independently of a single instance's lifetime and can be reattached after an instance failure. Which EBS volume type is BEST?
A. General Purpose SSD (gp3) with default settings.
B. Throughput Optimized HDD (st1).
C. Provisioned IOPS SSD (io2 / io2 Block Express).
D. Cold HDD (sc1).

**Câu 58.** A company needs synchronous replication of database writes so that a standby copy always has the same data as the primary at failover, with no data loss, within a single Region. Asynchronous cross-Region replication alone is not acceptable as the primary HA mechanism. Which concept describes the correct in-Region design?
A. Use read replicas with asynchronous replication as the HA standby.
B. Use Multi-AZ deployment, which uses synchronous replication to a standby in another AZ.
C. Copy snapshots to another Region every hour.
D. Use S3 Cross-Region Replication for the database files.

**Câu 59.** A new AWS account's root user must be secured immediately after creation. The company wants to prevent root user compromise and ensure day-to-day work never uses root. Which action is MOST important to do first?
A. Create an IAM user with full administrator access and share it among the team.
B. Enable MFA on the root user, set a strong password, and delete/create no root access keys; use IAM roles/users for daily work.
C. Enable S3 Versioning in the account.
D. Create a billing alarm for the root user.

**Câu 60.** A company wants to lower EC2 cost for instances that are stopped at night. Developers forget to stop test instances, which then run idle for days. Which approach will MOST reduce cost with the LEAST ongoing manual effort for these non-production instances?
A. Require developers to remember to stop instances manually every day.
B. Use AWS Instance Scheduler / EventBridge Scheduler with Lambda or Systems Manager to automatically stop instances on a schedule, and use hibernation or stop (not terminate) where appropriate.
C. Convert all test instances to 3-year Reserved Instances.
D. Increase the instance size so jobs finish faster.

**Câu 61.** Which TWO practices follow IAM least-privilege and security best practices for a production AWS account? (Select TWO)
A. Grant permissions through IAM groups/roles with policies scoped to only the actions and resources needed for the job.
B. Require MFA for human users signing in to the AWS Management Console.
C. Share long-term access keys among team members to simplify rotation.
D. Use the root user for daily application deployment tasks.
E. Grant AdministratorAccess to all developers to avoid permission errors.

**Câu 62.** A company wants a highly available architecture for a three-tier web application in a single Region. Which TWO design choices are required for high availability across Availability Zones? (Select TWO)
A. Deploy the Application Load Balancer and application instances across at least two Availability Zones.
B. Use Amazon RDS Multi-AZ with a synchronous standby in a different Availability Zone.
C. Store all application data on a single EBS volume in one AZ.
D. Place all EC2 instances in a single AZ to reduce latency.
E. Use a single NAT gateway in one AZ with no redundancy plan and consider the design fully HA.

**Câu 63.** Which TWO actions will MOST improve performance for a read-heavy application serving users worldwide from data stored in S3 and RDS? (Select TWO)
A. Use Amazon CloudFront to cache static S3 content at edge locations close to users.
B. Create RDS read replicas and route read traffic to them.
C. Route all reads through a single small EC2 instance in one AZ.
D. Disable caching to ensure every request reaches the origin.
E. Increase the RDS primary instance's workload by adding reporting queries to it.

**Câu 64.** A company wants to reduce its AWS bill without reducing reliability for production workloads. Which TWO actions are generally cost-effective and low risk? (Select TWO)
A. Use S3 Lifecycle policies to transition older, infrequently accessed objects to cheaper storage classes.
B. Purchase Savings Plans or Reserved Instances for steady-state, predictable baseline usage after analyzing usage in Cost Explorer.
C. Delete all backups and snapshots immediately after creation.
D. Run production databases on Spot Instances as the only copy.
E. Keep idle, unattached EBS volumes and unused Elastic IPs indefinitely.

**Câu 65.** A company must protect sensitive S3 data with encryption and controlled access. Which TWO configurations together provide strong protection for data at rest and in transit/access control? (Select TWO)
A. Enable default encryption with SSE-KMS using a customer managed key and restrict key usage via the KMS key policy.
B. Require TLS (aws:SecureTransport) and deny non-TLS requests in the bucket policy, combined with least-privilege bucket policies.
C. Make the bucket public so encryption can be validated by anyone.
D. Disable S3 Block Public Access to simplify access.
E. Store access keys for the bucket in a public code repository.
