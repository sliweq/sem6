(define (domain delivery)
    (:requirements 
    :strips 
    :typing 
    :negative-preconditions 
    :fluents 
    :action-costs 
    )

    (:functions (total-cost))


  
  (:types
    package
    location
    vehicle
    car plane ship - vehicle
    warehouse airport harbor - location
  )

  (:predicates
    (package ?p - package)
    (vehicle ?v - vehicle)
    (location ?l - location)
    
    (at ?p - package ?l - location)
    (at-vehicle ?v - vehicle ?l - location)
    (in ?p - package ?v - vehicle)
    
    (free ?v - vehicle)
    (allowed-move ?v - vehicle ?from - location ?to - location)
  )


  (:action load
    :parameters (?p - package ?v - vehicle ?l - location)
    :precondition (and
      (at ?p ?l)
      (at-vehicle ?v ?l)
      (free ?v)
    )
    :effect (and
      (not (at ?p ?l))
      (in ?p ?v)
    )
  )



  (:action unload
    :parameters (?p - package ?v - vehicle ?l - location)
    :precondition (and
      (in ?p ?v)
      (at-vehicle ?v ?l)
    )
    :effect (and
      (not (in ?p ?v))
      (at ?p ?l)
    )
  )



(:action move
  :parameters (?v - vehicle ?from - location ?to - location)
  :precondition (and
    (at-vehicle ?v ?from)
    (allowed-move ?v ?from ?to)
  )
  :effect (and
    (not (at-vehicle ?v ?from))
    (at-vehicle ?v ?to)
    (increase (total-cost) 5)
  )
)


)
