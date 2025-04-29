using Hotel.Common.Domain.Events;

namespace MicroCleanService.Domain.Events
{
    public class CreateReservationEvent : Event
    {
        public Guid ReservationId { get; protected set; }
        public int Room { get; protected set; }
        public int NumberOfPeople { get; protected set; }
        public DateTime StartDate { get; protected set; }
        public DateTime EndDate { get; protected set; }

        public CreateReservationEvent(Guid guid, int room, int numberOfPeople, DateTime startDate, DateTime endDate)
        {
            ReservationId = guid;
            Room = room;
            NumberOfPeople = numberOfPeople;
            StartDate = startDate;
            EndDate = endDate;
        }
    }
}
