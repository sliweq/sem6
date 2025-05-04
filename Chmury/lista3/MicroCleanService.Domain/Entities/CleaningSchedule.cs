using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MicroCleanService.Domain.Entities
{
    public class CleaningSchedule
    {
        public DateOnly Date { get; set; }
        public int Room { get; set; }
        public int Cleaner { get; set; }
        public int PeopleInRoom { get; set; }
    }
}
