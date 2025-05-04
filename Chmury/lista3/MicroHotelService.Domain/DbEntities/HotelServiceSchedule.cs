using Supabase.Postgrest.Attributes;
using Supabase.Postgrest.Models;

namespace MicroHotelService.Domain.DbEntities
{

    [Table("HotelServiceSchedules")]

    public class HotelServiceSchedule : BaseModel
    {
        public HotelServiceSchedule()
        {
        }
        public HotelServiceSchedule(DateOnly date, int room, int hotelBoy)
        {
            Id = Guid.NewGuid();
            Date = date;
            HotelBoy = hotelBoy;
            Room = room;
        }
        [PrimaryKey("id", false)]
        public Guid Id { get; set; }

        [Column("date")]
        public DateOnly Date { get; set; }

        [Column("room")]
        public int Room { get; set; }

        [Column("hotelBoy")]
        public int HotelBoy { get; set; }
    }
}
