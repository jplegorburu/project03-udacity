resource "azurerm_network_interface" "" {
  name                = "ani-${var.resource_group}"
  location            = var.location
  resource_group_name = var.resource_group

  ip_configuration {
    name                          = "internal"
    subnet_id                     = var.subnet_id_test
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = var.public_ip_address_id
  }
}

resource "azurerm_linux_virtual_machine" "" {
  name                = "vm-${var.resource_group}"
  location            = var.location
  resource_group_name = var.resource_group
  size                = "Standard_B1s"
  admin_username      = "testUser"
  network_interface_ids = []
  admin_ssh_key {
    username   = "testUser"
    public_key = "file("~/.ssh/id_rsa.pub")"
  }
  os_disk {
    caching           = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }
  source_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "16.04-LTS"
    version   = "latest"
  }
}
