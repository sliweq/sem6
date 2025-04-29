using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;

namespace MicroReservation.Domain.Entities
{
    public class Reservation
    {
        public Guid Id { get; set; }
        
        public string UserName { get; set; }

        public DateTime StartDate { get; set; }
        public DateTime EndDate { get; set; }
        public int NumberOfPeople { get; set; }

        public DateTime TimeOfReservation { get; set; }
        public int Room { get; set; }

        public Reservation(string userName, DateTime startDate, DateTime endDate, int numberOfPeople, int room)
        {
            Id = Guid.NewGuid();
            UserName = userName;
            StartDate = startDate;
            EndDate = endDate;
            NumberOfPeople = numberOfPeople;
            TimeOfReservation = DateTime.Now;
            Room = room;
        }

    }


}
