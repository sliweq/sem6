using Supabase.Postgrest.Models;
using Supabase.Postgrest.Interfaces;
using Supabase.Postgrest.Attributes;

namespace MicroLaundry.Domain.DbEntities
{
    [Table("Laundry")]
    public class Laundry : BaseModel
    {
        public Laundry()
        {
        }
        public Laundry(DateOnly date, int sheetsCount)
        {
            Date = date;
            Id = Guid.NewGuid();
            SheetsCount = sheetsCount;
        }
        public Laundry(Guid id, DateOnly date, int sheetsCount)
        {
            Date = date;
            Id = id;
            SheetsCount = sheetsCount;
        }

        [PrimaryKey("id", false)]
        public Guid Id { get; set; }

        [Column("date")]
        public DateOnly Date { get; set; }

        [Column("sheets")]
        public int SheetsCount { get; set; }

    
    }

}
