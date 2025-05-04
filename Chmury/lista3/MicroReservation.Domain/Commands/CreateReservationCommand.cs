using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Xml.Linq;

namespace MicroReservation.Domain.Commands
{
    public class CreateReservationCommand: ReservationCommand
    {
        public CreateReservationCommand(string userName, DateTime startDate, DateTime endDate, int numberOfPeople, int room)
        {
            UserName = userName;
            StartDate = startDate;
            EndDate = endDate;
            NumberOfPeople = numberOfPeople;
            Room = room;
        }


        public string UserName { get; protected set; }

        public DateTime StartDate { get; protected set; }
        public DateTime EndDate { get; protected set; }
        public int NumberOfPeople { get; protected set; }
        public int Room { get; protected set; }
    }
}
