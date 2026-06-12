# work

## hyper takes the keyboard at launch

- ask: the fix for tonight's dead keyboard — both 19:40 launches opened fullscreen with the keyboard still in the window behind, because the window manager's focus-stealing prevention vetoes ghostty's timestamp-0 activation; your keys went to the browser under the interface. beside the fullscreen retries hyper now confirms keyboard focus with the window manager each tick at launch, and where it was refused takes it directly — XSetInputFocus, which the activation politics cannot veto — until it is shown held; every outcome lands in .hyper.log like the fullscreen flashes
- try: relaunch hyper (q, then the menu) — the window that opens should answer keys at once, and .hyper.log gains "keyboard focus confirmed by the window manager"; the hyper open now wears the old code
- blocks: until accepted, any relaunch or the next login can open deaf again — and keys typed at a dead interface land in whatever window sits behind it
- state: awaiting acceptance
- since: 2026-06-11
