using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MicroLaundry.Domain.Entities
{
    public class Laundry
    {
        public DateOnly Date { get; set; }
        public int SheetsCount { get; set; }
    }
}
