using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MicroLaundry.Domain.DTO
{
    public class LaundryDTO
    {
        public Guid Id { get; set; }
        public DateOnly Date { get; set; }
        public int SheetCount { get; set; }
        public LaundryDTO(Guid id,DateOnly date, int sheetCount)
        {
            Id = id;
            Date = date;
            SheetCount = sheetCount;
        }

    }
}
