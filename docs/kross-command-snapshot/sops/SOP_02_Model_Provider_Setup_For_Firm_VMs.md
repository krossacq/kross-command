# SOP 02: Model Provider Setup For Firm VMs

Version: 0.1
Owner: Tax Mogul Bureau
Applies to: Kross Command

## Purpose

Define how Kross Command helps connect model provider access for a firm VM.

## Core Rule

Future firms should pay for and authorize their own AI/model provider subscription by default.

Returns and Revenue Office may use Sydne/Tax Mogul provider access as the pilot exception.

## Kross Command May Help With

- guiding the firm owner/admin through provider authorization
- documenting provider name and model family
- recording credential storage location without recording secret values
- testing whether Hermes can use the provider
- troubleshooting expired sessions or missing provider access

## Kross Command Must Not Do

- ask users to paste API keys, OAuth tokens, passwords, or recovery codes into chat
- store model provider secrets in repo files
- copy provider credentials between firms
- power one firm using another firm's provider account
- promise unlimited usage unless the firm's plan explicitly includes it

## Required Record

For each firm, document:

- provider name
- approved model or model family
- account owner/payer
- usage/cost owner
- access method
- credential storage location
- last verified date
- offboarding/revocation steps

## Acceptance Criteria

This SOP is working when each firm VM has clear, isolated, documented provider access.
