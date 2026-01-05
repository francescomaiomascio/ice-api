# ICE API

[![ICE Ecosystem](https://img.shields.io/badge/ICE-Ecosystem-8FB9FF?style=flat)](#)
[![Docs](https://img.shields.io/badge/docs-ICE%20Docs-8FB9FF?style=flat)](https://github.com/francescomaiomascio/ice-docs)
[![Status](https://img.shields.io/badge/status-active%20development-6B7280?style=flat)](#)
[![Language](https://img.shields.io/badge/python-3.x-111827?style=flat)](#)
[![License](https://img.shields.io/badge/license-MIT-7A7CFF?style=flat)](#)

ICE API defines the **public interface layer** of the ICE ecosystem.

It provides stable contracts, schemas, and interaction models used by
applications, agents, UIs, and runtimes to communicate with ICE systems in a
controlled and versioned way.

ICE API does not execute logic.
It defines **what can be said**, **what can be asked**, and **how systems interact**.

---

## Core Responsibilities

ICE API is responsible for:

- Defining public actions and agent specifications
- Modeling shared domains and system concepts
- Providing IPC message formats and event schemas
- Validating payloads and contracts
- Exposing lifecycle and interaction primitives
- Acting as the canonical boundary between ICE subsystems

---

## Architectural Scope

ICE API sits at the **boundary layer** of the ICE ecosystem.

It does not:
- orchestrate execution
- manage memory or cognition
- implement business logic
- control system state

It does:
- define interaction contracts
- standardize communication
- enforce schema correctness
- decouple producers and consumers

---

## Design Principles

- Explicit and versioned contracts
- Schema-first validation
- Clear separation between domains
- IPC as a first-class concern
- Backward compatibility by design
- APIs as boundaries, not conveniences

---

## Usage

ICE API is not a service and not an application.

It is consumed by:
- ICE Runtime
- ICE Engine
- ICE Studio
- ICE AI
- External tools and adapters

All ICE components communicate **through** this layer, not around it.

---

## Status

This project is under **active development**.
Public contracts aim to remain stable; extensions are additive.

---

## License

This project is licensed under the terms of the MIT license.
See the `LICENSE` file for details.
