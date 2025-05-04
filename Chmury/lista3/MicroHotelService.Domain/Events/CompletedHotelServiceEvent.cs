using Hotel.Common.Domain.Events;

namespace MicroHotelService.Domain.Events
{
    public class CompletedHotelServiceEvent : Event
    {
        public Guid Id { get; protected set; }
        public bool Error { get; protected set; }

        public CompletedHotelServiceEvent(bool error)
        {
            Error = error;
        }
    }
}
