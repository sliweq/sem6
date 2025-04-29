using Supabase.Postgrest.Attributes;
using Supabase.Postgrest.Models;

namespace MicroReservation.Domain.DbEntities
{
    [Table("Reservations")]

    public class Reservation : BaseModel
    {
        public Reservation()
        {
        }
        public Reservation(string userName, DateOnly startDate, DateOnly endDate, int numberOfPeople, int room)
        {
            Id = Guid.NewGuid();
            UserName = userName;
            StartDate = startDate;
            EndDate = endDate;
            NumberOfPeople = numberOfPeople;
            TimeOfReservation = DateTime.UtcNow;
            Room = room;
        }
        [PrimaryKey("id", false)]
        public Guid Id { get; set; }

        [Column("userName")]
        public string UserName { get; set; }

        [Column("startDate")]
        public DateOnly StartDate { get; set; }

        [Column("endDate")]
        public DateOnly EndDate { get; set; }

        [Column("numberOfPeople")]
        public int NumberOfPeople{ get; set; }

        [Column("timeOfReservation")]
        public DateTime TimeOfReservation { get; set; }

        [Column("room")]
        public int Room { get; set; }
    }
}
