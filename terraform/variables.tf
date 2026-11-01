variable "aws_region" {
  description = "AWS region to deploy into"
  type        = string
  default     = "ap-south-1" # Mumbai
}

variable "project_name" {
  description = "Prefix used for naming all resources"
  type        = string
  default     = "cicd-demo"
}

variable "owner" {
  description = "Owner tag applied to all resources"
  type        = string
  default     = "Ashwini Arude"
}

variable "instance_type" {
  description = "EC2 instance type for the Jenkins server (needs >= 2 GB RAM)"
  type        = string
  default     = "t3.small"
}

variable "root_volume_size" {
  description = "Root EBS volume size in GiB"
  type        = number
  default     = 20

  validation {
    condition     = var.root_volume_size >= 15 && var.root_volume_size <= 30
    error_message = "root_volume_size must be between 15 and 30 GiB (free-tier friendly)."
  }
}

variable "allowed_cidrs" {
  description = "CIDR blocks allowed to reach SSH, Jenkins and the app. Use [\"<your-ip>/32\"] for tighter security."
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "ingress_ports" {
  description = "Map of port => description opened on the security group"
  type        = map(string)
  default = {
    "22"   = "SSH"
    "8080" = "Jenkins UI"
    "5000" = "Shipment Tracker app"
  }
}
