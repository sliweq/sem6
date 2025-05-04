using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Hotel.Common.Domain.Commands;

namespace MicroReservation.Domain.Commands
{
    public abstract class ReservationCommand : Command
    {
        public Guid Id { get; protected set; }

        public string UserName { get; protected set; }

        public DateTime StartDate { get; protected set; }
        public DateTime EndDate { get; protected set; }
        public int NumberOfPeople { get; protected set; }

        public DateTime TimeOfReservation { get; protected set; }
        public int Room { get; protected set; }
    }
}
