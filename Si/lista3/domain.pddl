(define (domain delivery)
    (:requirements 
    :strips 
    :typing 
    :negative-preconditions 
    :action-costs 
    )

(:functions
  (capacity ?v - vehicle)  
  (load ?v - vehicle) 
  (total-cost)
  (move-cost ?v - vehicle)
    
)

  
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
    
    (allowed-move ?v - vehicle ?from - location ?to - location)
  )


(:action load
  :parameters (?p - package ?v - vehicle ?l - location)
  :precondition (and
    (at ?p ?l)
    (at-vehicle ?v ?l)
    (not (in ?p ?v))          
    (< (load ?v) (capacity ?v))
  )
  :effect (and
    (not (at ?p ?l))
    (in ?p ?v)
    (increase (load ?v) 1)
    (increase (total-cost) 1)
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
    (decrease (load ?v) 1)
    (increase (total-cost) 1)
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
    (increase (total-cost)(move-cost ?v))
  )
)
)