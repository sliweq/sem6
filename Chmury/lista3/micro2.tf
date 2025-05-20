resource "azurerm_container_app" "service2" {
  name                         = "micro2"
  container_app_environment_id = azurerm_container_app_environment.env.id
  resource_group_name          = azurerm_resource_group.rg.name
  revision_mode                = "Single"

  template {
    container {
      name   = "micro2"
      image  = "sliweq/cleansrvicemicroservice:v1"
      cpu    = 0.5
      memory = "1.0Gi"

      env {
        name  = "AmqpSettings__Amqpurl"
        value = var.amqp_url
      }

      env {
        name  = "AmqpSettings__SUPABASE_URL"
        value = var.supabase_url
      }

      env {
        name  = "AmqpSettings__SUPABASE_KEY"
        value = var.supabase_key
      }
    }
  }

  ingress {
    external_enabled = true
    target_port      = 80
    traffic_weight {
      latest_revision = true
      percentage      = 100
    }
  }
}
