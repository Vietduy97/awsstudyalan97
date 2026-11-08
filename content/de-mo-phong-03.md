# Đề mô phỏng SAA-C03 — Bộ 03

65 câu, 130 phút, đạt 720/1000.

**Câu 1.** A company is building a complete three-tier web application. The web and application tiers must scale automatically, survive the loss of one Availability Zone, and the database tier must fail over automatically with no data loss during a planned AZ maintenance. Which architecture meets these requirements?
A. EC2 instances in one AZ behind an Application Load Balancer, with a single RDS instance and manual snapshots
B. Application Load Balancer across multiple AZs, an Auto Scaling group of EC2 instances in private subnets across multiple AZs, and Amazon RDS deployed with Multi-AZ
C. Network Load Balancer in one AZ, EC2 instances in public subnets, and Amazon DynamoDB with on-demand capacity
D. CloudFront, Amazon S3 static hosting, and a single EC2 instance running a self-managed database

**Câu 2.** A solutions architect is about to update a production CloudFormation stack that contains an RDS database and an Auto Scaling group. Before applying the update, the architect must preview exactly which resources will be added, modified, or replaced, and obtain approval. What should the architect do?
A. Enable termination protection and update the stack directly
B. Use CloudFormation drift detection on the stack
C. Create a change set for the stack, review the proposed changes, and then execute the change set
D. Create a new stack from the updated template and delete the old stack

**Câu 3.** A company wants to migrate an on-premises Oracle database to Amazon Aurora PostgreSQL with minimal downtime. The source and target database engines are different, so the schema must be converted as part of the migration. Which combination of services should be used?
A. AWS DataSync and Amazon S3
B. AWS Snowball and AWS Storage Gateway
C. AWS Schema Conversion Tool (SCT) to convert the schema, and AWS DMS to replicate the data with ongoing replication
D. Amazon RDS snapshots and AWS CloudFormation

**Câu 4.** A gaming company runs a real-time multiplayer game using a custom UDP protocol. Players are in multiple continents and complain about inconsistent latency and packet routing over the public internet. The company also needs two static IP addresses that clients can hard-code. Which service should the company use?
A. Amazon CloudFront with origin shield
B. AWS Global Accelerator with a Network Load Balancer endpoint
C. Amazon Route 53 latency-based routing to regional EC2 instances
D. AWS Direct Connect to each player region

**Câu 5.** A company stores audit logs in Amazon S3. The logs are accessed frequently for the first 30 days, rarely for the next 60 days, and must then be retained for 7 years for compliance but are almost never accessed. The company wants the lowest storage cost while meeting these access patterns. What should a solutions architect recommend?
A. Keep all objects in S3 Standard for 7 years
B. Use an S3 Lifecycle configuration to transition objects to S3 Standard-IA after 30 days and to S3 Glacier Deep Archive after 90 days
C. Transition objects to S3 One Zone-IA after 30 days and delete them after 90 days
D. Store the logs on Amazon EBS volumes attached to EC2 instances

**Câu 6.** A security team discovered that an Amazon S3 bucket was deleted last week. They need to identify who deleted the bucket, when the action occurred, and from which IP address the request came. Which service provides this information?
A. Amazon CloudWatch metrics
B. AWS Config configuration history
C. AWS CloudTrail event history
D. AWS Trusted Advisor

**Câu 7.** A company wants its applications in a VPC to access an Amazon SQS queue and a partner SaaS application without traffic traversing the public internet. The security team also requires that the traffic stay on the AWS network. Which solutions meet these requirements? (Select TWO.)
A. Create a VPC interface endpoint for Amazon SQS powered by AWS PrivateLink
B. Place the EC2 instances in public subnets with Elastic IP addresses
C. Use AWS PrivateLink to access the partner SaaS application exposed through a Network Load Balancer
D. Create an internet gateway and route all traffic through it for inspection
E. Use Amazon CloudFront as a reverse proxy for SQS

**Câu 8.** A financial company needs a dedicated, private connection between its data center and AWS with consistent bandwidth and lower latency than an internet-based connection. The connection will carry sensitive workloads permanently. Which solution should the company choose?
A. AWS Site-to-Site VPN over the internet
B. AWS Direct Connect
C. Amazon CloudFront signed URLs
D. VPC peering to the data center

**Câu 9.** A company is releasing a new version of its application to production. It wants to send 10% of user traffic to the new version hosted in a second Region and 90% to the current version, and adjust the proportions gradually. Which Route 53 routing policy should be used?
A. Latency-based routing
B. Geolocation routing
C. Weighted routing
D. Failover routing

**Câu 10.** A mobile application has thousands of retail users who sign up with email and password and sign in to access an API. The company does not want to build its own identity store or custom authentication logic. The API is hosted behind Amazon API Gateway. Which authorization mechanism is the MOST appropriate?
A. IAM authorization with SigV4 signed by each retail user
B. Amazon Cognito user pool authorizer in API Gateway
C. AWS WAF IP allow list
D. API keys alone as the authentication mechanism

**Câu 11.** A company has 40 VPCs across multiple accounts and needs to connect all VPCs to each other and to an on-premises network through a central hub. Managing individual VPC peering connections has become operationally unmanageable. Which solution provides scalable hub-and-spoke connectivity?
A. Create a full mesh of VPC peering connections
B. Use AWS Transit Gateway with route tables to centrally manage connectivity
C. Use an internet gateway in each VPC
D. Use VPC endpoints between every pair of VPCs

**Câu 12.** A company requires a disaster recovery strategy in a second Region. A scaled-down but fully functional copy of the production environment must run continuously in the DR Region, and it must be able to scale up quickly during a failover. Recovery time must be faster than a backup-and-restore approach but the company accepts higher cost than pilot light. Which DR strategy is this?
A. Backup and restore
B. Pilot light
C. Warm standby
D. Multi-site active-active

**Câu 13.** An operations team suspects that someone manually changed a security group rule that was originally deployed by CloudFormation. They need to identify whether the actual state of stack resources differs from the template's expected configuration. What should they use?
A. CloudFormation change sets
B. CloudFormation drift detection
C. AWS CloudTrail Lake
D. Amazon CloudWatch alarms

**Câu 14.** A company needs to continuously synchronize 500 TB of file data from an on-premises NFS file system to Amazon S3 for a migration. The synchronization must be automated, handle large-scale transfers efficiently, preserve metadata, and can run over the network on a schedule. Which service is MOST appropriate?
A. AWS DataSync
B. AWS Snowball console manual copy
C. Amazon S3 Transfer Acceleration with manual uploads
D. AWS Storage Gateway Tape Gateway

**Câu 15.** Several EC2 instances have averaged 8% CPU utilization for the past three months. A finance team asks for a data-driven recommendation to rightsize the instances based on actual utilization history. Which AWS tool should be used?
A. AWS Cost Explorer forecasting only
B. AWS Compute Optimizer
C. AWS Config rules
D. Amazon CloudWatch Logs Insights

**Câu 16.** Applications running in private subnets must send messages to Amazon SQS. The security policy forbids internet access from these subnets, and there must be no NAT gateway route for this traffic. How can the applications access SQS?
A. Add an internet gateway to the private subnets
B. Create a gateway VPC endpoint for SQS
C. Create an interface VPC endpoint for SQS using AWS PrivateLink
D. Deploy a public proxy EC2 instance in a public subnet

**Câu 17.** A compliance team archived objects in S3 Glacier Flexible Retrieval. During an urgent legal investigation, they need to retrieve a small set of objects within a few minutes and are willing to pay a premium for the fastest retrieval. Which retrieval option should they choose?
A. Bulk retrieval
B. Standard retrieval
C. Expedited retrieval
D. S3 Batch Replication

**Câu 18.** A company wants to protect a production CloudFormation stack from accidental updates or deletions, especially for its stateful RDS resource. Which actions help achieve this? (Select TWO.)
A. Apply a CloudFormation stack policy that denies updates to the protected RDS resource
B. Enable termination protection on the stack
C. Disable CloudTrail logging for the stack
D. Store the template in a public S3 bucket
E. Use a change set without reviewing it

**Câu 19.** A startup needs to connect its office to a VPC within a few hours. Cost must be low, the connection will use the public internet, and variable bandwidth and latency are acceptable for now. Which solution meets these requirements?
A. Order a new AWS Direct Connect connection
B. Set up an AWS Site-to-Site VPN
C. Ship data with AWS Snowball
D. Deploy AWS Global Accelerator

**Câu 20.** A hybrid company runs applications both on premises and in AWS. Workloads in the VPC must resolve on-premises DNS names, and on-premises servers must resolve names in a Route 53 private hosted zone. Which solution provides this bidirectional DNS resolution?
A. Amazon CloudFront DNS routing
B. Route 53 Resolver with inbound and outbound endpoints and forwarding rules
C. AWS Direct Connect without DNS configuration
D. A public hosted zone for all internal names

**Câu 21.** A news website serves static images, CSS, and JavaScript files to a global audience. Users far from the origin Region experience slow downloads. The company wants to cache this static content close to users and reduce origin load. Which service is BEST suited?
A. AWS Global Accelerator
B. Amazon CloudFront
C. AWS Transit Gateway
D. Elastic Load Balancing

**Câu 22.** A compliance officer needs to be alerted whenever an S3 bucket is created without default encryption enabled, and wants a record of how each bucket's configuration changed over time. Which service should be used?
A. AWS Config with a managed rule for S3 bucket encryption
B. Amazon CloudWatch CPU metrics
C. AWS CloudTrail user sign-in events only
D. AWS Trusted Advisor cost checks

**Câu 23.** Factory systems on premises generate files that local applications need to access with low latency using standard file protocols, while the company wants the files durably stored in Amazon S3 in the cloud. Which service provides a local file interface backed by S3?
A. AWS DataSync agent only
B. Amazon S3 File Gateway (AWS Storage Gateway)
C. AWS Snowball Edge
D. Amazon EFS cross-Region replication

**Câu 24.** A remote research site has collected 80 TB of data. Its internet connection is very slow and unreliable, and transferring the data online would take months. The company needs to move this one-time dataset into Amazon S3. Which solution is MOST appropriate?
A. AWS Site-to-Site VPN
B. AWS Snowball
C. Amazon CloudFront upload
D. Route 53 Resolver endpoints

**Câu 25.** A central networking account created a VPC with shared subnets for application teams in multiple AWS accounts within an organization. Application teams must be able to launch resources into those subnets without each team creating its own VPC. Which service enables this sharing?
A. AWS Resource Access Manager (RAM) to share the subnets
B. VPC peering between every application account
C. Amazon Route 53 private hosted zones
D. AWS CloudFormation StackSets only

**Câu 26.** A global application runs identical deployments in three Regions. End users should automatically be directed to the Region that gives them the lowest network latency, based on measurements between the user and each Region. Which Route 53 routing policy should be used?
A. Simple routing
B. Weighted routing
C. Latency-based routing
D. Multivalue answer routing

**Câu 27.** An API uses an external identity provider that is not Amazon Cognito. For each request, custom logic must validate a proprietary token, check tenant permissions stored in a database, and return an IAM policy that API Gateway caches. Which API Gateway authorization mechanism fits best?
A. Cognito user pool authorizer
B. Lambda authorizer
C. IAM authorization only
D. API key validation only

**Câu 28.** A company cannot tolerate downtime for its global payment application. It runs the application actively in two Regions, both serving production traffic, with data replicated between Regions so either Region can handle all traffic immediately if the other fails. Which DR strategy gives the lowest RTO and RPO?
A. Backup and restore
B. Pilot light
C. Warm standby
D. Multi-site active-active

**Câu 29.** Which statements correctly describe AWS Global Accelerator? (Select TWO.)
A. It provides two static anycast IP addresses as a fixed entry point for an application
B. It routes traffic over the AWS global network to a healthy endpoint close to the user
C. It caches HTML and image content at edge locations like a CDN
D. It converts database schemas during migration
E. It provides a local file interface to Amazon S3

**Câu 30.** VPC A is peered with VPC B, and VPC B is peered with VPC C. Instances in VPC A cannot reach instances in VPC C through VPC B. What explains this behavior and the scalable alternative?
A. VPC peering supports transitive routing; check security groups only
B. VPC peering is non-transitive; use AWS Transit Gateway for transitive hub connectivity
C. VPC peering requires a NAT gateway in VPC B to forward traffic
D. VPC peering works only within the same Availability Zone; move VPC C

**Câu 31.** A web tier must automatically add EC2 instances when average CPU utilization exceeds 70% and remove instances when it falls below 30%. The metric data must come from continuous monitoring of the instances. Which service provides the metrics and alarms to trigger this scaling?
A. AWS CloudTrail
B. Amazon CloudWatch
C. AWS Config
D. AWS Trusted Advisor

**Câu 32.** Data in an S3 bucket is 100 TB. Objects are created once and must follow this rule: they cannot transition to S3 Standard-IA until they are at least 30 days old, and storage cost must be minimized for objects older than 90 days that are rarely accessed. A solutions architect configures a lifecycle rule. Which transition sequence respects S3 lifecycle constraints and minimizes cost?
A. Transition to Standard-IA on day 1, then to Glacier Flexible Retrieval on day 10
B. Transition to Standard-IA after 30 days, then to Glacier Flexible Retrieval or Glacier Deep Archive after 90 days
C. Keep objects in S3 Intelligent-Tiering for 30 days, then delete them
D. Transition directly from S3 Standard to Glacier Deep Archive on day 1 for all objects

**Câu 33.** A CloudFormation stack policy is attached to a production stack. An engineer attempts to update the stack in a way that would replace the production RDS database instance. The update must be blocked, while other non-critical resources can still be updated. How does the stack policy help?
A. It encrypts the RDS database at rest
B. It defines which stack operations are allowed or denied on specific resources during stack updates
C. It automatically backs up the database before every update
D. It detects drift between the template and actual resources

**Câu 34.** A company uses AWS Direct Connect as its primary hybrid connection and requires a backup connection that can take over if Direct Connect fails. The backup must be quick to set up and cost-effective, even if it uses the internet. Which backup solution should be implemented?
A. A second internet gateway
B. AWS Site-to-Site VPN as a backup to Direct Connect
C. Amazon S3 Transfer Acceleration
D. AWS Snowball Edge devices kept on site

**Câu 35.** An internal API must only be called by IAM principals from within the same AWS organization. Requests must be signed with AWS Signature Version 4, and no end-user sign-up flow is needed. Which API Gateway authorization type is MOST appropriate?
A. Amazon Cognito user pool authorizer
B. Lambda authorizer with a proprietary token
C. IAM authorization
D. No authorization with a public API

**Câu 36.** A finance team wants a quick, managed report identifying idle load balancers, underutilized EC2 instances, and unassociated Elastic IP addresses that are increasing the monthly bill. Which AWS service provides these ready-made cost optimization checks?
A. AWS Trusted Advisor
B. AWS Config
C. Amazon CloudWatch Logs
D. AWS CloudFormation

**Câu 37.** A Route 53 geoproximity routing policy is configured for resources in two Regions. The company wants to gradually shift more traffic to the US East Region by expanding its effective geographic area without moving any resources. Which setting should be adjusted?
A. Increase the bias value for the US East record
B. Decrease the TTL to zero
C. Enable health checks on the US West record only
D. Change the routing policy to simple routing

**Câu 38.** In a secure three-tier architecture, where should each component be placed?
A. Web, application, and database tiers all in public subnets for simplicity
B. Load balancer in public subnets, application instances in private subnets, and the database in private subnets with no direct internet route
C. Database in a public subnet, application instances in private subnets, and the load balancer in a private subnet
D. All tiers in a single private subnet with an internet gateway route

**Câu 39.** A company is migrating a live production database to Amazon RDS using AWS DMS. The source database must remain operational during migration, and changes made after the initial full load must also be replicated to the target to minimize cutover downtime. Which DMS capability should be used?
A. Full load only, performed once
B. Full load plus ongoing replication using Change Data Capture (CDC)
C. Manual CSV export and import
D. S3 Lifecycle transitions

**Câu 40.** A company wants to see exactly which service, account, and resource tag caused an unexpected cost spike last month, with a breakdown and filtering by those dimensions. Which tool should the finance team use first?
A. AWS Cost Explorer
B. Amazon CloudWatch alarms
C. AWS Config timeline
D. AWS CloudTrail event history

**Câu 41.** Which statements correctly describe AWS Direct Connect compared with a Site-to-Site VPN? (Select TWO.)
A. Direct Connect provides a dedicated private connection with consistent bandwidth
B. Direct Connect can be provisioned in minutes over the public internet with no physical connection
C. A Site-to-Site VPN runs over the internet and can typically be set up quickly at lower cost
D. A Site-to-Site VPN always provides higher and more consistent bandwidth than Direct Connect
E. Direct Connect traffic by default provides a public internet path for all users

**Câu 42.** An auditor asks: "What was the exact configuration of this EC2 security group three months ago, and when did its rules change?" Metrics and API caller identity alone are not enough. Which service answers the auditor's question?
A. Amazon CloudWatch
B. AWS CloudTrail
C. AWS Config configuration timeline
D. AWS Compute Optimizer

**Câu 43.** A company runs memory-intensive workloads on EC2. Standard CPU-based monitoring did not reveal that the instances are oversized for memory as well as CPU. The company wants recommendations that consider memory utilization collected by an agent. Which service provides these rightsizing recommendations?
A. AWS Compute Optimizer with the CloudWatch agent memory metrics enabled
B. AWS Trusted Advisor basic checks only
C. Amazon Route 53 health checks
D. AWS Storage Gateway metrics

**Câu 44.** A research team needs to restore 50 TB from S3 Glacier Flexible Retrieval for a project starting next week. The data is not urgent, and the team wants the cheapest retrieval option for this large volume. Which retrieval tier should they choose?
A. Expedited retrieval
B. Standard retrieval
C. Bulk retrieval
D. S3 Select on the archived objects in place

**Câu 45.** A SaaS provider wants to offer its service, hosted behind a Network Load Balancer in its own VPC, privately to customers in their VPCs. Customers should connect using private IP addresses in their own VPCs without VPC peering or internet exposure. Which solution should the provider use?
A. Expose the service with a public Application Load Balancer
B. Create a VPC endpoint service powered by AWS PrivateLink
C. Share the provider VPC using AWS RAM subnets
D. Set up VPC peering with every customer

**Câu 46.** A company uses Route 53 failover routing for a primary application in one Region and a secondary application in another Region. The secondary must receive traffic only when the primary is unhealthy. What must be configured for this to work correctly?
A. Route 53 health checks associated with the primary record
B. S3 Lifecycle rules on the application bucket
C. CloudFront origin failover groups only
D. Weighted records with equal weights

**Câu 47.** A platform team wants to reuse a proven three-tier design across many applications. The VPC, load balancer, application, and database layers should be deployable as separate reusable units that can be composed and updated independently within CloudFormation. Which approach should the team use?
A. Put every resource for every application into one monolithic template
B. Use nested stacks (or modular templates) so each tier is a reusable child stack referenced by a parent stack
C. Manually create each tier in the console for flexibility
D. Use AWS DMS to replicate the tiers

**Câu 48.** A company runs steady, always-on compute workloads across EC2, Fargate, and Lambda and wants a discount in exchange for a 1-year commitment to a consistent amount of compute usage, while keeping flexibility to change instance families and Regions. Which purchasing option fits best?
A. Standard Reserved Instances for a specific instance type only
B. Compute Savings Plans
C. Spot Instances for all workloads
D. On-Demand Instances with no commitment

**Câu 49.** Access patterns for a large set of S3 objects are unpredictable: some objects are accessed daily, others are untouched for months, and the pattern changes over time. The company wants to minimize storage cost automatically without creating and maintaining lifecycle rules for each pattern. Which S3 storage class should be used?
A. S3 Standard only
B. S3 Intelligent-Tiering
C. S3 Glacier Deep Archive for all objects
D. S3 One Zone-IA for all objects

**Câu 50.** An Auto Scaling group spans three Availability Zones. When an EC2 instance becomes impaired, the group must automatically terminate it and launch a healthy replacement, maintaining the desired capacity without manual intervention. Which combination enables this?
A. EC2 health checks and Auto Scaling health check replacement
B. CloudTrail event notifications sent to an administrator
C. Manual scaling scheduled once a week
D. S3 versioning and lifecycle expiration

**Câu 51.** A VPC interface endpoint for Amazon S3 is used by applications in a VPC. The security team wants to ensure that through this endpoint, users can access only one specific company bucket and no other S3 buckets. What should they configure?
A. A bucket policy on all public buckets
B. A VPC endpoint policy attached to the interface endpoint that allows access only to the specific bucket
C. A Route 53 private hosted zone for S3
D. An internet gateway route with a security group

**Câu 52.** A cost review finds an AWS account with rising storage and compute charges. Which actions directly reduce cost without harming production workloads? (Select TWO.)
A. Delete unattached EBS volumes and old, unneeded snapshots after verifying they are not required
B. Purchase additional On-Demand instances to increase capacity
C. Transition infrequently accessed S3 objects to a cheaper storage class using lifecycle rules
D. Disable all CloudWatch alarms to save monitoring effort
E. Keep idle Elastic IP addresses associated with stopped instances indefinitely

**Câu 53.** A mining site in a remote location has no reliable connectivity. It needs to collect data locally, run some local compute processing on the device, and later ship the device back to transfer petabyte-scale data into AWS. Which offering is designed for this?
A. AWS Snowball Edge with compute capabilities
B. Amazon CloudFront edge locations
C. AWS Site-to-Site VPN appliance
D. Route 53 Resolver inbound endpoint

**Câu 54.** A company encrypts its Site-to-Site VPN traffic, and now wants the same IPsec encryption for traffic traversing its AWS Direct Connect connection, which by itself does not provide that encryption over the private circuit. How can this be achieved?
A. Use a public virtual interface with a Site-to-Site VPN running over Direct Connect
B. Enable S3 default encryption on a bucket
C. Attach a WAF to the Direct Connect gateway
D. Use CloudTrail logging for the connection

**Câu 55.** An enterprise connects its on-premises data center to AWS Transit Gateway using Direct Connect Gateway. Over time it adds dozens of VPCs in multiple accounts. New VPCs should be able to communicate with on-premises networks through the same central gateway without building a new connection for each VPC. What makes this possible?
A. Transit Gateway acts as a central hub; attach each new VPC to the Transit Gateway and update its route tables
B. Each VPC requires its own Direct Connect connection by design
C. VPC peering between the data center and each VPC
D. A NAT instance in every VPC

**Câu 56.** A UDP-based voice application uses AWS Global Accelerator with endpoint groups in two Regions. If all endpoints in the primary Region become unhealthy, what does Global Accelerator do?
A. It caches voice packets at edge locations until the Region recovers
B. It automatically directs traffic to healthy endpoints in the next closest endpoint group based on health checks
C. It changes the application's static IP addresses to new addresses
D. It converts UDP traffic to HTTP and serves it from CloudFront

**Câu 57.** A company creates a private API in Amazon API Gateway that must be accessible only from a specific VPC using a VPC endpoint. No requests from the public internet should be allowed, even if the API URL is known. Which combination enforces this?
A. A public API with an API key shared with internal teams
B. A private API with a resource policy that allows the VPC endpoint and explicitly denies other sources
C. A Cognito authorizer with public sign-up enabled
D. CloudFront with a custom origin header

**Câu 58.** A hybrid DNS design uses Amazon Route 53 Resolver. Which components are required for bidirectional resolution between a VPC and an on-premises network? (Select TWO.)
A. A Resolver inbound endpoint in the VPC so on-premises servers can query Route 53 Resolver
B. A Resolver outbound endpoint in the VPC plus a forwarding rule so VPC workloads can query on-premises DNS servers
C. A CloudFront distribution for DNS queries
D. A public S3 bucket hosting zone files
E. A Snowball device acting as a DNS server

**Câu 59.** An application writes detailed application logs from EC2 instances. The operations team needs to search these logs, create filters for error patterns, and trigger an alarm when errors exceed a threshold. Which service should be used?
A. Amazon CloudWatch Logs with metric filters and CloudWatch alarms
B. AWS Config with configuration rules
C. AWS CloudTrail with event selectors only
D. Amazon S3 Glacier with vault lock

**Câu 60.** For a warm standby DR environment, production data is continuously replicated to an Amazon RDS database in the DR Region, where a smaller application stack is already running. During failover, what are the expected actions?
A. Restore the database from a weekly snapshot and build the entire application stack from scratch
B. Promote the replicated database, scale up the DR application capacity, and update Route 53 to direct traffic to the DR Region
C. Ship a Snowball device containing the latest data to the DR Region
D. Wait for S3 Cross-Region Replication to create the application servers

**Câu 61.** A bucket contains 10 TB of log objects. Keeping them in S3 Standard costs significantly more than in S3 Glacier Flexible Retrieval. The objects are accessed only for audits after 90 days. A manager proposes moving all objects to Glacier Flexible Retrieval on day 1 and retrieving them frequently during the first month for analysis. Why is this proposal flawed, and what is the better approach?
A. Glacier objects cannot ever be retrieved; keep everything in Standard forever
B. Frequent early retrievals incur retrieval costs and delays and Glacier is designed for archival access; keep recent logs in Standard or Standard-IA and transition to Glacier after the active analysis period (e.g., after 90 days)
C. S3 Glacier Flexible Retrieval is more expensive than Standard for storage; never use it
D. Lifecycle transitions happen instantly with no minimum storage duration considerations in any class

**Câu 62.** Several departments need access to a shared services VPC and to each other's VPCs only through approved central routing, with strict control over which VPCs can talk to each other. A single VPC peering mesh is rejected. Which design should a solutions architect propose?
A. AWS Transit Gateway with separate route tables to control which attachments can communicate
B. One public subnet shared by all departments
C. Internet gateways in every VPC with public routes between them
D. Amazon S3 as a message bus between VPCs

**Câu 63.** After a product launch, an account's bill doubled in one month. Leadership wants a visual breakdown of costs by service and by linked account for the last 6 months, including trends, without building a custom reporting pipeline. Which service should be used?
A. AWS Cost Explorer
B. Amazon CloudWatch dashboards for CPU metrics
C. AWS CloudFormation stack events
D. AWS Systems Manager inventory

**Câu 64.** Which statements about the relationship between CloudWatch, CloudTrail, and AWS Config are correct? (Select TWO.)
A. CloudWatch monitors performance metrics and logs and can raise alarms
B. CloudTrail records API activity showing who did what and when
C. AWS Config caches static web content at edge locations
D. CloudTrail is a content delivery network for archived logs
E. AWS Config is a relational database used for transactional workloads

**Câu 65.** A company is designing its final production architecture: a three-tier application deployed with CloudFormation across two Regions for disaster recovery, using Direct Connect for hybrid connectivity, S3 lifecycle policies for cost control, and Route 53 health checks for failover. Which combination BEST represents sound architecture across all these areas?
A. Single-AZ EC2 and RDS, manual DNS changes during failover, all data kept in S3 Standard indefinitely, and stack updates applied without review
B. Multi-AZ ALB and Auto Scaling group with Multi-AZ RDS in the primary Region, warm standby in the second Region, change sets reviewed before stack updates, Direct Connect with VPN backup, lifecycle transitions to cheaper S3 classes, and Route 53 failover routing driven by health checks
C. Public database instances in both Regions, VPC peering between all Regions for transitive routing, and CloudFront used for UDP gaming traffic
D. Pilot light with no data replication, Global Accelerator used to cache static images, and Glacier Expedited retrieval used for all routine daily access
