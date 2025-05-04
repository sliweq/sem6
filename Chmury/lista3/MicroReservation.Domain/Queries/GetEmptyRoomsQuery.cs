using MediatR;
using MicroReservation.Domain.DTO;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MicroReservation.Domain.Queries
{
    public class GetEmptyRoomsQuery : IRequest<List<RoomDTO>>
    {
        public DateTime StartTime { get; protected set; }
        public DateTime EndTime { get; protected set; }
        public int AmountOfPeople { get; protected set; }


        public GetEmptyRoomsQuery(DateTime startDate, DateTime endTime, int amountOfPeople)
        {
            StartTime = startDate;
            EndTime = endTime;
            AmountOfPeople = amountOfPeople;
        }
    }
}
