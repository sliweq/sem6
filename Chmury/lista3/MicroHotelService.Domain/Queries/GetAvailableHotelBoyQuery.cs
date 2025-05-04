using MediatR;
using MicroHotelService.Domain.DTO;
using MicroHotelService.Domain.Entities;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MicroHotelService.Domain.Queries
{
    public class GetAvailableHotelBoyQuery : IRequest<List<HotelBoyDTO>>
    {
        public DateOnly Date { get; protected set; }
        public int Room { get; protected set; }

        public GetAvailableHotelBoyQuery(DateOnly date, int room)
        {
            Date = date;
            Room = room;
        }
    }
}
