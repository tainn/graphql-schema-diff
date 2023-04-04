# graphql-schema-diff

[![Code style: black](https://img.shields.io/badge/style-black-000000.svg)](https://github.com/psf/black)

Periodic checks for changes in the [GraphQL schema](https://graphql.org/learn/schema) of the provided API endpoint, the
capture of diffs, and flat sequential versioning upon detected changes.

## Output

Four new files are created each time upon detecting changes, where `v0` corresponds to the current version increment:

- `schema-v0.graphql`: latest schema in `graphql` format
- `schema-v0.json`: latest schema in `json` format
- `graphql-diff-v0.txt`: per-line unified diff of `graphql` format
- `json-diff-v0.txt`: per-line unified diff of `json` format

A single file is created initially and then overwritten upon detecting changes:

- `latest-version.txt`: holds the info of the latest schema version to compare against

By default, they are volumed to `/var/data/graphql-schema-diff` on the host.

## Webhook

If provided, a notification of a new schema version is sent to the
specified [Discord webhook](https://discord.com/developers/docs/resources/webhook) URL.

## Env

Configurations should be specified in the root `.env` file. See `.env.example` for corresponding keys.

## Run

Create an `open` external network.

```shell
docker network create open
```

Run in a containerized environment. The process will persist unless explicitly stopped.

```shell
docker-compose up -d
```
