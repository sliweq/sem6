using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MicroReservation.Domain.DTO
{
    public class RoomDTO
    {

        public int Id { get; set; }

        public int maxCapacity { get; set; }

        public RoomDTO(int id, int maxCapacity)
        {
            Id = id;
            maxCapacity = maxCapacity;
        }
    }
}
