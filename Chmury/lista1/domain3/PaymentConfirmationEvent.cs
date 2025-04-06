namespace domain3
{
    public class PaymentConfirmationEvent
    {
        public Guid EventId { get; set; }
        public DateTime DateTime { get; set; } = DateTime.UtcNow;
        public string Data { get; set; } 
    }
}
