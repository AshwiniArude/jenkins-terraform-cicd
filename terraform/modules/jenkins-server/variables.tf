variable "name" {
  description = "Name of the server (used for tags and the security group)"
  type        = string
}

variable "ami_id" {
  description = "AMI ID to launch"
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
}

variable "key_name" {
  description = "Existing EC2 key pair name for SSH"
  type        = string
}

variable "root_volume_size" {
  description = "Root volume size in GiB"
  type        = number
  default     = 20
}

variable "allowed_cidrs" {
  description = "CIDR blocks allowed on the ingress ports"
  type        = list(string)
}

variable "ingress_ports" {
  description = "Map of TCP port => description"
  type        = map(string)
}

variable "user_data" {
  description = "Cloud-init / bootstrap script run on first boot"
  type        = string
  default     = null
}
