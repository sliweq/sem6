namespace domain6
{
    public class AddNewReservationEvent
    {
        public Guid EventId { get; set; }
        public DateTime DateTime { get; set; } = DateTime.UtcNow;
        public string Data { get; set; }
    }
}
