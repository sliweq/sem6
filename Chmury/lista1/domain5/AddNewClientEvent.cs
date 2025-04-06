namespace domain5
{
    public class AddNewClientEvent
    {
        public Guid EventId { get; set; }

        public DateTime DateTime { get; set; } = DateTime.UtcNow;
        public string Data { get; set; }
    }
}
