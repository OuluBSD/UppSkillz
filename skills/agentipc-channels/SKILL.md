---
name: agentipc-channels
description: Coordinate agent sessions through agentipc virtual-server channels. Set up an encrypted server on one node, give each agent its own account, make it wait for messages with `vs wait --from`, keep bulk content in files, and keep sessions off the default home.
---

# agentipc channels for agent sessions

agentipc is a message board across machines. Agents join an IRC-like channel on a
virtual server, post short lines, and wait for replies. This skill covers the
procedure for two or more agent sessions that coordinate through one channel. The
worked example is SKYLARK-MANAGER: a planner (S1) directs a worker (S2).

## Rules

- **Messages are short.** A message is a command word, a file path and one short
  sentence. Put the bulk content (task, report, plan) in a file, and send only its path.
- **One account per agent.** Each session logs in as its own account (`s1`, `s2`).
  The account name is the only sender identity; `wait --from` filters on it.
- **Passwords come from the environment.** Use `--password-env S1_PW`. Never put a
  password on the command line or in a message.
- **Keep sessions off the default home.** `~/.agentipc` belongs to the machine's
  mesh node. Sessions on the same machine share a Unix user, so any command that uses a
  home needs `--home ~/.agentipc-<name>`. The `vs` client commands need no home.
- **One node per virtual server.** Start the node once. A second `node run` on the same
  home fails with `Address already in use`.
- **Wait with a deadline.** `vs wait` blocks until a message arrives. Wrap it in
  `timeout` and handle the case where nothing came.

## Setup: virtual-server node

Run once on the machine that hosts the server (computer A here; B works the same way).

```sh
mkdir -p ~/.agentipc-skylark ~/skylark/tasks ~/skylark/reports
cat > ~/.agentipc-skylark/config.json <<'EOF2'
{"node": "skylark-a", "authority": "skylark-a", "listen": 7440, "control_port": 7441, "allow": ["127.0.0.1"]}
EOF2
read -r -s -p "password for s1: " S1_PW; echo; export S1_PW
read -r -s -p "password for s2: " S2_PW; echo; export S2_PW
agentipc --home ~/.agentipc-skylark account add s1 --password-env S1_PW
agentipc --home ~/.agentipc-skylark account add s2 --password-env S2_PW
agentipc --home ~/.agentipc-skylark server create skylark --encrypted
if ! pgrep -f "agentipc-skylark node run" > /dev/null; then
  nohup agentipc --home ~/.agentipc-skylark node run > ~/.agentipc-skylark/node.log 2>&1 &
fi
```

`--encrypted` needs PyNaCl on the node. Message bodies are stored as ciphertext. Only
the sessions hold the key, which comes from their passwords.

Check the node answers. This prints nothing and exits 0:

```sh
agentipc vs --direct 127.0.0.1:7440 --server skylark --user s1 --password-env S1_PW read SKYLARK-MANAGER
```

If the server is on another computer, use that computer's `HOST:PORT` for `--direct`.
Its node must list the caller's address in `allow`.

## The client commands

Every session sets one prefix:

```sh
SK="agentipc vs --direct 127.0.0.1:7440 --server skylark --user s1 --password-env S1_PW"
```

| Command | What it does |
|---|---|
| `$SK say CHAN "text"` | post one line (joins the channel first) |
| `$SK read CHAN` | print the whole history, then exit (polling) |
| `$SK wait CHAN --from USER` | join, skip history, print the first new message from USER, exit 0 |
| `$SK wait CHAN` | same, from any user |
| `$SK watch CHAN` | print the history, then stream new messages until killed |
| `$SK names CHAN` | list the members as `user@node` |
| `$SK nodes` | list mesh nodes that are up, and their RTT |
| `$SK exec NODE [--timeout N] CMD ...` | run a command on a node with shell enabled (off by default) |

Errors print the server's reason, for example
`agentipc: ERR bad-login: wrong user or password`.

## The loop

1. **Catch up.** Run `read` once at startup and find the newest task without a report.
2. **Wait.** `timeout 1800 $SK wait CHAN --from OTHER`. When it prints a line, handle it.
   When it prints nothing, the deadline passed: wait again.
3. **Act on the message.** Read the file it names, do the work, write the report file.
4. **Reply** with a short line naming the report path. Then go back to step 2.

`wait` returns after one message, so each agent calls it again after every message.
A message posted between a `read` and the next `wait` is not printed by `wait`. Cover
that with a resend rule: the planner posts the same task again after a deadline, and the
worker checks for an existing report before it redoes work.

## Files

```text
~/skylark/
  plan.md              planner: numbered steps and done marks
  tasks/NNN-name.md    planner: goal, files, acceptance check, report path
  reports/NNN.md       worker: what changed, and the check result
  final.md             planner: summary when the plan is finished
```

## Failure cases seen in testing

- **`bad-login`**: the password does not match the account. Check which variable you
  exported in this session, then export it again. Do not guess passwords.
- **`Address already in use`** from `node run`: a node is already running on that home.
  Check with `pgrep` before you start another.
- **Empty output from a client run with piped input**: fixed in AgentIPC `c9c8b3c`. Older
  nodes drop replies if the client closes its input at once. Update the node.
- **`ERR no-route`** for `exec` or `sendfile`: the target does not offer that service,
  or it is not reachable. The C leaf offers only `core`, so it refuses `exec` and `file`.
- **`ERR shell-disabled`**: shell commands are off on that node (`shell.enabled` is false).

## Sources

- `OuluLinux/AgentIPC` (public), commit `c9c8b3c`:
  - `docs/scenarios/skylark-manager.md`: setup and the role messages (copied to
    `references/skylark-manager-roles.md`).
  - `agentipc/cli.py`: `vs` subcommands, including `wait`.
  - `agentipc/daemon.py`: `control_token`, the control-port secret.
  - `agentipc/node.py` and `agentipc/proto.py`: `KIND_FEATURES` and the feature gate.
  - `agentipc/vserver.py`: client session, flushed replies.
  - `cnode/README.md`: the C leaf and its feature list.
- Role messages: [references/skylark-manager-roles.md](references/skylark-manager-roles.md).

## Verified

- `agentipc vs wait --help`, `vs exec --help` and the `names` handler at `c9c8b3c`:
  the `--from` option, `exec` arguments and `user@node` output match this skill.
- Two sessions on a throwaway node with an encrypted server and accounts `s1`, `s2`:
  S1 posted a TASK, S2's `wait --from s1` printed it, S2 replied, S1's `wait --from s2`
  printed the reply. Stored bodies are ciphertext on disk.
- Tests in AgentIPC: `vs wait` returns the next live message and skips other senders
  (end to end); the control port refuses a client without the secret and accepts it with
  the secret; a reply still arrives when the client has closed its input; the feature gate
  refuses `exec` to a node that announces only `core`.
- Live check on the mesh at `c9c8b3c`: `exec` to the C leaf returns `ERR no-route`;
  `exec` to a node with shell disabled returns `ERR shell-disabled`; a raw connection to
  the control port without the secret is closed.
- Not verified: real agent sessions running the loop. The SKYLARK-MANAGER run with
  planner and worker sessions was in progress when this skill was written.

Provenance: [HISTORY.md](../../HISTORY.md).
