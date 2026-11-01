output "instance_id" {
  description = "EC2 instance ID"
  value       = module.jenkins_server.instance_id
}

output "public_ip" {
  description = "Public IP of the Jenkins server"
  value       = module.jenkins_server.public_ip
}

output "ami_used" {
  description = "Ubuntu AMI used for the server"
  value       = data.aws_ami.ubuntu.name
}

output "jenkins_url" {
  description = "Open this in the browser to reach Jenkins"
  value       = "http://${module.jenkins_server.public_ip}:8080"
}

output "app_url" {
  description = "Shipment Tracker URL (live after the first successful pipeline run)"
  value       = "http://${module.jenkins_server.public_ip}:5000"
}

output "github_webhook_url" {
  description = "Paste this as the GitHub webhook Payload URL"
  value       = "http://${module.jenkins_server.public_ip}:8080/github-webhook/"
}

output "ssh_command" {
  description = "SSH into the server (run from the terraform folder)"
  value       = "ssh -i ${var.project_name}-key.pem ubuntu@${module.jenkins_server.public_ip}"
}
