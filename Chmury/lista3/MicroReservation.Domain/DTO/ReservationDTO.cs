using MicroReservation.Domain.DbEntities;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MicroReservation.Domain.DTO
{
    public class ReservationDTO
    {
        public Guid Id { get; set; }

        public string UserName { get; set; }

        public DateTime StartDate { get; set; }
        public DateTime EndDate { get; set; }
        public int NumberOfPeople { get; set; }
        public int Room { get; set; }

        public DateTime TimeOfReservation { get; set; }

        public ReservationDTO(Guid Id, string userName, DateTime startDate, DateTime endDate, int numberOfPeople, DateTime timeOfReservation , int room)
        {
            this.Id = Id;
            UserName = userName;
            StartDate = startDate;
            EndDate = endDate;
            NumberOfPeople = numberOfPeople;
            TimeOfReservation = timeOfReservation;
            Room = room;
        }
        public ReservationDTO(Reservation reservation) { 
            Id = reservation.Id;
            UserName = reservation.UserName;
            StartDate = reservation.StartDate.ToDateTime(new TimeOnly(0, 0));
            EndDate = reservation.EndDate.ToDateTime(new TimeOnly(0, 0));
            NumberOfPeople = reservation.NumberOfPeople;
            TimeOfReservation = reservation.TimeOfReservation;
            Room = reservation.Room;
        }
    }
}
