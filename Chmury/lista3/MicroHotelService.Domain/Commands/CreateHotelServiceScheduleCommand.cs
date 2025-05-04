using Hotel.Common.Domain.Commands;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MicroHotelService.Domain.Commands
{
    public class CreateHotelServiceScheduleCommand : Command
    {
        public DateOnly Date { get; set; }
        public int Room { get; set; }
        public int HotelBoy { get; set; }

        public CreateHotelServiceScheduleCommand(DateOnly date, int room ,int hotelBoy)
        {
            Date = date;
            Room = room;
            HotelBoy = hotelBoy;
        }
    }
}
