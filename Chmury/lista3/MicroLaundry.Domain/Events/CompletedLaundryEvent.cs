using Hotel.Common.Domain.Events;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MicroLaundry.Domain.Events
{
    public class CompletedLaundryEvent : Event
    {
        public Guid Id { get; protected set; }
        public bool Error { get; protected set; }

        public CompletedLaundryEvent(bool error)
        {
            Error = error;
        }
    }
}
