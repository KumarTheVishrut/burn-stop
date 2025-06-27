from pydantic import BaseModel
from typing import Optional
from enum import Enum
import uuid
from datetime import datetime

class CloudPlatform(str, Enum):
    aws = "aws"
    gcp = "gcp"
    azure = "azure"
    other = "other"

class ServiceType(str, Enum):
    # AWS Services (Core)
    ec2 = "ec2"
    s3 = "s3"
    rds = "rds"
    lambda_aws = "lambda"
    eks = "eks"
    ecs = "ecs"
    cloudfront = "cloudfront"
    route53 = "route53"
    vpc = "vpc"
    
    # AWS Services (Extended) - From aws_services.txt
    a4b = "a4b"  # Alexa for Business
    aiops = "aiops"  # Amazon AI Operations
    execute_api = "execute_api"  # Amazon API Gateway
    apigateway = "apigateway"  # Amazon API Gateway Management
    appflow = "appflow"  # Amazon AppFlow
    app_integrations = "app_integrations"  # Amazon AppIntegrations
    arc_zonal_shift = "arc_zonal_shift"  # Amazon Application Recovery Controller
    appstream = "appstream"  # Amazon AppStream 2.0
    athena = "athena"  # Amazon Athena
    dsql = "dsql"  # Amazon Aurora DSQL
    bedrock = "bedrock"  # Amazon Bedrock
    braket = "braket"  # Amazon Braket
    chime = "chime"  # Amazon Chime
    clouddirectory = "clouddirectory"  # Amazon Cloud Directory
    cloudfront_keyvaluestore = "cloudfront_keyvaluestore"  # Amazon CloudFront KeyValueStore
    cloudsearch = "cloudsearch"  # Amazon CloudSearch
    cloudwatch = "cloudwatch"  # Amazon CloudWatch
    applicationinsights = "applicationinsights"  # Amazon CloudWatch Application Insights
    application_signals = "application_signals"  # Amazon CloudWatch Application Signals
    evidently = "evidently"  # Amazon CloudWatch Evidently
    internetmonitor = "internetmonitor"  # Amazon CloudWatch Internet Monitor
    logs = "logs"  # Amazon CloudWatch Logs
    networkmonitor = "networkmonitor"  # Amazon CloudWatch Network Monitor
    oam = "oam"  # Amazon CloudWatch Observability Access Manager
    observabilityadmin = "observabilityadmin"  # Amazon CloudWatch Observability Admin Service
    synthetics = "synthetics"  # Amazon CloudWatch Synthetics
    codecatalyst = "codecatalyst"  # Amazon CodeCatalyst
    codeguru = "codeguru"  # Amazon CodeGuru
    codeguru_profiler = "codeguru_profiler"  # Amazon CodeGuru Profiler
    codeguru_reviewer = "codeguru_reviewer"  # Amazon CodeGuru Reviewer
    codeguru_security = "codeguru_security"  # Amazon CodeGuru Security
    codewhisperer = "codewhisperer"  # Amazon CodeWhisperer
    cognito_identity = "cognito_identity"  # Amazon Cognito Identity
    cognito_sync = "cognito_sync"  # Amazon Cognito Sync
    cognito_idp = "cognito_idp"  # Amazon Cognito User Pools
    comprehend = "comprehend"  # Amazon Comprehend
    comprehendmedical = "comprehendmedical"  # Amazon Comprehend Medical
    connect = "connect"  # Amazon Connect
    cases = "cases"  # Amazon Connect Cases
    profile = "profile"  # Amazon Connect Customer Profiles
    connect_campaigns = "connect_campaigns"  # Amazon Connect Outbound Campaigns
    voiceid = "voiceid"  # Amazon Connect Voice ID
    dlm = "dlm"  # Amazon Data Lifecycle Manager
    datazone = "datazone"  # Amazon DataZone
    detective = "detective"  # Amazon Detective
    devops_guru = "devops_guru"  # Amazon DevOps Guru
    docdb_elastic = "docdb_elastic"  # Amazon DocumentDB Elastic Clusters
    dynamodb = "dynamodb"  # Amazon DynamoDB
    dax = "dax"  # Amazon DynamoDB Accelerator (DAX)
    autoscaling = "autoscaling"  # Amazon EC2 Auto Scaling
    imagebuilder = "imagebuilder"  # Amazon EC2 Image Builder
    ec2_instance_connect = "ec2_instance_connect"  # Amazon EC2 Instance Connect
    eks_auth = "eks_auth"  # Amazon EKS Auth
    ebs = "ebs"  # Amazon Elastic Block Store
    ecr = "ecr"  # Amazon Elastic Container Registry
    ecr_public = "ecr_public"  # Amazon Elastic Container Registry Public
    elasticfilesystem = "elasticfilesystem"  # Amazon Elastic File System
    elasticmapreduce = "elasticmapreduce"  # Amazon Elastic MapReduce
    elastictranscoder = "elastictranscoder"  # Amazon Elastic Transcoder
    elasticache = "elasticache"  # Amazon ElastiCache
    emr_containers = "emr_containers"  # Amazon EMR on EKS (EMR Containers)
    emr_serverless = "emr_serverless"  # Amazon EMR Serverless
    events = "events"  # Amazon EventBridge
    pipes = "pipes"  # Amazon EventBridge Pipes
    scheduler = "scheduler"  # Amazon EventBridge Scheduler
    schemas = "schemas"  # Amazon EventBridge Schemas
    finspace = "finspace"  # Amazon FinSpace
    finspace_api = "finspace_api"  # Amazon FinSpace API
    forecast = "forecast"  # Amazon Forecast
    frauddetector = "frauddetector"  # Amazon Fraud Detector
    freertos = "freertos"  # Amazon FreeRTOS
    fsx = "fsx"  # Amazon FSx
    gamelift = "gamelift"  # Amazon GameLift
    gameliftstreams = "gameliftstreams"  # Amazon GameLift Streams
    groundtruthlabeling = "groundtruthlabeling"  # Amazon GroundTruth Labeling
    guardduty = "guardduty"  # Amazon GuardDuty
    honeycode = "honeycode"  # Amazon Honeycode
    inspector = "inspector"  # Amazon Inspector
    inspector2 = "inspector2"  # Amazon Inspector2
    inspector_scan = "inspector_scan"  # Amazon InspectorScan
    ivs = "ivs"  # Amazon Interactive Video Service
    ivschat = "ivschat"  # Amazon Interactive Video Service Chat
    kendra = "kendra"  # Amazon Kendra
    kendra_ranking = "kendra_ranking"  # Amazon Kendra Intelligent Ranking
    cassandra = "cassandra"  # Amazon Keyspaces (for Apache Cassandra)
    kinesisanalytics = "kinesisanalytics"  # Amazon Kinesis Analytics
    kinesis = "kinesis"  # Amazon Kinesis Data Streams
    firehose = "firehose"  # Amazon Kinesis Firehose
    kinesisvideo = "kinesisvideo"  # Amazon Kinesis Video Streams
    lex = "lex"  # Amazon Lex
    lightsail = "lightsail"  # Amazon Lightsail
    geo = "geo"  # Amazon Location
    geo_maps = "geo_maps"  # Amazon Location Service Maps
    geo_places = "geo_places"  # Amazon Location Service Places
    geo_routes = "geo_routes"  # Amazon Location Service Routes
    lookoutequipment = "lookoutequipment"  # Amazon Lookout for Equipment
    lookoutmetrics = "lookoutmetrics"  # Amazon Lookout for Metrics
    lookoutvision = "lookoutvision"  # Amazon Lookout for Vision
    machinelearning = "machinelearning"  # Amazon Machine Learning
    macie2 = "macie2"  # Amazon Macie
    managedblockchain = "managedblockchain"  # Amazon Managed Blockchain
    managedblockchain_query = "managedblockchain_query"  # Amazon Managed Blockchain Query
    grafana = "grafana"  # Amazon Managed Grafana
    aps = "aps"  # Amazon Managed Service for Prometheus
    kafka = "kafka"  # Amazon Managed Streaming for Apache Kafka
    kafkaconnect = "kafkaconnect"  # Amazon Managed Streaming for Kafka Connect
    airflow = "airflow"  # Amazon Managed Workflows for Apache Airflow
    mechanicalturk = "mechanicalturk"  # Amazon Mechanical Turk
    memorydb = "memorydb"  # Amazon MemoryDB
    ec2messages = "ec2messages"  # Amazon Message Delivery Service
    ssmmessages = "ssmmessages"  # Amazon Message Gateway Service
    mobileanalytics = "mobileanalytics"  # Amazon Mobile Analytics
    monitron = "monitron"  # Amazon Monitron
    mq = "mq"  # Amazon MQ
    neptune_db = "neptune_db"  # Amazon Neptune
    neptune_graph = "neptune_graph"  # Amazon Neptune Analytics
    nimble = "nimble"  # Amazon Nimble Studio
    one = "one"  # Amazon One Enterprise
    opensearch = "opensearch"  # Amazon OpenSearch
    osis = "osis"  # Amazon OpenSearch Ingestion
    aoss = "aoss"  # Amazon OpenSearch Serverless
    es = "es"  # Amazon OpenSearch Service
    personalize = "personalize"  # Amazon Personalize
    mobiletargeting = "mobiletargeting"  # Amazon Pinpoint
    ses = "ses"  # Amazon Pinpoint Email Service / SES
    sms_voice = "sms_voice"  # Amazon Pinpoint SMS and Voice Service
    polly = "polly"  # Amazon Polly
    q = "q"  # Amazon Q
    qbusiness = "qbusiness"  # Amazon Q Business
    qapps = "qapps"  # Amazon Q Business Q Apps
    qdeveloper = "qdeveloper"  # Amazon Q Developer
    wisdom = "wisdom"  # Amazon Q in Connect
    qldb = "qldb"  # Amazon QLDB
    quicksight = "quicksight"  # Amazon QuickSight
    rds_data = "rds_data"  # Amazon RDS Data API
    rds_db = "rds_db"  # Amazon RDS IAM Authentication
    redshift = "redshift"  # Amazon Redshift
    redshift_data = "redshift_data"  # Amazon Redshift Data API
    redshift_serverless = "redshift_serverless"  # Amazon Redshift Serverless
    rekognition = "rekognition"  # Amazon Rekognition
    tag = "tag"  # Amazon Resource Group Tagging API
    rhelkb = "rhelkb"  # Amazon RHEL Knowledgebase Portal
    route53domains = "route53domains"  # Amazon Route 53 Domains
    route53profiles = "route53profiles"  # Amazon Route 53 Profiles
    route53_recovery_cluster = "route53_recovery_cluster"  # Amazon Route 53 Recovery Cluster
    route53_recovery_control_config = "route53_recovery_control_config"  # Amazon Route 53 Recovery Controls
    route53_recovery_readiness = "route53_recovery_readiness"  # Amazon Route 53 Recovery Readiness
    route53resolver = "route53resolver"  # Amazon Route 53 Resolver
    s3express = "s3express"  # Amazon S3 Express
    glacier = "glacier"  # Amazon S3 Glacier
    s3_object_lambda = "s3_object_lambda"  # Amazon S3 Object Lambda
    s3_outposts = "s3_outposts"  # Amazon S3 on Outposts
    s3tables = "s3tables"  # Amazon S3 Tables
    sagemaker = "sagemaker"  # Amazon SageMaker
    sagemaker_data_science_assistant = "sagemaker_data_science_assistant"  # Amazon SageMaker data science assistant
    sagemaker_geospatial = "sagemaker_geospatial"  # Amazon SageMaker geospatial capabilities
    sagemaker_groundtruth_synthetic = "sagemaker_groundtruth_synthetic"  # Amazon SageMaker Ground Truth Synthetic
    sagemaker_mlflow = "sagemaker_mlflow"  # Amazon SageMaker with MLflow
    securitylake = "securitylake"  # Amazon Security Lake
    swf = "swf"  # Amazon Simple Workflow Service
    sdb = "sdb"  # Amazon SimpleDB
    sns = "sns"  # Amazon SNS
    sqs = "sqs"  # Amazon SQS
    textract = "textract"  # Amazon Textract
    timestream = "timestream"  # Amazon Timestream
    timestream_influxdb = "timestream_influxdb"  # Amazon Timestream InfluxDB
    transcribe = "transcribe"  # Amazon Transcribe
    translate = "translate"  # Amazon Translate
    verifiedpermissions = "verifiedpermissions"  # Amazon Verified Permissions
    vpc_lattice = "vpc_lattice"  # Amazon VPC Lattice
    vpc_lattice_svcs = "vpc_lattice_svcs"  # Amazon VPC Lattice Services
    workdocs = "workdocs"  # Amazon WorkDocs
    worklink = "worklink"  # Amazon WorkLink
    workmail = "workmail"  # Amazon WorkMail
    workmailmessageflow = "workmailmessageflow"  # Amazon WorkMail Message Flow
    workspaces = "workspaces"  # Amazon WorkSpaces
    wam = "wam"  # Amazon WorkSpaces Application Manager
    workspaces_web = "workspaces_web"  # Amazon WorkSpaces Secure Browser
    thinclient = "thinclient"  # Amazon WorkSpaces Thin Client
    mediaimport = "mediaimport"  # AmazonMediaImport
    kafka_cluster = "kafka_cluster"  # Apache Kafka APIs for Amazon MSK clusters
    arsenal = "arsenal"  # Application Discovery Arsenal
    account = "account"  # AWS Account Management
    activate = "activate"  # AWS Activate
    amplify = "amplify"  # AWS Amplify
    amplifybackend = "amplifybackend"  # AWS Amplify Admin
    amplifyuibuilder = "amplifyuibuilder"  # AWS Amplify UI Builder
    appmesh = "appmesh"  # AWS App Mesh
    appmesh_preview = "appmesh_preview"  # AWS App Mesh Preview
    apprunner = "apprunner"  # AWS App Runner
    appstudio = "appstudio"  # AWS App Studio
    a2c = "a2c"  # AWS App2Container
    appconfig = "appconfig"  # AWS AppConfig
    appfabric = "appfabric"  # AWS AppFabric
    application_autoscaling = "application_autoscaling"  # AWS Application Auto Scaling
    application_cost_profiler = "application_cost_profiler"  # AWS Application Cost Profiler Service
    discovery = "discovery"  # AWS Application Discovery Service
    mgn = "mgn"  # AWS Application Migration Service
    application_transformation = "application_transformation"  # AWS Application Transformation Service
    appsync = "appsync"  # AWS AppSync
    artifact = "artifact"  # AWS Artifact
    auditmanager = "auditmanager"  # AWS Audit Manager
    autoscaling_plans = "autoscaling_plans"  # AWS Auto Scaling
    b2bi = "b2bi"  # AWS B2B Data Interchange
    backup = "backup"  # AWS Backup
    backup_gateway = "backup_gateway"  # AWS Backup Gateway
    backup_search = "backup_search"  # AWS Backup Search
    backup_storage = "backup_storage"  # AWS Backup storage
    batch = "batch"  # AWS Batch
    billing = "billing"  # AWS Billing
    bcm_data_exports = "bcm_data_exports"  # AWS Billing And Cost Management Data Exports
    bcm_pricing_calculator = "bcm_pricing_calculator"  # AWS Billing And Cost Management Pricing Calculator
    billingconductor = "billingconductor"  # AWS Billing Conductor
    aws_portal = "aws_portal"  # AWS Billing Console
    budgets = "budgets"  # AWS Budget Service
    bugbust = "bugbust"  # AWS BugBust
    acm = "acm"  # AWS Certificate Manager
    chatbot = "chatbot"  # AWS Chatbot
    cleanrooms = "cleanrooms"  # AWS Clean Rooms
    cleanrooms_ml = "cleanrooms_ml"  # AWS Clean Rooms ML
    servicediscovery = "servicediscovery"  # AWS Cloud Map
    cloud9 = "cloud9"  # AWS Cloud9
    cloudformation = "cloudformation"  # AWS CloudFormation
    cloudhsm = "cloudhsm"  # AWS CloudHSM
    cloudshell = "cloudshell"  # AWS CloudShell
    cloudtrail = "cloudtrail"  # AWS CloudTrail
    cloudtrail_data = "cloudtrail_data"  # AWS CloudTrail Data
    rum = "rum"  # AWS CloudWatch RUM
    codeartifact = "codeartifact"  # AWS CodeArtifact
    codebuild = "codebuild"  # AWS CodeBuild
    codecommit = "codecommit"  # AWS CodeCommit
    codeconnections = "codeconnections"  # AWS CodeConnections
    codedeploy = "codedeploy"  # AWS CodeDeploy
    codedeploy_commands_secure = "codedeploy_commands_secure"  # AWS CodeDeploy secure host commands service
    codepipeline = "codepipeline"  # AWS CodePipeline
    codestar = "codestar"  # AWS CodeStar
    codestar_connections = "codestar_connections"  # AWS CodeStar Connections
    codestar_notifications = "codestar_notifications"  # AWS CodeStar Notifications
    compute_optimizer = "compute_optimizer"  # AWS Compute Optimizer
    config = "config"  # AWS Config
    awsconnector = "awsconnector"  # AWS Connector Service
    consoleapp = "consoleapp"  # AWS Console Mobile App
    consolidatedbilling = "consolidatedbilling"  # AWS Consolidated Billing
    controlcatalog = "controlcatalog"  # AWS Control Catalog
    controltower = "controltower"  # AWS Control Tower
    cur = "cur"  # AWS Cost and Usage Report
    ce = "ce"  # AWS Cost Explorer Service
    cost_optimization_hub = "cost_optimization_hub"  # AWS Cost Optimization Hub
    customer_verification = "customer_verification"  # AWS Customer Verification Service
    dataexchange = "dataexchange"  # AWS Data Exchange
    datapipeline = "datapipeline"  # AWS Data Pipeline
    dms = "dms"  # AWS Database Migration Service
    datasync = "datasync"  # AWS DataSync
    deadline = "deadline"  # AWS Deadline Cloud
    deepcomposer = "deepcomposer"  # AWS DeepComposer
    deepracer = "deepracer"  # AWS DeepRacer
    devicefarm = "devicefarm"  # AWS Device Farm
    ts = "ts"  # AWS Diagnostic tools
    directconnect = "directconnect"  # AWS Direct Connect
    ds = "ds"  # AWS Directory Service
    ds_data = "ds_data"  # AWS Directory Service Data
    elasticbeanstalk = "elasticbeanstalk"  # AWS Elastic Beanstalk
    drs = "drs"  # AWS Elastic Disaster Recovery
    elasticloadbalancing = "elasticloadbalancing"  # AWS Elastic Load Balancing
    elemental_appliances_software = "elemental_appliances_software"  # AWS Elemental Appliances and Software
    elemental_activations = "elemental_activations"  # AWS Elemental Appliances and Software Activation Service
    mediaconnect = "mediaconnect"  # AWS Elemental MediaConnect
    mediaconvert = "mediaconvert"  # AWS Elemental MediaConvert
    medialive = "medialive"  # AWS Elemental MediaLive
    mediapackage = "mediapackage"  # AWS Elemental MediaPackage
    mediapackagev2 = "mediapackagev2"  # AWS Elemental MediaPackage V2
    mediapackage_vod = "mediapackage_vod"  # AWS Elemental MediaPackage VOD
    mediastore = "mediastore"  # AWS Elemental MediaStore
    mediatailor = "mediatailor"  # AWS Elemental MediaTailor
    elemental_support_cases = "elemental_support_cases"  # AWS Elemental Support Cases
    elemental_support_content = "elemental_support_content"  # AWS Elemental Support Content
    social_messaging = "social_messaging"  # AWS End User Messaging Social
    entityresolution = "entityresolution"  # AWS Entity Resolution
    fis = "fis"  # AWS Fault Injection Service
    fms = "fms"  # AWS Firewall Manager
    freetier = "freetier"  # AWS Free Tier
    globalaccelerator = "globalaccelerator"  # AWS Global Accelerator
    glue = "glue"  # AWS Glue
    databrew = "databrew"  # AWS Glue DataBrew
    groundstation = "groundstation"  # AWS Ground Station
    health = "health"  # AWS Health APIs and Notifications
    medical_imaging = "medical_imaging"  # AWS HealthImaging
    healthlake = "healthlake"  # AWS HealthLake
    omics = "omics"  # AWS HealthOmics
    access_analyzer = "access_analyzer"  # AWS IAM Access Analyzer
    sso = "sso"  # AWS IAM Identity Center
    sso_directory = "sso_directory"  # AWS IAM Identity Center directory
    sso_oauth = "sso_oauth"  # AWS IAM Identity Center OIDC service
    iam = "iam"  # AWS Identity and Access Management (IAM)
    rolesanywhere = "rolesanywhere"  # AWS Identity and Access Management Roles Anywhere
    identitystore = "identitystore"  # AWS Identity Store
    identitystore_auth = "identitystore_auth"  # AWS Identity Store Auth
    identity_sync = "identity_sync"  # AWS Identity Sync
    importexport = "importexport"  # AWS Import Export Disk Service
    invoicing = "invoicing"  # AWS Invoicing Service
    iot = "iot"  # AWS IoT
    iot1click = "iot1click"  # AWS IoT 1-Click
    iotanalytics = "iotanalytics"  # AWS IoT Analytics
    iotdeviceadvisor = "iotdeviceadvisor"  # AWS IoT Core Device Advisor
    iot_device_tester = "iot_device_tester"  # AWS IoT Device Tester
    iotevents = "iotevents"  # AWS IoT Events
    iotfleethub = "iotfleethub"  # AWS IoT Fleet Hub for Device Management
    iotfleetwise = "iotfleetwise"  # AWS IoT FleetWise
    greengrass = "greengrass"  # AWS IoT Greengrass
    iotjobsdata = "iotjobsdata"  # AWS IoT Jobs DataPlane
    iotmanagedintegrations = "iotmanagedintegrations"  # AWS IoT managed integrations feature
    iotsitewise = "iotsitewise"  # AWS IoT SiteWise
    iottwinmaker = "iottwinmaker"  # AWS IoT TwinMaker
    iotwireless = "iotwireless"  # AWS IoT Wireless
    iq = "iq"  # AWS IQ
    iq_permission = "iq_permission"  # AWS IQ Permissions
    kms = "kms"  # AWS Key Management Service
    lakeformation = "lakeformation"  # AWS Lake Formation

    launchwizard = "launchwizard"  # AWS Launch Wizard
    license_manager = "license_manager"  # AWS License Manager
    license_manager_linux_subscriptions = "license_manager_linux_subscriptions"  # AWS License Manager Linux Subscriptions Manager
    license_manager_user_subscriptions = "license_manager_user_subscriptions"  # AWS License Manager User Subscriptions
    apptest = "apptest"  # AWS Mainframe Modernization Application Testing
    m2 = "m2"  # AWS Mainframe Modernization Service
    aws_marketplace = "aws_marketplace"  # AWS Marketplace
    marketplacecommerceanalytics = "marketplacecommerceanalytics"  # AWS Marketplace Commerce Analytics Service
    aws_marketplace_management = "aws_marketplace_management"  # AWS Marketplace Management Portal
    vendor_insights = "vendor_insights"  # AWS Marketplace Vendor Insights
    serviceextract = "serviceextract"  # AWS Microservice Extractor for .NET
    mapcredits = "mapcredits"  # AWS Migration Acceleration Program Credits
    mgh = "mgh"  # AWS Migration Hub
    migrationhub_orchestrator = "migrationhub_orchestrator"  # AWS Migration Hub Orchestrator
    refactor_spaces = "refactor_spaces"  # AWS Migration Hub Refactor Spaces
    migrationhub_strategy = "migrationhub_strategy"  # AWS Migration Hub Strategy Recommendations
    network_firewall = "network_firewall"  # AWS Network Firewall
    networkmanager = "networkmanager"  # AWS Network Manager
    networkmanager_chat = "networkmanager_chat"  # AWS Network Manager Chat
    opsworks = "opsworks"  # AWS OpsWorks
    opsworks_cm = "opsworks_cm"  # AWS OpsWorks Configuration Management
    organizations = "organizations"  # AWS Organizations
    outposts = "outposts"  # AWS Outposts
    panorama = "panorama"  # AWS Panorama
    pcs = "pcs"  # AWS Parallel Computing Service
    partnercentral_account_management = "partnercentral_account_management"  # AWS Partner central account management
    partnercentral = "partnercentral"  # AWS Partner Central Selling
    payment_cryptography = "payment_cryptography"  # AWS Payment Cryptography
    payments = "payments"  # AWS Payments
    pi = "pi"  # AWS Performance Insights
    pricing = "pricing"  # AWS Price List
    pca_connector_ad = "pca_connector_ad"  # AWS Private CA Connector for Active Directory
    pca_connector_scep = "pca_connector_scep"  # AWS Private CA Connector for SCEP
    acm_pca = "acm_pca"  # AWS Private Certificate Authority
    vpce = "vpce"  # AWS PrivateLink
    proton = "proton"  # AWS Proton
    purchase_orders = "purchase_orders"  # AWS Purchase Orders Console
    rbin = "rbin"  # AWS Recycle Bin
    repostspace = "repostspace"  # AWS rePost Private
    resiliencehub = "resiliencehub"  # AWS Resilience Hub
    ram = "ram"  # AWS Resource Access Manager (RAM)
    resource_explorer_2 = "resource_explorer_2"  # AWS Resource Explorer
    resource_groups = "resource_groups"  # AWS Resource Groups
    robomaker = "robomaker"  # AWS RoboMaker
    savingsplans = "savingsplans"  # AWS Savings Plans
    secretsmanager = "secretsmanager"  # AWS Secrets Manager
    securityhub = "securityhub"  # AWS Security Hub
    security_ir = "security_ir"  # AWS Security Incident Response
    sts = "sts"  # AWS Security Token Service
    sms = "sms"  # AWS Server Migration Service
    serverlessrepo = "serverlessrepo"  # AWS Serverless Application Repository
    servicecatalog = "servicecatalog"  # AWS Service Catalog
    private_networks = "private_networks"  # AWS service providing managed private networks
    shield = "shield"  # AWS Shield
    signer = "signer"  # AWS Signer
    signin = "signin"  # AWS Signin
    simspaceweaver = "simspaceweaver"  # AWS SimSpace Weaver
    snow_device_management = "snow_device_management"  # AWS Snow Device Management
    snowball = "snowball"  # AWS Snowball
    sqlworkbench = "sqlworkbench"  # AWS SQL Workbench
    states = "states"  # AWS Step Functions
    storagegateway = "storagegateway"  # AWS Storage Gateway
    scn = "scn"  # AWS Supply Chain
    support = "support"  # AWS Support
    supportapp = "supportapp"  # AWS Support App in Slack
    supportplans = "supportplans"  # AWS Support Plans
    supportrecommendations = "supportrecommendations"  # AWS Support Recommendations
    sustainability = "sustainability"  # AWS Sustainability
    ssm = "ssm"  # AWS Systems Manager
    ssm_sap = "ssm_sap"  # AWS Systems Manager for SAP
    ssm_guiconnect = "ssm_guiconnect"  # AWS Systems Manager GUI Connect
    ssm_incidents = "ssm_incidents"  # AWS Systems Manager Incident Manager
    ssm_contacts = "ssm_contacts"  # AWS Systems Manager Incident Manager Contacts
    ssm_quicksetup = "ssm_quicksetup"  # AWS Systems Manager Quick Setup
    tax = "tax"  # AWS Tax Settings
    tnb = "tnb"  # AWS Telco Network Builder
    tiros = "tiros"  # AWS Tiros
    transfer = "transfer"  # AWS Transfer Family
    trustedadvisor = "trustedadvisor"  # AWS Trusted Advisor
    notifications = "notifications"  # AWS User Notifications
    notifications_contacts = "notifications_contacts"  # AWS User Notifications Contacts
    user_subscriptions = "user_subscriptions"  # AWS User Subscriptions
    verified_access = "verified_access"  # AWS Verified Access
    waf = "waf"  # AWS WAF
    waf_regional = "waf_regional"  # AWS WAF Regional
    wafv2 = "wafv2"  # AWS WAF V2
    wellarchitected = "wellarchitected"  # AWS Well-Architected Tool
    wickr = "wickr"  # AWS Wickr
    xray = "xray"  # AWS X-Ray
    dbqms = "dbqms"  # Database Query Metadata Service
    networkflowmonitor = "networkflowmonitor"  # Network Flow Monitor
    servicequotas = "servicequotas"  # Service Quotas
    resource_explorer = "resource_explorer"  # Tag Editor
    
    # GCP Services (Core Compute & Storage)
    compute_engine = "compute_engine"
    cloud_storage = "cloud_storage"
    cloud_sql = "cloud_sql"
    cloud_functions = "cloud_functions"
    gke = "gke"  # Kubernetes Engine
    cloud_run = "cloud_run"
    bigquery = "bigquery"
    vertex_ai = "vertex_ai"
    
    # GCP Services (Extended) - From gcp_services.txt
    # Networking
    gcp_networking = "gcp_networking"
    cloud_dns = "cloud_dns"
    
    # App Engine & Application Services
    app_engine = "app_engine"
    cloud_composer = "cloud_composer"
    cloud_dataflow = "cloud_dataflow"
    cloud_pub_sub = "cloud_pub_sub"
    pub_sub_lite = "pub_sub_lite"
    cloud_tasks = "cloud_tasks"
    cloud_scheduler = "cloud_scheduler"
    workflows = "workflows"
    
    # AI & Machine Learning
    cloud_video_intelligence = "cloud_video_intelligence"
    cloud_vision_api = "cloud_vision_api"
    cloud_speech_api = "cloud_speech_api"
    cloud_text_to_speech = "cloud_text_to_speech"
    cloud_translate = "cloud_translate"
    cloud_natural_language = "cloud_natural_language"
    vertex_ai_vision = "vertex_ai_vision"
    cloud_automl = "cloud_automl"
    cloud_machine_learning_engine = "cloud_machine_learning_engine"
    cloud_tpu = "cloud_tpu"
    recommendations_ai = "recommendations_ai"
    cloud_dialogflow = "cloud_dialogflow"
    contact_center_ai = "contact_center_ai"
    contact_center_ai_insights = "contact_center_ai_insights"
    cloud_talent_solution = "cloud_talent_solution"
    discovery_engine = "discovery_engine"
    retail_api = "retail_api"
    
    # Data & Analytics
    cloud_bigtable = "cloud_bigtable"
    cloud_spanner = "cloud_spanner"
    alloydb = "alloydb"
    bigquery_storage_api = "bigquery_storage_api"
    bigquery_reservation_api = "bigquery_reservation_api"
    bigquery_bi_engine = "bigquery_bi_engine"
    bigquery_data_transfer = "bigquery_data_transfer"
    dataplex = "dataplex"
    dataproc = "dataproc"
    dataproc_metastore = "dataproc_metastore"
    datastream = "datastream"
    data_catalog = "data_catalog"
    cloud_data_fusion = "cloud_data_fusion"
    cloud_data_labeling = "cloud_data_labeling"
    looker_data_platform = "looker_data_platform"
    
    # Storage & File Systems
    cloud_filestore = "cloud_filestore"
    artifact_registry = "artifact_registry"
    storage_insights = "storage_insights"
    transfer_appliance = "transfer_appliance"
    transfer_service = "transfer_service"
    backup_for_gke = "backup_for_gke"
    backup_and_dr = "backup_and_dr"
    
    # Memory & Caching
    cloud_memorystore_redis = "cloud_memorystore_redis"
    cloud_memorystore_memcached = "cloud_memorystore_memcached"
    
    # Healthcare & Life Sciences
    cloud_healthcare = "cloud_healthcare"
    genomics = "genomics"
    
    # Security & Identity
    cloud_kms = "cloud_kms"  # Key Management Service
    security_command_center = "security_command_center"
    cloud_data_loss_prevention = "cloud_data_loss_prevention"
    identity_platform = "identity_platform"
    secret_manager = "secret_manager"
    certificate_authority_service = "certificate_authority_service"
    certificate_manager = "certificate_manager"
    web_risk = "web_risk"
    recaptcha_enterprise = "recaptcha_enterprise"
    beyondcorp_enterprise = "beyondcorp_enterprise"
    cloud_ids = "cloud_ids"
    binary_authorization = "binary_authorization"
    
    # Developer Tools & CI/CD
    cloud_build = "cloud_build"
    source_repository = "source_repository"
    cloud_deploy = "cloud_deploy"
    remote_build_execution = "remote_build_execution"
    container_registry_scanning = "container_registry_scanning"
    
    # Monitoring & Operations
    cloud_monitoring = "cloud_monitoring"
    cloud_logging = "cloud_logging"
    cloud_trace = "cloud_trace"
    stackdriver = "stackdriver"
    workload_manager = "workload_manager"
    on_demand_scanning = "on_demand_scanning"
    
    # Notebooks & Development
    notebooks = "notebooks"
    earth_engine = "earth_engine"
    zync = "zync"
    
    # Gaming & Media
    game_services = "game_services"
    live_stream_api = "live_stream_api"
    transcoder_api = "transcoder_api"
    transcode_api = "transcode_api"
    video_stitcher_api = "video_stitcher_api"
    cloud_media_translation = "cloud_media_translation"
    immersive_stream_xr = "immersive_stream_xr"
    
    # Anthos & Hybrid Cloud
    anthos_gdc = "anthos_gdc"
    anthos_service_mesh = "anthos_service_mesh"
    anthos_policy_controller = "anthos_policy_controller"
    anthos_config_management = "anthos_config_management"
    multiclusteringress = "multiclusteringress"
    
    # API Management & Integration
    api_gateway = "api_gateway"
    apigee = "apigee"
    application_integration = "application_integration"
    integration_connectors = "integration_connectors"
    google_service_control = "google_service_control"
    
    # Maps & Location Services
    maps_api = "maps_api"
    maps_embed_api = "maps_embed_api"
    maps_static_api = "maps_static_api"
    maps_elevation_api = "maps_elevation_api"
    maps_sdk_unity = "maps_sdk_unity"
    google_maps_mobile_sdk = "google_maps_mobile_sdk"
    google_maps_routes = "google_maps_routes"
    places_api = "places_api"
    directions_api = "directions_api"
    distance_matrix_api = "distance_matrix_api"
    geocoding_api = "geocoding_api"
    geolocation_api = "geolocation_api"
    roads_api = "roads_api"
    street_view_static_api = "street_view_static_api"
    time_zone_api = "time_zone_api"
    address_validation_api = "address_validation_api"
    
    # Firebase Services
    firebase = "firebase"
    firebase_realtime_database = "firebase_realtime_database"
    firebase_hosting = "firebase_hosting"
    firebase_auth = "firebase_auth"
    firebase_test_lab = "firebase_test_lab"
    
    # Virtual Machines & Infrastructure
    vm_manager = "vm_manager"
    vmware_engine = "vmware_engine"
    google_distributed_cloud_edge = "google_distributed_cloud_edge"
    managed_service_active_directory = "managed_service_active_directory"
    
    # Cloud IoT & Edge
    cloud_iot_core = "cloud_iot_core"
    
    # Search & Knowledge
    custom_search = "custom_search"
    programmable_search = "programmable_search"
    
    # Business & Enterprise
    cloud_domains = "cloud_domains"
    enterprise_agreement = "enterprise_agreement"
    cloud_optimization = "cloud_optimization"
    payment_gateway = "payment_gateway"
    
    # Specialized & Industry Solutions
    confidential_computing = "confidential_computing"
    spectrum_sas = "spectrum_sas"
    htcondor_gcp = "htcondor_gcp"
    prediction = "prediction"
    speaker_id = "speaker_id"
    document_warehouse = "document_warehouse"
    cloud_document_ai = "cloud_document_ai"
    cloud_document_api = "cloud_document_api"
    cloud_vision_ocr_onprem = "cloud_vision_ocr_onprem"
    speech_to_text_onprem = "speech_to_text_onprem"
    
    # Third-party & Partner Solutions
    actifio_go = "actifio_go"
    actifio_go_gcp = "actifio_go_gcp"
    actifio_sky = "actifio_sky"
    elastifile_cloud_file_system = "elastifile_cloud_file_system"
    
    # Click to Deploy Solutions (Popular ones)
    click_deploy_wordpress = "click_deploy_wordpress"
    click_deploy_lamp = "click_deploy_lamp"
    click_deploy_mysql = "click_deploy_mysql"
    click_deploy_nginx = "click_deploy_nginx"
    click_deploy_jenkins = "click_deploy_jenkins"
    click_deploy_elasticsearch = "click_deploy_elasticsearch"
    click_deploy_kafka = "click_deploy_kafka"
    click_deploy_redis = "click_deploy_redis"
    click_deploy_postgresql = "click_deploy_postgresql"
    click_deploy_cassandra = "click_deploy_cassandra"
    click_deploy_drupal = "click_deploy_drupal"
    click_deploy_joomla = "click_deploy_joomla"
    click_deploy_magento = "click_deploy_magento"
    click_deploy_nodejs = "click_deploy_nodejs"
    click_deploy_django = "click_deploy_django"
    click_deploy_tomcat = "click_deploy_tomcat"
    click_deploy_grafana = "click_deploy_grafana"
    click_deploy_influxdb = "click_deploy_influxdb"
    click_deploy_elk_stack = "click_deploy_elk_stack"
    click_deploy_sonarqube = "click_deploy_sonarqube"
    click_deploy_discourse = "click_deploy_discourse"
    click_deploy_mattermost = "click_deploy_mattermost"
    click_deploy_ghost = "click_deploy_ghost"
    click_deploy_moodle = "click_deploy_moodle"
    
    # Azure Services
    virtual_machines = "virtual_machines"
    blob_storage = "blob_storage"
    sql_database = "sql_database"
    azure_functions = "azure_functions"
    aks = "aks"
    container_instances = "container_instances"
    cosmos_db = "cosmos_db"
    cognitive_services = "cognitive_services"
    
    # AWS Instance Types - General Purpose
    # T4g (Graviton2 - Burstable)
    t4g_nano = "t4g_nano"
    t4g_micro = "t4g_micro"
    t4g_small = "t4g_small"
    t4g_medium = "t4g_medium"
    t4g_large = "t4g_large"
    t4g_xlarge = "t4g_xlarge"
    t4g_2xlarge = "t4g_2xlarge"
    
    # T3 (Burstable Performance)
    t3_nano = "t3_nano"
    t3_micro = "t3_micro"
    t3_small = "t3_small"
    t3_medium = "t3_medium"
    t3_large = "t3_large"
    t3_xlarge = "t3_xlarge"
    t3_2xlarge = "t3_2xlarge"
    
    # T3a (AMD Burstable)
    t3a_nano = "t3a_nano"
    t3a_micro = "t3a_micro"
    t3a_small = "t3a_small"
    t3a_medium = "t3a_medium"
    t3a_large = "t3a_large"
    t3a_xlarge = "t3a_xlarge"
    t3a_2xlarge = "t3a_2xlarge"
    
    # T2 (Burstable Performance - Previous Gen)
    t2_nano = "t2_nano"
    t2_micro = "t2_micro"
    t2_small = "t2_small"
    t2_medium = "t2_medium"
    t2_large = "t2_large"
    t2_xlarge = "t2_xlarge"
    t2_2xlarge = "t2_2xlarge"
    
    # M7g (Graviton3 - General Purpose)
    m7g_medium = "m7g_medium"
    m7g_large = "m7g_large"
    m7g_xlarge = "m7g_xlarge"
    m7g_2xlarge = "m7g_2xlarge"
    m7g_4xlarge = "m7g_4xlarge"
    m7g_8xlarge = "m7g_8xlarge"
    m7g_12xlarge = "m7g_12xlarge"
    m7g_16xlarge = "m7g_16xlarge"
    
    # M7i (Intel - General Purpose)
    m7i_large = "m7i_large"
    m7i_xlarge = "m7i_xlarge"
    m7i_2xlarge = "m7i_2xlarge"
    m7i_4xlarge = "m7i_4xlarge"
    m7i_8xlarge = "m7i_8xlarge"
    m7i_12xlarge = "m7i_12xlarge"
    m7i_16xlarge = "m7i_16xlarge"
    m7i_24xlarge = "m7i_24xlarge"
    m7i_48xlarge = "m7i_48xlarge"
    
    # M7a (AMD - General Purpose)
    m7a_medium = "m7a_medium"
    m7a_large = "m7a_large"
    m7a_xlarge = "m7a_xlarge"
    m7a_2xlarge = "m7a_2xlarge"
    m7a_4xlarge = "m7a_4xlarge"
    m7a_8xlarge = "m7a_8xlarge"
    m7a_12xlarge = "m7a_12xlarge"
    m7a_16xlarge = "m7a_16xlarge"
    m7a_24xlarge = "m7a_24xlarge"
    m7a_32xlarge = "m7a_32xlarge"
    m7a_48xlarge = "m7a_48xlarge"
    
    # M6g (Graviton2 - General Purpose)
    m6g_medium = "m6g_medium"
    m6g_large = "m6g_large"
    m6g_xlarge = "m6g_xlarge"
    m6g_2xlarge = "m6g_2xlarge"
    m6g_4xlarge = "m6g_4xlarge"
    m6g_8xlarge = "m6g_8xlarge"
    m6g_12xlarge = "m6g_12xlarge"
    m6g_16xlarge = "m6g_16xlarge"
    
    # M6i (Intel - General Purpose)
    m6i_large = "m6i_large"
    m6i_xlarge = "m6i_xlarge"
    m6i_2xlarge = "m6i_2xlarge"
    m6i_4xlarge = "m6i_4xlarge"
    m6i_8xlarge = "m6i_8xlarge"
    m6i_12xlarge = "m6i_12xlarge"
    m6i_16xlarge = "m6i_16xlarge"
    m6i_24xlarge = "m6i_24xlarge"
    m6i_32xlarge = "m6i_32xlarge"
    
    # M6a (AMD - General Purpose)
    m6a_large = "m6a_large"
    m6a_xlarge = "m6a_xlarge"
    m6a_2xlarge = "m6a_2xlarge"
    m6a_4xlarge = "m6a_4xlarge"
    m6a_8xlarge = "m6a_8xlarge"
    m6a_12xlarge = "m6a_12xlarge"
    m6a_16xlarge = "m6a_16xlarge"
    m6a_24xlarge = "m6a_24xlarge"
    m6a_32xlarge = "m6a_32xlarge"
    m6a_48xlarge = "m6a_48xlarge"
    
    # M5 (Intel - General Purpose)
    m5_large = "m5_large"
    m5_xlarge = "m5_xlarge"
    m5_2xlarge = "m5_2xlarge"
    m5_4xlarge = "m5_4xlarge"
    m5_8xlarge = "m5_8xlarge"
    m5_12xlarge = "m5_12xlarge"
    m5_16xlarge = "m5_16xlarge"
    m5_24xlarge = "m5_24xlarge"
    
    # M5a (AMD - General Purpose)
    m5a_large = "m5a_large"
    m5a_xlarge = "m5a_xlarge"
    m5a_2xlarge = "m5a_2xlarge"
    m5a_4xlarge = "m5a_4xlarge"
    m5a_8xlarge = "m5a_8xlarge"
    m5a_12xlarge = "m5a_12xlarge"
    m5a_16xlarge = "m5a_16xlarge"
    m5a_24xlarge = "m5a_24xlarge"
    
    # M5n (Intel with Enhanced Networking)
    m5n_large = "m5n_large"
    m5n_xlarge = "m5n_xlarge"
    m5n_2xlarge = "m5n_2xlarge"
    m5n_4xlarge = "m5n_4xlarge"
    m5n_8xlarge = "m5n_8xlarge"
    m5n_12xlarge = "m5n_12xlarge"
    m5n_16xlarge = "m5n_16xlarge"
    m5n_24xlarge = "m5n_24xlarge"
    
    # AWS Instance Types - Compute Optimized
    # C7g (Graviton3 - Compute Optimized)
    c7g_medium = "c7g_medium"
    c7g_large = "c7g_large"
    c7g_xlarge = "c7g_xlarge"
    c7g_2xlarge = "c7g_2xlarge"
    c7g_4xlarge = "c7g_4xlarge"
    c7g_8xlarge = "c7g_8xlarge"
    c7g_12xlarge = "c7g_12xlarge"
    c7g_16xlarge = "c7g_16xlarge"
    
    # C7i (Intel - Compute Optimized)
    c7i_large = "c7i_large"
    c7i_xlarge = "c7i_xlarge"
    c7i_2xlarge = "c7i_2xlarge"
    c7i_4xlarge = "c7i_4xlarge"
    c7i_8xlarge = "c7i_8xlarge"
    c7i_12xlarge = "c7i_12xlarge"
    c7i_16xlarge = "c7i_16xlarge"
    c7i_24xlarge = "c7i_24xlarge"
    c7i_48xlarge = "c7i_48xlarge"
    
    # C7a (AMD - Compute Optimized)
    c7a_medium = "c7a_medium"
    c7a_large = "c7a_large"
    c7a_xlarge = "c7a_xlarge"
    c7a_2xlarge = "c7a_2xlarge"
    c7a_4xlarge = "c7a_4xlarge"
    c7a_8xlarge = "c7a_8xlarge"
    c7a_12xlarge = "c7a_12xlarge"
    c7a_16xlarge = "c7a_16xlarge"
    c7a_24xlarge = "c7a_24xlarge"
    c7a_32xlarge = "c7a_32xlarge"
    c7a_48xlarge = "c7a_48xlarge"
    
    # C6g (Graviton2 - Compute Optimized)
    c6g_medium = "c6g_medium"
    c6g_large = "c6g_large"
    c6g_xlarge = "c6g_xlarge"
    c6g_2xlarge = "c6g_2xlarge"
    c6g_4xlarge = "c6g_4xlarge"
    c6g_8xlarge = "c6g_8xlarge"
    c6g_12xlarge = "c6g_12xlarge"
    c6g_16xlarge = "c6g_16xlarge"
    
    # C6i (Intel - Compute Optimized)
    c6i_large = "c6i_large"
    c6i_xlarge = "c6i_xlarge"
    c6i_2xlarge = "c6i_2xlarge"
    c6i_4xlarge = "c6i_4xlarge"
    c6i_8xlarge = "c6i_8xlarge"
    c6i_12xlarge = "c6i_12xlarge"
    c6i_16xlarge = "c6i_16xlarge"
    c6i_24xlarge = "c6i_24xlarge"
    c6i_32xlarge = "c6i_32xlarge"
    
    # C6a (AMD - Compute Optimized)
    c6a_large = "c6a_large"
    c6a_xlarge = "c6a_xlarge"
    c6a_2xlarge = "c6a_2xlarge"
    c6a_4xlarge = "c6a_4xlarge"
    c6a_8xlarge = "c6a_8xlarge"
    c6a_12xlarge = "c6a_12xlarge"
    c6a_16xlarge = "c6a_16xlarge"
    c6a_24xlarge = "c6a_24xlarge"
    c6a_32xlarge = "c6a_32xlarge"
    c6a_48xlarge = "c6a_48xlarge"
    
    # C5 (Intel - Compute Optimized)
    c5_large = "c5_large"
    c5_xlarge = "c5_xlarge"
    c5_2xlarge = "c5_2xlarge"
    c5_4xlarge = "c5_4xlarge"
    c5_9xlarge = "c5_9xlarge"
    c5_12xlarge = "c5_12xlarge"
    c5_18xlarge = "c5_18xlarge"
    c5_24xlarge = "c5_24xlarge"
    
    # C5a (AMD - Compute Optimized)
    c5a_large = "c5a_large"
    c5a_xlarge = "c5a_xlarge"
    c5a_2xlarge = "c5a_2xlarge"
    c5a_4xlarge = "c5a_4xlarge"
    c5a_8xlarge = "c5a_8xlarge"
    c5a_12xlarge = "c5a_12xlarge"
    c5a_16xlarge = "c5a_16xlarge"
    c5a_24xlarge = "c5a_24xlarge"
    
    # C5n (Intel with Enhanced Networking)
    c5n_large = "c5n_large"
    c5n_xlarge = "c5n_xlarge"
    c5n_2xlarge = "c5n_2xlarge"
    c5n_4xlarge = "c5n_4xlarge"
    c5n_9xlarge = "c5n_9xlarge"
    c5n_18xlarge = "c5n_18xlarge"
    
    # AWS Instance Types - Memory Optimized
    # R7g (Graviton3 - Memory Optimized)
    r7g_medium = "r7g_medium"
    r7g_large = "r7g_large"
    r7g_xlarge = "r7g_xlarge"
    r7g_2xlarge = "r7g_2xlarge"
    r7g_4xlarge = "r7g_4xlarge"
    r7g_8xlarge = "r7g_8xlarge"
    r7g_12xlarge = "r7g_12xlarge"
    r7g_16xlarge = "r7g_16xlarge"
    
    # R7i (Intel - Memory Optimized)
    r7i_large = "r7i_large"
    r7i_xlarge = "r7i_xlarge"
    r7i_2xlarge = "r7i_2xlarge"
    r7i_4xlarge = "r7i_4xlarge"
    r7i_8xlarge = "r7i_8xlarge"
    r7i_12xlarge = "r7i_12xlarge"
    r7i_16xlarge = "r7i_16xlarge"
    r7i_24xlarge = "r7i_24xlarge"
    r7i_48xlarge = "r7i_48xlarge"
    
    # R7a (AMD - Memory Optimized)
    r7a_medium = "r7a_medium"
    r7a_large = "r7a_large"
    r7a_xlarge = "r7a_xlarge"
    r7a_2xlarge = "r7a_2xlarge"
    r7a_4xlarge = "r7a_4xlarge"
    r7a_8xlarge = "r7a_8xlarge"
    r7a_12xlarge = "r7a_12xlarge"
    r7a_16xlarge = "r7a_16xlarge"
    r7a_24xlarge = "r7a_24xlarge"
    r7a_32xlarge = "r7a_32xlarge"
    r7a_48xlarge = "r7a_48xlarge"
    
    # R6g (Graviton2 - Memory Optimized)
    r6g_medium = "r6g_medium"
    r6g_large = "r6g_large"
    r6g_xlarge = "r6g_xlarge"
    r6g_2xlarge = "r6g_2xlarge"
    r6g_4xlarge = "r6g_4xlarge"
    r6g_8xlarge = "r6g_8xlarge"
    r6g_12xlarge = "r6g_12xlarge"
    r6g_16xlarge = "r6g_16xlarge"
    
    # R6i (Intel - Memory Optimized)
    r6i_large = "r6i_large"
    r6i_xlarge = "r6i_xlarge"
    r6i_2xlarge = "r6i_2xlarge"
    r6i_4xlarge = "r6i_4xlarge"
    r6i_8xlarge = "r6i_8xlarge"
    r6i_12xlarge = "r6i_12xlarge"
    r6i_16xlarge = "r6i_16xlarge"
    r6i_24xlarge = "r6i_24xlarge"
    r6i_32xlarge = "r6i_32xlarge"
    
    # R6a (AMD - Memory Optimized)
    r6a_large = "r6a_large"
    r6a_xlarge = "r6a_xlarge"
    r6a_2xlarge = "r6a_2xlarge"
    r6a_4xlarge = "r6a_4xlarge"
    r6a_8xlarge = "r6a_8xlarge"
    r6a_12xlarge = "r6a_12xlarge"
    r6a_16xlarge = "r6a_16xlarge"
    r6a_24xlarge = "r6a_24xlarge"
    r6a_32xlarge = "r6a_32xlarge"
    r6a_48xlarge = "r6a_48xlarge"
    
    # R5 (Intel - Memory Optimized)
    r5_large = "r5_large"
    r5_xlarge = "r5_xlarge"
    r5_2xlarge = "r5_2xlarge"
    r5_4xlarge = "r5_4xlarge"
    r5_8xlarge = "r5_8xlarge"
    r5_12xlarge = "r5_12xlarge"
    r5_16xlarge = "r5_16xlarge"
    r5_24xlarge = "r5_24xlarge"
    
    # R5a (AMD - Memory Optimized)
    r5a_large = "r5a_large"
    r5a_xlarge = "r5a_xlarge"
    r5a_2xlarge = "r5a_2xlarge"
    r5a_4xlarge = "r5a_4xlarge"
    r5a_8xlarge = "r5a_8xlarge"
    r5a_12xlarge = "r5a_12xlarge"
    r5a_16xlarge = "r5a_16xlarge"
    r5a_24xlarge = "r5a_24xlarge"
    
    # R5n (Intel with Enhanced Networking)
    r5n_large = "r5n_large"
    r5n_xlarge = "r5n_xlarge"
    r5n_2xlarge = "r5n_2xlarge"
    r5n_4xlarge = "r5n_4xlarge"
    r5n_8xlarge = "r5n_8xlarge"
    r5n_12xlarge = "r5n_12xlarge"
    r5n_16xlarge = "r5n_16xlarge"
    r5n_24xlarge = "r5n_24xlarge"
    
    # X2gd (Graviton2 - Memory Optimized with NVMe SSD)
    x2gd_medium = "x2gd_medium"
    x2gd_large = "x2gd_large"
    x2gd_xlarge = "x2gd_xlarge"
    x2gd_2xlarge = "x2gd_2xlarge"
    x2gd_4xlarge = "x2gd_4xlarge"
    x2gd_8xlarge = "x2gd_8xlarge"
    x2gd_12xlarge = "x2gd_12xlarge"
    x2gd_16xlarge = "x2gd_16xlarge"
    
    # X2idn (Intel - Memory Optimized with NVMe SSD)
    x2idn_large = "x2idn_large"
    x2idn_xlarge = "x2idn_xlarge"
    x2idn_2xlarge = "x2idn_2xlarge"
    x2idn_4xlarge = "x2idn_4xlarge"
    x2idn_8xlarge = "x2idn_8xlarge"
    x2idn_12xlarge = "x2idn_12xlarge"
    x2idn_16xlarge = "x2idn_16xlarge"
    x2idn_24xlarge = "x2idn_24xlarge"
    x2idn_32xlarge = "x2idn_32xlarge"
    
    # X2iedn (Intel - Memory Optimized with NVMe SSD Enhanced)
    x2iedn_large = "x2iedn_large"
    x2iedn_xlarge = "x2iedn_xlarge"
    x2iedn_2xlarge = "x2iedn_2xlarge"
    x2iedn_4xlarge = "x2iedn_4xlarge"
    x2iedn_8xlarge = "x2iedn_8xlarge"
    x2iedn_12xlarge = "x2iedn_12xlarge"
    x2iedn_16xlarge = "x2iedn_16xlarge"
    x2iedn_24xlarge = "x2iedn_24xlarge"
    x2iedn_32xlarge = "x2iedn_32xlarge"
    
    # X2iezn (Intel - Memory Optimized with Enhanced Networking)
    x2iezn_large = "x2iezn_large"
    x2iezn_xlarge = "x2iezn_xlarge"
    x2iezn_2xlarge = "x2iezn_2xlarge"
    x2iezn_4xlarge = "x2iezn_4xlarge"
    x2iezn_6xlarge = "x2iezn_6xlarge"
    x2iezn_8xlarge = "x2iezn_8xlarge"
    x2iezn_12xlarge = "x2iezn_12xlarge"
    
    # X1e (Intel - High Memory)
    x1e_xlarge = "x1e_xlarge"
    x1e_2xlarge = "x1e_2xlarge"
    x1e_4xlarge = "x1e_4xlarge"
    x1e_8xlarge = "x1e_8xlarge"
    x1e_16xlarge = "x1e_16xlarge"
    x1e_32xlarge = "x1e_32xlarge"
    
    # X1 (Intel - High Memory)
    x1_16xlarge = "x1_16xlarge"
    x1_32xlarge = "x1_32xlarge"
    
    # AWS Instance Types - Storage Optimized
    # I4g (Graviton2 - Storage Optimized)
    i4g_large = "i4g_large"
    i4g_xlarge = "i4g_xlarge"
    i4g_2xlarge = "i4g_2xlarge"
    i4g_4xlarge = "i4g_4xlarge"
    i4g_8xlarge = "i4g_8xlarge"
    i4g_16xlarge = "i4g_16xlarge"
    
    # I4i (Intel - Storage Optimized)
    i4i_large = "i4i_large"
    i4i_xlarge = "i4i_xlarge"
    i4i_2xlarge = "i4i_2xlarge"
    i4i_4xlarge = "i4i_4xlarge"
    i4i_8xlarge = "i4i_8xlarge"
    i4i_12xlarge = "i4i_12xlarge"
    i4i_16xlarge = "i4i_16xlarge"
    i4i_24xlarge = "i4i_24xlarge"
    i4i_32xlarge = "i4i_32xlarge"
    
    # I3 (Intel - Storage Optimized)
    i3_large = "i3_large"
    i3_xlarge = "i3_xlarge"
    i3_2xlarge = "i3_2xlarge"
    i3_4xlarge = "i3_4xlarge"
    i3_8xlarge = "i3_8xlarge"
    i3_16xlarge = "i3_16xlarge"
    
    # I3en (Intel - Storage Optimized Enhanced)
    i3en_large = "i3en_large"
    i3en_xlarge = "i3en_xlarge"
    i3en_2xlarge = "i3en_2xlarge"
    i3en_3xlarge = "i3en_3xlarge"
    i3en_6xlarge = "i3en_6xlarge"
    i3en_12xlarge = "i3en_12xlarge"
    i3en_24xlarge = "i3en_24xlarge"
    
    # D3 (Intel - Dense HDD Storage)
    d3_xlarge = "d3_xlarge"
    d3_2xlarge = "d3_2xlarge"
    d3_4xlarge = "d3_4xlarge"
    d3_8xlarge = "d3_8xlarge"
    
    # D3en (Intel - Dense HDD Storage Enhanced)
    d3en_xlarge = "d3en_xlarge"
    d3en_2xlarge = "d3en_2xlarge"
    d3en_4xlarge = "d3en_4xlarge"
    d3en_6xlarge = "d3en_6xlarge"
    d3en_8xlarge = "d3en_8xlarge"
    d3en_12xlarge = "d3en_12xlarge"
    
    # AWS Instance Types - Accelerated Computing
    # P5 (NVIDIA H100 - ML Training)
    p5_48xlarge = "p5_48xlarge"
    
    # P4d (NVIDIA A100 - ML Training)
    p4d_24xlarge = "p4d_24xlarge"
    
    # P4de (NVIDIA A100 - ML Training Enhanced)
    p4de_24xlarge = "p4de_24xlarge"
    
    # P3 (NVIDIA V100 - ML Training)
    p3_2xlarge = "p3_2xlarge"
    p3_8xlarge = "p3_8xlarge"
    p3_16xlarge = "p3_16xlarge"
    
    # P3dn (NVIDIA V100 with Enhanced Networking)
    p3dn_24xlarge = "p3dn_24xlarge"
    
    # P2 (NVIDIA K80 - ML Training)
    p2_xlarge = "p2_xlarge"
    p2_8xlarge = "p2_8xlarge"
    p2_16xlarge = "p2_16xlarge"
    
    # G5 (NVIDIA A10G - ML Inference/Graphics)
    g5_xlarge = "g5_xlarge"
    g5_2xlarge = "g5_2xlarge"
    g5_4xlarge = "g5_4xlarge"
    g5_8xlarge = "g5_8xlarge"
    g5_12xlarge = "g5_12xlarge"
    g5_16xlarge = "g5_16xlarge"
    g5_24xlarge = "g5_24xlarge"
    g5_48xlarge = "g5_48xlarge"
    
    # G5g (NVIDIA T4G - ARM-based Graphics)
    g5g_xlarge = "g5g_xlarge"
    g5g_2xlarge = "g5g_2xlarge"
    g5g_4xlarge = "g5g_4xlarge"
    g5g_8xlarge = "g5g_8xlarge"
    g5g_16xlarge = "g5g_16xlarge"
    
    # G4dn (NVIDIA T4 - ML Inference)
    g4dn_xlarge = "g4dn_xlarge"
    g4dn_2xlarge = "g4dn_2xlarge"
    g4dn_4xlarge = "g4dn_4xlarge"
    g4dn_8xlarge = "g4dn_8xlarge"
    g4dn_12xlarge = "g4dn_12xlarge"
    g4dn_16xlarge = "g4dn_16xlarge"
    
    # G4ad (AMD Radeon Pro V520 - Graphics)
    g4ad_xlarge = "g4ad_xlarge"
    g4ad_2xlarge = "g4ad_2xlarge"
    g4ad_4xlarge = "g4ad_4xlarge"
    g4ad_8xlarge = "g4ad_8xlarge"
    g4ad_16xlarge = "g4ad_16xlarge"
    
    # G3 (NVIDIA M60 - Graphics)
    g3_4xlarge = "g3_4xlarge"
    g3_8xlarge = "g3_8xlarge"
    g3_16xlarge = "g3_16xlarge"
    
    # Inf2 (AWS Inferentia2 - ML Inference)
    inf2_xlarge = "inf2_xlarge"
    inf2_8xlarge = "inf2_8xlarge"
    inf2_24xlarge = "inf2_24xlarge"
    inf2_48xlarge = "inf2_48xlarge"
    
    # Inf1 (AWS Inferentia - ML Inference)
    inf1_xlarge = "inf1_xlarge"
    inf1_2xlarge = "inf1_2xlarge"
    inf1_6xlarge = "inf1_6xlarge"
    inf1_24xlarge = "inf1_24xlarge"
    
    # Trn1 (AWS Trainium - ML Training)
    trn1_2xlarge = "trn1_2xlarge"
    trn1_32xlarge = "trn1_32xlarge"
    
    # Trn1n (AWS Trainium with Enhanced Networking)
    trn1n_32xlarge = "trn1n_32xlarge"
    
    # DL1 (Gaudi - Deep Learning)
    dl1_24xlarge = "dl1_24xlarge"
    
    # AWS Instance Types - High Performance Computing
    # Hpc7g (Graviton3E - HPC)
    hpc7g_4xlarge = "hpc7g_4xlarge"
    hpc7g_8xlarge = "hpc7g_8xlarge"
    hpc7g_16xlarge = "hpc7g_16xlarge"
    
    # Hpc7a (AMD - HPC)
    hpc7a_12xlarge = "hpc7a_12xlarge"
    hpc7a_24xlarge = "hpc7a_24xlarge"
    hpc7a_48xlarge = "hpc7a_48xlarge"
    hpc7a_96xlarge = "hpc7a_96xlarge"
    
    # Hpc6id (Intel - HPC with Local SSD)
    hpc6id_32xlarge = "hpc6id_32xlarge"
    
    # Hpc6a (AMD - HPC)
    hpc6a_48xlarge = "hpc6a_48xlarge"
    
    # GCP Instance Types - General Purpose
    # E2 (Cost-Optimized)
    e2_micro = "e2_micro"
    e2_small = "e2_small"
    e2_medium = "e2_medium"
    e2_standard_2 = "e2_standard_2"
    e2_standard_4 = "e2_standard_4"
    e2_standard_8 = "e2_standard_8"
    e2_standard_16 = "e2_standard_16"
    e2_standard_32 = "e2_standard_32"
    e2_highmem_2 = "e2_highmem_2"
    e2_highmem_4 = "e2_highmem_4"
    e2_highmem_8 = "e2_highmem_8"
    e2_highmem_16 = "e2_highmem_16"
    e2_highcpu_2 = "e2_highcpu_2"
    e2_highcpu_4 = "e2_highcpu_4"
    e2_highcpu_8 = "e2_highcpu_8"
    e2_highcpu_16 = "e2_highcpu_16"
    e2_highcpu_32 = "e2_highcpu_32"
    
    # N1 (First Generation - Balanced)
    n1_standard_1 = "n1_standard_1"
    n1_standard_2 = "n1_standard_2"
    n1_standard_4 = "n1_standard_4"
    n1_standard_8 = "n1_standard_8"
    n1_standard_16 = "n1_standard_16"
    n1_standard_32 = "n1_standard_32"
    n1_standard_64 = "n1_standard_64"
    n1_standard_96 = "n1_standard_96"
    n1_highmem_2 = "n1_highmem_2"
    n1_highmem_4 = "n1_highmem_4"
    n1_highmem_8 = "n1_highmem_8"
    n1_highmem_16 = "n1_highmem_16"
    n1_highmem_32 = "n1_highmem_32"
    n1_highmem_64 = "n1_highmem_64"
    n1_highmem_96 = "n1_highmem_96"
    n1_highcpu_2 = "n1_highcpu_2"
    n1_highcpu_4 = "n1_highcpu_4"
    n1_highcpu_8 = "n1_highcpu_8"
    n1_highcpu_16 = "n1_highcpu_16"
    n1_highcpu_32 = "n1_highcpu_32"
    n1_highcpu_64 = "n1_highcpu_64"
    n1_highcpu_96 = "n1_highcpu_96"
    
    # N2 (Second Generation - Balanced)
    n2_standard_2 = "n2_standard_2"
    n2_standard_4 = "n2_standard_4"
    n2_standard_8 = "n2_standard_8"
    n2_standard_16 = "n2_standard_16"
    n2_standard_32 = "n2_standard_32"
    n2_standard_48 = "n2_standard_48"
    n2_standard_64 = "n2_standard_64"
    n2_standard_80 = "n2_standard_80"
    n2_standard_96 = "n2_standard_96"
    n2_standard_128 = "n2_standard_128"
    n2_highmem_2 = "n2_highmem_2"
    n2_highmem_4 = "n2_highmem_4"
    n2_highmem_8 = "n2_highmem_8"
    n2_highmem_16 = "n2_highmem_16"
    n2_highmem_32 = "n2_highmem_32"
    n2_highmem_48 = "n2_highmem_48"
    n2_highmem_64 = "n2_highmem_64"
    n2_highmem_80 = "n2_highmem_80"
    n2_highmem_96 = "n2_highmem_96"
    n2_highmem_128 = "n2_highmem_128"
    n2_highcpu_2 = "n2_highcpu_2"
    n2_highcpu_4 = "n2_highcpu_4"
    n2_highcpu_8 = "n2_highcpu_8"
    n2_highcpu_16 = "n2_highcpu_16"
    n2_highcpu_32 = "n2_highcpu_32"
    n2_highcpu_48 = "n2_highcpu_48"
    n2_highcpu_64 = "n2_highcpu_64"
    n2_highcpu_80 = "n2_highcpu_80"
    n2_highcpu_96 = "n2_highcpu_96"
    
    # N2D (AMD EPYC - Balanced)
    n2d_standard_2 = "n2d_standard_2"
    n2d_standard_4 = "n2d_standard_4"
    n2d_standard_8 = "n2d_standard_8"
    n2d_standard_16 = "n2d_standard_16"
    n2d_standard_32 = "n2d_standard_32"
    n2d_standard_48 = "n2d_standard_48"
    n2d_standard_64 = "n2d_standard_64"
    n2d_standard_80 = "n2d_standard_80"
    n2d_standard_96 = "n2d_standard_96"
    n2d_standard_128 = "n2d_standard_128"
    n2d_standard_224 = "n2d_standard_224"
    n2d_highmem_2 = "n2d_highmem_2"
    n2d_highmem_4 = "n2d_highmem_4"
    n2d_highmem_8 = "n2d_highmem_8"
    n2d_highmem_16 = "n2d_highmem_16"
    n2d_highmem_32 = "n2d_highmem_32"
    n2d_highmem_48 = "n2d_highmem_48"
    n2d_highmem_64 = "n2d_highmem_64"
    n2d_highmem_80 = "n2d_highmem_80"
    n2d_highmem_96 = "n2d_highmem_96"
    n2d_highcpu_2 = "n2d_highcpu_2"
    n2d_highcpu_4 = "n2d_highcpu_4"
    n2d_highcpu_8 = "n2d_highcpu_8"
    n2d_highcpu_16 = "n2d_highcpu_16"
    n2d_highcpu_32 = "n2d_highcpu_32"
    n2d_highcpu_48 = "n2d_highcpu_48"
    n2d_highcpu_64 = "n2d_highcpu_64"
    n2d_highcpu_80 = "n2d_highcpu_80"
    n2d_highcpu_96 = "n2d_highcpu_96"
    n2d_highcpu_128 = "n2d_highcpu_128"
    n2d_highcpu_224 = "n2d_highcpu_224"
    
    # T2D (AMD EPYC - Burstable)
    t2d_standard_1 = "t2d_standard_1"
    t2d_standard_2 = "t2d_standard_2"
    t2d_standard_4 = "t2d_standard_4"
    t2d_standard_8 = "t2d_standard_8"
    
    # T2A (Arm-based Tau - Burstable)
    t2a_standard_1 = "t2a_standard_1"
    t2a_standard_2 = "t2a_standard_2"
    t2a_standard_4 = "t2a_standard_4"
    t2a_standard_8 = "t2a_standard_8"
    t2a_standard_16 = "t2a_standard_16"
    t2a_standard_32 = "t2a_standard_32"
    t2a_standard_48 = "t2a_standard_48"
    
    # C3 (Latest Generation Intel - Compute Optimized)
    c3_standard_4 = "c3_standard_4"
    c3_standard_8 = "c3_standard_8"
    c3_standard_22 = "c3_standard_22"
    c3_standard_44 = "c3_standard_44"
    c3_standard_88 = "c3_standard_88"
    c3_standard_176 = "c3_standard_176"
    c3_highcpu_4 = "c3_highcpu_4"
    c3_highcpu_8 = "c3_highcpu_8"
    c3_highcpu_22 = "c3_highcpu_22"
    c3_highcpu_44 = "c3_highcpu_44"
    c3_highcpu_88 = "c3_highcpu_88"
    c3_highcpu_176 = "c3_highcpu_176"
    c3_highmem_4 = "c3_highmem_4"
    c3_highmem_8 = "c3_highmem_8"
    c3_highmem_22 = "c3_highmem_22"
    c3_highmem_44 = "c3_highmem_44"
    c3_highmem_88 = "c3_highmem_88"
    c3_highmem_176 = "c3_highmem_176"
    
    # C2 (Intel Cascade Lake - Compute Optimized)
    c2_standard_4 = "c2_standard_4"
    c2_standard_8 = "c2_standard_8"
    c2_standard_16 = "c2_standard_16"
    c2_standard_30 = "c2_standard_30"
    c2_standard_60 = "c2_standard_60"
    
    # C2D (AMD EPYC - Compute Optimized)
    c2d_standard_2 = "c2d_standard_2"
    c2d_standard_4 = "c2d_standard_4"
    c2d_standard_8 = "c2d_standard_8"
    c2d_standard_16 = "c2d_standard_16"
    c2d_standard_32 = "c2d_standard_32"
    c2d_standard_56 = "c2d_standard_56"
    c2d_standard_112 = "c2d_standard_112"
    c2d_highcpu_2 = "c2d_highcpu_2"
    c2d_highcpu_4 = "c2d_highcpu_4"
    c2d_highcpu_8 = "c2d_highcpu_8"
    c2d_highcpu_16 = "c2d_highcpu_16"
    c2d_highcpu_32 = "c2d_highcpu_32"
    c2d_highcpu_56 = "c2d_highcpu_56"
    c2d_highcpu_112 = "c2d_highcpu_112"
    c2d_highmem_2 = "c2d_highmem_2"
    c2d_highmem_4 = "c2d_highmem_4"
    c2d_highmem_8 = "c2d_highmem_8"
    c2d_highmem_16 = "c2d_highmem_16"
    c2d_highmem_32 = "c2d_highmem_32"
    c2d_highmem_56 = "c2d_highmem_56"
    c2d_highmem_112 = "c2d_highmem_112"
    
    # H3 (Intel Sapphire Rapids - High Performance)
    h3_standard_88 = "h3_standard_88"
    
    # GCP Instance Types - Memory Optimized
    # M1 (Intel Broadwell - Memory Optimized)
    m1_ultramem_40 = "m1_ultramem_40"
    m1_ultramem_80 = "m1_ultramem_80"
    m1_ultramem_160 = "m1_ultramem_160"
    m1_megamem_96 = "m1_megamem_96"
    
    # M2 (Intel Cascade Lake - Memory Optimized)
    m2_ultramem_208 = "m2_ultramem_208"
    m2_ultramem_416 = "m2_ultramem_416"
    m2_megamem_416 = "m2_megamem_416"
    m2_hypermem_416 = "m2_hypermem_416"
    
    # M3 (Latest Generation - Memory Optimized)
    m3_ultramem_32 = "m3_ultramem_32"
    m3_ultramem_64 = "m3_ultramem_64"
    m3_ultramem_128 = "m3_ultramem_128"
    m3_megamem_64 = "m3_megamem_64"
    m3_megamem_128 = "m3_megamem_128"
    
    # GCP Instance Types - Accelerated Computing
    # A2 (NVIDIA A100 - AI/ML)
    a2_highgpu_1g = "a2_highgpu_1g"
    a2_highgpu_2g = "a2_highgpu_2g"
    a2_highgpu_4g = "a2_highgpu_4g"
    a2_highgpu_8g = "a2_highgpu_8g"
    a2_megagpu_16g = "a2_megagpu_16g"
    a2_ultragpu_1g = "a2_ultragpu_1g"
    a2_ultragpu_2g = "a2_ultragpu_2g"
    a2_ultragpu_4g = "a2_ultragpu_4g"
    a2_ultragpu_8g = "a2_ultragpu_8g"
    
    # A3 (NVIDIA H100 - Latest AI/ML)
    a3_highgpu_8g = "a3_highgpu_8g"
    a3_megagpu_8g = "a3_megagpu_8g"
    
    # G2 (NVIDIA L4 - AI Inference/Graphics)
    g2_standard_4 = "g2_standard_4"
    g2_standard_8 = "g2_standard_8"
    g2_standard_12 = "g2_standard_12"
    g2_standard_16 = "g2_standard_16"
    g2_standard_24 = "g2_standard_24"
    g2_standard_32 = "g2_standard_32"
    g2_standard_48 = "g2_standard_48"
    g2_standard_96 = "g2_standard_96"
    
    # GCP Instance Types - Preemptible & Spot
    # All above instances can also be preemptible/spot, but these are the pricing models
    # preemptible_* and spot_* prefixes can be added to any instance type
    
    # GCP Instance Types - Custom Machine Types
    # Custom machine types allow custom vCPU and memory configurations
    # custom_* indicates custom configurations beyond standard types
    
    # GCP Instance Types - Sole Tenant Nodes
    # Dedicated hardware for compliance and licensing requirements
    sole_tenant_n1 = "sole_tenant_n1"
    sole_tenant_n2 = "sole_tenant_n2"
    sole_tenant_n2d = "sole_tenant_n2d"
    sole_tenant_c2 = "sole_tenant_c2"
    sole_tenant_c2d = "sole_tenant_c2d"
    sole_tenant_m1 = "sole_tenant_m1"
    sole_tenant_m2 = "sole_tenant_m2"
    
    # General Categories
    cloud = "cloud"
    infra = "infra"
    subscription = "subscription"
    api = "api"
    database = "database"
    storage = "storage"
    networking = "networking"
    security = "security"
    monitoring = "monitoring"
    analytics = "analytics"

class ServiceStatus(str, Enum):
    active = "active"
    pending_deletion = "pending_deletion"
    suspended = "suspended"
    terminated = "terminated"

class ServiceBase(BaseModel):
    name: str
    platform: CloudPlatform
    service_type: ServiceType
    cost: float
    reminder_date: str  # ISO date string
    
    # Infrastructure tracking
    iam_number: Optional[str] = None
    instance_id: Optional[str] = None
    service_id: Optional[str] = None
    instance_type: Optional[ServiceType] = None  # For AWS/GCP instance types
    region: Optional[str] = None
    
    # API specific
    api_quota_tokens: Optional[int] = None
    api_usage_tokens: Optional[int] = None
    
    # Additional metadata
    description: Optional[str] = None
    tags: Optional[str] = None  # JSON string of tags
    owner_email: Optional[str] = None

class ServiceCreate(ServiceBase):
    pass

class Service(ServiceBase):
    id: str
    org_id: str
    status: ServiceStatus = ServiceStatus.active
    created_at: str
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True

class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    platform: Optional[CloudPlatform] = None
    service_type: Optional[ServiceType] = None
    cost: Optional[float] = None
    reminder_date: Optional[str] = None
    status: Optional[ServiceStatus] = None
    
    # Infrastructure tracking
    iam_number: Optional[str] = None
    instance_id: Optional[str] = None
    service_id: Optional[str] = None
    instance_type: Optional[ServiceType] = None  # For AWS/GCP instance types
    region: Optional[str] = None
    
    # API specific
    api_quota_tokens: Optional[int] = None
    api_usage_tokens: Optional[int] = None
    
    # Additional metadata
    description: Optional[str] = None
    tags: Optional[str] = None
    owner_email: Optional[str] = None

class Reminder(BaseModel):
    id: str
    service_id: str
    service_name: str
    cost: float
    reminder_date: str
    org_id: str

class ReminderAcknowledge(BaseModel):
    action_taken: str  # Description of what action was taken

class ServiceAnalytics(BaseModel):
    total_monthly_cost: float
    total_services: int
    cost_by_platform: dict
    cost_by_type: dict
    predicted_next_month: float
    cost_trend: list  # Historical cost data for predictions
