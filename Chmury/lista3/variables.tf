variable "amqp_url" {
  description = "RabbitMQ connection URL"
  type        = string
  sensitive   = true
}

variable "supabase_url" {
  description = "Supabase URL"
  type        = string
  sensitive   = true

}

variable "supabase_key" {
  description = "Supabase Key"
  type        = string
  sensitive   = true
}
