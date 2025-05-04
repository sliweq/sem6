using MediatR;
using MicroCleanService.Domain.DTO;

namespace MicroCleanService.Domain.Queries
{
    public class GetCleaningScheduleQuery : IRequest<List<CleaningScheduleDTO>>
    {

        public DateOnly Date { get; protected set; }
        public int Room { get; protected set; }
        public int Cleaner { get; protected set; }
        public int PeopleInRoom { get; protected set; }

        public GetCleaningScheduleQuery(DateOnly date, int room, int cleaner, int peopleInRoom)
        {
            Date = date;
            Room = room;
            Cleaner = cleaner;
            PeopleInRoom = peopleInRoom;
        }
    }
}
