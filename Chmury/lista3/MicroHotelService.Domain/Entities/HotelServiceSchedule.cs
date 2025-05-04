using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MicroHotelService.Domain.Entities
{
    public class HotelServiceSchedule
    {
        public DateOnly Date { get; set; }
        public int Room { get; set; }
        public int HotelBoy { get; set; }
    }
}
