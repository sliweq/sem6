(define (domain cleaning)
    (:requirements 
    :strips 
    :typing 
    :negative-preconditions 
    :fluents 
    )

  
  (:types
    room
    robo
  )

  (:predicates
    (at ?r - robo ?p - room)
    (dirty ?p - room)
    (clean ?p - room)

  )


  (:action clean
    :parameters (?r - robo ?p - room)
    :precondition (and
      (at ?r ?p)
      (dirty ?p)
    )
    :effect (and
      (clean ?p)
      (not (dirty ?p))
    )
  )

    (:action move
      :parameters (?r - robo ?from - room ?to - room)
      :precondition (at ?r ?from)
      :effect (and
        (not (at ?r ?from))
        (at ?r ?to)
      )
    )
)
