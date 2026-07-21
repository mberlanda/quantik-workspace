# System Overview

`quantik-workspace` is a file-based control plane around four independent implementation/contract repositories. It records inventory, intent, dependency edges, bounded context, compatibility evidence, and release state. It invokes repository-owned commands but never copies or reimplements engine/model logic.

The durable flow is: discovery evidence → initiative → repository tasks → repository-owned changes/tests → structured handoffs → compatibility report → release train → immutable lock/matrix. Local checkout paths are configurable with ignored `workspace.local.yaml`.
