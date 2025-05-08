# CI/CD and Build System best practices

## Authentication

- When possible, prefer to use `teleport` or another short-lived access token for authentication, rather than raw SSH public/private key pairs.

## Build Hosting Location

- Use configured, shared servers for any code that merges into the mainline. The `main` version of workflows should not contain any calls to private, individual servers.