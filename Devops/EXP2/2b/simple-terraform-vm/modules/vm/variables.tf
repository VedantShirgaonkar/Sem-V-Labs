variable "vm_name" {
  description = "Name of the VM"
  type        = string
}

variable "machine_type" {
  description = "Machine type for VM"
  type        = string
}

variable "image" {
  description = "Boot disk image for VM"
  type        = string
}
