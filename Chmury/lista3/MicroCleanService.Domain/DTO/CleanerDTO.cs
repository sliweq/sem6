using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MicroCleanService.Domain.DTO
{
    public class CleanerDTO
    {
        public int Id { get; set; }
        public CleanerDTO(int id)
        {
            Id = id;
        }
    }
}
