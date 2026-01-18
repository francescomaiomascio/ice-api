# ICE API
## Public Contract and Interaction Boundary of the ICE Ecosystem

ICE API defines the **public contract layer** of the ICE ecosystem.

It establishes **what may be expressed, exchanged, and interpreted**
between ICE components and external systems,
under the constraints defined by **ICE Foundation**.

ICE API does not execute logic.
It does not infer intent.
It does not grant authority.

It defines **what is structurally allowed to be communicated**.

---

## Foundation Dependency

This project derives its assumptions and constraints from  
**ICE Foundation v1.0.0**.

In particular, it is bound by:

- Explicit Authority and Control Separation (Axiom A-002)
- State as a Derived Artifact (Axiom A-003)
- Structural Traceability (Invariant I-001)
- Governance (Invariant I-003)

ICE API is a boundary, not a source of truth.

---

## What ICE API Is

ICE API is:

- a **canonical contract definition layer**
- a **schema authority for interaction**
- a **boundary between execution domains**
- a **stability surface for ICE systems**
- a **decoupling mechanism between producers and consumers**

It defines **what may be said and asked**,
not **what must be done**.

---

## What ICE API Is Not

ICE API is **not**:

- a runtime service
- an execution engine
- a business logic layer
- an orchestration system
- an authority or policy layer

APIs do not decide.
APIs do not execute.
APIs do not authorize.

They constrain interaction.

---

## Architectural Role

ICE API sits at the **interaction boundary** of the ICE ecosystem.

It connects:

- ICE Runtime
- ICE Engine
- ICE AI
- ICE Studio
- external tools, adapters, and integrations

No ICE component communicates around this layer.
All interaction must pass **through** explicit contracts.

This is intentional.

---

## Contract Model

ICE API defines:

- action and command schemas
- event and message formats
- domain object representations
- lifecycle and interaction primitives
- versioned and evolvable contracts

All contracts are:

- explicit
- inspectable
- versioned
- traceable

Implicit interaction is forbidden.

---

## Authority and Execution Separation

ICE API does **not** grant authority.

- Receiving a request does not imply permission.
- Emitting a command does not cause execution.
- Producing a payload does not justify action.

Authority and execution are handled downstream
by Runtime and Engine layers,
under Foundation-defined invariants.

---

## Versioning and Evolution

ICE API is designed to evolve **without semantic drift**.

- Contracts are versioned explicitly
- Changes are additive whenever possible
- Breaking changes are deliberate and explicit
- Compatibility is a structural concern

Evolution is allowed.
Ambiguity is not.

---

## Repository Scope

This repository contains:

- canonical API schemas
- interaction and event definitions
- validation rules
- contract documentation

It explicitly does **not** contain:

- runtime execution logic
- orchestration code
- persistence layers
- UI components

---

## Canonical Status

ICE API is **normative at the interaction boundary**.

Any ICE-compliant system must:

- conform to these contracts
- respect their semantics
- not reinterpret them implicitly

If communication violates these definitions,
the system is incorrect by construction.

---

## Status

ICE API is under **active development**.

Contracts are expected to stabilize
as higher-level ICE systems mature.

---

## Notes

Execution is power.

ICE API exists to ensure that  
**power never enters the system through ambiguity**.
