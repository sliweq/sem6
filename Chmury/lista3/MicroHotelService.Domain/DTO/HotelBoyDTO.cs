using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MicroHotelService.Domain.DTO
{
    public class HotelBoyDTO
    {

        public int Id { get; set; }

        public HotelBoyDTO(int id)
        {
            Id = id;
        }

    }
}
