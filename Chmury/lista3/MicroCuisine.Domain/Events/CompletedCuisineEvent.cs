using Hotel.Common.Domain.Events;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MicroCuisine.Domain.Events
{
    public class CompletedCuisineEvent : Event
    {
        public Guid Id { get; protected set; }
        public bool Error { get; protected set; }

        public CompletedCuisineEvent(bool error)
        {
            Error = error;
        }
    }
}
