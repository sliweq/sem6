using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MicroReservation.Domain.Entities
{
    public class Room
    {
        public int Id { get; set; }

        public int maxCapacity { get; set; }

        public Room(int id, int maxCapacity)
        {
            Id = id;
            maxCapacity = maxCapacity;
        }
    }
}
