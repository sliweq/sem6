using Hotel.Common.Domain.Events;

namespace MicroLaundry.Domain.Events
{
    public class CreateCleaningEvent : Event
    {
        public int Room { get; protected set; }
        public int NumberOfPeople { get; protected set; }
        public DateOnly StartDate { get; protected set; }
        public int Cleaner { get; protected set; }
        public DateOnly EndDate { get; protected set; }

        public CreateCleaningEvent(int room, int numberOfPeople, DateOnly startDate, DateOnly endDate, int cleaner)
        {
            Room = room;
            NumberOfPeople = numberOfPeople;
            StartDate = startDate;
            EndDate = endDate;
            Cleaner = cleaner;
        }
    }
}
