---
name: tmux
description: Arrange separate terminal programs in tmux panes and detach or reattach an existing session. Use when concurrent output needs separate terminals or work should survive a client disconnect.
---

# Keep the terminal contexts visible

Read this entire SKILL.md before acting. Select the owned session and pane before typing; finish with the intended pane arrangement or attachment state and the programs still running.

Check `tmux -V`. Define a distinct `session` name:

~~~bash
tmux new-session -s "$session"
~~~

With default bindings, press Ctrl-b then `%` for side-by-side panes, or Ctrl-b then `"` for stacked panes. Ctrl-b followed by an arrow selects a pane. Custom configuration may change these bindings; inspect `tmux list-keys` when they disagree. Each pane has its own terminal/program context, so check its current prompt before issuing commands.

Ctrl-b then `d` detaches the client while the session's programs continue. From an outside terminal:

~~~bash
tmux list-sessions
tmux attach-session -t "$session"
~~~

Detach is not program cancellation. Exiting a pane's shell or killing a session can terminate its programs. A session persists on its server host; tmux does not preserve programs across a host reboot. See the [upstream guide](https://github.com/tmux/tmux/wiki/Getting-Started) for layout and binding differences.
