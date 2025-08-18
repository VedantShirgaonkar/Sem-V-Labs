terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.8.0"
    }
  }
}

provider "google" {
  project = var.project
  region  = var.region
  zone    = var.zone
}

# Call our simple VM module
module "vm" {
  source       = "./modules/vm"
  vm_name      = var.vm_name
  machine_type = var.machine_type
  image        = var.image
}
