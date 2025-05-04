using Supabase.Postgrest.Models;
using Supabase.Postgrest.Attributes;

namespace MicroCleanService.Domain.DbEntities
{
    [Table("CleaningSchedule")]
    public class CleaningSchedule: BaseModel
    {
        public CleaningSchedule() { 
        }
        public CleaningSchedule(DateOnly date, int room, int cleaner, int peopleInRoom)
        {
            Date = date;
            Id = Guid.NewGuid();
            Room = room;
            Cleaner = cleaner;
            PeopleInRoom = peopleInRoom;
        }
        [PrimaryKey("id", false)]
        public Guid Id { get; set; }
        [Column("date")]
        public DateOnly Date { get; set; }
        [Column("room")]
        public int Room { get; set; }
        [Column("cleaner")]
        public int Cleaner { get; set; }
        [Column("peopleInRoom")]
        public int PeopleInRoom { get; set; }
    }
}
