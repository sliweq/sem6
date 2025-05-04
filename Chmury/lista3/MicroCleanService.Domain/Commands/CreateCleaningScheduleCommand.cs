using Hotel.Common.Domain.Commands;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MicroCleanService.Domain.Commands
{
    public class CreateCleaningScheduleCommand : Command
    {
        public DateOnly EndDate { get; set; }
        public DateOnly StartDate { get; set; }
        public int Room { get; set; }
        public int Cleaner { get; set; }
        public int PeopleInRoom { get; set; }

        public CreateCleaningScheduleCommand(DateOnly startDate,DateOnly endDate, int room, int cleaner, int peopleInRoom)
        {
            StartDate = startDate;
            EndDate = endDate;
            Room = room;
            Cleaner = cleaner;
            PeopleInRoom = peopleInRoom;
        }
    }
}
