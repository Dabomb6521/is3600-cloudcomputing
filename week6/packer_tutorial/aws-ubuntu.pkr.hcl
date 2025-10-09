packer {
  required_plugins {
    amazon = {
      version = ">= 1.2.8"
      source  = "github.com/hashicorp/amazon"
    }
  }
}

source "amazon-ebs" "ubuntu" {
  ami_name      = "assignment-6-packer"
  instance_type = "t2.micro"
  region        = "us-west-2"
  ssh_username = "ubuntu"
  source_ami = "ami-04c174f38aefd7dc8"
  
  tags = {
    Name = "Assignment 6 Packer AMI"
    CreatedBy = "Packer"
    CreatedOn = "{{timestamp}}"
  }
}

build {
  name    = "assignment6-packer"
  sources = [
    "source.amazon-ebs.ubuntu"
  ]
  provisioner "file" {
    content = <<-EOT
        #!/bin/bash
        echo "Build from Packer AMI based on Ubuntu Nobal Numbat LTS ami-04c174f38aefd7dc8!"
        apt update && apt upgrade -y
        apt install -y python3.12 git vim 
    EOT
    destination = "/home/ubuntu/setup.sh"
  }
  
  # Make script executable
  provisioner "shell" {
    inline = [
        "chmod +x /home/ubuntu/setup.sh"
    ]
  }
}