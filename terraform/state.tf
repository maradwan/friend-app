terraform {
  backend "s3" {
    bucket = "terraform-state-apps"
    key    = "production/eu-west-1/terraform.tfstate"
    region = "eu-west-1"
    access_key = ""
    secret_key = ""
  }
}

